from alvinbot.services.language.tools.donations_search import BuscarAbrigosPrecisandoDeDoacoes, BuscarChavesPixCadastradas, VerificarValidadeDeChavePix
from alvinbot.services.language.tools.shelthers_search import BuscarListaDeAbrigosCadastrados, BuscarListaDeAbrigosParaMulheresECriancasApenas
from alvinbot.services.language.tools.alerts_search import BuscarAlertasDePerigoParaAPopulacaoAtuais, BuscarAlertasDePerigoParaAPopulacaoExpirados

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
        VerificarValidadeDeChavePix,
        BuscarAlertasDePerigoParaAPopulacaoAtuais,
        BuscarAlertasDePerigoParaAPopulacaoExpirados
    ]
