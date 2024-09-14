from langsmith.schemas import Run, Example
from langsmith.evaluation import evaluate
from openai import OpenAI
import json

from dotenv import load_dotenv
load_dotenv()

from langsmith.wrappers import wrap_openai
from langsmith import traceable

client = wrap_openai(OpenAI())

evaluation_criteria = ""
evaluation_key = ""

@traceable
def response_evaluator(run: Run, example: Example) -> dict:
  inputs = example.inputs['input']
  outputs = example.outputs['output']

  # Extract system prompt
  system_prompt = next((msg['data']['content'] for msg in inputs if msg['data']['role'] == 'system'), "")

  # Extract message history
  message_history = []
  for msg in inputs:
      if msg['type'] in ['human', 'ai']:
          message_history.append({
              "role": "user" if msg['type'] == 'human' else "assistant",
              "content": msg['data']['content']
          })

  # Extract latest user message and model output
  latest_message = message_history[-1]['content'] if message_history else ""
  model_output = outputs['data']['content']

  evaluation_prompt = f"""
    System Prompt: {system_prompt}

    Message History:
    {json.dumps(message_history, indent=2)}

    Latest User Message: {latest_message}

    Model Output: {model_output}

    {evaluation_criteria}

    Also provide a brief explanation for your score.

    Respond in the following JSON format:
    {{
        "score": <int>,
        "explanation": "<string>"
    }}
    """
  
  response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an AI assistant tasked with providing an evaluation that conforms to the user's specification."},
            {"role": "user", "content": evaluation_prompt}
        ],
        temperature=0.2
    )

  try:
    result = json.loads(response.choices[0].message.content)
    return {
        "key": evaluation_key,
        "score": result["score"] / 5,  # Normalize to 0-1 range
        "reason": result["explanation"]
    }
  except json.JSONDecodeError:
    return {
        "key": evaluation_key,
        "score": 0,
        "reason": "Failed to parse evaluator response"
    }

def run_evaluation(dataset, experiment_prefix, key, criteria):
    global evaluation_criteria, evaluation_key
    evaluation_criteria = criteria
    evaluation_key = key

    # List of evaluators to score the outputs of target task
    evaluators = [
        response_evaluator
    ]

    # Evaluate the target task
    results = evaluate(
        lambda inputs: inputs,
        data=dataset,
        evaluators=evaluators,
        experiment_prefix=experiment_prefix,
    )

    print(results)