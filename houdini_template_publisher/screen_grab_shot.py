"""
This example shows how to capture a screenshot of a specific area of the screen.
Warning: This has not been tested with multiple monitors.
Example:
    to capture the entire the current screen::
        from PySide2 import QtCore, QtWidgets
        app = QtWidgets.QApplication([])
        overlay = OverlayWidget()
        if overlay.exec_() == QtWidgets.QDialog.Accepted:
            rect = overlay.rect
            pixmap = capture_screen(rect)
            label = QtWidgets.QLabel()
            label.setPixmap(pixmap)
            label.show()
            sys.exit(app.exec_())
"""
import sys

from PySide2 import QtCore, QtGui, QtWidgets


def capture_screen(rect: QtCore.QRect = None) -> QtGui.QPixmap:
    screen = QtWidgets.QApplication.primaryScreen()
    if rect is None:
        return screen.grabWindow(0)
    return screen.grabWindow(0, rect.x(), rect.y(), rect.width(), rect.height())


class OverlayWidget(QtWidgets.QDialog):
    def __init__(self, parent=None, font=None):
        super().__init__(parent)
        self.rect = QtCore.QRect(0, 0, 0, 0)
        self._mouse_pressed = False

        # set up the window so that it is always on top and transparent
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # enable mouse tracking so that we can update the overlay as the mouse moves
        self.setMouseTracking(True)

        # set the cursor to a crosshair so that the user knows they can click and drag
        self.setCursor(QtCore.Qt.CrossCursor)

        # set up the semi-transparent brush for drawing the 'light-box' overlay
        self.brush = QtGui.QBrush()
        self.brush.setColor(QtGui.QColor(0, 0, 0, 127))
        self.brush.setStyle(QtCore.Qt.SolidPattern)

        # set up the pen for drawing the text
        self.text_pen = QtGui.QPen()
        self.text_pen.setColor(QtGui.QColor(255, 255, 255, 255))
        self.text_pen.setWidth(2)

        if font is None:
            self.font = QtGui.QFont()
            self.font.setPointSize(24)
        else:
            self.font = font

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)

        # draw a semi-transparent 'light-box' over the entire screen, we do this by first creating a polygon
        # that covers the entire screen, then subtracting the selection rectangle from the polygon if it has
        # a size greater than zero
        polygon = QtGui.QPolygon([
            QtCore.QPoint(0, 0),
            QtCore.QPoint(self.width(), 0),
            QtCore.QPoint(self.width(), self.height()),
            QtCore.QPoint(0, self.height()),
        ])

        # if the selection rectangle has a size greater than zero, subtract it from the polygon so that
        # the overlay is transparent in the selection area
        if self.rect.width() > 0 and self.rect.height() > 0:
            polygon = polygon.subtracted(QtGui.QPolygon(self.rect))
        else:
            # otherwise, draw the text instructing the user to click and drag to select an area
            painter.setPen(self.text_pen)
            painter.setFont(self.font)
            painter.drawText(event.rect(), QtCore.Qt.AlignCenter, "click & drag to select area")

        # finally draw the polygon
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(self.brush)
        painter.drawPolygon(polygon)
        painter.end()

    def mousePressEvent(self, event):
        # initiate the selection process when the left mouse button is pressed
        if event.button() == QtCore.Qt.LeftButton:
            self._mouse_pressed = True
            self.rect = QtCore.QRect(event.pos(), QtCore.QSize(0, 0))
            self.update()
        else:
            # cancel the selection process if any other mouse button is pressed
            self.reject()

    def mouseMoveEvent(self, event):
        # update the selection rectangle as the mouse is dragged
        if self._mouse_pressed:
            self.rect.setBottomRight(event.pos())
            self.update()

    def mouseReleaseEvent(self, event):
        # accept the selection when the left mouse button is released
        if event.button() == QtCore.Qt.LeftButton:
            self.accept()

    def keyPressEvent(self, event):
        # cancel the selection process if the escape key is pressed
        if event.key() == QtCore.Qt.Key_Escape:
            self.reject()

    def exec_(self):
        # make sure the overlay is always on top of other windows
        self.showFullScreen()
        return super().exec_()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    overlay = OverlayWidget()

    # if the user selects an area, capture the screen and display it in a label
    # otherwise just exit
    if overlay.exec_() == QtWidgets.QDialog.Accepted:
        rect = overlay.rect
        pixmap = capture_screen(rect)
        pixmap.save(r'D:\fastapi_tut\shot.jpg', 'jpg')
        label = QtWidgets.QLabel()
        label.setPixmap(pixmap)
        label.show()

        # only start the applications event loop if we want to display the captured image
        app.exec_()
    else:
        sys.exit(0)