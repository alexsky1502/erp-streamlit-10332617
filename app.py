# Fluxo de Caixa por Mês: Gráfico de linha ou de barras mostrando a receita e despesa ao longo dos meses
# Distribuição das Contas a Pagar por Fornecedor: Gráfico de pizza ou barras mostrando os principais fornecedores e os valores devidos.
# Status das Contas a Pagar e Receber: Gráfico de barras mostrando o total de contas "Pendentes" vs "Pagas/Recebidas"
# Top 5 Clientes com Maior Receita: Tabela e gráfico de barras mostrando os clientes que mais geram receita
# Comparação Receita vs Despesa (Gráfico de Barras): Comparação entre total de receitas e despesas do mês atual.
# Previsão de Fluxo de Caixa: Exibir contas a pagar e receber nos próximos 30 dias para estimar saldo futuro.

import streamlit as st
import pandas as pd
import sqlite3
from faker import Faker
import matplotlib.pyplot as plt
import seaborn as sns

# Interface Streamlit
def main():
    st.title("ERP Financeiro com Streamlit")
    
    menu = ["Clientes", "Contas a Pagar", "Contas a Receber", "Lançamentos", "Relatórios", "Status Contas"]
    choice = st.sidebar.selectbox("Selecione uma opção", menu)
    conn = sqlite3.connect("erp_finance.db", detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = conn.cursor()
    
    if choice == "Clientes":
        st.subheader("Cadastro de Clientes")
        df = pd.read_sql_query("SELECT * FROM clientes", conn)
        st.dataframe(df)
        
    elif choice == "Contas a Pagar":
        st.subheader("Contas a Pagar")
        df = pd.read_sql_query("SELECT * FROM contas_pagar", conn)
        st.dataframe(df)
        st.subheader("Distribuição das Contas a Pagar por Fornecedor")
        query = "SELECT fornecedor, SUM(valor) as total FROM contas_pagar GROUP BY fornecedor"
        df = pd.read_sql_query(query, conn)
        st.dataframe(df)
    
        if not df.empty:
            fig, ax = plt.subplots()
            ax.pie(df['total'], labels=df['fornecedor'], autopct='%1.1f%%', startangle=90)
            ax.axis('equal')  # Deixar o gráfico circular
            st.pyplot(fig)
        else:
            st.write("Nenhum dado disponível.")
    elif choice == "Contas a Receber":
        st.subheader("Contas a Receber")
        df = pd.read_sql_query("SELECT * FROM contas_receber", conn)
        st.dataframe(df)

    elif choice == "Lançamentos":
        st.subheader("Lançamentos Financeiros")
        df = pd.read_sql_query("SELECT * FROM lancamentos", conn)
        st.dataframe(df)
        
    elif choice == "Relatórios":
        st.subheader("Relatório de Fluxo de Caixa")
        df = pd.read_sql_query("SELECT tipo, SUM(valor) as total FROM lancamentos GROUP BY tipo", conn)
        st.dataframe(df)
    ##############################################################################################################
        st.subheader("Fluxo de Caixa por Mês")
        query = "SELECT strftime('%Y-%m', data) AS mes, tipo, SUM(valor) as total FROM lancamentos GROUP BY mes, tipo"
        df = pd.read_sql_query(query, conn)
        
        if not df.empty:
            df_pivot = df.pivot(index='mes', columns='tipo', values='total').fillna(0)
            st.line_chart(df_pivot)
        else:
            st.write("Nenhum dado disponível.")
    
    elif choice == "Status Contas":
        st.subheader("Status das Contas a Pagar e Receber")
        query = """
            SELECT status, COUNT(*) as total FROM (
                SELECT status FROM contas_pagar 
                UNION ALL
                SELECT status FROM contas_receber
            ) GROUP BY status
        """
        df = pd.read_sql_query(query, conn)
        
        if not df.empty:
            fig, ax = plt.subplots()
            sns.barplot(x='status', y='total', data=df, ax=ax)
            st.pyplot(fig)
        else:
            st.write("Nenhum dado disponível.")
    
    conn.close()
    
if __name__ == "__main__":
    main()
