# app/main.py

import pandas as pd
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.models.schemas import ClienteInput, PredicaoOutput
from app.explainer import get_prediction_and_explanation

app = FastAPI(title="API de Predição de Churn")
templates = Jinja2Templates(directory="app/static")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/predict", response_model=PredicaoOutput)
def predict_churn(cliente_input: ClienteInput):
    """ Recebe os dados de um cliente, faz a predição e retorna a explicação. """
    # Converte o objeto Pydantic recebido para um DataFrame do Pandas.
    # O pipeline espera um DataFrame com os nomes das colunas originais.
    input_df = pd.DataFrame([cliente_input.dict()])

    # Chama nossa função de serviço, que agora lida com tudo.
    result = get_prediction_and_explanation(input_df)
    return result
