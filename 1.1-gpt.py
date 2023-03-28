# Import required libraries
import openai
import yaml
import os
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Define get_chatgpt_response(messages) function
def get_chatgpt_response(messages, temperature=0.8):
    try:
        # Set up OpenAI API key and configuration
        openai.api_key = os.environ.get("OPENAI_API_KEY")

        # Make a call to the ChatGPT API with the given messages
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=temperature
        )

        # Extract and return the assistant's reply from the API result
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Error while fetching response from ChatGPT API: {e}")
        return None

def generate_questions_answers_and_prompts(famous_person, num_questions=5):
    data = []
    generated_questions = []

    for i in range(num_questions):
        # Create a message with previously generated questions
        previous_questions_message = "\n".join(generated_questions)

        # Generate a question for the famous person
        question_messages = [
            {"role": "system", "content": "You are a creative and interesting question-generator. You enjoy coming up with out-of-the-box questions that are very different from what's been asked before."},
            {"role": "user", "content": f"Generate a unique and interesting question to ask {famous_person} that hasn't been asked before. Avoid repeating these or similar questions:\n{previous_questions_message}\nThe new question (without quotes):"},
        ]
        question = get_chatgpt_response(question_messages)

        # Add the new question to the list of generated questions
        generated_questions.append(question)

        # Generate an answer for the question in the famous person's voice
        answer_messages = [
            {"role": "system", "content": f"You are {famous_person}. Answer the following question for a short TikTok video. You can only reply with spoken words, no asides or unspoken thoughts."},
            {"role": "user", "content": f"{question} Your response (without quotes):"},
        ]
        answer = get_chatgpt_response(answer_messages)

        # Generate a DALL-E prompt for the question and answer
        dall_e_prompt_messages = [
            {"role": "system", "content": "You are a master text-to-image prompt engineer. You don't reference 'question' or 'answer' in your prompts."},
            {"role": "user", "content": f"Generate a descriptive and effective DALL-E prompt that visualizes a scene related to the following:\n\nQuestion for {famous_person}:\n{question}\n\n{famous_person}'s response: \n{answer}. DALL-E prompt (without quotes):"},
        ]
        dall_e_prompt = get_chatgpt_response(dall_e_prompt_messages)

         # Add the question, answer, and DALL-E prompt to the data list
        data.append({
            "P": dall_e_prompt,
            "A": answer,
            "Q": question
        })

    return data

# Define save_to_yaml(data, filename) function
def save_to_yaml(data, filename):
    formatted_data = {}
    for idx, item in enumerate(data, start=1):
        formatted_data[idx] = item

    try:
        with open(filename, 'w') as file:
            yaml.dump(formatted_data, file, default_flow_style=False)
    except Exception as e:
        logging.error(f"Error while saving data to YAML file: {e}")

# Main function or script execution
def main():
    # Set famous_person via user input
    famous_person = input("Enter the name of a famous person: ")

    # Set num_questions via user input
    num_questions = int(input("Enter the number of questions to generate: "))

    # Generate a timestamped filename with the famous person's name
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{famous_person.replace(' ', '_')}_content_{timestamp}.yaml"

    # Generate questions, answers, and DALL·E prompts
    data = generate_questions_answers_and_prompts(famous_person, num_questions)

    # Save the generated data to a YAML file
    save_to_yaml(data, filename)

if __name__ == "__main__":
    main()
