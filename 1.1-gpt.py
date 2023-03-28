# Import required libraries
import openai
import yaml
import os
from concurrent.futures import ThreadPoolExecutor
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


# Define get_chatgpt_response(prompt) function
def get_chatgpt_response(prompt):
    try:
        # Set up OpenAI API key and configuration
        openai.api_key = os.environ.get("OPENAI_API_KEY")

        # Make a call to the ChatGPT API with the given prompt
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=100, # Remember to change the token size
            n=1,
            stop=None,
            temperature=0.7,
        )

        # Extract and return the response from the API result
        return response.choices[0].text.strip()
    except Exception as e:
        logging.error(f"Error while fetching response from ChatGPT API: {e}")
        return None


# Define generate_questions_answers_and_prompts(famous_person, num_questions) function
def generate_questions_answers_and_prompts(famous_person, num_questions=5):
    questions_answers_prompts = []
    generic_prompts = [
        f"funny question to ask {famous_person}",
        f"interesting question to ask {famous_person}",
        f"ask {famous_person} a very funny question like a comedian"
        # Add more templates as desired
    ]

    # Generate unique questions
    while len(questions_answers_prompts) < num_questions:
        for prompt in generic_prompts:
            question = get_chatgpt_response(prompt)
            if question not in questions_answers_prompts:
                questions_answers_prompts.append(question)
                if len(questions_answers_prompts) == num_questions:
                    break

    # Define a function to process each question-answer-prompt set
    def process_question(question):
        answer = get_chatgpt_response(f"In the voice of {famous_person}, how would they answer this question: {question}?")
        dall_e_prompt = get_chatgpt_response(f"DALL-E prompt to represent a scene where {famous_person} is answering the question: {question}")
        return {"Q": question, "A": answer, "P": dall_e_prompt}

    # Parallelize the process for each question
    with ThreadPoolExecutor() as executor:
        processed_data = list(executor.map(process_question, questions_answers_prompts))

    return processed_data


# Define save_to_yaml(data, filename) function
def save_to_yaml(data, filename):
    try:
        with open(filename, 'w') as file:
            yaml.dump(data, file)
    except Exception as e:
        logging.error(f"Error while saving data to YAML file: {e}")


# Main function or script execution
def main():
    famous_person = "Albert Einstein"  # Replace with desired famous person's name
    num_questions = 5
    filename = "generated_content.yaml"

    # Call generate_questions_answers_and_prompts function
    data = generate_questions_answers_and_prompts(famous_person, num_questions)

    # Save the generated data to a YAML file
    save_to_yaml(data, filename)
    logging.info(f"Data saved to {filename}")


if __name__ == "__main__":
    main()