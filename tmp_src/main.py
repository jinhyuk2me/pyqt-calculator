import sys
from PyQt6.QtWidgets import QApplication
from view import CalculatorView
from controller import CalculatorController

def main():
    app = QApplication(sys.argv)
    view = CalculatorView()
    controller = CalculatorController(view)
    view.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
