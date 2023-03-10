import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class CircuitElement(QGraphicsPixmapItem):
    def __init__(self, icon):
        self.icon = icon
        super().__init__(icon)
        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)
        self.setPos(0, 0)
        self.state = False
    
    def evaluate(self): 
        pass
    
    def mouseReleaseEvent(self, event):
        self.scene().clearSelection()
        self.setZValue(1)
        self.setCursor(Qt.OpenHandCursor)
        super().mouseReleaseEvent(event)
    
    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if self.isSelected():
            for sel_item in self.scene().selectedItems():
                sel_item.update()
    
class AndGate(CircuitElement):
    def __init__(self):
        super().__init__(QPixmap("res/and.png").scaled(70, 40))
        self.inputs = [QPointF(0, 5), QPointF(0, 25)]
        self.output = QPointF(60, 15)
        self.input_wires = [False, False]
    
    def evaluate(self):
        self.state = all(self.input_wires)

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
            self.setZValue(2)
            self.setCursor(Qt.ClosedHandCursor)
        super().mousePressEvent(event)

class OrGate(CircuitElement):
    def __init__(self):
        super().__init__(QPixmap("res/or.png").scaled(70, 40))
        self.inputs = [QPointF(0, 5), QPointF(0, 25)]
        self.output = QPointF(60, 15)
        self.input_wires = [False, False]
    
    def evaluate(self):
        self.state = any(self.input_wires)
    
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
            self.setZValue(2)
            self.setCursor(Qt.ClosedHandCursor)
        super().mousePressEvent(event)

class NotGate(CircuitElement):
    def __init__(self):
        super().__init__(QPixmap("res/not.png").scaled(70, 40))
        self.input = QPointF(0, 15)
        self.output = QPointF(60, 15)
        self.input_wire = False
    
    def evaluate(self):
        self.state = not self.input_wire

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
            self.setZValue(2)
            self.setCursor(Qt.ClosedHandCursor)
        super().mousePressEvent(event)

class XorGate(CircuitElement):
    def __init__(self):
        super().__init__(QPixmap("res/xor.png").scaled(70, 40))
        self.inputs = [QPointF(0, 5), QPointF(0, 25)]
        self.output = QPointF(60, 15)
        self.input_wires = [False, False]
    
    def evaluate(self):
        self.state = self.input_wires[0] != self.input_wires[1]
    
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
            self.setZValue(2)
            self.setCursor(Qt.ClosedHandCursor)
        super().mousePressEvent(event)

class Wire(QGraphicsLineItem):
    signal_updated = pyqtSignal()
    
    def __init__(self, input_gate, output_gate, parent=None):
        super().__init__(parent=parent)
        
        self.input_gate = input_gate
        self.output_gate = output_gate
        self.input_gate.add_output(self)
        self.output_gate.add_input(self)
        
        self.setFlags(QGraphicsLineItem.ItemIsSelectable |
                      QGraphicsLineItem.ItemIsMovable)
        self.setAcceptHoverEvents(True)
        self.setZValue(-1)
        
        self.pen = QPen(QColor(0, 0, 0), 3, Qt.SolidLine)
        self.update_line()
        
    def update_line(self):
        self.setLine(QLineF(self.mapFromItem(self.input_gate, 0, 0),
                            self.mapFromItem(self.output_gate, 0, 0)))
        
    def update_output(self):
        output_signal = self.input_gate.get_output()
        self.output_gate.set_input(output_signal)
        self.signal_updated.emit()

    def hoverEnterEvent(self, event):
        self.setPen(QPen(QColor(255, 0, 0), 3, Qt.SolidLine))
        self.update()

    def hoverLeaveEvent(self, event):
        self.setPen(QPen(QColor(0, 0, 0), 3, Qt.SolidLine))
        self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            for item in self.collidingItems():
                if isinstance(item, Gate):
                    if item is not self.input_gate and item is not self.output_gate:
                        if self.output_gate is item or self.input_gate is item:
                            self.scene().removeItem(self)
                            return
                        if isinstance(self.input_gate, InputGate):
                            self.input_gate.set_output(None)
                        elif isinstance(self.output_gate, OutputGate):
                            self.output_gate.set_input(None)
                        self.output_gate.remove_input(self)
                        self.input_gate.remove_output(self)
                        self.output_gate = item
                        self.output_gate.add_input(self)
                        self.update_line()
                        self.update_output()
                        return
            self.scene().removeItem(self)

class InputPin(QGraphicsItem):
    size = 30

    def __init__(self, parent=None):
        super().__init__(parent)
        self.rect = QRectF(-self.size/2, -self.size/2, self.size, self.size)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges, True)
        self.setAcceptHoverEvents(True)
        self.output = QPointF(5, -5)
        self._state = False

    def boundingRect(self):
        return self.rect

    def paint(self, painter, option, widget=None):
        painter.setBrush(QBrush(QColor("white")))
        painter.drawEllipse(self.boundingRect())

        if self._state:
            painter.setBrush(QBrush(QColor("green")))
        else:
            painter.setBrush(QBrush(QColor("red")))
        painter.drawEllipse(self.boundingRect().adjusted(5, 5, -5, -5))

        painter.setPen(QPen(QColor("black")))
        painter.drawText(self.boundingRect().adjusted(0, 5, 0, 0),
                         Qt.AlignHCenter, "{}".format(1 if self._state else 0))
        
        painter.drawRect(int(self.output.x()), int(self.output.y()), 10, 10)

    def mouseReleaseEvent(self, event):
        self.scene().clearSelection()
        self.setZValue(1)
        super().mouseReleaseEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setZValue(2)
            self._state = not self._state
            self.update()
            self.scene().update()
        print("INPUT pin clicked - {}".format("ON" if self._state else "OFF"))

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if self.isSelected():
            for sel_item in self.scene().selectedItems():
                sel_item.update()

    def value(self):
        return self._state

class OutputPin(QGraphicsItem):
    size = 30

    def __init__(self, parent=None):
        super().__init__(parent)
        self.rect = QRectF(-self.size/2, -self.size/2, self.size, self.size)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges, True)
        self.setAcceptHoverEvents(True)
        self.input = QPointF(-15, -5)
        self._state = False

    def boundingRect(self):
        return self.rect

    def paint(self, painter, option, widget=None):
        painter.setBrush(QBrush(QColor("white")))
        painter.drawRect(self.boundingRect())

        if self._state:
            painter.setBrush(QBrush(QColor("green")))
        else:
            painter.setBrush(QBrush(QColor("red")))
        painter.drawRect(self.boundingRect().adjusted(5, 5, -5, -5))

        painter.setPen(QPen(QColor("black")))
        painter.drawText(self.boundingRect().adjusted(0, 5, 0, 0),
                         Qt.AlignHCenter, "{}".format(1 if self._state else 0))
                         
        painter.drawRect(int(self.input.x()), int(self.input.y()), 10, 10)
    
    def mousePressEvent(self, event):
        self.setZValue(2)
        print("OUTPUT pin clicked - {}".format("ON" if self._state else "OFF"))

    def mouseReleaseEvent(self, event):
        self.scene().clearSelection()
        self.setZValue(1)
        super().mouseReleaseEvent(event)
    
    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if self.isSelected():
            for sel_item in self.scene().selectedItems():
                sel_item.update()

    def value(self):
        return self._state

    def setValue(self, state):
        self._state = state
        self.update()
        self.scene().update()

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
        inp_button = toolbar.addAction("INPUT")
        out_button = toolbar.addAction("OUTPUT")

        # Connect the buttons to the slot that handles their click events
        and_button.triggered.connect(self.andClicked)
        or_button.triggered.connect(self.orClicked)
        not_button.triggered.connect(self.notClicked)
        xor_button.triggered.connect(self.xorClicked)
        inp_button.triggered.connect(self.inpPinClicked)
        out_button.triggered.connect(self.outPinClicked)
    
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
    
    def inpPinClicked(self):
        # Create a new InputPin object and add it to the graphics scene
        pin = InputPin()
        self.scene.addItem(pin)
    
    def outPinClicked(self):
        # Create a new OutputPin object and add it to the graphics scene
        pin = OutputPin()
        self.scene.addItem(pin)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

