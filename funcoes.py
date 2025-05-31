import pandas as pd
from datetime import datetime
ARQUIVO = "dados.csv"

def salvar_agendamento(nome, exame, data_agendada):
    """Salva o agendamento com a data agendada e o horário exato de registro"""
    if not nome or not str(nome).strip():
      raise ValueError("Nome do paciente inválido.")
    if not exame:
      raise ValueError("Exame não informado.")
    if not data_agendada:
      raise ValueError("Data do exame não informada.")
    
    registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    novo = pd.DataFrame([[nome, exame, data_agendada.strftime("%Y-%m-%d"), registro]],
    columns=["Nome", "Exame", "Data_Agendada", "Data_Registro"])
    
    try:
        dados = pd.read_csv(ARQUIVO)
        dados = pd.concat([dados, novo], ignore_index=True)
    except FileNotFoundError:
        dados = novo
    dados.to_csv(ARQUIVO, index=False)

def carregar_dados():
    """Carrega os agendamentos salvos"""
    try:
        df = pd.read_csv(ARQUIVO)
        df["Data_Agendada"] = pd.to_datetime(df["Data_Agendada"])
        df["Data_Registro"] = pd.to_datetime(df["Data_Registro"])
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=["Nome", "Exame", "Data_Agendada", "Data_Registro"])
