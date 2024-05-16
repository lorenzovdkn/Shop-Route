import sys
from PyQt6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PyQt6.QtGui import QColor, QMouseEvent, QWheelEvent
from PyQt6.QtCore import Qt, QPointF

class GraphicsView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        
        self.setSceneRect(-500, -500, 1000, 1000)  # Initial scene rectangle
        self.centerOn(0, 0)  # Center the view on the origin

        self._zoom = 0
        self.zoom_factor = 1.25

class MainWindow(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        # Add some items to the scene
        self.scene.addRect(-100, -100, 200, 200, pen=QColor("black"))
        self.scene.addRect(-200, -200, 400, 400, pen=QColor("red"))

        # Enable dragging the scene with the mouse
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setSceneRect(-300, -300, 600, 600)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    view = GraphicsView()
    scene = QGraphicsScene()
    view.setScene(scene)

    # Add a few rectangles to the scene
    for i in range(5):
        for j in range(5):
            rect = QGraphicsRectItem(i * 100, j * 100, 80, 80)
            rect.setBrush(QColor("lightblue"))
            scene.addItem(rect)

    view.show()
    sys.exit(app.exec())
