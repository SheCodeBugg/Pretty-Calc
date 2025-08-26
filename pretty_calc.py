import sys
from functools import partial
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget
from window import Ui_Form

ERROR_MSG = "ERROR"

class PrettyCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self._createButtonMap()
        self._connectSignalsAndSlots()
        
    def _createButtonMap(self):

        self.buttonMap = {
            '0': self.ui.pushButton_0,
            '1': self.ui.pushButton_1,
            '2': self.ui.pushButton_2,
            '3': self.ui.pushButton_3,
            '4': self.ui.pushButton_4,
            '5': self.ui.pushButton_5,
            '6': self.ui.pushButton_6,
            '7': self.ui.pushButton_7,
            '8': self.ui.pushButton_8,
            '9': self.ui.pushButton_9,
            '00': self.ui.pushButton_00,
            '.': self.ui.pushButton_dec,
            '+': self.ui.pushButton_plus,
            '-': self.ui.pushButton_minus,
            '*': self.ui.pushButton_times,
            '/': self.ui.pushButton_divide,
            '=': self.ui.pushButton_equal,
            'C': self.ui.pushButton_clear,
            '(': self.ui.pushButton_oPar,
            ')': self.ui.pushButton_cPar,
        }

    def _connectSignalsAndSlots(self):
        for key, button in self.buttonMap.items():
            if key not in {'=', 'C'}:
                button.clicked.connect(partial(self._buildExpression, key))

        self.buttonMap['='].clicked.connect(self._calculateResult)
        self.buttonMap['C'].clicked.connect(self._clearDisplay)

        self.ui.lineEdit.returnPressed.connect(self._calculateResult)        

    def _buildExpression(self, subExpression):
        current_text = self.displayText()
        if current_text == ERROR_MSG:
            self._clearDisplay()
            current_text = ""

        if current_text == "0" and subExpression.isdigit():
            self.setDisplayText(subExpression)
        elif current_text == "0" and subExpression == "00":
            self.setDisplayText("0")
        else:
            new_expression = current_text + subExpression
            self.setDisplayText(new_expression)

    def _calculateResult(self):
        expression = self.displayText()
        if not expression or expression == "0":
            return
        try: 
            result = str(eval(expression, {"__builtins__": {}}, {}))
            self.setDisplayText(result)
        except ZeroDivisionError:
            self.setDisplayText("0")
        except Exception:
            self.setDisplayText(ERROR_MSG)

    def _clearDisplay(self):
        self.setDisplayText("0")

    def setDisplayText(self, text):
        self.ui.lineEdit.setText(str(text))
        self.ui.lineEdit.setFocus()

    def displayText(self):
        return self.ui.lineEdit.text()
    
def main():
    app = QApplication(sys.argv)
    calculator = PrettyCalculator()
    calculator.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()