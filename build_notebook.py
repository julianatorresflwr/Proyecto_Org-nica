import json
import os

notebook_content = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Análisis Gráfico: Proyecto de Química Orgánica\n",
    "\n",
    "Este análisis fue ajustado para manejar campos vacíos en el dataset original y eliminar errores atípicos (outliers). "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import numpy as np\n",
    "import plotly.express as px\n",
    "import plotly.graph_objects as go\n",
    "import plotly.io as pio\n",
    "\n",
    "pio.templates.default = \"plotly_white\""
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Carga de Datos y Limpieza de Errores Tipográficos"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "archivo_excel = 'Proyecto reacciones qu\u00edmica v.1.xlsx'\n",
    "df = pd.read_excel(archivo_excel)\n",
    "\n",
    "cols_numericas = [\n",
    "    'Peso molecular sustrato (g/mol)', 'Punto de ebullici\u00f3n sustrato (\u00b0C)',\n",
    "    'Densidad sustrato (g/mL)', 'pKa sustrato', 'LD50 sustrato (mg/kg)',\n",
    "    'Peso molecular producto (g/mol)', 'Punto de ebullici\u00f3n producto (\u00b0C)',\n",
    "    'Densidad producto (g/mL)', 'pKa producto', 'LD50 producto (mg/kg)'\n",
    "]\n",
    "\n",
    "# Convertimos valores problemáticos\n",
    "for col in cols_numericas:\n",
    "    if col in df.columns:\n",
    "        df[col] = pd.to_numeric(df[col], errors='coerce')\n",
    "\n",
    "# Eliminamos datos extremos causados por errores tipográficos en el Excel (Ej. valores de 91000 °C)\n",
    "df.loc[df['Punto de ebullici\u00f3n sustrato (\u00b0C)'] > 1000, 'Punto de ebullici\u00f3n sustrato (\u00b0C)'] = np.nan\n",
    "\n",
    "display(df.head())"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Gráfico 1: Conteo por Función Química (La columna original 'Tipo de reacción' estaba vacía)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "conteo = df['Funci\u00f3n qu\u00edmica'].value_counts().reset_index()\n",
    "conteo.columns = ['Funci\u00f3n qu\u00edmica', 'Frecuencia']\n",
    "\n",
    "fig1 = px.bar(\n",
    "    conteo,\n",
    "    x='Funci\u00f3n qu\u00edmica',\n",
    "    y='Frecuencia',\n",
    "    title='1. Frecuencia de los sustratos por Función Química',\n",
    "    labels={'Frecuencia': 'Cantidad observada', 'Funci\u00f3n qu\u00edmica': 'Función Química'},\n",
    "    color='Frecuencia',\n",
    "    color_continuous_scale=px.colors.sequential.Viridis\n",
    ")\n",
    "fig1.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Gr\u00e1fico 2: Peso Molecular vs Punto de Ebullici\u00f3n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "fig2 = px.scatter(\n",
    "    df,\n",
    "    x='Peso molecular sustrato (g/mol)',\n",
    "    y='Punto de ebullici\u00f3n sustrato (\u00b0C)',\n",
    "    color='Grupo funcional',\n",
    "    hover_data=['Nombre del sustrato', 'Nombre de la reacci\u00f3n'],\n",
    "    title='2. Relaci\u00f3n: Peso Molecular vs Punto de Ebullici\u00f3n (Sustratos)'\n",
    ")\n",
    "\n",
    "df_limpio = df.dropna(subset=['Peso molecular sustrato (g/mol)', 'Punto de ebullici\u00f3n sustrato (\u00b0C)'])\n",
    "if not df_limpio.empty:\n",
    "    z = np.polyfit(df_limpio['Peso molecular sustrato (g/mol)'], df_limpio['Punto de ebullici\u00f3n sustrato (\u00b0C)'], 1)\n",
    "    p = np.poly1d(z)\n",
    "    fig2.add_trace(go.Scatter(\n",
    "        x=df_limpio['Peso molecular sustrato (g/mol)'],\n",
    "        y=p(df_limpio['Peso molecular sustrato (g/mol)']),\n",
    "        mode='lines',\n",
    "        name='Tendencia Global',\n",
    "        line=dict(color='red', dash='dash')\n",
    "    ))\n",
    "\n",
    "fig2.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Gr\u00e1fico 3: Distribución de Ebullición"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "fig3 = px.box(\n",
    "    df,\n",
    "    x='Funci\u00f3n qu\u00edmica',\n",
    "    y='Punto de ebullici\u00f3n sustrato (\u00b0C)',\n",
    "    color='Funci\u00f3n qu\u00edmica',\n",
    "    title='3. Variabilidad del Punto de Ebullici\u00f3n seg\u00fan la Funci\u00f3n Qu\u00edmica',\n",
    "    points=\"all\"\n",
    ")\n",
    "fig3.update_layout(xaxis_tickangle=-45)\n",
    "fig3.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Gr\u00e1fico 4: Mapa de Calor de Correlaciones"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "df_numerico = df[cols_numericas]\n",
    "correlacion = df_numerico.corr()\n",
    "\n",
    "fig4 = px.imshow(\n",
    "    correlacion,\n",
    "    text_auto=\".2f\",\n",
    "    aspect=\"auto\",\n",
    "    title='4. Mapa de Correlaciones Anal\u00edticas entre Variables Num\u00e9ricas',\n",
    "    color_continuous_scale='RdBu_r',\n",
    "    zmin=-1, zmax=1\n",
    ")\n",
    "fig4.update_xaxes(tickangle=-45)\n",
    "fig4.show()"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.10"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}

with open('Proyecto_química_orgánica.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook_content, f, indent=1)

print("Notebook generado exitosamente.")
