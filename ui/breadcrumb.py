from PySide import QtGui
from PySide import QtCore


class QBreadcrumb(QtGui.QWidget):
    def __init__(self, parent=None):
        super(QBreadcrumb, self).__init__(parent)        
        self.parent = parent
        self.layout = QtGui.QHBoxLayout(self)
        self.layout.setSpacing(2)
        m = 3
        self.layout.setContentsMargins(m, m, m, m)
        self.layout.setAlignment(QtCore.Qt.AlignTop)

        self.buttons = []
        self.dividers = []

        num_of_buttons = 5
        for value in range(num_of_buttons):
            self._add_button()        

    def set_breadcrumb_label(self, *args):
        
        button_activators = [args[-1]]
        parent = args[-1].parent()
        if parent:
            button_activators.append(parent)
            while parent.parent() is not None:
                parent = parent.parent()
                button_activators.append(parent)

        if button_activators:
            button_activators.reverse()
            for idx, item in enumerate(button_activators):
                self.buttons[idx].setText(item.get_name())
                self.buttons[idx].setVisible(True)
                self.dividers[idx].setVisible(True)
                self.buttons[idx].clicked.connect(lambda: self._select_in_tree(item))

    def _select_in_tree(self, item):
        # print self.parent, item.get_name()
        self.parent.setCurrentItem(item)

    def _add_button(self):
        button = QtGui.QPushButton('..')
        button.setFixedWidth(70)
        button.setVisible(False)
        self.layout.addWidget(button)
        self._add_divider()
        self.buttons.append(button)

    def _add_divider(self):
        divider = QtGui.QLabel('>')
        divider.setFixedWidth(8)
        divider.setVisible(False)
        self.layout.addWidget(divider)
        self.dividers.append(divider)
