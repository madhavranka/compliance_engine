# contracts/rules/base.py

from typing import Any, Dict
import re

class Rule:
    def __init__(self, field_name: str, operator: str, value: Any):
        self.field_name = field_name
        self.operator = operator
        self.value = value

    def evaluate(self, context: Dict[str, Any]) -> bool:
        field_value = context.get(self.field_name)
        if field_value is None:
            return False
        
        try:
            if isinstance(field_value, int):
                self.value = int(self.value)
        except ValueError:
            return False

        if self.operator == '==':
            return field_value == self.value
        elif self.operator == '!=':
            return field_value != self.value
        elif self.operator == '>':
            return field_value > self.value
        elif self.operator == '<':
            return field_value < self.value
        elif self.operator == '>=':
            return field_value >= self.value
        elif self.operator == '<=':
            return field_value <= self.value
        else:
            raise ValueError(f"Unsupported operator: {self.operator}")

class RuleSet:
    def __init__(self, rules: list, logic: str = 'AND'):
        self.rules = rules
        self.logic = logic

    def evaluate(self, context: Dict[str, Any]) -> bool:
        if self.logic == 'AND':
            return all(rule.evaluate(context) for rule in self.rules)
        elif self.logic == 'OR':
            return any(rule.evaluate(context) for rule in self.rules)
        else:
            raise ValueError(f"Unsupported logic: {self.logic}")

class RuleWithPlaceholder(Rule):
    def __init__(self, field_name: str, operator: str, value: str):
        super().__init__(field_name, operator, value)
        self.placeholders = self.extract_placeholders(value)

    def extract_placeholders(self, value: str):
        return re.findall(r"\{\{(.*?)\}\}", value)

    def evaluate(self, context: Dict[str, Any], placeholder_values: Dict[str, Any]) -> bool:
        actual_value = self.value
        for placeholder in self.placeholders:
            if placeholder in placeholder_values:
                actual_value = actual_value.replace(f"{{{{{placeholder}}}}}", str(placeholder_values[placeholder]))

        try:
            if isinstance(context.get(self.field_name), int):
                actual_value = int(actual_value)
        except ValueError:
            return False
        self.value = actual_value
        return super().evaluate(context)
