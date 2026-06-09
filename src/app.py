from fastapi import FastAPI
from .database import engine, Base


app = FastAPI(
    tittle="The unnoficial world cup chatbot",
    description="Multi user chatbot with session autentication using gemini and langchain", 
    version="1.0.0"
)


@app.get('/healthy')
def health_check():
    return {'status': 'Healthy'}


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)