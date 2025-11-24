import os
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from utils.models import get_model
from utils.parsers import read_pdf, clean_text

class ResearchAgent:
    def __init__(self, model_name: str = "openai"):
        """
        Initializes the Research Agent.

        Args:
            model_name (str): The name of the model to use ('openai' or 'huggingface').
        """
        # Load the language model
        self.llm = get_model(model_name)
        
        # Load the prompt template
        prompt_path = os.path.join("prompts", "research_prompt.txt")
        with open(prompt_path, "r") as f:
            self.prompt_template = PromptTemplate(
                template=f.read(),
                input_variables=["text"]
            )
        
        # Create the LLM chain
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt_template)

    def analyze_document(self, file_path: str) -> str:
        """
        Analyzes a PDF document and extracts structured insights.

        Args:
            file_path (str): The path to the PDF file.

        Returns:
            A string containing the structured insights.
        """
        # 1. Read and clean the document text
        try:
            raw_text = read_pdf(file_path)
            if "Error:" in raw_text:
                return raw_text
            
            document_text = clean_text(raw_text)
            
            # Truncate text if it's too long for the model's context window
            # A simple approach; more advanced methods could use summarization chains
            max_chars = 15000 # GPT-3.5-turbo context is ~16k tokens, roughly 4 chars/token
            if len(document_text) > max_chars:
                document_text = document_text[:max_chars]
                
        except Exception as e:
            return f"Error during document processing: {e}"

        # 2. Run the LLM chain with the document text
        try:
            response = self.chain.run({"text": document_text})
            return response
        except Exception as e:
            return f"Error during LLM chain execution: {e}"

# Example usage:
if __name__ == "__main__":
    # Ensure you have a .env file with OPENAI_API_KEY
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not found. Please create a .env file.")
    else:
        try:
            print("Initializing Research Agent...")
            research_agent = ResearchAgent(model_name="openai")
            print("Agent initialized.")

            # Test with the sample annual report
            # Note: The sample PDF is a placeholder and may not yield a perfect analysis.
            # A real annual report would provide much better results.
            sample_pdf_path = os.path.join("data", "sample_annual_report.pdf")
            
            if not os.path.exists(sample_pdf_path):
                print(f"Sample PDF not found at {sample_pdf_path}. Skipping analysis.")
            else:
                print(f"\nAnalyzing document: '{sample_pdf_path}'")
                analysis = research_agent.analyze_document(sample_pdf_path)
                
                print("\n--- Generated Analysis ---")
                print(analysis)
            
        except (ValueError, RuntimeError) as e:
            print(f"An error occurred: {e}")
