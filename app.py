# dashboard_tarea_grupo_22.py

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Cargar datos
df = pd.read_csv('data.csv', parse_dates=['Date'])

# Título
st.title("Dashboard de Análisis de Ventas - Supermarket Sales")

# Sidebar - Filtros
st.sidebar.header("Filtros")
branch = st.sidebar.multiselect("Sucursal", df['Branch'].unique(), default=df['Branch'].unique())
product_line = st.sidebar.multiselect("Línea de Producto", df['Product line'].unique(), default=df['Product line'].unique())
customer_type = st.sidebar.radio("Tipo de Cliente", df['Customer type'].unique().tolist() + ['Todos'])

# Aplicar filtros
df_filtered = df[df['Branch'].isin(branch) & df['Product line'].isin(product_line)]
if customer_type != 'Todos':
    df_filtered = df_filtered[df_filtered['Customer type'] == customer_type]

# Evolución de Ventas Totales
st.subheader("Evolución de Ventas Totales")
sales_by_date = df_filtered.groupby("Date")["Total"].sum().reset_index()
fig, ax = plt.subplots()
sns.lineplot(data=sales_by_date, x="Date", y="Total", ax=ax)
ax.set_title("Ventas Totales por Fecha")
st.pyplot(fig)

# Ingresos por Línea de Producto
st.subheader("Ingresos por Línea de Producto")
sales_by_product = df_filtered.groupby("Product line")["Total"].sum().sort_values(ascending=False)
st.bar_chart(sales_by_product)

# Distribución de Calificación de Clientes
st.subheader("Distribución de Calificaciones de Clientes")
fig, ax = plt.subplots()
sns.histplot(df_filtered["Rating"], bins=10, kde=True, ax=ax)
st.pyplot(fig)

# Comparación del Gasto por Tipo de Cliente
st.subheader("Gasto Total por Tipo de Cliente")
fig, ax = plt.subplots()
sns.boxplot(data=df, x="Customer type", y="Total", ax=ax)
st.pyplot(fig)

# Relación entre Costo y Ganancia Bruta
st.subheader("Relación entre Costo y Ganancia Bruta")
fig, ax = plt.subplots()
sns.scatterplot(data=df_filtered, x="cogs", y="gross income", ax=ax)
st.pyplot(fig)

# Métodos de Pago Preferidos
st.subheader("Métodos de Pago Preferidos")
payment_counts = df_filtered["Payment"].value_counts()
fig, ax = plt.subplots()
ax.pie(payment_counts, labels=payment_counts.index, autopct='%1.1f%%')
ax.axis('equal')
st.pyplot(fig)

# Mapa de calor de correlación
st.subheader("Correlación entre Variables Numéricas")
corr = df_filtered[["Unit price", "Quantity", "Tax 5%", "Total", "cogs", "gross income", "Rating"]].corr()
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
st.pyplot(fig)

# Composición del Ingreso Bruto por Sucursal y Producto
st.subheader("Ingreso Bruto por Sucursal y Línea de Producto")
pivot = df.pivot_table(values="gross income", index="Product line", columns="Branch", aggfunc="sum")
fig, ax = plt.subplots()
sns.heatmap(pivot, annot=True, cmap="YlGnBu", ax=ax)
st.pyplot(fig)

# Parámetro: tamaño de los puntos en el gráfico 3D
st.sidebar.subheader("Parámetros del gráfico 3D")
# Parámetros adicionales para gráficos
st.sidebar.subheader("Visualización Avanzada")
num_top_clients = st.sidebar.slider("Cantidad de clientes más importantes", min_value=5, max_value=30, value=10)
point_size = st.sidebar.slider("Tamaño de los puntos", min_value=10, max_value=200, value=60)

# Top clientes por total de ventas
st.subheader(f"Top {num_top_clients} Clientes por Valor Total de Ventas")

top_customers = df_filtered.groupby("Customer ID")["Total"].sum().sort_values(ascending=False).head(num_top_clients)
fig, ax = plt.subplots()
top_customers.plot(kind="bar", ax=ax, color="skyblue")
ax.set_ylabel("Total de Ventas")
ax.set_xlabel("Customer ID")
ax.set_title(f"Top {num_top_clients} Clientes")
st.pyplot(fig)

# Gráfico 3D: Unit price vs Quantity vs Total
st.subheader("Visualización 3D: Precio Unitario, Cantidad y Total")

from mpl_toolkits.mplot3d import Axes3D  # Necesario para 3D
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

x = df_filtered["Unit price"]
y = df_filtered["Quantity"]
z = df_filtered["Total"]

scatter = ax.scatter(x, y, z, c=z, cmap='plasma', s=point_size, alpha=0.7)
ax.set_xlabel("Unit price")
ax.set_ylabel("Quantity")
ax.set_zlabel("Total")
ax.set_title("Gráfico 3D: Precio, Cantidad y Total")
fig.colorbar(scatter, ax=ax, shrink=0.5, aspect=5)

st.pyplot(fig)