import pandas as pd
from langchain.tools import tool

# @tool
def BuscarAlertasDePerigoParaAPopulacaoAtuais() -> str:
    """
        Retorna as URLs com os alertas publicados no site da Defesa Civil para a população do Rio Grande do Sul (RS).
        Essa função considera apenas os alertas ainda válidos
    """
    dfAlerts = pd.read_csv("/alvinbot/data/tables/Real_ListaDeAlertasEmRS.csv", header=1)

    dfAlerts_filtered = dfAlerts.loc[dfAlerts['esta_expirado'] == False]

    return dfAlerts_filtered.to_json()

# @tool
def BuscarAlertasDePerigoParaAPopulacaoExpirados() -> str:
    """
        Retorna as URLs com os alertas publicados no site da Defesa Civil para a população do Rio Grande do Sul (RS).
        Essa função considera apenas os alertas já expirados.
    """
    dfAlerts = pd.read_csv("/alvinbot/data/tables/Real_ListaDeAlertasEmRS.csv", header=1)

    dfAlerts_filtered = dfAlerts.loc[dfAlerts['esta_expirado'] == True]

    return dfAlerts_filtered.to_json()
