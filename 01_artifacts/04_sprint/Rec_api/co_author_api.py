import uvicorn
import logging
import json
from fastapi import FastAPI
from typing import Union, List
from collections import defaultdict

from api_params import XInput, ModelResponse

app_ = FastAPI()
logger = logging.getLogger(__name__)
reference_model = defaultdict()


def get_recommendation(authors_links: defaultdict, author_id: str,
                       num_recommendations=2) -> Union[list, str]:
    if authors_links[author_id]:
        authors_available = authors_links[author_id]
        recds = [author[1] for author in authors_available[:max(
            len(authors_available),
            num_recommendations)]]
        return recds

    elif not authors_links[author_id]:
        return f'Author {author_id} does not need the recommendation of any co-author'

    else:
        return 'No recommendation available'


@app_.get('/')
def main():
    return 'Welcome to the scientific hub!'


@app_.post('/recommend', response_model=Union[List[str], str])
def predict(request: XInput):
    logger.debug(f'{request.data=}')
    result = get_recommendation(reference_model, request.data)
    logger.info(f'successful recommendation: {result}')
    return result


@app_.get("/health")
def status() -> int:
    model_status = reference_model is not None
    logger.info(f"Model is{' not ' if not model_status else ' '}ready")
    if model_status:
        return 200


@app_.on_event('startup')
def get_model():
    global reference_model
    logger.info(f"Loading model from 'recomendations.json'")
    with open('recomendations.json', 'r') as j:
        reference_model = json.loads(j.read())


if __name__ == '__main__':
    uvicorn.run('co_author_api:app_', host='127.0.0.1', port=8000)
