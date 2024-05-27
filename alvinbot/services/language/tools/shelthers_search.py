import os
import pandas as pd
from langchain_core.tools import tool

@tool
def BuscarListaDeAbrigosCadastrados(cidade: str = None) -> str:
    """
        Retorna entidades ou organizações cadastradas para servirem de abrigos em caso de algum desastre.
        Parâmetro cidade é opcional.
    """
    dfEntities = pd.read_excel("data/tables/Mock_Entidades.xlsx".replace('/', os.sep), header=1)

    df = dfEntities[(dfEntities.CadastradoComoAbrigo == True)]
    if cidade:
        df = dfEntities[(dfEntities.Cidade == cidade)]
    df = df[["Nome", "EndereçoLogradouro", "EndereçoNúmero", "EndereçoComplemento", "CEP", "Bairro", "Cidade", "Estado", "Telefone", "LotacaoAutorizada"]]

    return df.to_json()

@tool
def BuscarListaDeAbrigosParaMulheresECriancasApenas(cidade: str = None) -> str:
    """
        Retorna abrigos que acolhem apenas mulheres e crianças.
        Parâmetro cidade é opcional.
    """
    dfOccurences = pd.read_excel("data/tables/Mock_Ocorrencias.xlsx".replace('/', os.sep), header=1)
    dfEntities = pd.read_excel("data/tables/Mock_Entidades.xlsx".replace('/', os.sep), header=1)
    dfShelters = pd.read_excel("data/tables/Mock_Abrigos.xlsx".replace('/', os.sep), header=1)

    df = dfOccurences[dfOccurences["DataFim"].isna()]
    df = df.merge(dfShelters[(dfShelters["GruposRestritos"] == "Apenas Mulheres e Crianças") & (dfShelters["DataTermino"].isna())], how='inner', left_on=['ID'],right_on=['IDOcorrencia'])

    if cidade:
        df = dfEntities[(dfEntities.Cidade == cidade)]
    df = df.merge(dfEntities, how='inner', left_on=['IDEntidade'],right_on=['ID'])

    df = df[["Nome_y", "EndereçoLogradouro", "EndereçoNúmero", "EndereçoComplemento", "CEP", "Bairro", "Cidade", "Estado", "Telefone", "LotacaoAutorizada", "GruposRestritos"]]

    return df.to_json()
