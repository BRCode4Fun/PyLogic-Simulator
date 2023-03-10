import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class AndGate(QGraphicsPixmapItem):
   def __init__(self):
        self.icon = QPixmap("res/and.png").scaled(70, 40)
        super().__init__(self.icon)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.inputs = [QPointF(0, 5), QPointF(0, 25)]
        self.output = QPointF(60, 15)
        self.setPos(0, 0)
    
   def paint(self, painter, option, widget):
        # Draw the gate's shape and label
        painter.drawPixmap(self.icon.rect(), self.icon)
        painter.setFont(QFont("times", 12))
        painter.drawText(self.icon.rect(), Qt.AlignCenter, "&")

        # Draw the gate's input and output terminals
        for point in self.inputs:
            painter.drawRect(int(point.x()), int(point.y()), 10, 10)
        painter.drawRect(int(self.output.x()), int(self.output.y()), 10, 10)

   def mousePressEvent(self, event):
        print("AND gate clicked")
        if event.button() == Qt.LeftButton:
            self.setCursor(Qt.ClosedHandCursor)
        super().mousePressEvent(event)
        
   def mouseReleaseEvent(self, event):
        self.setCursor(Qt.OpenHandCursor)
        super().mouseReleaseEvent(event)
    
   def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if self.isSelected():
            for sel_item in self.scene().selectedItems():
                sel_item.update()

class OrGate(QGraphicsPixmapItem):
   def __init__(self):
        self.icon = QPixmap("res/or.png").scaled(70, 40)
        super().__init__(self.icon)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.inputs = [QPointF(0, 5), QPointF(0, 25)]
        self.output = QPointF(60, 15)
        self.setPos(0, 0)
    
   def paint(self, painter, option, widget):
        # Draw the gate's shape and label
        painter.drawPixmap(self.icon.rect(), self.icon)
        painter.setFont(QFont("times", 12))
        painter.drawText(self.icon.rect(), Qt.AlignCenter, "≥1")

        # Draw the gate's input and output terminals
        for point in self.inputs:
            painter.drawRect(int(point.x()), int(point.y()), 10, 10)
        painter.drawRect(int(self.output.x()), int(self.output.y()), 10, 10)

   def mousePressEvent(self, event):
        print("OR gate clicked")
        if event.button() == Qt.LeftButton:
            self.setCursor(Qt.ClosedHandCursor)
        super().mousePressEvent(event)
        
   def mouseReleaseEvent(self, event):
        self.setCursor(Qt.OpenHandCursor)
        super().mouseReleaseEvent(event)
    
   def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if self.isSelected():
            for sel_item in self.scene().selectedItems():
                sel_item.update()


class NotGate(QGraphicsPixmapItem):
    def __init__(self):
        self.icon = QPixmap("res/not.png").scaled(70, 40)
        super().__init__(self.icon)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.input = QPointF(0, 15)
        self.output = QPointF(60, 15)
        self.setPos(0, 0)

    def paint(self, painter, option, widget):
        # Draw the gate's shape and label
        painter.drawPixmap(self.icon.rect(), self.icon)
        painter.setFont(QFont("times", 14))
        painter.drawText(self.icon.rect(), Qt.AlignCenter, "~  ")

        # Draw the gate's input and output terminals
        painter.drawRect(int(self.input.x()), int(self.input.y()), 10, 10)
        painter.drawRect(int(self.output.x()), int(self.output.y()), 10, 10)

    def mousePressEvent(self, event):
        print("NOT gate clicked")
        if event.button() == Qt.LeftButton:
            self.setCursor(Qt.ClosedHandCursor)
        super().mousePressEvent(event)
        
    def mouseReleaseEvent(self, event):
        self.setCursor(Qt.OpenHandCursor)
        super().mouseReleaseEvent(event)
    
    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if self.isSelected():
            for sel_item in self.scene().selectedItems():
                sel_item.update()

class XorGate(QGraphicsPixmapItem):
   def __init__(self):
        self.icon = QPixmap("res/xor.png").scaled(70, 40)
        super().__init__(self.icon)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.inputs = [QPointF(0, 5), QPointF(0, 25)]
        self.output = QPointF(60, 15)
        self.setPos(0, 0)
    
   def paint(self, painter, option, widget):
        # Draw the gate's shape and label
        painter.drawPixmap(self.icon.rect(), self.icon)
        painter.setFont(QFont("times", 12))
        painter.drawText(self.icon.rect(), Qt.AlignCenter, "=1")

        # Draw the gate's input and output terminals
        for point in self.inputs:
            painter.drawRect(int(point.x()), int(point.y()), 10, 10)
        painter.drawRect(int(self.output.x()), int(self.output.y()), 10, 10)

   def mousePressEvent(self, event):
        print("XOR gate clicked")
        if event.button() == Qt.LeftButton:
            self.setCursor(Qt.ClosedHandCursor)
        super().mousePressEvent(event)
        
   def mouseReleaseEvent(self, event):
        self.setCursor(Qt.OpenHandCursor)
        super().mouseReleaseEvent(event)
    
   def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if self.isSelected():
            for sel_item in self.scene().selectedItems():
                sel_item.update()

class MainWindow(QMainWindow):
    def __init__(self):
     
        super().__init__()
        self.initUI()

    def initUI(self):
        # Create the main window and set its properties
        self.setWindowTitle("Digital Logic Simulator")
        self.setGeometry(100, 100, 800, 600)

        # Create a toolbar and add it to the main window
        toolbar = QToolBar("Tools", self)
        self.addToolBar(toolbar)

        # Create buttons for the toolbar
        and_button = toolbar.addAction("AND")
        or_button = toolbar.addAction("OR")
        not_button = toolbar.addAction("NOT")
        xor_button = toolbar.addAction("XOR")

        # Connect the buttons to the slot that handles their click events
        and_button.triggered.connect(self.andClicked)
        or_button.triggered.connect(self.orClicked)
        not_button.triggered.connect(self.notClicked)
        xor_button.triggered.connect(self.xorClicked)

        # Create a central widget and set it as the main widget for the main window
        self.central_widget = QGraphicsView()
      
        self.setCentralWidget(self.central_widget)

        # Create a graphics scene and set it as the scene for the graphics view
        self.scene = QGraphicsScene()
        self.central_widget.setScene(self.scene)
    

    def andClicked(self):
         # Create a new AndGate object and add it to the graphics scene
        gate = AndGate()
        self.scene.addItem(gate)

    def orClicked(self):
        # Create a new OrGate object and add it to the graphics scene
        gate = OrGate()
        self.scene.addItem(gate)

    def notClicked(self):
        # Create a new NotGate object and add it to the graphics scene
        gate = NotGate()
        self.scene.addItem(gate)

    def xorClicked(self):
        # Create a new XorGate object and add it to the graphics scene
        gate = XorGate()
        self.scene.addItem(gate)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

