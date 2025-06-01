from PySide2 import QtCore, QtWidgets, QtWebEngineWidgets, QtWebChannel
from PySide2.QtCore import QCoreApplication
from PySide2 import QtCore
import os

# NOTE: QTWEBENGINE_CHROMIUM_FLAGS=--enable-gpu-rasterization is an environment variable 
# used to control Chromium's behavior within Qt WebEngine applications. 
# Specifically, it enables the use of GPU rasterization for rendering web content. 
#
#--enable-gpu-rasterization:
#This flag instructs Chromium to utilize the GPU for rendering web content by rasterizing it. 
# Rasterization is the process of converting 3D or 2D graphics into a pixel-by-pixel image
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--enable-gpu-rasterization"
os.environ["D3D_ADAPTER_OVERRIDE"] = "NVIDIA"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"  # Use first NVIDIA GPU
os.environ["QT_OPENGL"] = "angle"  # Use ANGLE backend which works better with NVIDIA


class Toast(QtWidgets.QWidget):
    """Custom Toast widget
    
    Class for custom toast notifications
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Tool | QtCore.Qt.NoFocus)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_ShowWithoutActivating)
        self.setAttribute(QtCore.Qt.WA_QuitOnClose, False)
        
        self.setLayout(QtWidgets.QVBoxLayout())
        self.label = QtWidgets.QLabel(self)
        self.label.setStyleSheet("""
            background-color: #333333;
            color: white;
            padding: 10px;
            border-radius: 5px;
            font-size: 20px;
        """)
        self.layout().addWidget(self.label)
        self.layout().setContentsMargins(0, 0, 0, 0)
        
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.hide)
        
        self.animation = QtCore.QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(300)
    
    def show_toast(self, message, duration=3000):
        """Show the toast notification for given timing

        Args:
            message (str): Message to show
            duration (int, int): Seconds to show. Defaults to 3000.
        """
        self.label.setText(message)
        self.label.adjustSize()
        self.adjustSize()
        
        # Position at bottom right of parent or screen
        parent_geometry = self.parent().geometry() if self.parent() else QtWidgets.QApplication.desktop().availableGeometry()
        self.move(parent_geometry.right() - self.width() - 1200,
                 parent_geometry.bottom() - self.height() - 100)
        
        self.show()
        
        # Fade in animation
        self.animation.stop()
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()
        
        self.timer.start(duration)
    
    def hide(self):
        """Hide the toast"""
        # Fade out animation
        self.animation.stop()
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.finished.connect(super().hide)
        self.animation.start()
        
        self.timer.stop()
        


class HoudiniTemplateManager(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(HoudiniTemplateManager, self).__init__(parent)

        # NOTE: backend and channel MUST be class or global variables
        self.setGeometry(0, 0, 1900, 950)
        self.setWindowTitle("Houdini Template Manger")

        self.backend = HoudiniWebManager()
        self.channel = QtWebChannel.QWebChannel()
        self.channel.registerObject("manager", self.backend)

        self.view = QtWebEngineWidgets.QWebEngineView()
        self.view.reload()
        # self.view.settings().setAttribute(QWebEngineSettings.Accelerated2dCanvasEnabled, False)
        self.view.page().setWebChannel(self.channel)

        self.load()
        self.setCentralWidget(self.view)
        self.view.setZoomFactor(1.3)
        
        toolbar = QtWidgets.QToolBar()
        self.addToolBar(toolbar)
         
        # Add a back action to the toolbar
        back_action = QtWidgets.QAction("Reload", self)
        back_action.triggered.connect(self.load)
        toolbar.addAction(back_action)
        # this fully stops the instance from running after the window is closed
        self.setAttribute(QtCore.Qt.WA_NativeWindow, True )

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    
    def load(self):
        self.view.page().profile().clearHttpCache()
        url = QtCore.QUrl('http://houdini-template-manager.com/')
        self.view.load(url)
        

class HoudiniWebManager(QtCore.QObject):
    """Houdini web manager communicate with JS
    """
    def __init__(self, *args, **kwargs):
        super(HoudiniWebManager, self).__init__(*args, **kwargs)

    @QtCore.Slot(str, str, str, str)
    def import_file(self, 
                    file_path:str, 
                    context: str,
                    bundle_list: str,
                    bundle_name) -> None:

        """Import file into houdini

        Args:
            file_path (str): path of the file
        """

        def show_toast(msg):
            toast = Toast(hou.qt.mainWindow())
            toast.show_toast(msg, 2000)

        # Merge the hip file to current working hip file
        if file_path.endswith(".hip"):
            if hou.ui.displayMessage("Merge hip file?", buttons=("Yes", "No")) == 0:
                hou.hipFile.merge(file_path,
                                overwrite_on_conflict=False
                                )
                show_toast(f"Hip Merged!")

        elif file_path.endswith(".snip"):

            def create_geo():
                geo_node = hou.node('/obj').createNode('geo')
                name = bundle_list.replace(' ', '_') +'_' + bundle_name.replace(' ', '_')
                geo_node.setName(name, unique_name=True)
                return geo_node

            desktop = hou.ui.curDesktop()
            pane =  desktop.paneTabOfType(hou.paneTabType.NetworkEditor)
            current_network_editor_path = pane.pwd()
            get_current_network_editor_path = pane.pwd().type().name()
            
            if context == 'vop':
                if get_current_network_editor_path == 'attribvop' or \
                            get_current_network_editor_path == 'volumevop':
                    current_network_editor_path.loadItemsFromFile(file_path)
                    show_toast("Imported!")
                else:
                    if hou.ui.displayMessage("No Path Found. Import In New Node?", buttons=("Yes", "No")) == 0:
                        geo_node = create_geo()
                        vop_node = geo_node.createNode("attribvop")
                        pane.cd(vop_node.path())
                        vop_node.loadItemsFromFile(file_path)
                        show_toast(f"New node created and loaded!")


            if context == 'sop':
                if get_current_network_editor_path == 'geo':
                    current_network_editor_path.loadItemsFromFile(file_path)
                    show_toast("Imported!")
                else:
                    if hou.ui.displayMessage("No Path Found. Import In New Node?", buttons=("Yes", "No")) == 0:
                        geo_node = create_geo()
                        pane.cd(geo_node.path())
                        geo_node.loadItemsFromFile(file_path)
                        show_toast(f"New node created and loaded!")


            if context == 'dop':
                if get_current_network_editor_path == 'dopnet':
                    show_toast("Imported!")
                    current_network_editor_path.loadItemsFromFile(file_path)
                else:
                    if hou.ui.displayMessage("No Path Found. Import In New Node?", buttons=("Yes", "No")) == 0:
                        geo_node = create_geo()
                        dop_node = geo_node.createNode("dopnet")
                        pane.cd(dop_node.path())
                        dop_node.loadItemsFromFile(file_path)
                        show_toast(f"New node created and loaded!")

if __name__ == "__main__":
    from PySide2.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    demo = HoudiniTemplateManager()
    demo.show()
    app.exec_()