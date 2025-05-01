# Website Chat Bot

A FastAPI-based intelligent chat bot for ISecServ, a professional information security services company. This chat bot uses LangChain with Google Gemini models to provide context-aware responses based on website content.

## Features

- **Context-Aware Responses**: Uses vector embeddings to retrieve relevant information from the company website
- **Professional Tone**: Maintains ISecServ's brand identity with professionally crafted responses
- **FastAPI Backend**: High-performance asynchronous API with automatic OpenAPI documentation
- **Background Initialization**: Non-blocking startup with a status endpoint to check readiness
- **Customizable Prompts**: Template system for tailoring the chat bot's responses
- **Web UI Integration**: Ready-to-use web interface for customer interactions

## Project Structure

```
Website_chat_bot/
├── .env                   # Environment variables (API keys)
├── .venv/                 # Virtual environment
├── README.md              # This documentation
├── app.py                 # FastAPI application entry point
├── requirements.txt       # Python dependencies
├── setup.py               # Package setup script
├── src/
│   ├── __init__.py        # Package initialization
│   ├── helper.py          # LLM pipeline and vector store utilities
│   └── url.py             # URL configuration for content scraping
├── static/                # Static assets for the web interface
└── templates/
    └── index.html         # Main chat interface template
```

## Prerequisites

- Python 3.8+
- Google AI API key (for Gemini models)
- Internet connection for URL content scraping

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd Website_chat_bot
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with your Google API key:
   ```
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```

## Configuration

1. Update the URLs in `src/url.py` to point to your website content:
   ```python
   urls = [
       "https://your-website.com/about",
       "https://your-website.com/services",
       # Add more pages as needed
   ]
   ```

2. Customize the chat prompt template in `src/helper.py` if needed to match your company's tone and style.

## Usage

1. Start the application:
   ```
   python app.py
   ```

2. Access the chat interface at http://localhost:8090

3. The API will be available at:
   - Chat endpoint: `POST /ask` with JSON body `{"question": "your question here"}`
   - Status endpoint: `GET /status` to check if the chatbot is initialized

## Vector Store

The application creates a vector store from website content on first run, which is saved in the `Vector_store` directory. This improves startup time on subsequent runs as it doesn't need to re-scrape and process the content.

To force a refresh of the vector store, simply delete the `Vector_store` directory.

## Customization

### Prompt Engineering

The chat bot's responses can be customized by modifying the prompt template in `src/helper.py`. The current template is designed for an information security services company, but can be adapted for different industries or tones.

### Embedding Model

The project uses Google's embedding model by default, but you can switch to other embedding providers by modifying the `embeddings` initialization in `src/helper.py`.

## Deployment

For production deployment:

1. Use a production ASGI server like Uvicorn with Gunicorn:
   ```
   pip install gunicorn
   gunicorn -k uvicorn.workers.UvicornWorker app:app
   ```

2. Consider deploying behind a reverse proxy like Nginx for SSL termination and load balancing.

3. Set appropriate environment variables for production settings.


## Acknowledgements

- [LangChain](https://github.com/langchain-ai/langchain) for the LLM framework
- [FastAPI](https://fastapi.tiangolo.com/) for the web framework
- [Google Gemini](https://ai.google.dev/) for the language models