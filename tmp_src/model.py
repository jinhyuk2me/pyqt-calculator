from enum import Enum, auto

class CalcState(Enum):
    READY = auto()
    INPUTTING = auto()
    CALCULATED = auto()
    ERROR = auto()

class CalculatorModel:
    def __init__(self):
        self.tokens = []
        self.prev_expression = []
        self.current_input = ""
        self.state = CalcState.READY

    # 숫자 또는 소수점 입력
    def input_digit(self, digit):
        if self.state == CalcState.ERROR:
            self.reset()

        # 계산 직후 새 입력 시작
        if self.state == CalcState.CALCULATED:
            self.tokens.clear()
            self.prev_expression.clear()
            self.current_input = ""
            self.state = CalcState.READY

        if self.tokens and self.tokens[-1] == ")":
            self.tokens.append("*")

        if len(self.current_input) >= 20:
            return "TOO_LONG"

        if digit == ".":
            if "." in self.current_input:
                return "MULTIPLE_DOT"
            if self.current_input == "":
                self.current_input = "0"
            elif self.current_input == "-":
                self.current_input = "-0"
        else:
            if self.tokens and self.is_float(self.tokens[-1]):
                return "NO_OPERATOR"
            if self.current_input == "0":
                self.current_input = ""

        self.current_input += digit
        self.state = CalcState.INPUTTING
        return "OK"


    # 연산자 입력
    def input_operator(self, op):
        if self.state == CalcState.ERROR:
            self.reset()
            return
        
        if self.state == CalcState.CALCULATED:
            self.tokens = [self.current_input, op]
            self.current_input = ""
            self.prev_expression.clear()
            self.state = CalcState.INPUTTING
            return

        if self.current_input:
            if self.current_input.endswith("."):
                self.current_input += "0"
            if self.current_input == "-":
                if op in "-+":
                    self.current_input = ""
                    return
                else:
                    return "OPERATOR_AFTER_MINUS"
            if self.is_float(self.current_input):
                if self.tokens and self.tokens[-1] == ")":
                    self.tokens.append("*")
                self.tokens.append(self.current_input)
                self.current_input = ""
        elif not self.tokens:
            if op == "-":
                self.current_input = "-"
                self.state = CalcState.INPUTTING
                return
            else:
                self.tokens = ["0", op]
                self.state = CalcState.INPUTTING
                return
        elif self.tokens[-1] == "(":
            if op == "-":
                self.current_input = "-"
                self.state = CalcState.INPUTTING
                return
            else:
                return "INVALID_AFTER_LPAREN"

        self._handle_operator_override(op)
        self.state = CalcState.INPUTTING

    def input_lparen(self):
        if self.state == CalcState.ERROR:
            self.reset()

        if self.state == CalcState.CALCULATED:
            if self.current_input:
                self.tokens = [self.current_input, "*"]
                self.current_input = ""
            else:
                self.tokens.clear()
                self.prev_expression.clear()

        if self.current_input:
            if self.current_input == "-":
                self.tokens.append("-1")
                self.tokens.append("*")
            else:
                self.tokens.append(self.current_input)
            self.current_input = ""

        if self.tokens and (self.is_float(self.tokens[-1]) or self.tokens[-1] == ")"):
            self.tokens.append("*")

        self.tokens.append("(")
        self.state = CalcState.INPUTTING

    def input_rparen(self):
        if self.state in (CalcState.ERROR, CalcState.CALCULATED):
            self.reset()
            return

        if self.tokens.count("(") <= self.tokens.count(")"):
            return "UNMATCHED_PAREN"

        if self.current_input:
            if self.is_float(self.current_input):
                self.tokens.append(self.current_input)
            self.current_input = ""

        if self.tokens and self.tokens[-1] == "(":
            self.tokens.pop()
            return "EMPTY_PAREN"

        if self.tokens and self.tokens[-1] in "+-*/":
            self.tokens.pop()

        self.tokens.append(")")
        self.state = CalcState.INPUTTING

    def evaluate(self):
        if self.state == CalcState.ERROR:
            self.reset()

        if self.current_input:
            if self.tokens and self.tokens[-1] == ")":
                self.tokens.append("*")
            self.tokens.append(self.current_input)
            self.current_input = ""

        if not self.tokens:
            return "EMPTY"

        self._auto_complete_expression()

        postfix = self.to_postfix(self.tokens)
        if postfix == "Error":
            self.state = CalcState.ERROR
            return "INVALID"

        result = self.evaluate_postfix(postfix)
        if result == "Error":
            self.state = CalcState.ERROR
            self.current_input = "Error"
            return "ERROR"

        self.prev_expression = self.tokens.copy()
        self.tokens = []
        self.current_input = result
        self.state = CalcState.CALCULATED
        return result

    def toggle_sign(self):
        if self.current_input == "Error" or self.state == CalcState.ERROR:
            self.reset()
            return
        elif self.state == CalcState.CALCULATED :
            self.prev_expression.clear()
            self.tokens.clear()
        elif self.state == CalcState.READY:
            self.current_input = "-"
        elif self.current_input.startswith("-"):
            self.current_input = self.current_input[1:]
        elif self.current_input == "0":
            return
        elif self.current_input:
            self.current_input = "-" + self.current_input

    def reset(self):
        self.tokens.clear()
        self.prev_expression.clear()
        self.current_input = ""
        self.state = CalcState.READY

    def to_postfix(self, tokens):
        prec = {'+': 2, '-': 2, '*': 3, '/': 3}
        output, stack = [], []
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
                return "Error"
            output.append(stack.pop())

        if paren_balance != 0:
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
                            return "Error"
                        stack.append(a / b)
            if len(stack) == 1:
                return str(int(stack[0])) if stack[0].is_integer() else str(stack[0])
            else:
                return "Error"
        except:
            return "Error"

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

        while self.tokens.count("(") > self.tokens.count(")"):
            if self.tokens and self.tokens[-1] in "+-*/":
                self.tokens.pop()
            self.tokens.append(")")
            if len(self.tokens) >= 2:
                if self.tokens[-2] == "(" and self.tokens[-1] == ")":
                    self.tokens = self.tokens[:-2]
                elif self.tokens[-2] in "+-*/" and self.tokens[-1] == ")":
                    self.tokens = self.tokens[:-2] + [")"]

    def is_float(self, target):
        try:
            float(target)
            return True
        except:
            return False
