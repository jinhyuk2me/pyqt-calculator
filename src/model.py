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
        elif self.state == CalcState.CALCULATED:
            self.tokens.clear()
            self.prev_expression.clear()
            self.current_input = ""
            self.state = CalcState.READY

        if self.state in (CalcState.READY, CalcState.INPUTTING):
            # 닫는 괄호 뒤에 숫자 입력시 자동 곱셈 처리
            if self.tokens and self.tokens[-1] == ")":
                self.tokens.append("*")
            # 입력 길이 초과
            if len(self.current_input) >= 20:
                return "TOO_LONG"
            
            # 소수점 입력시
            if digit == ".":
                # 소수점 중복 입력 방지
                if "." in self.current_input:
                    return "MULTIPLE_DOT"
                # 입력 없는 상태에서 소수점 처리
                if self.current_input == "":
                    self.current_input = "0"
                # 음수부호 뒤에 오는 소수점 처리
                elif self.current_input == "-":
                    self.current_input = "-0"
            # digit 입력시
            else:
                # self.tokens가 연산자가 아니라 숫자로 끝났을 경우
                if self.tokens and self.is_float(self.tokens[-1]):
                    return "NO_OPERATOR"
                # 0 상태에서 다른 정수 입력 처리
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
        elif self.state == CalcState.CALCULATED:
            self.tokens = [self.current_input, op]
            self.current_input = ""
            self.prev_expression.clear()
            self.state = CalcState.INPUTTING
            return
        elif self.state in (CalcState.READY, CalcState.INPUTTING):
            # 입력이 존재하는 경우
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
            # 입력이 존재하지 않는 경우
            elif not self.current_input:
                # token이 없는 경우
                if not self.tokens:
                    if op == "-":
                        self.current_input = "-"
                        self.state = CalcState.INPUTTING
                        return
                    else:
                        self.tokens = ["0", op]
                        self.state = CalcState.INPUTTING
                        return
                # token이 적어도 하나 존재하는 경우
                elif self.tokens:
                    # 마지막 token이 여는 괄호인 경우
                    if self.tokens[-1] == "(":
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
        elif self.state == CalcState.CALCULATED:
            # 결과가 current_input에 쓰여진 경우 '(' 입력 전 '*' 자동 추가
            if self.current_input:
                self.tokens = [self.current_input, "*"]
                self.current_input = ""
            # 예외 상황
            else:
                self.tokens.clear()
                self.prev_expression.clear()

        if self.state in (CalcState.READY, CalcState.INPUTTING):
            # 입력이 존재하는 경우
            if self.current_input:
                # 음수부호 입력만 있을 경우 자동 -1 곱셈 처리
                if self.current_input == "-":
                    self.tokens.append("-1")
                    self.tokens.append("*")
                # 숫자 입력의 경우 그대로 tokens에 등록
                else:
                    self.tokens.append(self.current_input)
                self.current_input = ""

            # '(' 삽입 전 tokens의 마지막 요소를 고려하기 위한 로직
            if self.tokens:
                # 숫자나 ')' 다음에 '('가 올 경우 곱셈 생략을 막기 위해 '*' 자동 삽입
                if (self.is_float(self.tokens[-1]) or self.tokens[-1] == ")"):
                    self.tokens.append("*")
                
        self.tokens.append("(")
        self.state = CalcState.INPUTTING
        

    def input_rparen(self):

        if self.state in (CalcState.ERROR, CalcState.CALCULATED):
            self.reset()
            return
        
        elif self.state == CalcState.READY:
            return "EMPTY_PAREN"
        
        elif self.state == CalcState.INPUTTING:

            # 닫는 괄호가 더 많아지는 상황을 방지
            if self.tokens.count("(") <= self.tokens.count(")"):
                return "UNMATCHED_PAREN"

            # 숫자 입력이 있는 경우 등록
            if self.current_input:
                if self.is_float(self.current_input):
                    self.tokens.append(self.current_input)
                self.current_input = ""

            # ')' 삽입 전 tokens의 마지막 요소를 고려하기 위한 로직
            if self.tokens :
                if self.tokens[-1] == "(":
                    self.tokens.pop()
                    return "EMPTY_PAREN"
                if self.tokens[-1] in "+-*/":
                    self.tokens.pop()

            self.tokens.append(")")
            self.state = CalcState.INPUTTING


    def evaluate(self):

        if self.state == CalcState.READY:
            return "EMPTY"
        elif self.state == CalcState.ERROR:
            self.reset()
            return
        elif self.state == CalcState.CALCULATED:
            self.prev_expression = [self.current_input]
            self.tokens = []
            return
        elif self.state == CalcState.INPUTTING:
            # 입력이 존재할 경우 
            if self.current_input:
                # 마지막 token이 닫는 괄호일 경우
                if self.tokens and self.tokens[-1] == ")":
                    self.tokens.append("*")
                self.tokens.append(self.current_input)
                self.current_input = ""

            # evaluation 전 tokens가 비어있는지 평가
            if not self.tokens:
                return "EMPTY"

            # 괄호 및 부호 전처리
            self._auto_complete_expression()

            # tokens를 후위 표시법으로 변환
            postfix = self.to_postfix(self.tokens)
            if postfix == "Error":
                self.state = CalcState.ERROR
                return "INVALID"

            # 후위 표시법으로 변환된 postfix로 결과값을 도출
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
        if  self.state == CalcState.ERROR or self.current_input == "Error":
            self.reset()
            return
        elif self.state == CalcState.CALCULATED :
            self.prev_expression.clear()
            self.tokens.clear()
        elif self.state == CalcState.READY:
            self.current_input = "-"
        elif self.state == CalcState.INPUTTING:
            if self.current_input:
                if self.current_input.startswith("-"):
                    self.current_input = self.current_input[1:]
                elif self.current_input == "0":
                    self.current_input = "-"
                else:
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
