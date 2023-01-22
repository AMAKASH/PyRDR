from PyRDR.RDR import RDR, Rule


class SCRDR(RDR):
    def __init__(self, features: list, rule: Rule = None) -> None:
        super().__init__(features, rule)
        self.last_major_rule = rule

    def add_rule(self, rule: Rule):
        rule.rule_no = len(self.rules)+1
        if rule.is_refinement:
            parent = self.get_rule(rule.parent)
            if parent.if_true is None:
                parent.if_true = rule
            else:
                ref_rule = parent.if_true
                while ref_rule.if_false:
                    ref_rule = ref_rule.if_false
                ref_rule.if_false = rule
        else:
            if self.last_major_rule:
                self.last_major_rule.if_false = rule
            self.last_major_rule = rule

        self.rules.append(rule)

    def eval_case(self, case: list) -> tuple | bool:
        rules_fired = []
        rules_evaluated = []
        if len(self.rules) <= 0:
            current_rule = None
        else:
            current_rule = self.rules[0]
        current_conclusion = None
        conclusion_rule = 0
        while current_rule:
            rules_evaluated.append(current_rule.rule_no)
            if self.rule_satisfied(current_rule, case):
                rules_fired.append(current_rule.rule_no)
                current_conclusion = current_rule.conclusion
                conclusion_rule = current_rule.rule_no
                current_rule = current_rule.if_true
            else:
                # print(current_rule.if_false)
                current_rule = current_rule.if_false

        if current_conclusion:
            return current_conclusion, conclusion_rule, rules_evaluated, rules_fired
        else:
            return False
