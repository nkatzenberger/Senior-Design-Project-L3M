"""
Test file for calling modelPrompt and ensuring proper functionality
"""
import os
from modelPrompt import PromptModel

if __name__ == "__main__":
    script_directory = os.path.dirname(os.path.abspath(__file__))
    model_name = "openai-community-gpt2"
    model_path = os.path.join(script_directory, "models", model_name)
    prompt = "What is AI"

    # Initialize the model
    prompt_model = PromptModel(model_path)

    # Generate a response for the prompt
    response = prompt_model.generate_response(prompt)

    # Print the response
    print(response)