# -*- coding: utf-8 -*-
"""webapp.py

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1PM3DxARt-ZQa7-ezWHl2gi1bJ_a6dRge
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Try to read existing CSV file or create new DataFrame
try:
    dados = pd.read_csv("compras.csv")
except:
    dados = pd.DataFrame({"produto": [], "preço": []})
    dados.to_csv("compras.csv", index=False)

# Display title and input for budget
st.title("Controlo de Gastos")
orcamento = st.number_input("Orçamento:", min_value=0.0)

# Calculate total spent so far
total = dados["preço"].sum() if not dados.empty else 0

# Form for adding new purchase
with st.form("nova_compra"):
    produto = st.text_input("Produto:")
    preco = st.number_input("Preço:", min_value=0.0)

    # Submit button for adding the purchase
    if st.form_submit_button("Adicionar"):
        if preco <= (orcamento - total):  # Check if there's enough budget
            nova_linha = pd.DataFrame({"produto": [produto], "preço": [preco]})
            dados = pd.concat([dados, nova_linha], ignore_index=True)
            dados.to_csv("compras.csv", index=False)
            st.success("Compra adicionada!")
        else:
            st.error("Sem orçamento suficiente!")

# If budget is set, create donut chart
if orcamento > 0:
    # Create Donut Chart
    fig, ax = plt.subplots(figsize=(8, 8))
    if not dados.empty:
        produtos = dados["produto"].tolist()
        valores = dados["preço"].tolist()
        restante = orcamento - total
        if restante > 0:
            produtos.append("Disponível")
            valores.append(restante)

        ax.pie(valores, labels=produtos, autopct='%1.1f%%', pctdistance=0.85)
        ax.set_title(f"Orçamento: {orcamento}€")

        # Create circular "donut" shape
        centro = plt.Circle((0, 0), 0.70, fc='white')
        ax.add_artist(centro)

    # Display the donut chart and the table
    st.pyplot(fig)

# Show the DataFrame and financial summary
st.dataframe(dados)
st.write(f"Total gasto: {total}€")
st.write(f"Restante: {orcamento - total}€")