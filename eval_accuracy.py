from eval import run_evaluation

criteria = """
Based on the provided information, evaluate how much the model's output accurately reflects the information provided in the context.
Provide a score from 1 to 5 where:
1 - The model's output is irrelevant or doesn't appropriately use the context provided.
5 - The model's output is highly relevant and accurately reflects the information provided in the context.
"""

run_evaluation("lol-strategy-dataset", "lol-strategy-accuracy-eval", "response_accuracy", criteria)