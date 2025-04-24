import sys
from enum import Enum, auto
from PyQt6.QtWidgets import *
from PyQt6 import uic
from PyQt6.QtCore import QTimer


form_class = uic.loadUiType("/home/jinhyuk2me/project/iot/qt_calculator/src/calculator.ui")[0]

class CalcState(Enum):
    READY = auto()
    INPUTTING = auto()
    CALCULATED = auto()
    ERROR = auto()

class Calculator(QDialog, form_class):

    # ---------------------------------------------------------
    # UI Initialization
    # ---------------------------------------------------------

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.tokens = []
        self.prev_expression = []
        self.current_input = ""
        self.state = CalcState.READY

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

    # ---------------------------------------------------------
    # Public Input Handlers
    # ----------------------------------------------------------

    def input_digit(self, digit):

        if self.state == CalcState.ERROR:
            self.reset_all()

        if self._handle_after_calculation("digit", digit):
            self.update_display()
            return
        
        if len(self.current_input) >= 20:
            self.show_message("20자리까지만 입력할 수 있습니다.")
            return

        if digit.isdigit():
            if not self._handle_number_input(digit):
                return
        elif digit == ".":
            if not self._handle_dot_input():
                return

        if self.tokens and self.tokens[-1] == ")":
            self.tokens.append("*")

        self.current_input += digit
        self.set_state(CalcState.INPUTTING)
        self.clear_message()
        self.update_display()


    def input_operator(self, op):

        if self.state == CalcState.ERROR or self.current_input == "Error":
            self.reset_all()
            return

        if self._handle_after_calculation("operator", op):
            self.update_display()
            return

        if self.current_input:
            if not self._handle_operator_with_input(op):
                return
        elif not self.tokens:
            if not self._handle_operator_no_token(op):
                return
        elif self.tokens[-1] == "(":
            if not self._handle_operator_after_lparen(op):
                return
        
        self._handle_operator_override(op)
        self.set_state(CalcState.INPUTTING)
        self.clear_message()
        self.update_display()



    def input_lparen(self):
        
        # Error 상태 초기화
        if self.current_input == "Error" or self.state == CalcState.ERROR:
            self.reset_all()

        # 계산이 끝난 직후면 괄호로 이어지는 수식 처리
        if self._handle_after_calculation("lparen"):
            self.update_display()
            return
        
        else:
            # 현재 입력 중인 숫자가 있다면 토큰으로 옮김
            if self.current_input:
                self._handle_lparen_with_input()

            # 암시적 곱셈 처리: 숫자 or ')' 다음이면 * 삽입
            if self.tokens and (self.is_float(self.tokens[-1]) or self.tokens[-1] == ")"):
                self.tokens.append("*")
            
            # 여는 괄호 추가
            self.tokens.append("(")
            self.set_state(CalcState.INPUTTING)
            self.update_display()
            return
        
    
    def input_rparen(self):

        # Error 상태 초기화 후 return
        if self.current_input == "Error" or self.state == CalcState.ERROR:
            self.reset_all()
            return

        # 계산 직후면 수식 초기화
        if self.state == CalcState.CALCULATED:
            self.reset_all()
            return

        # 괄호 짝 확인
        left = self.tokens.count("(")
        right = self.tokens.count(")")
        if left <= right:
            self.show_message("닫는 괄호가 더 많을 수는 없습니다.")
            self.update_display()
            return

        # 현재 입력된 숫자 있으면 토큰에 추가
        if self.current_input:
            if self.is_float(self.current_input):
                self.tokens.append(self.current_input)
            self.current_input = ""

        # 마지막 토큰이 '('인 경우 빈 괄호 → 제거
        if self.tokens and self.tokens[-1] == "(":
            self.tokens.pop()
            self.show_message("빈 괄호가 자동 삭제되었습니다.")
            self.update_display()
            return

        # 마지막이 연산자일 경우 pop
        if self.tokens and self.tokens[-1] in "+-*/":
            self.tokens.pop()

        # 닫는 괄호 추가
        self.tokens.append(")")
        self.set_state(CalcState.INPUTTING)
        self.clear_message()
        self.update_display() 


    def press_equal(self):
        
        # 현재 에러 상태면 초기화
        if self.state == CalcState.ERROR or self.current_input == "Error":
            self.reset_all()
            return

        # current_input 있는 경우 tokens에 추가
        if self.current_input:
            if self.tokens and self.tokens[-1] == ")":
                self.tokens.append("*")
            self.tokens.append(self.current_input)
            self.current_input = ""
        
        # 빈 토큰 처리
        if not self.tokens:
            self.show_message("계산할 수식이 없습니다.")
            return
        
        # 수식 보정 (연산자 제거, 괄호 보정 등)
        self._auto_complete_expression()

        # 후위표기 변환
        postfix = self.to_postfix(self.tokens)

        # 변환 실패
        if postfix == "Error" or not postfix:
            self.reset_all()
            self.show_message("완전하지 않은 수식입니다.")
            return

        # 계산 시도
        result = self._evaluate_expression(postfix)
        self.prev_expression = self.tokens.copy()
        self.tokens = []

        # 성공 or 실패
        if result == "Error":
            self.current_input = "Error"
            self.set_state(CalcState.ERROR)
        else:
            self.current_input = result
            self.set_state(CalcState.CALCULATED)

        self.update_display()


    def press_ac(self):
       self.reset_all()


    def press_c(self):
        if self.state == CalcState.ERROR:
            self.reset_all()
            return

        if self.current_input:
            self.current_input = ""

        elif self.tokens:
            self.tokens.pop()

            # 마지막 토큰이 숫자면 다시 current_input으로 복원
            if self.tokens and self.is_float(self.tokens[-1]):
                token = self.tokens.pop()
                self.current_input = str(int(float(token))) if float(token).is_integer() else token

        self.set_state(CalcState.INPUTTING)
        self.clear_message()
        self.update_display()


    def toggle_sign(self):
        # 에러 상태면 초기화
        if self.current_input == "Error" or self.state == CalcState.ERROR:
            self.reset_all()
            return

        self.clear_message()

        # '-' 붙은 경우 제거
        if self.current_input.startswith("-"): 
            self.current_input = self.current_input[1:]
        # '0'은 부호 변경 무효
        elif self.current_input == "0": 
            return
        # 일반적인 숫자에는 '-' 붙이기
        elif self.current_input: 
            self.current_input = "-" + self.current_input

        self.set_state(CalcState.INPUTTING)
        self.update_display()

    # ---------------------------------------------------------------------
    # Expression Evaluation
    # ----------------------------------------------------------------------

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
                    self.set_state(CalcState.ERROR)
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
                self.set_state(CalcState.ERROR)
                return "Error"
            output.append(stack.pop())

        if paren_balance != 0:
            self.set_state(CalcState.ERROR)
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
            self.set_state(CalcState.ERROR)
            return "Error"

    # ---------------------------------------------------------------------
    # Utiltity & Validation
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
    
    # ----------------------------------------------------------
    # State Manangement
    # ----------------------------------------------------------

    def set_state(self, state):
        self.state = state

    def clear_error_state(self):
        if self.state == CalcState.ERROR :
            self.reset_all()
            return True
        return False
    
    def reset_all(self):
        self.tokens.clear()
        self.prev_expression.clear()
        self.current_input = ""
        self.set_state(CalcState.READY)
        self.update_display()
    
    # ----------------------------------------------------------------------
    # Display & Messaging
    # ----------------------------------------------------------------------

    def update_display(self):
        self.update_lineEdit_2()
        self.update_lineEdit()


    def update_lineEdit(self):
        if self.current_input == "":
            self.lineEdit.setText("0" if not self.tokens else "")
        else:
            if self.current_input.endswith("."):
                self.lineEdit.setText(self.current_input)
            elif self.is_float(self.current_input):
                val = float(self.current_input)
                # 계산 완료 상태에서 정수값이면 .0 제거
                if val.is_integer() and self.state == CalcState.CALCULATED:
                    self.lineEdit.setText(str(int(val)))
                else:
                    self.lineEdit.setText(self.current_input)
            else:
                self.lineEdit.setText(self.current_input)


    def update_lineEdit_2(self):
        pretty_tokens = []

        # 계산이 끝난 경우 prev_expression 표시
        if self.state == CalcState.CALCULATED and self.prev_expression:
            tokens_to_display = self.prev_expression
        else:
            tokens_to_display = self.tokens

        for token in tokens_to_display:
            if self.is_float(token):
                val = float(token)
                pretty_tokens.append(str(int(val)) if val.is_integer() else token)
            else:
                pretty_tokens.append(token)

        self.lineEdit_2.setText(" ".join(pretty_tokens))


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
    # Internal Logic Helpers (Private)
    # --------------------------------------------------------------------

    def _handle_after_calculation(self, next_input_type, value=""):
        if self.state != CalcState.CALCULATED:
            return False # 계산 직후 상태가 아니면 아무 일도 안 함
        
        self.tokens.clear()
        self.prev_expression.clear()

        if next_input_type == "digit":
            self.current_input = "0." if value == "." else value
        
        elif next_input_type == "operator":
            self.tokens = [self.current_input, value]
            self.current_input = ""

        elif next_input_type == "lparen":
            if self.current_input:
                self.tokens = [self.current_input, "*"]
            else:
                self.tokens = []
            self.current_input = ""
        
        self.set_state(CalcState.INPUTTING)
        return True # 계산 직후 처리했음을 알림
    

    def _handle_number_input(self, digit):

        # 숫자 뒤 숫자 불가 (ex: 3 5)
        if self.tokens and self.is_float(self.tokens[-1]):
            self.show_message("숫자 뒤에는 연산자를 입력해야 합니다.")
            return False
        
        # 앞에 "0"만 있으면 제거
        if self.current_input == "0":
            self. current_input = ""

        return True
    
    
    def _handle_dot_input(self):
        if "." in self.current_input:
            self.show_message("소수점은 한 번만 입력할 수 있습니다.")
            return False
        if self.current_input == "":
            self.current_input = "0"
        elif self.current_input == "-":
            self.current_input = "-0"
        return True
    
    
    def _handle_operator_with_input(self, op):
        if self.current_input.endswith("."):
            self.current_input += "0"
        elif self.current_input == "-":
            if op in "+*/":
                self.show_message("음수 기호 뒤에는 연산자를 넣을 수 없습니다.")
                return False
            else:
                self.current_input = ""
                self.update_display()
                return False

        if self.is_float(self.current_input):
            if self.tokens and self.tokens[-1] == ")":
                self.tokens.append("*")
            self.tokens.append(self.current_input)
            self.current_input = ""
        return True
    

    def _handle_operator_no_token(self, op):
        if op == "-":
            self.current_input = "-"
            self.set_state(CalcState.INPUTTING)
            self.update_display()
            return False  # 이후 처리 중단
        else:
            self.tokens = ["0", op]
            self.set_state(CalcState.INPUTTING)
            self.update_display()
            return False
        
        
    def _handle_operator_after_lparen(self, op):
        if op == "-":
            self.current_input = "-"
            self.set_state(CalcState.INPUTTING)
            self.update_display()
            return False
        else:
            self.show_message("괄호 뒤에는 '-'만 입력 가능합니다.")
            return False
        

    def _handle_operator_override(self, op):
        if self.tokens:
            if self.tokens[-1] == "-":
                self.current_input = "-" if op == "-" else ""
                self.tokens[-1] = op
            elif self.tokens[-1] in "+*/":
                self.tokens[-1] = op
            else:
                self.tokens.append(op)
        else:
            self.tokens.append(op)

    def _auto_complete_expression(self):
        while self.tokens and self.tokens[-1] in "+-*/":
            self.tokens.pop()
            self.show_message("마지막 연산자가 제거되었습니다.")

        # 닫는 괄호 부족 → 자동 추가
        while self.tokens.count("(") > self.tokens.count(")"):
            if self.tokens and self.tokens[-1] in "+-*/":
                self.tokens.pop()
            self.tokens.append(")")
            self.show_message("닫는 괄호가 자동으로 추가되었습니다.")

            # 추가: 비정상 괄호 조합 제거
            if len(self.tokens) >= 2:
                if self.tokens[-2] == "(" and self.tokens[-1] == ")":
                    self.tokens = self.tokens[:-2]
                    self.show_message("빈 괄호가 제거되었습니다.")
                elif self.tokens[-2] in "+-*/" and self.tokens[-1] == ")":
                    self.tokens = self.tokens[:-2] + [")"]
                    self.show_message("잘못된 괄호 앞 연산자가 제거되었습니다.")



    def _evaluate_expression(self, postfix):
        try:
            result = self.evaluate_postfix(postfix)
            if result == "Error":
                raise Exception
            return result
        except:
            self.show_message("수식에 오류가 있습니다.")
            return "Error"
        
        
    def _handle_lparen_with_input(self):
        # 단독 '-' 입력은 -1 * ( 로 변환
        if self.current_input == "-":
            self.tokens.append("-1")
            self.tokens.append("*")
        else:
            self.tokens.append(self.current_input)
        self.current_input = ""



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Calculator()
    window.show()
    sys.exit(app.exec())