from fastapi import FastAPI
from .database import engine
from .models import Base
from .routes import auth, chat_session

app = FastAPI(
    tittle="The unnoficial world cup chatbot",
    description="Multi user chatbot with session autentication using gemini and langchain", 
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(chat_session.router)

@app.get('/healthy')
def health_check():
    return {'status': 'Healthy'}


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)