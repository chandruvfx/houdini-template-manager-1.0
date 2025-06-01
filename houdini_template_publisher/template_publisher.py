
#
# Houdini Publisher tool 
#
from PySide2.QtUiTools import QUiLoader
from PySide2 import QtWidgets
from PySide2 import QtCore, QtGui
import psycopg2
# from psycopg2.extras import NamedTupleCursor
import os 
import sys
import constant
import templates_restapi
from screen_grab_shot import OverlayWidget, capture_screen
from importlib  import reload
import publish
import toast_notification
reload(toast_notification)
reload(publish)
reload(templates_restapi)


class TagWidget(QtWidgets.QWidget):

    """TagWidget 

    Created with  label following with a button with 'x' close symbol.
    This is a single tag gonna added into the scroll bar
    """
    STYLES = {
        'primary': {'bg': '#3498db', 'text': 'white'},
    }
    
    closed = QtCore.Signal(QtWidgets.QWidget)  # Signal emitted when tag is closed
    
    def __init__(self, text, style='default', parent=None):
        super().__init__(parent)
        self.text = text
        self.style = style if style in self.STYLES else 'default'
        
        self.setup_ui()
        
    def setup_ui(self):
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setContentsMargins(6, 2, 2, 2)
        self.layout.setSpacing(4)
        
        # Tag label
        self.label = QtWidgets.QLabel(self.text)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        
        font = self.label.font()
        font.setPointSize(9)
        font.setWeight(QtGui.QFont.Medium)
        self.label.setFont(font)
        
        # Close button
        self.close_btn = QtWidgets.QPushButton()
        self.close_btn.setFixedSize(16, 16)
        self.close_btn.setStyleSheet("""
            QPushButton {
                border: none;
                background: transparent;
                color: inherit;
                padding: 0px;
            }
            QPushButton:hover {
                color: white;
            }
        """)
        self.close_btn.setText("×")  # Using multiplication sign as close X
        self.close_btn.setCursor(QtCore.Qt.PointingHandCursor)
        self.close_btn.clicked.connect(self.handle_close)
        
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.close_btn)
        self.setLayout(self.layout)
        
        self.setFixedHeight(24)
        self.setMinimumWidth(40)
        
    def handle_close(self):
        self.closed.emit(self)  # Emit signal before closing
        
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        
        color = QtGui.QColor(self.STYLES[self.style]['bg'])
        painter.setBrush(color)
        painter.setPen(QtCore.Qt.NoPen)
        
        path = QtGui.QPainterPath()
        rect = self.rect()
        radius = rect.height() / 2
        path.addRoundedRect(rect, radius, radius)
        painter.drawPath(path)
        
        text_color = self.STYLES[self.style]['text']
        self.label.setStyleSheet(f"color: {text_color};")
        self.close_btn.setStyleSheet(f"""
            QPushButton {{
                border: none;
                background: transparent;
                color: {text_color};
                padding: 0px;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                color: white;
            }}
        """)
        
        super().paintEvent(event)


class TemplatePublisher(QtWidgets.QMainWindow):
    
    def __init__(self) -> None:
        
        super().__init__()
        
        self.subtask_path = ''
        dirname = os.path.dirname(__file__)
        ui_file = os.path.join(dirname, 
                               "ui/template_publisher.ui"
        )
        ui_loader = QUiLoader()
        self.template_publisher_window = ui_loader.load(ui_file)
        self.all_tag = []
        self.temp_snap_file_path = ''

        self.template_api = templates_restapi.TemplatesRestApi()

        self.icon = self.template_publisher_window.findChild(QtWidgets.QLabel,
                                                              "icon")
        self.icon.setText("<html> <span style='color: #ff6600; font-size: 50px;'>✧</span></html>")

        self.bundle_icon = self.template_publisher_window.findChild(QtWidgets.QLabel,
                                                              "bundle_icon")
        self.bundle_icon.setText("<html><span style='font-size: 20px;'>🎁</span></html>")
        self.category_icon = self.template_publisher_window.findChild(QtWidgets.QLabel,
                                                              "category_icon")
        self.category_icon.setText("<span style='font-size: 20px;'>📚</span>")
        self.context_icon = self.template_publisher_window.findChild(QtWidgets.QLabel,
                                                              "context_icon")
        self.context_icon.setText("<span style='font-size: 20px;'>🧿</span>")
        self.tag_icon = self.template_publisher_window.findChild(QtWidgets.QLabel,
                                                              "tag_icon")
        self.tag_icon.setText("<span style='font-size: 20px;'>🏷️</span>")


        self.bundle_name = self.template_publisher_window.findChild(QtWidgets.QTextEdit,
                                                              "bundle_name")

        # Create a QCompleter
        self.completer = QtWidgets.QCompleter(self)
        self.completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.completer.setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
        
        # Create a model for the completer
        self.completer_model = QtGui.QStandardItemModel(self.completer)
        self.completer.setModel(self.completer_model)
        
        # Create a proxy widget to handle the completer for QTextEdit
        self.bundle_name_completer_proxy = CompleterProxyWidget(self.bundle_name)
        self.bundle_name_completer_proxy.setCompleter(self.completer)
        
        # Connect signals to update suggestions
        self.bundle_name.textChanged.connect(self.update_bundle_name_suggestions)
        # Install event filter on the viewport
        self.bundle_name.viewport().installEventFilter(self)

        #Latest_version label
        self.latest_version_label = self.template_publisher_window.findChild(QtWidgets.QLabel,
                                                              "latest_version")
                                                              
        self.description = self.template_publisher_window.findChild(QtWidgets.QTextEdit,
                                                              "description")
        # add all bundles list                                                  
        self.bundle_type = self.template_publisher_window.findChild(QtWidgets.QComboBox,
                                                              "bundle_type")
        bundle_types = self.template_api.bundle_lists()
        for bundle_type in [items for items in bundle_types][0]:
            self.bundle_type.addItem(bundle_type[-1])
        self.bundle_type.setCurrentIndex(-1) 

        #Check template
        self.is_template = self.template_publisher_window.findChild(QtWidgets.QCheckBox,
                                                              "is_template")
        self.is_template.stateChanged.connect(self.templates_widgets_visibility_switch)

        # add category                                                                                                           
        self.category = self.template_publisher_window.findChild(QtWidgets.QComboBox,
                                                              "category")

        self.category.setStyleSheet(constant.CATEGORY_DISABLE)
        self.category.setDisabled(True)
        categories = self.template_api.categories()
        for category in [items for items in categories][0]:
            self.category.addItem(category[-1])
        self.category.setCurrentIndex(-1) 


        self.is_nodesnippet = self.template_publisher_window.findChild(QtWidgets.QCheckBox,
                                                              "is_nodesnippet")
        self.is_nodesnippet.stateChanged.connect(self.nodes_snippet_widgets_visibility_switch)
        

        #add contexts                                                     
        self.context = self.template_publisher_window.findChild(QtWidgets.QComboBox,
                                                              "context")

        self.context.setStyleSheet(constant.CONTEXT_DISABLE)
        self.context.setDisabled(True)
        contexts = self.template_api.contexts()
        for context in [items for items in contexts][0]:
            self.context.addItem(context[-1])
        self.context.setCurrentIndex(-1) 
        
        #blink text
        self.blink_text = self.template_publisher_window.findChild(QtWidgets.QLabel,
                                                              "blink_text")
        self.blink_text.setHidden(True)

        #image path widget
        self.image_path = self.template_publisher_window.findChild(QtWidgets.QTextEdit,
                                                              "image_path")
        self.image_path.setDisabled(True)
        self.image_path.setStyleSheet(constant.IMG_PATH_DISABLE)
        
        #file dialog button
        self.file_dialog = self.template_publisher_window.findChild(QtWidgets.QPushButton,
                                                              "file_dialog")                                             
        self.file_dialog.clicked.connect(self.set_file_path)
        self.file_dialog.setDisabled(True)
        
        self.file_dialog.setStyleSheet(constant.FILE_BROWSER_BUTTON_DISABLE)
                                            
        self.snapshot = self.template_publisher_window.findChild(QtWidgets.QPushButton,
                                                              "snapshot") 
        self.snapshot.setDisabled(True)                                                     
        self.snapshot.setStyleSheet(constant.SNAPSHOT_DISABLE)
        self.snapshot.clicked.connect(self.toggle_minimize)

        self.snapshot.clicked.connect(self.grab_screen_shot)

        #add tags                                                      
        self.tags = self.template_publisher_window.findChild(QtWidgets.QComboBox,
                                                              "tags")
        tags = self.template_api.tags()
        for tag in [items for items in tags][0]:
            self.tags.addItem(tag[-1])
        self.tags.setCurrentIndex(-1)
        self.tags.activated[str].connect(self.insert_tag_in_scrollview)                                                  

        self.tags_scroll = self.template_publisher_window.findChild(QtWidgets.QScrollArea,
                                                              "tags_scroll")
        
        # Publishing
        self.publish_btn = self.template_publisher_window.findChild(QtWidgets.QPushButton,
                                                              "publish")
        self.publish_btn.clicked.connect(self.publish)
        self.setup_tags()

    def toggle_blink_text(self):
        """Toggle the visibility of the blink_text label"""
        self.blink_text.setVisible(not self.blink_text.isVisible())

    def nodes_snippet_widgets_visibility_switch(self) -> None:
        if self.is_nodesnippet.isChecked() and not self.is_template.isChecked():
            self.blink_text.setHidden(False)
            self.is_template.setStyleSheet(constant.IS_TEMPLATE_DISABLE)
            self.category.setStyleSheet(constant.CATEGORY_DISABLE)
            self.context.setStyleSheet(constant.CONTEXT_ENABLE)
            self.snapshot.setStyleSheet(constant.SNAPSHOT_ENABLE)
            self.is_template.setDisabled(True)
            self.category.setDisabled(True)
            self.context.setDisabled(False)
            self.snapshot.setDisabled(False)

            # Blick qlablel text to notify user to select nodes
            self.blink_timer = QtCore.QTimer()
            self.blink_timer.timeout.connect(self.toggle_blink_text)
            self.blink_timer.start(500)  # Blink every 500ms (half second)

        else:
            self.blink_text.setHidden(True)
            self.is_template.setStyleSheet(constant.IS_TEMPLATE_ENABLE)
            self.context.setStyleSheet(constant.CONTEXT_DISABLE)
            self.snapshot.setStyleSheet(constant.SNAPSHOT_DISABLE)
            self.is_template.setDisabled(False)
            self.context.setDisabled(True)
            self.snapshot.setDisabled(True)
            self.context.setCurrentIndex(-1)

            self.blink_timer.stop() 


    def templates_widgets_visibility_switch(self) -> None:
        """
            node snippet based context and snapshot widgets disbled if templates
            were selected. As same template checkbox and image path and category
            disbled if node snippet selected.

            Stylesheets revorted selection and unselections
        """

        if self.is_template.isChecked() and not self.is_nodesnippet.isChecked():
            self.is_nodesnippet.setStyleSheet(constant.IS_NODE_SNIPPET_DISABLE)
            self.context.setStyleSheet(constant.CONTEXT_DISABLE)
            self.category.setStyleSheet(constant.CATEGORY_ENABLE)
            self.image_path.setStyleSheet(constant.IMG_PATH_ENABLE)
            self.file_dialog.setStyleSheet(constant.FILE_BROWSER_BUTTON_ENABLE)

            self.is_nodesnippet.setDisabled(True)
            self.context.setDisabled(True)
            self.category.setDisabled(False)
            self.image_path.setDisabled(False)
            self.file_dialog.setDisabled(False)

        else:
            self.is_nodesnippet.setStyleSheet(constant.IS_NODE_SNIPPET_ENABLE)
            self.context.setStyleSheet(constant.CONTEXT_ENABLE)
            self.category.setStyleSheet(constant.CATEGORY_DISABLE)
            self.image_path.setStyleSheet(constant.IMG_PATH_DISABLE)
            self.file_dialog.setStyleSheet(constant.FILE_BROWSER_BUTTON_DISABLE)

            self.is_nodesnippet.setDisabled(False)
            self.context.setDisabled(False)
            self.category.setDisabled(True)
            self.image_path.setDisabled(True)
            self.file_dialog.setDisabled(True)
            self.category.setCurrentIndex(-1)
            self.image_path.clear()

        
        
    def insert_tag_in_scrollview(self, tag):
        """
        User selected tags appended into set and 
        inserted into the scroll based qwidget.

        1.  Clear all the tags as set are getting updated at
            each time when user selects a tag
        2. Update in scroll area with the style
        3. Reset the index of tags dropdown to -1

        Args:
            tag (str): User selected tag from tag drop down
        """
        self.clear_all_tags()
        if tag not in self.all_tag:
            self.all_tag.append(tag)
        
        # After clearing, you might want to add the stretch back if it was removed
        if self.tags_layout.count() == 0:
            self.tags_layout.addStretch()
            
        # Create rows of tags
        row = None
        for i, tag in enumerate(self.all_tag):
            if i % 4 == 0:
                row = QtWidgets.QHBoxLayout()
                row.setSpacing(5)
                self.tags_layout.insertLayout(self.tags_layout.count()-1, row)
            
            style = list(TagWidget.STYLES.keys())[0]
            tag_widget = TagWidget(tag, style)
            tag_widget.closed.connect(self.remove_tag)  # Connect close signal
            row.addWidget(tag_widget)
        self.tags.setCurrentIndex(-1)
        

    def setup_tags(self):

        # Create scroll area
        self.tags_scroll.setWidgetResizable(True)
        self.tags_scroll.setFrameShape(QtWidgets.QFrame.NoFrame)
        
        # Create container widget for tags
        self.tags_widget = QtWidgets.QWidget()
        self.tags_layout = QtWidgets.QVBoxLayout(self.tags_widget)
        self.tags_layout.setSpacing(10)
        self.tags_layout.setContentsMargins(10, 10, 10, 10)
        
        # Add stretch to push tags to top
        self.tags_layout.addStretch()
        
        # Set the widget to scroll area
        self.tags_scroll.setWidget(self.tags_widget)


    def clear_all_tags(self):

        """Remove all tag widgets from the container"""

        # We'll work backwards through the layouts to avoid issues while removing
        for i in reversed(range(self.tags_layout.count())):
            item = self.tags_layout.itemAt(i)
            
            if item.layout():  # This is a row layout
                row_layout = item.layout()
                # Remove all widgets in this row
                for j in reversed(range(row_layout.count())):
                    widget = row_layout.takeAt(j).widget()
                    if widget is not None:
                        widget.deleteLater()
                # Remove the row layout itself
                self.tags_layout.removeItem(item)
        
        # # After clearing, you might want to add the stretch back if it was removed
        if self.tags_layout.count() == 0:
            self.tags_layout.addStretch()
    
    def remove_tag(self, tag_widget):

        """Remove a tag from the layout also from the list"""

        # Find which layout contains this widget
        for i in range(self.tags_layout.count() - 1):  # Skip the last stretch
            item = self.tags_layout.itemAt(i)
            if item.layout():  # This is a row layout
                row_layout = item.layout()
                for j in reversed(range(row_layout.count())):
                    if row_layout.itemAt(j).widget() == tag_widget:
                        # Remove the widget
                        widget = row_layout.takeAt(j).widget()
                        # remove from list too
                        self.all_tag.remove(widget.label.text())
                        widget.deleteLater()
                        
                        # If row is now empty, remove it
                        if row_layout.count() == 0:
                            self.tags_layout.removeItem(item)
                        return

    def eventFilter(self, obj, event):

        """ Handle the click event here. You can emit a custom signal here or call a method directly

        Returns:
            event: NOTE to include
        """
        if event.type() == QtCore.QEvent.MouseButtonPress:
            self.update_bundle_name_suggestions()
            # Return False to allow normal event processing to continue
            return False
        return super().eventFilter(obj, event)

    def update_bundle_name_suggestions(self):

        """Update the suggestions based on current text and bundle type"""

        current_text = self.bundle_name.toPlainText()
        
        if not current_text:
            # Get suggestions from your API or data source
            suggestions = self.get_bundle_name_suggestions()
            self.latest_version_label.clear()
            self.latest_version_label.setText('Latest Version: 1')
            
        else:
            self.user_bunlde_versions = set()
            suggestions = self.get_bundle_name_suggestions(current_text)
            self.latest_version_label.clear()
            get_versions = self.template_api.user_bundle_versions(current_text)
            for i in [i for i in get_versions][0]:
                self.user_bunlde_versions.add(i[0])
            self.user_bunlde_versions = max(self.user_bunlde_versions)+1 if self.user_bunlde_versions else 1
            self.latest_version_label.setText(f'Available Version: {self.user_bunlde_versions}')
            

        # Update the completer model
        self.completer_model.clear()
        for suggestion in suggestions:
            item = QtGui.QStandardItem(suggestion)
            self.completer_model.appendRow(item)
        
        self.completer.complete()

    def get_bundle_name_suggestions(self, text=''):

        tags = set()
        for items in [items for items in self.template_api.user_bundles()][0]:
            if text:
                if text in items[-1]:
                    tags.add(items[-1])
            else:
                tags.add(items[-1])
        return tags
    
    def grab_screen_shot(self):

        """User Selected Area is Screen shotted and saved inside
        C: drive temprory path  
        """
        overlay = OverlayWidget()

        if overlay.exec_() == QtWidgets.QDialog.Accepted:
            rect = overlay.rect
            pixmap = capture_screen(rect)
            # Temp Path of os system
            self.temp_snap_file_path = os.path.join(os.environ.get('TEMP'), 
                                            f"{self.bundle_name.toPlainText().replace(' ', '_')}.jpg"
            )
            pixmap.save(self.temp_snap_file_path, 'jpg')

            #Maximize the window once done 
            self.template_publisher_window.showNormal()
    
    def toggle_minimize(self) -> None:

        """Minimize the window and also maximize"""

        if self.template_publisher_window.isMinimized():
            self.template_publisher_window.showNormal()
        else:
            self.template_publisher_window.showMinimized()

    def set_file_path(self) -> None:
        """ Set File Dialog searched Folder Path to Imge path widget text"""

        img_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select JPG Img Directory", "")
        self.image_path.setText(img_path)

    def get_user_selected_tags(self) -> set:

        user_tags = set()
        for i in reversed(range(self.tags_layout.count())):
            item = self.tags_layout.itemAt(i)
            if item.layout():
                row_layout = item.layout()
                for j in reversed(range(row_layout.count())):
                    widget = row_layout.itemAt(j).widget()
                    user_tags.add(widget.label.text())
        return user_tags

    def publish(self) -> None:

        """Publihing the bundle

        Copying the bundles data from src to destination
        Registering in database
        """
        try:
            import hou
        except ImportError:
            pass
        
        user_tags = self.get_user_selected_tags()

        bundle_version_path = os.path.join(constant.TEMPLATE_BUNDLE_PATH, 
                                    self.bundle_type.currentText().replace(" ", "_"),
                                    self.bundle_name.toPlainText().replace(" ", "_"),
                                    f"v{str(self.user_bunlde_versions).zfill(3)}"
                                    )

        if self.is_template.isChecked():
            bundle_type_id = 1
            file_type = '.hip'

        if self.is_nodesnippet.isChecked():
            bundle_type_id = 2
            file_type = '.snip'
        
        bundle_file_path = os.path.join(bundle_version_path, 
                                        file_type.split(".")[-1])
        bundle_img_path = os.path.join(bundle_version_path, 'img')
        
        pub = publish.Publish(bundle_name= self.bundle_name.toPlainText().replace(" ", "_"), 
                description = self.description.toPlainText(),
                version=self.user_bunlde_versions,
                file_path=bundle_file_path,
                file_type = file_type,
                frame_start = hou.playbar.playbackRange()[0],
                frame_end = hou.playbar.playbackRange()[-1],
                artist = 'Chandrakanth',
                img_path= bundle_img_path,
                bundle_type_id = bundle_type_id,
                bundle_list_id= self.bundle_type.currentIndex()+1,
                category_id = self.category.currentIndex()+1 or 'null',
                context_id = self.context.currentIndex()+1 or 'null',
                houdini_version_id = 2,
                frame_count=(hou.playbar.playbackRange()[-1] - hou.playbar.playbackRange()[0])+1,
                user_selected_img_path=self.image_path.toPlainText(),
                user_screen_shot_img_path=self.temp_snap_file_path,
                user_tags= user_tags) #User browsed path
        pub.ops()
        self.toast = toast_notification.Toast()
        pub.register_db()
        self.toast.show_toast("Published .. Reload Houdini Template Manager....", 2000)


class CompleterProxyWidget(QtWidgets.QWidget):
    
    """A proxy widget to handle QCompleter for QTextEdit"""

    def __init__(self, text_edit):
        super().__init__(text_edit)
        self.text_edit = text_edit
        self.completer = None
        self.text_edit.installEventFilter(self)
        self.text_edit.viewport().installEventFilter(self)
        
    def setCompleter(self, completer):
        if self.completer:
            self.completer.activated.disconnect()
        self.completer = completer
        if self.completer:
            self.completer.setWidget(self.text_edit)
            self.completer.activated.connect(self.insertCompletion)
            
    def insertCompletion(self, completion):
        tc = self.text_edit.textCursor()
        tc.select(QtGui.QTextCursor.WordUnderCursor)
        tc.removeSelectedText()
        tc.insertText(completion)
        self.text_edit.setTextCursor(tc)
        
    def eventFilter(self, obj, event):
        if self.completer is None:
            return False
            
        if event.type() == QtCore.QEvent.KeyPress:
            key = event.key()
            
            if key in (QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return, QtCore.Qt.Key_Escape):
                if self.completer.popup().isVisible():
                    event.ignore()
                    return True
                    
            # Let the completer handle these keys
            if (key == QtCore.Qt.Key_Tab or key == QtCore.Qt.Key_Backtab):
                if self.completer.popup().isVisible():
                    event.ignore()
                    return True
                    
        return super().eventFilter(obj, event)

        
if __name__ == "__main__":
    
    import sys
    app = QtWidgets.QApplication(sys.argv)
    import_view = TemplatePublisher()
    import_view.template_publisher_window.show()
    app.exec_()
    