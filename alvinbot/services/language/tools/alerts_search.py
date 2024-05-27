import os
import pandas as pd
from langchain_core.tools import tool

@tool
def BuscarAlertasDePerigoParaAPopulacaoAtuais(apenasUltimo: str = "False") -> str:
    """
        Retorna as URLs com os alertas publicados no site da Defesa Civil para a população do Rio Grande do Sul (RS).
        Essa função considera apenas os alertas ainda válidos.
        Para filtrar para o último alerta emitido, defina apenasUltimo como True.
    """
    dfAlerts = pd.read_csv("data/tables/Real_ListaDeAlertasEmRS.csv".replace('/', os.sep), header=0)

    dfAlerts_filtered = dfAlerts.loc[dfAlerts['esta_expirado'] == False]
    if apenasUltimo.lower() == "true":
        dfAlerts_filtered = dfAlerts_filtered[(dfAlerts_filtered["data_fim"] == dfAlerts_filtered["data_fim"].max())]

    return dfAlerts_filtered.to_json()

@tool
def BuscarAlertasDePerigoParaAPopulacaoExpirados(apenasUltimo: str = "False") -> str:
    """
        Retorna as URLs com os alertas publicados no site da Defesa Civil para a população do Rio Grande do Sul (RS).
        Essa função considera apenas os alertas já expirados.
        Para filtrar para o alerta mais recente que ja expirou, defina apenasUltimo como True.
    """
    dfAlerts = pd.read_csv("data/tables/Real_ListaDeAlertasEmRS.csv".replace('/', os.sep), header=0)

    dfAlerts_filtered = dfAlerts.loc[dfAlerts['esta_expirado'] == True]
    if apenasUltimo.lower() == "true":
        dfAlerts_filtered = dfAlerts_filtered[(dfAlerts_filtered["data_fim"] == dfAlerts_filtered["data_fim"].max())]

    return dfAlerts_filtered.to_json()
