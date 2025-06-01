import streamlit as st
import pandas as pd
from datetime import datetime, date
from funcoes import salvar_agendamento, carregar_dados

st.set_page_config(page_title="Agendamento de Exames", layout="centered")
st.title("📋 Agendamento de Exames Médicos")
df = carregar_dados()

# Formulário
st.header("➕ Novo Agendamento")
with st.form("form_agendamento"):
    nome = st.text_input("Nome do paciente").upper()
    exame = st.selectbox("Exame", ["ECG", "Raio X", "Mamografia", "Laboratório", "USG", "Endoscopia"])
    data_agendada = st.date_input("Data desejada para o exame", min_value=date.today())
    enviar = st.form_submit_button("Salvar Agendamento")

    if enviar:  
      nome_valido = nome.strip() != ""  
      data_valida = data_agendada >= date.today()  
      exame_valido = exame.strip() != ""  

      if not nome_valido:  
        st.error("⚠️ Informe o nome do paciente.")  
      elif not exame_valido:  
        st.error("⚠️ Selecione um exame.")  
      elif not data_valida:  
        st.error("⚠️ Não é permitido agendar para datas passadas.")  
      else:  
        nome_norm = nome.strip().lower()  
        exame_norm = exame.strip().lower()  

        if not df.empty:  
          df["Data_Agendada"] = pd.to_datetime(df["Data_Agendada"], errors="coerce")  
          df["Nome_Normalizado"] = df["Nome"].str.strip().str.lower()  
          df["Exame_Normalizado"] = df["Exame"].str.strip().str.lower()  

          # Usando filter + lambda para buscar conflitos (nome + exame + data)
          conflito = list(filter(lambda row: 
            row["Nome_Normalizado"] == nome_norm and 
            row["Exame_Normalizado"] == exame_norm and 
            row["Data_Agendada"].date() == data_agendada, df.to_dict("records")))

          if conflito:  
            st.warning("⚠️ Este paciente já possui este exame agendado para esta data.")  
          else:  
            #Verifica se já existem 5 agendamentos na mesma data
            agendamentos_do_dia = df[df["Data_Agendada"].dt.date == data_agendada]

            if len(agendamentos_do_dia) >= 5:  
              st.warning("⚠️ Limite de 5 agendamentos atingido para esta data. Escolha outro dia.")  
            else: 
              # Primeiro agendamento do sistema 
              try:  
                salvar_agendamento(nome.strip(), exame, data_agendada)  
                st.success(f"✅ Agendamento salvo com sucesso em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")  
              except Exception as e:  
                st.error(f"Erro ao salvar: {e}")  
        else:  
            # Nenhum dado ainda, pode agendar  
            try:  
              salvar_agendamento(nome.strip(), exame, data_agendada)  
              st.success(f"✅ Agendamento salvo com sucesso em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")  
            except Exception as e:  
              st.error(f"Erro ao salvar: {e}")  





# Exibir agendamentos salvos
st.header("📅 Agendamentos Registrados")
df = carregar_dados()
df["Data_Agendada"] = pd.to_datetime(df["Data_Agendada"], errors="coerce")
data_filtro = st.date_input("🔍 Filtrar por data agendada", value=date.today())

#data_filtro = st.date_input("🔍 Filtrar por data agendada", value=date.today())
# Filtrar os dados
#filtrados = df[df["Data_Agendada"].dt.date == data_filtro]

filtrados = pd.DataFrame([
linha for _, linha in df.iterrows()
if linha["Data_Agendada"].date() == data_filtro])

# Exibir resultados
st.subheader(f"📆 Agendamentos em {data_filtro.strftime('%d/%m/%Y')}")
if not filtrados.empty:
    st.dataframe(filtrados.drop(columns=["Nome_Normalizado", "Exame_Normalizado"], errors="ignore"))
else:
    st.info("Nenhum agendamento para a data selecionada.")

