from PyRDR.RDR import RDR, Rule


class MCRDR(RDR):

    def add_rule(self, rule_object: Rule):
        rule_object.rule_no = len(self.rules)+1
        if rule_object.is_stopping:
            parent = rule_object.parent
            parent_rule_object = self.get_rule(parent)
            rule_object.if_false = parent_rule_object.if_true
            parent_rule_object.if_true = rule_object.rule_no

        self.rules.append(rule_object)

    def eval_case(self, case: list, all_rules=None) -> tuple | bool:
        rules_fired = []
        rules_evaluated = []
        conclusions = []
        if not all_rules:
            all_rules = self.rules
        for current_rule in all_rules:
            stopped = False
            if current_rule.is_stopping:
                continue
            rules_evaluated.append(current_rule.rule_no)
            satisfied = self.rule_satisfied(current_rule, case)
            if satisfied:
                rules_fired.append(current_rule.rule_no)
                if current_rule.if_true:
                    stopping_rule = self.get_rule(current_rule.if_true)
                    while stopping_rule:
                        rules_evaluated.append(stopping_rule.rule_no)
                        if self.rule_satisfied(stopping_rule, case):
                            rules_fired.append(stopping_rule.rule_no)
                            stopped = True
                            break
                        stopping_rule = self.get_rule(stopping_rule.if_false)

                if not stopped and current_rule.conclusion not in conclusions:
                    conclusions.append(current_rule.conclusion)
        if len(conclusions) == 0:
            return False, rules_evaluated, rules_fired
        else:
            return conclusions, rules_evaluated, rules_fired
