from model import CalculatorModel, CalcState
from view import CalculatorView


class CalculatorController:
    def __init__(self, view: CalculatorView):
        self.model = CalculatorModel()
        self.view = view
        self.view.connect_signals(self)
        self._update_display()


    def handle_digit(self, digit: str):
        result = self.model.input_digit(digit)
        if result == "TOO_LONG":
            self.view.show_message("20자리까지만 입력할 수 있습니다.")
        elif result == "MULTIPLE_DOT":
            self.view.show_message("소수점은 한 번만 입력할 수 있습니다.")
        elif result == "NO_OPERATOR":
            self.view.show_message("숫자 뒤에는 연산자를 입력해야 합니다.")

        print("[버튼] 숫자:", digit)
        self._debug_state()
        self._update_display()


    def handle_operator(self, op: str):
        result = self.model.input_operator(op)
        if result == "OPERATOR_AFTER_MINUS":
            self.view.show_message("음수 기호 뒤에는 연산자를 넣을 수 없습니다.")
        elif result == "INVALID_AFTER_LPAREN":
            self.view.show_message("괄호 뒤에는 '-'만 입력 가능합니다.")

        print("[버튼] 연산자:", op)
        self._debug_state()
        self._update_display()


    def handle_lparen(self):
        self.model.input_lparen()

        print("[버튼] LPAREN:")
        self._debug_state()
        self._update_display()


    def handle_rparen(self):
        result = self.model.input_rparen()
        if result == "UNMATCHED_PAREN":
            self.view.show_message("닫는 괄호가 더 많을 수 없습니다.")
        elif result == "EMPTY_PAREN":
            self.view.show_message("빈 괄호가 자동 삭제되었습니다.")

        print("[버튼] RPAREN:")
        self._debug_state()
        self._update_display()


    def handle_equal(self):
        result = self.model.evaluate()
        if result == "EMPTY":
            self.view.show_message("계산할 수식이 없습니다.")
        elif result == "INVALID":
            self.view.show_message("완전하지 않은 수식입니다.")
        elif result == "ERROR":
            self.view.show_message("수식에 오류가 있습니다.")
        elif result == "AUTO_PAREN_COMPLETE":
            self.view.show_message("빈 괄호가 자동으로 채워집니다.")
        else:
            self.view.clear_message()
        print("[버튼] 등호")
        self._debug_state()
        self._update_display()


    def handle_ac(self):
        self.model.reset()
        print("[버튼] AC:")
        self._debug_state()
        self._update_display()


    def handle_c(self):
        if self.model.state in (CalcState.ERROR, CalcState.CALCULATED):
            self.model.reset()

        elif self.model.state == CalcState.READY:
            self.model.reset()
    
        elif self.model.state == CalcState.INPUTTING:
            if self.model.current_input:
                self.model.current_input = ""
                if not self.model.tokens:
                    self.model.state = CalcState.READY
            elif self.model.tokens:
                self.model.tokens.pop()
                if self.model.tokens and self.model.is_float(self.model.tokens[-1]):
                    popped = self.model.tokens.pop()
                    val = float(popped)
                    if val == int(val):
                        self.model.current_input = str(int(val))
                    else:
                        self.model.current_input = popped
                elif not self.model.tokens:
                    self.model.state = CalcState.READY

        print("[버튼] C:")
        self._debug_state()
        self._update_display()
        

    def handle_sign(self):
        self.model.toggle_sign()

        print("[버튼] 부호전환")
        self._debug_state()
        self._update_display()


    def _update_display(self):
        # lineEdit_2: 수식
        tokens = self.model.prev_expression if self.model.state == CalcState.CALCULATED else self.model.tokens
        self.view.update_expression_display(tokens)

        # lineEdit: 현재 입력 or 결과
        current = self.model.current_input
        if current == "":
            current = "0" if not tokens else ""
        elif self.model.is_float(current):
            val = float(current)
            current = str(int(val)) if val.is_integer() and self.model.state == CalcState.CALCULATED else current
        self.view.update_result_display(current)

    def _debug_state(self):
        print("=" * 30)
        print(f"State: {self.model.state.name}")
        print(f"current_input: {self.model.current_input}")
        print(f"tokens: {self.model.tokens}")
        print(f"prev_expression: {self.model.prev_expression}")
        print("=" * 30)