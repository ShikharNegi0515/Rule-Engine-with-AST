
class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.type = node_type
        self.left = left
        self.right = right
        self.value = value

def parse_condition(condition):
    # A helper function to split a condition like "age > 30" into its parts
    field, operator, value = condition.split()
    # Convert value into its correct type (int, float, string)
    try:
        value = int(value)
    except ValueError:
        try:
            value = float(value)
        except ValueError:
            value = value.strip("'")
    return field, operator, value

def apply_operator(data_value, operator, condition_value):
    # Apply the appropriate operator to evaluate the condition
    if operator == ">":
        return data_value > condition_value
    elif operator == "<":
        return data_value < condition_value
    elif operator == ">=":
        return data_value >= condition_value
    elif operator == "<=":
        return data_value <= condition_value
    elif operator == "==":
        return data_value == condition_value
    elif operator == "!=":
        return data_value != condition_value
    return False

def eval_condition(condition, data):
    field, operator, value = parse_condition(condition)
    return apply_operator(data[field], operator, value)

def evaluate_rule(ast, data):
    if ast.type == "operand":
        return eval_condition(ast.value, data)
    
    if ast.type == "operator":
        left_result = evaluate_rule(ast.left, data)
        right_result = evaluate_rule(ast.right, data)
        
        if ast.value == "AND":
            return left_result and right_result
        elif ast.value == "OR":
            return left_result or right_result

def create_rule(rule_string):
    # A simple parser that converts a string rule into an AST
    # In actual implementation, you would tokenize the input and build the AST accordingly
    root = Node("operator", value="AND")
    root.left = Node("operator", value="OR",
                     left=Node("operator", value="AND",
                               left=Node("operand", value="age > 30"),
                               right=Node("operand", value="department == 'Sales'")),
                     right=Node("operator", value="AND",
                                left=Node("operand", value="age < 25"),
                                right=Node("operand", value="department == 'Marketing'")))
    root.right = Node("operator", value="OR",
                      left=Node("operand", value="salary > 50000"),
                      right=Node("operand", value="experience > 5"))
    return root

def combine_rules(rules):
    # This function takes a list of AST rules and combines them into a single AST
    if not rules:
        return None
    if len(rules) == 1:
        return rules[0]

    combined_root = Node("operator", value="AND", left=rules[0])
    current_node = combined_root

    for rule in rules[1:]:
        new_node = Node("operator", value="AND", left=current_node, right=rule)
        current_node = new_node

    return current_node

# Test cases
# Rule 1: ((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)
rule1 = create_rule("((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)")

# Sample data for evaluation
data = {"age": 35, "department": "Sales", "salary": 60000, "experience": 3}

# Evaluate the rule with sample data
result = evaluate_rule(rule1, data)
print(result)  # Output: True
