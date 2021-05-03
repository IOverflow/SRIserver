from fastapi import FastAPI
import loaders

# Initialize database here
loaders.load_database()

app = FastAPI()

@app.get("/")
async def home():
    return "Hello World"

@app.post("/")
async def post_home(message: str):
    return f"Posted: {message}"