import sys
import json
import logging
import pathlib
from typing import Union, List
import faiss

from fastapi import FastAPI
from fastapi_health import health

from pydantic import BaseModel, conlist
from sentence_transformers import SentenceTransformer


logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


class ResponseData(BaseModel):
    response: List[List[str]]


class RequestData(BaseModel):
    text: conlist(item_type=str, min_items=1)


app = FastAPI()

model_path = pathlib.Path(".") / "models" / "flat.index"
print(model_path)

globs = {"model": None, "stmodel": None}

ids_path = pathlib.Path(".") / "models" / "ids.json"
stmodel_path = pathlib.Path(".") / "models" / "model.pkl"
with open(ids_path) as f:
    ids = json.load(f)

TOPN = 10


@app.on_event("startup")
def load_model():
    """Load model"""
    model_path = pathlib.Path(".") / "models" / "flat.index"
    logger.info("Загрузка faiss...")
    globs["model"] = faiss.read_index(str(model_path))
    logger.info("Загрузка SentenceTransformer...")
    globs["stmodel"] = SentenceTransformer("all-MiniLM-L6-v2")
    logger.info("Загрузка завершена!")


@app.get("/")
async def root():
    """Root app message"""
    return {"..."}


@app.post("/predict", response_model=ResponseData)
def predict(data: RequestData):
    data = data.dict()
    logger.info("Загрузка эмбеддингов...")
    print(data["text"])
    query_embeddings = globs["stmodel"].encode(
        data["text"], batch_size=4, show_progress_bar=True
    )
    logger.info("Предсказание классов...")
    D, I = globs["model"].search(query_embeddings, TOPN)
    print(I)
    result = []
    for i in range(len(I)):
        result.append([ids.get(str(idx), "None") for idx in I[i]])
    print(result)
    response = ResponseData(response=result)
    return response


def check_health():
    return globs["model"] is not None


app.add_api_route("/health", health([check_health]))
