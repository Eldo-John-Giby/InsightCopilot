# InsightCopilot – GenAI Research & Reporting Agent

InsightCopilot is a powerful GenAI-powered agent designed to streamline business research and reporting. It comprises two specialized agents:

1.  **FAQ / Guidance Copilot Agent**: Answers business questions with step-by-step guidance, pulling from a dedicated knowledge base.
2.  **Research Extraction Agent**: Extracts and summarizes key business insights from PDF documents like annual reports.

This project is built with Python, LangChain, and FastAPI, providing a robust and scalable architecture for agentic AI workflows.

## How to Run the Project

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd InsightCopilot
    ```

2.  **Install dependencies:**
    Make sure you have Python 3.9+ installed.
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up environment variables:**
    Create a `.env` file in the root directory and add your OpenAI API key:
    ```
    OPENAI_API_KEY="your_openai_api_key_here"
    ```

4.  **Run the application:**
    ```bash
    python main.py
    ```
    The server will start on `http://localhost:8000`.

## API Endpoints

You can interact with the agents via the following API endpoints.

### 1. FAQ / Guidance Copilot

-   **Endpoint**: `/faq`
-   **Method**: `POST`
-   **Description**: Ask a business-related question and get guidance.
-   **Request Body**:
    ```json
    {
      "query": "How do I calculate customer lifetime value?"
    }
    ```
-   **cURL Example**:
    ```bash
    curl -X POST "http://localhost:8000/faq" \
         -H "Content-Type: application/json" \
         -d '{"query": "How do I calculate customer lifetime value?"}'
    ```

### 2. Research Extraction Agent

-   **Endpoint**: `/research`
-   **Method**: `POST`
-   **Description**: Upload a PDF report to extract structured insights.
-   **Request Body**: This is a `multipart/form-data` request.
-   **cURL Example**:
    ```bash
    curl -X POST "http://localhost:8000/research" \
         -F "file=@./data/sample_annual_report.pdf"
    ```

## Project Structure

```
/insightcopilot/
│
├─ data/
│   ├─ faq_knowledge_base.csv     # Sample FAQ dataset
│   └─ sample_annual_report.pdf   # Dummy business report
│
├─ agents/
│   ├─ faq_agent.py               # LangChain FAQ agent logic
│   └─ research_agent.py          # LangChain research agent logic
│
├─ api/
│   └─ server.py                  # FastAPI application
│
├─ prompts/
│   ├─ faq_prompt.txt             # Prompt template for the FAQ agent
│   └─ research_prompt.txt        # Prompt template for the research agent
│
├─ utils/
│   ├─ parsers.py                 # PDF parsing and text cleaning utilities
│   └─ models.py                  # LLM model loader
│
├─ README.md                      # This file
├─ requirements.txt               # Project dependencies
├─ main.py                        # Application entry point
└─ .gitignore                     # Git ignore file
```

## Folder-by-Folder Explanation

-   **`data/`**: Contains the raw data sources for the agents, including the FAQ knowledge base and a sample PDF report.
-   **`agents/`**: Core logic for the AI agents is defined here. Each agent is a self-contained module responsible for a specific task.
-   **`api/`**: The FastAPI server that exposes the agents' functionalities through RESTful endpoints.
-   **`prompts/`**: Stores prompt templates, allowing for easy modification and versioning of prompts without changing the application code.
-   **`utils/`**: A collection of helper modules for common tasks like loading models and parsing documents.
-   **`main.py`**: The main entry point that launches the FastAPI application.

## Screenshots

*(Placeholder for a screenshot of the API documentation at http://localhost:8000/docs)*

![API Docs](https://via.placeholder.com/800x400.png?text=API+Documentation+Screenshot)

*(Placeholder for a screenshot of a sample cURL request and response)*

![API Example](https://via.placeholder.com/800x400.png?text=cURL+Request/Response+Example)

## Deployment

### Local Deployment

Follow the "How to Run the Project" section to run the application locally. The API will be accessible at `http://localhost:8000`.

### Deploy on Render

1.  **Fork this repository** to your GitHub account.
2.  **Create a new Web Service** on [Render](https://render.com/).
3.  **Connect your GitHub repository**.
4.  **Configure the service**:
    -   **Environment**: `Python 3.9`
    -   **Build Command**: `pip install -r requirements.txt`
    -   **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5.  **Add Environment Variables**:
    -   `OPENAI_API_KEY`: Your OpenAI API key.
6.  **Deploy!** Render will automatically build and deploy your application.
