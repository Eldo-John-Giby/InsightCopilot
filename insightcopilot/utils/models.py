import os
from langchain.chat_models import ChatOpenAI
from langchain.llms import HuggingFaceHub
from dotenv import load_dotenv

load_dotenv()

def get_model(model_name: str = "openai"):
    """
    Loads a specified language model.

    Args:
        model_name (str): The name of the model to load ('openai' or 'huggingface').

    Returns:
        A LangChain model instance.
    """
    if model_name == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables.")
        return ChatOpenAI(api_key=api_key, model_name="gpt-3.5-turbo")
    
    elif model_name == "huggingface":
        api_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
        if not api_token:
            raise ValueError("HUGGINGFACEHUB_API_TOKEN not found in environment variables.")
        # Example model, you can choose others from the Hugging Face Hub
        return HuggingFaceHub(
            repo_id="google/flan-t5-large",
            huggingfacehub_api_token=api_token,
            model_kwargs={"temperature": 0.7, "max_length": 512}
        )
        
    else:
        raise ValueError(f"Unsupported model_name: {model_name}. Choose 'openai' or 'huggingface'.")

# Example usage:
if __name__ == "__main__":
    # Make sure you have a .env file with your API keys
    try:
        print("Loading OpenAI model...")
        openai_model = get_model("openai")
        print("OpenAI model loaded successfully:", type(openai_model))
        
        # To test Hugging Face, uncomment the following lines
        # print("\nLoading Hugging Face model...")
        # hf_model = get_model("huggingface")
        # print("Hugging Face model loaded successfully:", type(hf_model))

    except ValueError as e:
        print(e)
