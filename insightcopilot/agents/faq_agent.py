import os
import pandas as pd
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from utils.models import get_model

class FAQAgent:
    def __init__(self, model_name: str = "openai", data_path: str = "data/faq_knowledge_base.csv"):
        """
        Initializes the FAQ Agent.

        Args:
            model_name (str): The name of the model to use ('openai' or 'huggingface').
            data_path (str): Path to the FAQ CSV knowledge base.
        """
        # Load the language model
        self.llm = get_model(model_name)
        
        # Load the prompt template
        prompt_path = os.path.join("prompts", "faq_prompt.txt")
        with open(prompt_path, "r") as f:
            self.prompt_template = PromptTemplate(
                template=f.read(),
                input_variables=["context", "question"]
            )
        
        # Create the LLM chain
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt_template)
        
        # Load and process the knowledge base
        self.vector_store = self._create_vector_store(data_path)

    def _create_vector_store(self, data_path: str):
        """
        Creates a FAISS vector store from the FAQ CSV file.
        """
        try:
            df = pd.read_csv(data_path)
            # Combine question and answer for richer context
            df['text'] = df['question'] + " " + df['answer']
            
            # Use OpenAI embeddings
            embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
            
            # Create the vector store
            return FAISS.from_texts(df['text'].tolist(), embeddings)
        except FileNotFoundError:
            raise ValueError(f"FAQ data file not found at {data_path}")
        except Exception as e:
            raise RuntimeError(f"Failed to create vector store: {e}")

    def get_answer(self, query: str) -> str:
        """
        Answers a user's query using the retrieval-augmented generation pipeline.

        Args:
            query (str): The user's question.

        Returns:
            The generated answer.
        """
        # 1. Retrieve relevant context from the vector store
        try:
            docs = self.vector_store.similarity_search(query, k=3)
            context = "\n".join([doc.page_content for doc in docs])
        except Exception as e:
            return f"Error during context retrieval: {e}"

        # 2. Run the LLM chain with the retrieved context
        try:
            response = self.chain.run({"context": context, "question": query})
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
            print("Initializing FAQ Agent...")
            faq_agent = FAQAgent(model_name="openai")
            print("Agent initialized.")

            # Test with a sample query
            test_query = "How is Customer Lifetime Value calculated?"
            print(f"\nTesting with query: '{test_query}'")
            answer = faq_agent.get_answer(test_query)
            
            print("\n--- Generated Answer ---")
            print(answer)
            
        except (ValueError, RuntimeError) as e:
            print(f"An error occurred: {e}")
