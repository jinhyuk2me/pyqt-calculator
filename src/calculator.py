import sys
from PyQt6.QtWidgets import *
from PyQt6 import uic

form_class = uic.loadUiType("/home/jinhyuk2me/project/iot/qt_calculator/src/calculator.ui")[0]

class Calculator(QDialog, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.tokens = []
        self.prev_expression = []
        self.current_input = ""
        self.just_calculated = True
        self.just_errored = False

        for i in range(10):
            getattr(self, f"pushButton_{i}").clicked.connect(lambda _, x=str(i): self.input_digit(x))
        self.pushButton_point.clicked.connect(lambda: self.input_digit("."))

        self.pushButton_add.clicked.connect(lambda: self.input_operator("+"))
        self.pushButton_sub.clicked.connect(lambda: self.input_operator("-"))
        self.pushButton_mul.clicked.connect(lambda: self.input_operator("*"))
        self.pushButton_div.clicked.connect(lambda: self.input_operator("/"))
        self.pushButton_paren.clicked.connect(self.input_paren)

        self.pushButton_equal.clicked.connect(self.press_equal)
        self.pushButton_AC.clicked.connect(self.press_ac)
        self.pushButton_C.clicked.connect(self.press_c)
        self.pushButton_sign.clicked.connect(self.toggle_sign)

        self.update_display()

    # ----------------------------------------------------------

    def input_digit(self, digit):
        self.clear_error()

        # 계산되어 출력된 값이 있을 경우
        if self.just_calculated:
            self.tokens = []
            if digit == ".":
                self.current_input = "0."
            else:
                self.current_input = digit
            self.just_calculated = False
            self.update_display()
            return

        # 초기상태에서 digit을 입력할 경우
        if self.current_input == "0" and digit != ".":
            self.current_input = digit
        else:
            # point가 2개 이상 입력되는 것을 방지
            if digit == "." and "." in self.current_input:
                return
            # 초기상태에서 point를 입력할 경우
            if digit == "." and self.current_input == "":
                self.current_input = "0"
            # 입력값이 입력창보다 커지는 것을 방지
            if len(self.current_input) >= 20:
                return
            self.current_input += digit

        self.update_display()

    def input_operator(self, op):
        # 입력된 값이 있을 경우
        if self.current_input:
            # 입력된 값이 에러 메세지인 경우 별도 함수를 통해 처리
            if self.clear_error():
                return
            # 입력된 값이 '.'으로 끝났을 경우 0을 추가
            if self.current_input[-1] == ".":
                self.current_input += "0"
            # 입력된 값이 '-'로 끝날 경우
            elif self.current_input[-1] == "-":
                # 입력된 operator가 '-'이 아닌 경우 입력 무시
                if op in "+*/":
                    return
                # 입력된 operator가 '-'일 경우 다시 초기상태로 복귀
                else:
                    self.current_input = ""
                    self.update_display()
                    return
            self.tokens.append(self.current_input)
            self.current_input = ""
        # 입력된 값이 없고 self.tokens가 비어있을 경우
        elif not self.tokens :
            # '-'를 operator가 아니라 sign으로 처리
            if op == "-":
                self.current_input = "-"
                self.just_calculated = False
                self.update_display()
                return
            # 다른 연산자의 경우 0을 대상으로 연산
            else :
                self.tokens = ["0", op]
                self.current_input = ""
                self.update_display()
                return

        # '('로 끝나는 self.tokens가 존재하고 입력된 연산자가 '-'일 때
        # 입력된 연산자는 operator가 아니라 sign으로 처리
        if self.tokens and self.tokens[-1] == "(" and op == "-":
            self.current_input = "-"
            self.just_calculated = False
            self.update_display()
            return

        # [+-*/]로 끝나는 self.tokens가 존재할 때
        if self.tokens and self.tokens[-1] in "+-*/":
            self.tokens[-1] = op # operator를 교체
        else:
            self.tokens.append(op)

        self.just_calculated = False
        self.update_display()

    def input_paren(self):

        # 에러 출력시 바로 누를 것을 고려하여 별도 함수를 통해서 error 비우기
        self.clear_error()

        # 현재 존재하는 괄호 수
        left = self.tokens.count("(")
        right = self.tokens.count(")")

        #  출력된 값이 존재하는 상황
        if self.just_calculated:
            # 출력된 값에 괄호를 곱하는 것으로 처리
            if self.current_input:
                self.tokens = [self.current_input, "*"]
            # 없어도 무방한 방어적 else
            else: 
                self.tokens = []
            self.current_input = ""
            self.just_calculated = False

        # 출력값이 아닌 입력된 값이 존재하는 상황
        if self.current_input:
            # 초기 상태에서 [-] 입력 후 곧바로 [(] 입력시 [-1*(]로 자동 변환
            if self.current_input == "-" and not self.tokens:
                self.tokens.append("-1")
                self.tokens.append("*")
                self.current_input = ""
            else:
                self.tokens.append(self.current_input)
                self.current_input = ""

        # 괄호의 수를 자동으로 검사하여 '('와 ')'를 선택한다.
        if left <= right:
            if self.tokens and (self.is_number(self.tokens[-1]) or self.tokens[-1] == ")"):
                self.tokens.append("*")
            self.tokens.append("(")
        else:
            self.tokens.append(")")

        self.update_display()

    # ----------------------------------------------------------

    def press_equal(self):
        if self.current_input:
            self.tokens.append(self.current_input)
        elif not self.tokens:
            return

        self.prev_expression = self.tokens.copy()  # 💡 수식 저장

        postfix = self.to_postfix(self.tokens)
        try:
            if postfix == "Error": raise Exception
            result = self.evaluate_postfix(postfix)
            self.current_input = result
            self.tokens = []
        except:
            self.current_input = "Error"
            self.just_errored = True
            self.tokens = []
        self.just_calculated = True
        self.update_display()


    # ----------------------------------------------------------

    def press_ac(self):
        self.tokens = []
        self.current_input = ""
        self.just_calculated = False
        self.update_display()

    def press_c(self):
        self.current_input = ""
        self.just_calculated = False
        self.update_display()

    def toggle_sign(self):
        if self.current_input.startswith("-"): 
            self.current_input = self.current_input[1:]
        elif self.current_input == "0": 
            return
        elif self.current_input: 
            self.current_input = "-" + self.current_input
        self.update_display()

    # ----------------------------------------------------------

    def update_display(self):
        self.update_lineEdit_2()
        self.update_lineEdit()

    # 하단 lineEdit
    def update_lineEdit(self):
        if self.current_input == "":
            #if self.tokens == [] and not self.just_calculated:
            if self.tokens == []:
                self.lineEdit.setText("0")
            else:
                self.lineEdit.setText("")
        else:
            if self.current_input.endswith("."):
                self.lineEdit.setText(self.current_input)
            elif self.is_number(self.current_input):
                val = float(self.current_input)
                if val.is_integer() and self.just_calculated:
                    self.lineEdit.setText(str(int(val)))
                else:
                    self.lineEdit.setText(self.current_input)
            else:
                self.lineEdit.setText(self.current_input)

    # 상단 lineEdit
    def update_lineEdit_2(self):
        pretty_tokens = []

        # 계산이 방금 끝난 경우, prev_expression을 보여줌
        tokens_to_display = self.prev_expression if self.just_calculated and self.prev_expression else self.tokens

        for token in tokens_to_display:
            if self.is_number(token):
                val = float(token)
                if val.is_integer():
                    pretty_tokens.append(str(int(val)))
                else:
                    pretty_tokens.append(token)
            else:
                pretty_tokens.append(token)
        self.lineEdit_2.setText(" ".join(pretty_tokens))

    # ----------------------------------------------------------

    # evaluate_postfix()를 위한 전처리 단계
    def to_postfix(self, tokens):
        prec = {'+': 2, '-': 2, '*': 3, '/': 3}
        output = []
        stack = []
        paren_balance = 0

        for token in tokens:
            if token not in "+-*/()":
                output.append(token)
            elif token == "(":
                stack.append(token)
                paren_balance += 1
            elif token == ")":
                paren_balance -= 1
                if paren_balance < 0:
                    self.just_errored = True
                    return "Error"
                while stack and stack[-1] != "(":
                    output.append(stack.pop())
                stack.pop()
            else:
                while stack and stack[-1] != "(" and prec.get(stack[-1], 0) >= prec[token]:
                    output.append(stack.pop())
                stack.append(token)

        while stack:
            if stack[-1] in "()":
                self.just_errored = True
                return "Error"
            output.append(stack.pop())

        if paren_balance != 0:
            self.just_errored = True
            return "Error"

        return output

    def evaluate_postfix(self, postfix):
        stack = []
        try:
            for token in postfix:
                if token not in "+-*/":
                    stack.append(float(token))
                else:
                    b = stack.pop()
                    a = stack.pop()
                    if token == "+":
                        stack.append(a + b)
                    elif token == "-":
                        stack.append(a - b)
                    elif token == "*":
                        stack.append(a * b)
                    elif token == "/":
                        if b == 0:
                            raise ZeroDivisionError
                        stack.append(a / b)

            if len(stack) == 1:
                return str(stack[0])
            else:
                raise ValueError
        except:
            self.just_errored = True
            return "Error"
    
    # ----------------------------------------------------------------------

    def is_number(self, target):
        try:
            float(target)
            return True
        except:
            return False

    def is_zero(self, target):
        return self.is_number(target) and float(target) == 0
    
    # ----------------------------------------------------------------------

    def clear_error(self):
        if self.just_errored:
            self.tokens = []
            self.current_input = ""
            self.just_errored = False
            self.update_display()
            return True
        return False
    
    # ----------------------------------------------------------------------

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Calculator()
    window.show()
    sys.exit(app.exec())