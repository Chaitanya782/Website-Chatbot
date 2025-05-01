from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from contextlib import asynccontextmanager
import asyncio
import uvicorn
from src.helper import llm_pipeline  # Make sure this module exists and is importable
from src.url import urls

# Global placeholders
chatbot_chain = None
chatbot_ready = False

# Background initialization function
async def initialize_chain():
    global chatbot_chain, chatbot_ready
    print("Starting background chain initialization...")
    chatbot_chain = llm_pipeline(urls)  # Replace with your actual initialization
    chatbot_ready = True
    print("Chatbot chain initialized and ready.")

# Lifespan event to trigger background task
@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(initialize_chain())  # Non-blocking init
    yield  # App is now ready to serve requests

# Create FastAPI app with custom lifespan
app = FastAPI(lifespan=lifespan)

# Static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Pydantic model
class QuestionInput(BaseModel):
    question: str

# Root endpoint for the UI
@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Question endpoint
@app.post("/ask")
async def ask_question(data: QuestionInput):
    if not chatbot_ready:
        return JSONResponse(
            content={"answer": "Chatbot is still initializing. Please try again in a few seconds."},
            status_code=503
        )
    try:
        response = chatbot_chain.invoke({"query": str(data)}, return_only_outputs=True)
        return JSONResponse(content={"answer": response['result']})
    except Exception as e:
        print(f"Error: {e}")
        return JSONResponse(content={"answer": "Error processing the question."}, status_code=500)

# Status endpoint
@app.get("/status")
async def status():
    return {"ready": chatbot_ready}



if __name__ == "__main__":
    uvicorn.run("app:app", host='0.0.0.0', port=8090, reload=True)

