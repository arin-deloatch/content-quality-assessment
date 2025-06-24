from fastapi import FastAPI, Body
import textstat
from pydantic import BaseModel

app = FastAPI()

# Readability score 
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.get("/", tags=["Q.o.L"])
async def root():
    return {"message": "Home"}

@app.get("/health", tags=["Q.o.L"])
async def health():
    if True:
        return 200
    
@app.get("/readability-score", tags=["Readability Service"])
async def get_readability_score(text:str = Body()):
    return {
        "flesch_reading_ease": textstat.flesch_reading_ease(text),
        "flesch_kincaid_grade": textstat.flesch_kincaid_grade(text),
        "difficult_words": textstat.difficult_words(text)
    }
