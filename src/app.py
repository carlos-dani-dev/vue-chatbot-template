from fastapi import FastAPI


app = FastAPI(
    tittle="The unnoficial world cup chatbot",
    description="Multi user chatbot with session autentication using gemini and langchain", 
    version="1.0.0"
)


app.include