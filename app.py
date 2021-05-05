from fastapi import FastAPI
import loaders
from controllers.disease_controller import disease_controller

# Initialize database here
# loaders.load_database()

app = FastAPI()

# Load controllers here
app.include_router(disease_controller)