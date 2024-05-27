from services.language.tools.donations_search import BuscarAbrigosPrecisandoDeDoacoes, BuscarChavesPixCadastradas, VerificarValidadeDeChavePix
from services.language.tools.shelthers_search import BuscarListaDeAbrigosCadastrados, BuscarListaDeAbrigosParaMulheresECriancasApenas
from services.language.tools.alerts_search import BuscarAlertasDePerigoParaAPopulacaoAtuais, BuscarAlertasDePerigoParaAPopulacaoExpirados

def get_all_available_tools() -> list:
    """
    Retorna uma lista de funcionalidades que o Alvin pode acessar, como consultas em banco de dados, consultas em API, entre disponíveis para o modelo LLM.
    """
    return [
        BuscarListaDeAbrigosCadastrados,
        BuscarListaDeAbrigosParaMulheresECriancasApenas,
        BuscarAbrigosPrecisandoDeDoacoes,
        BuscarChavesPixCadastradas,
        VerificarValidadeDeChavePix,
        BuscarAlertasDePerigoParaAPopulacaoAtuais,
        BuscarAlertasDePerigoParaAPopulacaoExpirados
    ]

def get_tool_map() -> dict:
    return {tool.name: tool for tool in get_all_available_tools()}
