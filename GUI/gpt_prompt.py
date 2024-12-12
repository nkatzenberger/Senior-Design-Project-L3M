import os
import argparse
from transformers import AutoModelForCausalLM, AutoTokenizer


def load_model(model_path):
    """
    Load the tokenizer and model from a path.
    """
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(model_path)
    return tokenizer, model


def generate_response(prompt, tokenizer, model, max_length=100):
    """
    Generate a response to the given prompt using the loaded model.
    """
    # Ensure the tokenizer has a padding token
    if tokenizer.pad_token is None:
        tokenizer.add_special_tokens({'pad_token': '[PAD]'})
        model.resize_token_embeddings(len(tokenizer))  # Update model for new tokens

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        padding=True,  # Ensure padding is applied if needed
        truncation=True,  # Truncate if input is too long
    )
    
    pad_token_id = tokenizer.pad_token_id if tokenizer.pad_token_id is not None else tokenizer.eos_token_id

    # Generate text
    outputs = model.generate(
        inputs["input_ids"],
        attention_mask=inputs["attention_mask"],  # Explicitly pass the attention mask
        max_length=max_length,
        num_return_sequences=1,
        repetition_penalty=1.2,
        no_repeat_ngram_size=3,
        pad_token_id=pad_token_id,  # Explicitly set pad_token_id
        eos_token_id=tokenizer.eos_token_id,  # Ensure EOS token is used
    )
    
    # Decode the response
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

def main():
    parser = argparse.ArgumentParser(description="Prompt a GPT model and get a response.")
    parser.add_argument("--model-path", type=str, help="Path to the GPT model directory.")
    parser.add_argument("--prompt", type=str, required=True, help="Input prompt for the GPT model.")
    parser.add_argument("--max-length", type=int, default=500, help="Maximum length of the generated response.")
    
    args = parser.parse_args()

    # Default to a relative path if --model-path is not provided
    if not args.model_path:
        script_directory = os.path.dirname(os.path.abspath(__file__))
        model_name = "openai-community-gpt2"
        args.model_path = os.path.join(script_directory, "models", model_name)

    # Load the model and tokenizer
    tokenizer, model = load_model(args.model_path)

    # Generate a response to the prompt
    response = generate_response(args.prompt, tokenizer, model, args.max_length)

    # Print the response
    print("\nGenerated Response:")
    print(response)


if __name__ == "__main__":
    main()
