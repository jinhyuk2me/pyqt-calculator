import sys
from PyQt6.QtWidgets import *
from PyQt6 import uic

form_class = uic.loadUiType("/home/jinhyuk2me/project/iot/qt_calculator/src/calculator.ui")[0]

class Calculator(QDialog, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.tokens = []
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

        if self.just_calculated:
            self.tokens = []
            if digit == ".":
                self.current_input = "0."
            else:
                self.current_input = digit
            self.just_calculated = False
            self.update_display()
            return

        if self.current_input == "0" and digit != ".":
            self.current_input = digit
        else:
            if digit == "." and "." in self.current_input:
                return
            if digit == "." and self.current_input == "":
                self.current_input = "0"
            if len(self.current_input) >= 20:
                return
            self.current_input += digit

        self.update_display()

    def input_operator(self, op):
        if self.current_input:
            if self.clear_error():
                return
            if self.current_input[-1] == ".":
                self.current_input += "0"
            elif self.current_input[-1] == "-":
                if op in "-*/":
                    return
                else:
                    self.current_input = ""
                    self.update_display()
                    return
            self.tokens.append(self.current_input)
            self.current_input = ""
        elif not self.tokens :
            if op == "-":
                self.current_input = "-"
                self.just_calculated = False
                self.update_display()
                return
            else :
                return

        # 괄호 뒤 음수 처리: ( -3 ) → "-3"
        if self.tokens and self.tokens[-1] == "(" and op == "-":
            self.current_input = "-"
            self.just_calculated = False
            self.update_display()
            return

        if self.tokens and self.tokens[-1] in "+-*/":
            self.tokens[-1] = op
        else:
            self.tokens.append(op)

        self.just_calculated = False
        self.update_display()

    def input_paren(self):
        self.clear_error()
        left = self.tokens.count("(")
        right = self.tokens.count(")")

        if self.just_calculated:
            if self.current_input:
                self.tokens = [self.current_input, "*"]
            else:
                self.tokens = []
            self.current_input = ""
            self.just_calculated = False

        if self.current_input:
            self.tokens.append(self.current_input)
            self.current_input = ""

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
        #merged_tokens = self.merge_negative_numbers(self.tokens)
        #postfix = self.to_postfix(merged_tokens)
        postfix = self.to_postfix(self.tokens)
        try:
            if postfix == "Error":
                raise Exception
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
        elif self.current_input:
            self.current_input = "-" + self.current_input
        self.update_display()

    # ----------------------------------------------------------

    def update_display(self):
        self.update_lineEdit_2()
        self.update_lineEdit()

    def update_lineEdit(self):
        if self.current_input == "":
            if self.tokens == [] and not self.just_calculated:
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

    def update_lineEdit_2(self):
        pretty_tokens = []
        for token in self.tokens:
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

    # def merge_negative_numbers(self, tokens):
    #     result = []
    #     i = 0
    #     while i < len(tokens):
    #         if (tokens[i] == "-" and
    #             i > 0 and tokens[i - 1] == "(" and
    #             i + 1 < len(tokens) and self.is_number(tokens[i + 1])):
    #             result.append("-" + tokens[i + 1])
    #             i += 2
    #         else:
    #             result.append(tokens[i])
    #             i += 1
    #     return result
    
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