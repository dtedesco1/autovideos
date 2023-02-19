import openai

# Initialize the API key
with open("config.txt", "r") as f:
    API_KEY = f.readline().strip()
openai.api_key = API_KEY

# Define the prompt for generating questions
questions_prompt = "Generate five interesting and funny questions to ask Abraham Lincoln for a 60-second TikTok video."

# Use the OpenAI API to generate the questions
questions_response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=questions_prompt,
    max_tokens=1024,
    n=1,
    stop=None,
    temperature=0.5,
)

# Get the generated questions
generated_questions = questions_response["choices"][0]["text"].strip().split("\n")

# print(generated_questions)

# # Define the prompt for generating responses
responses_prompt = "Respond to the following questions as if you were Abraham Lincoln:\n\n{0}".format('\n'.join(generated_questions))

# print(responses_prompt)

# Use the OpenAI API to generate the responses
responses_response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=responses_prompt,
    max_tokens=1024,
    n=1,
    stop=None,
    temperature=0.5,
)

# # Get the generated responses
generated_responses = responses_response["choices"][0]["text"].strip().split("\n")

print(generated_responses)

# # Define the prompt for generating DALL·E prompts
# dalle_prompt = "Generate a Stable Diffusion or Midjourney prompt for each of the following questions and responses for Abraham Lincoln:\n\n{0}".format('\\n'.join(f'{q}: {r}' for q, r in zip(generated_questions, generated_responses)))

# # Use the OpenAI API to generate the DALL·E prompts
# dalle_response = openai.Completion.create(
#     engine="text-davinci-002",
#     prompt=dalle_prompt,
#     max_tokens=1024,
#     n=1,
#     stop=None,
#     temperature=0.5,
# )

# # Get the generated DALL·E prompts
# generated_dalle_prompts = dalle_response["choices"][0]["text"].strip().split("\n")

# # Print the generated questions, responses, and DALL·E prompts
# for q, r, dp in zip(generated_questions, generated_responses, generated_dalle_prompts):
#     print(f"Question: {q}")
#     print(f"Response: {r}")
#     print(f"DALL·E Prompt: {dp}\n")
