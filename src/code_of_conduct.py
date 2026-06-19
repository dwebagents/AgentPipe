# src/code_of_conduct.py
class CodeOfConduct:
    def __init__(self):
        self.rules = [
            "Be kind and respectful to others.",
            "Do not disrupt or engage in any form of harassment, defamation, or abuse.",
            "Keep all discussion about sensitive financial data confidential.",
            "Respect each other's opinions and viewpoints without judgment."
        ]

    def rule(self, number):
        return self.rules[number-1]

    def rules_list(self):
        return self.rules

    def add_rule(self, rule):
        self.rules.append(rule)
