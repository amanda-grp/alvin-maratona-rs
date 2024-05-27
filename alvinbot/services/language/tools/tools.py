from alvinbot.services.language.tools.donations_search import BuscarAbrigosPrecisandoDeDoacoes, BuscarChavesPixCadastradas, VerificarValidadeDeChavePix
from alvinbot.services.language.tools.shelthers_search import BuscarListaDeAbrigosCadastrados, BuscarListaDeAbrigosParaMulheresECriancasApenas

def get_all_available_tools() -> list:
    """
        Returns a list o tools (such as API and database requests, and other functions) available
        to the LLM model.
    """
    return [
        BuscarListaDeAbrigosCadastrados,
        BuscarListaDeAbrigosParaMulheresECriancasApenas,
        BuscarAbrigosPrecisandoDeDoacoes,
        BuscarChavesPixCadastradas,
        VerificarValidadeDeChavePix
    ]

def get_tool_map() -> dict:
    return {tool.name: tool for tool in get_all_available_tools()}