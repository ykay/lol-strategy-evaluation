from eval import run_evaluation

criteria = """
Based on the provided information, evaluate how well the model's output conforms to the system prompt.
Provide a score from 1 to 5 where:
1 - The model's output does not conform to the specifications in the system prompt at all.
5 - The model's output is consistent with the specifications in the system prompt.
"""

run_evaluation("lol-strategy-dataset", "lol-strategy-system-compliance-eval", "response_system_compliance", criteria)
