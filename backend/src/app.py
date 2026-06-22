from fastapi.middleware.cors import CORSMiddleware

from .routes import auth

from .routes import chat_message
from fastapi import FastAPI
from .database import engine
from .models import Base
from .routes import chat_session

app = FastAPI(
    tittle="The unnoficial world cup chatbot",
    description="Multi user chatbot with session autentication using gemini and langchain", 
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # a origem do seu frontend Vite
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(chat_session.router)
app.include_router(chat_message.router)

@app.get('/healthy')
def health_check():
    return {'status': 'Healthy'}


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)