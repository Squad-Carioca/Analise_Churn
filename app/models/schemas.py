# app/models/schemas.py
from pydantic import BaseModel, Field
from typing import List


class ClienteInput(BaseModel):
    """
    Schema para os dados de entrada de um cliente, vindos do formulário.
    Os nomes dos campos devem corresponder exatamente às colunas do dataset original.
    """
    Estado: str = Field(..., example="KS") 
    TempoConta: int = Field(..., example=0)  
    CodigoArea: int = Field(..., example=0)   
    PlanoInternacional: str = Field(..., example="KS") 
    PlanoCorreioVoz: str = Field(..., example="KS") 
    NumerodeMensagensdeVoz: int = Field(..., example=0)  
    TotalMinutosDia: float = Field(..., example=29.85)
    TotalChamadasDia: int = Field(..., example=0)  
    CustoTotalDia: float = Field(..., example=29.85)
    TotalMinutosTardeNoite: float = Field(..., example=29.85)
    TotalChamadasTardeNoite: int = Field(..., example=0)  
    CustoTotalTardeNoite: float = Field(..., example=29.85)
    TotalMinutosNoturno: float = Field(..., example=29.85)
    TotalChamadasNoturno: int = Field(..., example=0)  
    CustoTotalNoturno: float = Field(..., example=29.85)
    TotalMinutosInternacionais: float = Field(..., example=29.85)
    TotalChamadasInternacionais: int = Field(..., example=0)
    CustoTotalInternacional: float = Field(..., example=29.85)
    ChamadasSuporte: int = Field(..., example=0)  


class PredicaoOutput(BaseModel):
    """
    Schema para a resposta da API, incluindo a predição e a explicação.
    """
    predicao: str
    probabilidade_churn: float
    explicacao: List[str]
