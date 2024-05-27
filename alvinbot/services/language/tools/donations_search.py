import pandas as pd
from langchain_core.tools import tool

@tool
def BuscarAbrigosPrecisandoDeDoacoes(cidade: str = None, item: str = None) -> str:
    """
        Retorna entidades ou organizações precisando de doações, quais items, urgência e quantidade.
        Parâmetros cidade e item são opcionais. O item deve ser informado no singular.
    """
    dfOccurences = pd.read_excel("/alvinbot/data/tables/Mock_Ocorrencias.xlsx", header=1)
    dfEntities = pd.read_excel("/alvinbot/data/tables/Mock_Entidades.xlsx", header=1)
    dfShelters = pd.read_excel("/alvinbot/data/tables/Mock_Abrigos.xlsx", header=1)
    dfDonationAsks = pd.read_excel("/alvinbot/data/tables/Mock_RequisicaoDeDoacoes.xlsx", header=1)

    df = dfOccurences[dfOccurences["DataFim"].isna()]
    df = df.merge(dfShelters[(dfShelters["DataTermino"].isna())], how='inner', left_on=['ID'],right_on=['IDOcorrencia'])
    df = df.merge(dfEntities, how='inner', left_on=['IDEntidade'],right_on=['ID'])
    if cidade:
        df = df[(df["Cidade"] == cidade)]

    df2 = dfDonationAsks[dfDonationAsks["DataRecebido"].isna()]
    df2 = df2.merge(df, how='inner', left_on=['IDAbrigo'],right_on=['ID_y'])
    if item:
        df2 = df2[(df2["Item"].str.contains(item))]
    df2 = df2[["Nome_y", "EndereçoLogradouro", "EndereçoNúmero", "EndereçoComplemento", "CEP", "Bairro", "Cidade", "Estado", "Telefone", "LotacaoAutorizada", "Categoria", "Item", "Quantidade", "Urgência"]]

    return df2.to_json()

@tool
def BuscarChavesPixCadastradas(cidade: str = None) -> str:
    """
        Retorna chaves pix válidas de entidades ou organizações cadastradas para receberem doações em dinheiro.
        Parâmetro cidade é opcional.
    """
    dfOccurences = pd.read_excel("/alvinbot/data/tables/Mock_Ocorrencias.xlsx", header=1)
    dfEntities = pd.read_excel("/alvinbot/data/tables/Mock_Entidades.xlsx", header=1)
    dfShelters = pd.read_excel("/alvinbot/data/tables/Mock_Abrigos.xlsx", header=1)
    dfDonationCenters = pd.read_excel("/alvinbot/data/tables/Mock_CentroDeDoacoes.xlsx", header=1)

    df = dfOccurences[dfOccurences["DataFim"].isna()]
    dfShelters = df.merge(dfShelters[(dfShelters["DataTermino"].isna())], how='inner', left_on=['ID'],right_on=['IDOcorrencia'])[["IDEntidade", "ChavePix"]]
    dfDonationCenters = df.merge(dfDonationCenters[(dfDonationCenters["DataTermino"].isna())], how='inner', left_on=['ID'],right_on=['IDOcorrencia'])[["IDEntidade", "ChavePix"]]

    df = pd.concat([dfShelters, dfDonationCenters])
    df = (df[~df["ChavePix"].isna()]).merge(dfEntities, how='inner', left_on=['IDEntidade'],right_on=['ID'])[["Nome", "ChavePix", "EndereçoLogradouro", "EndereçoNúmero", "EndereçoComplemento", "CEP", "Bairro", "Cidade", "Estado", "Telefone", "AreaDeAtuacao"]]

    if cidade:
        df = df[(df["Cidade"] == cidade)]

    return df.to_json()

@tool
def VerificarValidadeDeChavePix(chave_pix: str) -> str:
  """
    Verifica se a chave pix informada pelo usuário existe e qual a entidade que a cadastrou.
  """
  dfOccurences = pd.read_excel("/alvinbot/data/tables/Mock_Ocorrencias.xlsx", header=1)
  dfEntities = pd.read_excel("/alvinbot/data/tables/Mock_Entidades.xlsx", header=1)
  dfShelters = pd.read_excel("/alvinbot/data/tables/Mock_Abrigos.xlsx", header=1)
  dfDonationCenters = pd.read_excel("/alvinbot/data/tables/Mock_CentroDeDoacoes.xlsx", header=1)

  df = dfOccurences[dfOccurences["DataFim"].isna()]
  dfShelters = df.merge(dfShelters[(dfShelters["DataTermino"].isna())], how='inner', left_on=['ID'],right_on=['IDOcorrencia'])[["IDEntidade", "ChavePix"]]
  dfDonationCenters = df.merge(dfDonationCenters[(dfDonationCenters["DataTermino"].isna())], how='inner', left_on=['ID'],right_on=['IDOcorrencia'])[["IDEntidade", "ChavePix"]]

  df = pd.concat([dfShelters, dfDonationCenters])
  df = df[(df["ChavePix"] == chave_pix)]

  return df.to_json() or "Chave pix não encontrada no banco de dados oficial"

