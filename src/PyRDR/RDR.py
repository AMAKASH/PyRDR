import os
import pickle


class Rule:

    def __init__(self, conditions: dict, cornerstone: list, conclusion: str, if_false=None, if_true=None,
                 is_refinement=False, is_stopping=False, parent: int = None) -> None:
        self.parent = parent
        self.is_refinement = is_refinement
        self.conditions = conditions
        self.cornerstone = cornerstone
        self.conclusion = conclusion
        self.if_true = if_true
        self.if_false = if_false
        self.is_stopping = is_stopping
        self.rule_no = -1

    def __repr__(self):
        tobe_returned = f"Rule No: {self.rule_no}, conditions: {self.conditions}, \n\t\tconclusion: {self.conclusion},"
        if self.is_refinement:
            tobe_returned += f" parent: {self.parent},"
        tobe_returned += f"\n\t cornerstone: {self.cornerstone}"
        return tobe_returned


class RDR:
    def __init__(self, features: list, rule: Rule = None) -> None:
        self.rules = []
        if rule:
            self.rules = [rule]
        self.features = features

    def get_rule(self, rule_no) -> Rule | bool:
        for r in self.rules:
            if r.rule_no == rule_no:
                return r
        return False

    def rule_satisfied(self, rule: Rule, case: list) -> bool:
        conditions = rule.conditions
        condition_keys = conditions.keys()
        for key in condition_keys:
            feature_index = self.features.index(key)
            condition = conditions[key]
            if key in condition:
                tobe_evaluated_string = condition.replace(
                    key, str(case[feature_index]))
            else:
                tobe_evaluated_string = f"{case[feature_index]} {condition}"
            if not eval(tobe_evaluated_string):
                return False
        return True

    def print_rules(self):
        print("The following rules are available for this kb:")
        for i, r in enumerate(self.rules):
            print(f"{i + 1}. {r}")
        print("\n            -End of Rules- \n\n")

    def save_kb_to_file(self, filename, path=None):
        if path:
            save_path = os.path.join(path, filename)
        else:
            save_path = filename
        with open(save_path, 'wb') as file:
            pickle.dump(self, file)

    @staticmethod
    def load_kb_from_file(path):
        with open(path, 'rb') as file:
            return pickle.load(file)
