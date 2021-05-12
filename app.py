import json
from fastapi import FastAPI
from controllers.disease_controller import disease_controller
from controllers.search_controller import search_controller
from services.search_service import Index, index
from colorama import Fore
import uvicorn
from config import settings as conf
from fastapi.middleware.cors import CORSMiddleware
from dependencies.dbconnection import database
from engines.ranking.nn_model import FeedForwardRankingNNModel, ranker
from tensorflow.keras.models import model_from_json
from tensorflow.keras.losses import MeanSquaredError


app = FastAPI()

# Add middlewares here
app.add_middleware(
    CORSMiddleware,
    allow_origins=conf.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def make_index():
    """
    Create the index for search engine.
    """
    if conf.USE_DATABASE_BACKEND:
        await database.connect()
    await Index.initialize(index)
    print(f"{Fore.GREEN}INFO{Fore.RESET}:     Index created")

    # load the NN model
    with open("model.json", "r") as model_file:
        model_bytecode = model_file.read()
        ranker.model = model_from_json(model_bytecode)

    # load the model weights
    ranker.model.load_weights("model.h5")
    ranker.model.compile(loss=MeanSquaredError, optimizer="adam")

    print(f"{Fore.GREEN}INFO{Fore.RESET}:     Loaded NN model")


@app.on_event("shutdown")
async def shutdown():
    if conf.USE_DATABASE_BACKEND:
        await database.disconnect()


# Load controllers here
app.include_router(disease_controller)
app.include_router(search_controller)

if __name__ == "__main__":
    uvicorn.run(app, host=conf.HOST_IP, port=conf.HOST_PORT)
