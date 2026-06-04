# calculator/pkg/calculator.py

import re


class Calculator:
    def __init__(self):
        self.operators = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": self._safe_divide,
            "~": lambda a: -a,  # Unary minus
        }
        self.precedence = {"+": 1, "-": 1, "*": 2, "/": 2, "~": 3}

    def _safe_divide(self, a, b):
        if b == 0:
            raise ValueError("Division by zero is not allowed.")
        return a / b

    def evaluate(self, expression):
        if not expression or expression.isspace():
            return None
        tokens = self._tokenize(expression)
        return self._evaluate_infix(tokens)

    def _tokenize(self, expression):
        # Add spaces around operators and parentheses for easier splitting.
        expression = re.sub(r"([+\-*/()])", r" \1 ", expression)
        return expression.strip().split()

    def _evaluate_infix(self, tokens):
        values = []
        operators = []
        expect_operand = True

        for token in tokens:
            if token == "(":
                if not expect_operand:
                    raise ValueError("Invalid expression.")
                operators.append(token)
                expect_operand = True
            elif token == ")":
                if expect_operand:
                    raise ValueError("Invalid expression: empty parentheses.")
                while operators and operators[-1] != "(":
                    self._apply_operator(operators, values)
                if not operators or operators.pop() != "(":
                    raise ValueError("Mismatched parentheses.")
                expect_operand = False
            elif token in self.operators:
                if expect_operand:
                    if token == "-":
                        operators.append("~")
                    elif token != "+":  # Ignore unary plus
                        raise ValueError(f"Invalid unary operator: {token}")
                else:  # Binary operator
                    while (
                        operators
                        and operators[-1] in self.precedence
                        and self.precedence[operators[-1]] >= self.precedence[token]
                    ):
                        self._apply_operator(operators, values)
                    operators.append(token)
                    expect_operand = True
            else:  # Number
                if not expect_operand:
                    raise ValueError("Invalid expression: consecutive numbers.")
                try:
                    values.append(float(token))
                    expect_operand = False
                except ValueError:
                    raise ValueError(f"Invalid token: {token}")

        while operators:
            if operators[-1] == "(":
                raise ValueError("Mismatched parentheses.")
            self._apply_operator(operators, values)

        if len(values) != 1 or operators:
            raise ValueError("Invalid expression.")

        return values[0]

    def _apply_operator(self, operators, values):
        if not operators:
            raise ValueError("Invalid expression: missing operator.")

        operator = operators.pop()
        if operator == "~":
            if not values:
                raise ValueError("Not enough operands for unary minus.")
            operand = values.pop()
            values.append(self.operators[operator](operand))
        else:
            if len(values) < 2:
                raise ValueError(f"Not enough operands for operator: {operator}")

            b = values.pop()
            a = values.pop()
            values.append(self.operators[operator](a, b))
