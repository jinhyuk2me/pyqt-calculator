import sys
from PyQt6.QtWidgets import *
from PyQt6 import uic
from PyQt6.QtCore import QTimer


form_class = uic.loadUiType("/home/jinhyuk2me/project/iot/qt_calculator/src/advanced_calculator.ui")[0]

class Calculator(QDialog, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.tokens = []
        self.prev_expression = []
        self.current_input = ""
        self.just_calculated = True
        self.just_errored = False

        self.textBrowser.setFixedWidth(310)
        self.textBrowser.setFixedHeight(40)

        for i in range(10):
            getattr(self, f"pushButton_{i}").clicked.connect(lambda _, x=str(i): self.input_digit(x))
        self.pushButton_point.clicked.connect(lambda: self.input_digit("."))

        self.pushButton_add.clicked.connect(lambda: self.input_operator("+"))
        self.pushButton_sub.clicked.connect(lambda: self.input_operator("-"))
        self.pushButton_mul.clicked.connect(lambda: self.input_operator("*"))
        self.pushButton_div.clicked.connect(lambda: self.input_operator("/"))
        self.pushButton_lparen.clicked.connect(self.input_lparen)
        self.pushButton_rparen.clicked.connect(self.input_rparen)

        self.pushButton_equal.clicked.connect(self.press_equal)
        self.pushButton_AC.clicked.connect(self.press_ac)
        self.pushButton_C.clicked.connect(self.press_c)
        self.pushButton_sign.clicked.connect(self.toggle_sign)

        self.update_display()

    # ----------------------------------------------------------

    def input_digit(self, digit):

        if self.current_input == "Error":
            self.current_input = ""
        self.clear_error()

        if self.tokens and self.tokens[-1] == ")":
            self.tokens.append("*")

        if self.just_calculated:
            self.tokens = []
            if digit == ".":
                self.current_input = "0."
            else:
                self.current_input = digit
            self.just_calculated = False
            self.clear_message()
            self.update_display()
            return
        
        if len(self.current_input) >= 20:
            self.show_message("20자리까지만 입력할 수 있습니다.")
            return

        if digit != ".":
            if (len(self.tokens) > 0 and self.is_float(self.tokens[-1])):
                self.show_message("숫자 뒤에는 연산자를 입력해야 합니다.")
                return
            if (self.current_input == "0"):
                self.current_input = ""
            
        elif digit == ".":
            if "." in self.current_input:
                self.show_message("소수점은 한 번만 입력할 수 있습니다.")
                return
            elif self.current_input == "":
                self.current_input = "0"
            elif self.current_input == "-":
                self.current_input = "-0"

        self.clear_message()
        self.current_input += digit
        self.update_display()


    # -------------------------------------------------------------------

    def input_operator(self, op):
        if self.current_input == "Error":
            self.prev_expression = []
            self.current_input = ""
            self.tokens = []
            self.update_display()
            return

        if self.just_calculated:
            self.tokens = [self.current_input, op]
            self.prev_expression = []
            self.current_input = ""
            self.just_calculated = False
            self.clear_message()
            self.update_display()
            return

        if self.current_input:
            if self.clear_error():
                return
            if self.current_input[-1] == ".":
                self.current_input += "0"
            elif self.current_input[-1] == "-":
                if op in "+*/":
                    self.show_message("음수 기호 뒤에는 연산자를 넣을 수 없습니다.")
                    return
                else:
                    self.current_input = ""
                    self.clear_message()
                    self.update_display()
                    return
            elif self.is_float(self.current_input):
                print("hello4")
                if (len(self.tokens) > 0):
                    if(self.tokens[-1] == ")"):
                         self.tokens.append("*")
            self.tokens.append(self.current_input)
            self.current_input = ""

        elif not self.tokens:
            if op == "-":
                self.current_input = "-"
                self.just_calculated = False
                self.clear_message()
                self.update_display()
                return
            else:
                self.tokens = ["0", op]
                self.current_input = ""
                self.clear_message()
                self.update_display()
                return

        elif self.tokens[-1] == "(":
            if(op == "-"):
                self.current_input = "-"
                self.just_calculated = False
                self.clear_message()
                self.update_display()
                return
            else:
                self.show_message("괄호 뒤에는 '-'만 입력 가능합니다.")
                self.update_display()
                return

        if self.tokens:
            print(f"self.tokens: {self.tokens}")
            if self.tokens[-1] == "-":
                if op == '-':
                    self.current_input = "-"
                else:
                    self.tokens[-1] = op
            elif self.tokens[-1] in "+*/":
                self.tokens[-1] = op
            else: 
                self.tokens.append(op)  
        else:
            print("Debug4444444444444444")
            self.tokens.append(op)

        self.just_calculated = False
        self.clear_message()
        self.update_display()


    # -------------------------------------------------------------------

    def input_lparen(self):
        if self.current_input == "Error":
            self.current_input = ""

        # 에러 상태일 경우 초기화
        if(self.clear_error()):
            return

        #  출력된 값이 존재하는 상황
        if self.just_calculated:
            # 출력된 값에 괄호를 곱하는 것으로 처리
            if self.current_input:
                self.tokens = [self.current_input, "*"]
            else: 
                self.tokens = []
            self.current_input = ""
            self.just_calculated = False

        # 출력값이 아닌 입력된 값이 존재하는 상황
        if self.current_input:
            # '-'만 입력된 상태에서 '(' 입력하면 -1*(로 변환
            if self.current_input == "-" and not self.tokens:
                self.tokens.append("-1")
                self.tokens.append("*")
                self.current_input = ""
            else:
                self.tokens.append(self.current_input)
                self.current_input = ""
        
        # 숫자나 ')' 다음에 '('가 올 경우 곱셈 생략을 막기 위해 '*' 자동 삽입
        if self.tokens and (self.is_float(self.tokens[-1]) or self.tokens[-1] == ")"):
            self.tokens.append("*")

        # lparen 추가
        self.tokens.append("(")

        # 화면 갱신
        self.update_display()
        
    
    def input_rparen(self):
        if self.clear_error() or self.just_calculated:
            self.tokens = []
            self.current_input = ""
            self.prev_expression = []
            self.just_calculated = False
            self.clear_message()
            self.update_display()
            return

        left = self.tokens.count("(")
        right = self.tokens.count(")")
        if left > right:
            if self.current_input:
                if self.is_float(self.current_input):
                    self.tokens.append(self.current_input)
                self.current_input = ""
            if self.tokens[-1] == "(":
                self.tokens.pop()
                self.show_message("빈 괄호가 자동 삭제되었습니다.")
                self.update_display()
                return
            if self.tokens[-1] in "+-*/":
                self.tokens.pop()
            self.tokens.append(")")
        else:
            self.show_message("닫는 괄호가 더 많을 수는 없습니다.")
            self.update_display()
            return

        self.clear_message()
        self.update_display()



    # ----------------------------------------------------------

    def press_equal(self):
        if self.clear_error():
            return

        if self.current_input:
            if (self.is_float(self.current_input) and len(self.tokens) > 0 and self.tokens[-1] == ")"):
                self.tokens.append("*")
            self.tokens.append(self.current_input)
        elif self.tokens:
            if (self.tokens[-1] in "+-*/"):
                self.tokens = self.tokens[:-1]
                self.show_message("피연산자 부족으로 마지막 연산자가 자동으로 삭제됩니다.")
        elif not self.tokens:
            self.show_message("계산할 수식이 없습니다.")
            return

        while (self.tokens.count("(") > self.tokens.count(")")) :
            self.show_message("닫는 괄호 부족으로 자동으로 채워집니다.")
            if (self.tokens[-1] in "+-*/"):
                self.tokens = self.tokens[:-1]
            self.tokens.append(")")
            if (self.tokens[-2] == '(' and self.tokens[-1] == ')'):
                self.tokens = self.tokens[:-2]
            elif (self.tokens[-2] in "+-*/" and self.tokens[-1] == ')'):
                self.tokens = self.tokens[:-2] + [self.tokens[-1]]
                print("3333333333333333")
        if len(self.tokens) > 0 and self.tokens[-1] in "+-*/":
            self.tokens.pop()

        self.prev_expression = self.tokens.copy()

        postfix = self.to_postfix(self.tokens)

        print(f"prev_expression: {self.prev_expression}")
        print(f"postfix: {postfix}")

        if not postfix:
            self.press_ac()
            self.show_message("완전하지 않은 수식입니다.")
            return

        try:
            if postfix == "Error":
                raise Exception
            result = self.evaluate_postfix(postfix)
            self.current_input = result
            self.tokens = []
            self.just_errored = False
            self.clear_message()
        except:
            self.current_input = "Error"
            self.just_errored = True
            self.tokens = []
            self.show_message("수식에 오류가 있습니다.")
        self.just_calculated = True
        self.update_display()



    # ----------------------------------------------------------

    def press_ac(self):
        self.tokens = []
        self.current_input = ""
        self.prev_expression = []
        self.just_calculated = False
        self.clear_message() 
        self.update_display()


    def press_c(self):
        if self.current_input:
            self.current_input = ""
        elif self.tokens:
            self.tokens.pop()
            if (len(self.tokens) > 0 and self.is_float(self.tokens[-1])):
                pop_token = self.tokens.pop()
                val = float(pop_token)
                if val == int(val):
                    self.current_input = str(int(val))
                else:
                    self.current_input = pop_token



        self.just_calculated = False
        self.clear_message() 
        self.update_display()

    def toggle_sign(self):
        if self.clear_error():
            return
        self.clear_message()
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
            if self.tokens == []:
                self.lineEdit.setText("0")
            else:
                self.lineEdit.setText("")
        else:
            if self.current_input.endswith("."):
                self.lineEdit.setText(self.current_input)
            elif self.is_float(self.current_input):
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
            if self.is_float(token):
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
                            self.show_message("0으로 나눌 수 없습니다.")
                            raise ZeroDivisionError
                        stack.append(a / b)

            if len(stack) == 1:
                return str(stack[0])
            else:
                raise ValueError
        except:
            self.show_message("수식에 오류가 있습니다.")
            self.just_errored = True
            return "Error"
    
    # ----------------------------------------------------------------------

    def is_float(self, target):
        try:
            float(target)
            return True
        except:
            return False
        
    def is_int(self, target):
        try:
            int(target)
            return True
        except ValueError:
            return False

    def is_zero(self, target):
        return self.is_float(target) and float(target) == 0
    
    # ----------------------------------------------------------------------

    def clear_error(self):
        if self.just_errored:
            self.tokens = []
            self.prev_expression = []
            self.current_input = ""
            self.just_errored = False
            self.update_display()
            return True
        return False
    
    # ----------------------------------------------------------------------

    def show_message(self, msg):
        QTimer.singleShot(50, lambda: self._delayed_show_message(msg))
        QTimer.singleShot(2050, self.clear_message)

    def _delayed_show_message(self, msg):
        self.textBrowser.setText(msg)
        self.textBrowser.setVisible(True)
        self.textBrowser.adjustSize()


    def clear_message(self):
        self.textBrowser.setText("")

    # --------------------------------------------------------------------

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Calculator()
    window.show()
    sys.exit(app.exec())