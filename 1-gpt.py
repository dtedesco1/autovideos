import openai
import json

# Initialize the API key
with open("config.txt", "r") as f:
    API_KEY = f.readline().strip()
openai.api_key = API_KEY

# Define the prompt for generating questions
questions_prompt = 'Generate two interesting and funny questions to ask Abraham Lincoln for a 60-second TikTok video. Return the questions in json format, like {"1": "question", "2": "question"}.'

# Use the OpenAI API to generate the questions
questions_response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=questions_prompt,
    max_tokens=4000,
    n=1,
    stop=None,
    temperature=0.5,
)

# Get the generated questions
generated_questions = json.loads(questions_response["choices"][0]["text"].strip())

print(generated_questions, "\n\n\n")

# # Define the prompt for generating responses
responses_prompt = 'Respond in json format like {"Question 1":"Response 1", "Question 2":"Response 2"} to the following questions as if you were a drunk and happy Abraham Lincoln:  '
for key, val in generated_questions.items():
    responses_prompt += f"\n{key}: {val}\n"

# responses_prompt = "Respond to the following questions as if you were Abraham Lincoln:\n\n{0}".format('\n'.join(generated_questions))

# print(responses_prompt)

# Use the OpenAI API to generate the responses
responses_response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=responses_prompt,
    max_tokens=4000,
    n=1,
    stop=None,
    temperature=0.5,
)

# # Get the generated responses
generated_responses = json.loads(responses_response["choices"][0]["text"].strip())

print(generated_responses, "\n\n\n")

# # Define the prompt for generating DALL·E prompts
dalle_prompt = "Generate a Stable Diffusion or Midjourney prompt for each of the following questions and responses for Abraham Lincoln:\n\n{0}".format('\\n'.join(f'{q}: {r}' for q, r in zip(generated_questions, generated_responses)))

print(dalle_prompt, "\n\n\n")

# Use the OpenAI API to generate the DALL·E prompts
dalle_response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=dalle_prompt,
    max_tokens=1024,
    n=1,
    stop=None,
    temperature=0.5,
)

# Get the generated DALL·E prompts
generated_dalle_prompts = dalle_response["choices"][0]["text"].strip().split("\n")

print(generated_dalle_prompts)

# # Print the generated questions, responses, and DALL·E prompts
# for q, r, dp in zip(generated_questions, generated_responses, generated_dalle_prompts):
#     print(f"Question: {q}")
#     print(f"Response: {r}")
#     print(f"DALL·E Prompt: {dp}\n")

#-----------------------------------------
# Pipeline 