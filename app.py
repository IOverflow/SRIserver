from fastapi import FastAPI
import loaders
from controllers.disease_controller import disease_controller
from controllers.search_controller import search_controller
from services.search_service import Index, index
from colorama import Fore
import uvicorn
import config.settings as conf
from fastapi.middleware.cors import CORSMiddleware

# Initialize database here
# loaders.load_database()

app = FastAPI()

# Add middlewares here
app.add_middleware(
    CORSMiddleware,
    allow_origins=conf.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.on_event("startup")
async def make_index():
    """
    Create the index for search engine.
    """
    Index.initialize(index)
    print(f"{Fore.GREEN}INFO{Fore.RESET}:     Index created")


# Load controllers here
app.include_router(disease_controller)
app.include_router(search_controller)

if __name__ == "__main__":
    uvicorn.run(app, host=conf.HOST_IP, port=conf.HOST_PORT)
