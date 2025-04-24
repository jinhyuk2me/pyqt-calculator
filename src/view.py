from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import QTimer
from PyQt6 import uic


class CalculatorView(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("calculator.ui", self)

        # 메시지 영역 사이즈 고정
        self.textBrowser.setFixedWidth(310)
        self.textBrowser.setFixedHeight(40)

    def connect_signals(self, controller):
        # 숫자 버튼 연결
        for i in range(10):
            getattr(self, f"pushButton_{i}").clicked.connect(lambda _, x=i: controller.handle_digit(str(x)))
        self.pushButton_point.clicked.connect(lambda: controller.handle_digit("."))

        # 연산자 버튼
        self.pushButton_add.clicked.connect(lambda: controller.handle_operator("+"))
        self.pushButton_sub.clicked.connect(lambda: controller.handle_operator("-"))
        self.pushButton_mul.clicked.connect(lambda: controller.handle_operator("*"))
        self.pushButton_div.clicked.connect(lambda: controller.handle_operator("/"))

        # 괄호
        self.pushButton_lparen.clicked.connect(controller.handle_lparen)
        self.pushButton_rparen.clicked.connect(controller.handle_rparen)

        # 기능 버튼
        self.pushButton_equal.clicked.connect(controller.handle_equal)
        self.pushButton_AC.clicked.connect(controller.handle_ac)
        self.pushButton_C.clicked.connect(controller.handle_c)
        self.pushButton_sign.clicked.connect(controller.handle_sign)

    def update_result_display(self, value: str):
        # 아래 라인: 현재 입력값 or 계산 결과 표시
        self.lineEdit.setText(value)

    def update_expression_display(self, tokens: list[str]):
        # 위 라인: 수식 구성 상태 표시
        pretty = []
        for token in tokens:
            try:
                val = float(token)
                pretty.append(str(int(val)) if val.is_integer() else token)
            except:
                pretty.append(token)
        self.lineEdit_2.setText(" ".join(pretty))

    def show_message(self, msg: str):
        # 사용자 메시지 (오류 등) 표시
        QTimer.singleShot(50, lambda: self._delayed_show_message(msg))
        QTimer.singleShot(2050, self.clear_message)

    def _delayed_show_message(self, msg: str):
        self.textBrowser.setText(msg)
        self.textBrowser.setVisible(True)
        self.textBrowser.adjustSize()

    def clear_message(self):
        self.textBrowser.setText("")
