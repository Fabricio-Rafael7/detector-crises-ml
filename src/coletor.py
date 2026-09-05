import pandas as pd
import yfinance as yf
from datetime import date

class ColetorFinanceiro:
    """
    Coleta os dados por meio da API do Yahoo
    """
    def __init__(self, ticker: str) -> None:
        """
        Inicializa o coletor com o código do ativo
        Parameters
        --------
        ticker: str
            É o ticker do ativo (ex: 'BRL=x' para Dólar)

        Returns
        -------
        None
        """
        self.__ticker = ticker
       
    def obter_dados_historicos(self, data_inicio: str, data_fim: str) -> pd.DataFrame:
        """
        Parameters
        -------
        data_inicio: str
            Data no formato AAAA-MM-DD
        data_fim: str
            Data no formato AAAA-MM-DD

        Raises
        ------
        ValueError: A tabela selecionada está vazia | A data selecionada é inválida
        Exception: Ocorreu um erro inesperado!

        Returns:
        tabela_fechamento: pd.Dataframe
            Dataframe do pandas somente com a coluna fechamento da tabela yfinance

        Example
        --------
        >>> coletor = ColetorFinanceiro("USDBRL=X")
        >>> coletor.obter_dados_historicos("2025-05-10", "2025-05-01")
        Traceback (most recent call last):
        ...
       ValueError: A data selecionada é inválida!
        >>> coletor.obter_dados_historicos("2300-05-10", "2300-05-11")
        Traceback (most recent call last):
        ...
        ValueError: A data selecionada é inválida!
        """
        
        if date.fromisoformat(data_inicio) > date.fromisoformat(data_fim) or date.fromisoformat(data_inicio) > date.today() or date.fromisoformat(data_fim) > date.today():
            # Se data for absurda
            raise ValueError("A data selecionada é inválida!")
      
        try:
            # Carrega os dados nas categorias e períodos desejados.
            tabela = yf.download(self.__ticker, start=data_inicio, end=data_fim)
                                    
        except Exception as erro:
            # Caso tenho ocorrido um erro não previsto
            raise Exception(f"Ocorreu um erro inesperado! {erro}")

        if tabela.empty:
            # Se tiver vazia retorna um erro
            raise ValueError("A tabela selecionada está vazia")
                    
        else:                    
            # Seleciona somenta a coluna na qual mostra os favores no fechamento da bolsa
            tabela_fechamento = tabela[['Close']]
            return tabela_fechamento
                
if __name__ == "__main__":
    coletor = ColetorFinanceiro("USDBRL=x")

    df_cotacoes = coletor.obter_dados_historicos("2025-05-05", "2025-05-10")

    # Verifica se o ticker possui alguma linha no periodo selecionado
    if df_cotacoes is not None:
        print("Tipo do dado retornado", type(df_cotacoes))
        print(df_cotacoes.head())