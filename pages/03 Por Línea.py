import streamlit as st

import pandas as pd

from pathlib import Path
from datetime import date

# Librerías propias
import sources.graph as gr
import sources.lectura_datos as lec


# Lectura de datos
BASE_DIR = Path.cwd()
hoy = date.today()
df_ventas = lec.leer_ventas()
df_stock = lec.leer_stock()

# Solo tenemos detalles de ventas a partir de 2021
df_linea_prod = df_ventas.query('fecha > "2020-12-31"').loc[:,['fecha', 'cod', 'producto', 'cantidad', 'monto_dolar', 'num', 'mes_año', 'año']]
df_linea_prod = pd.merge(df_linea_prod, df_stock, on=['cod', 'producto'], how='outer')
df_linea_prod.dropna(inplace=True)

st.title('Líneas de Producto')

st.markdown('**Seleccione uno o varios años para analizar:**')

años = [2021, 2022, 'Todo']

año = st.multiselect(label='', options=años, default='Todo', help = 'Escoja un año para el análisis')

if año==['Todo'] or not año:
    df_ventas_año = df_linea_prod.loc[:,['fecha', 'linea', 'cod', 'producto', 'cantidad', 'monto_dolar', 'num', 'mes_año', 'año']]
else:
    df_ventas_año = df_linea_prod.loc[df_linea_prod.año.isin(año),['fecha', 'linea', 'cod', 'producto', 'cantidad', 'monto_dolar', 'num', 'mes_año', 'año']]



df_linea_met = lec.leer_metricas(df_ventas_año, 'linea') 

df_linea_met_print = df_linea_met.loc[:,['linea', 'monto_dolar', 'cantidad', 'num']]
df_linea_met_print.columns = ['Línea', 'Ventas en $', 'Volumen de Ventas', 'N° Facturas']
df_linea_met_print = df_linea_met_print.sort_values('Ventas en $', ascending=False)


st.subheader('Resumen de las métricas por Línea de Producto')
st.markdown('**Seleccione una o varias Líneas para ver el detalle:**')

df = gr.graph_table_select(df_linea_met_print)

df_linea_met_print.set_index('Línea', inplace=True)
df_linea_met_print.to_excel(f"{BASE_DIR / 'data/out/lineas_productos_{hoy}.xlsx'}")

st.markdown('**Descargue un archivo Excel con la lista de Líneas de Productos:**')
with open(f"{BASE_DIR / 'data/out/lineas_productos_{hoy}.xlsx'}", 'rb') as xlsx:
    st.download_button(
        label="Descargar Excel",
        data=xlsx,
        file_name='lineas_productos_{hoy}.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )


if not df.empty :

    linea_selected = df['Línea'].to_list()

    df_ventas_linea = df_ventas_año.loc[df_ventas_año.linea.isin(linea_selected),['fecha', 'linea', 'cantidad', 'monto_dolar', 'num', 'mes_año']]

    df_ventas_linea_mes = lec.leer_metricas(df_ventas_linea, ['mes_año', 'linea']) 

    st.markdown(f'**Ventas en $ {linea_selected}**')
    metrica='monto_dolar'
    titulo='Ventas en $'
    color='goldgreen'

    graph1 = gr.graph_bars_text(df_ventas_linea_mes, metrica, titulo, color)

    st.altair_chart(graph1, use_container_width=False)


    st.markdown(f'**Volumen de Ventas {linea_selected}**')
    metrica='cantidad'
    titulo='Volumen de Ventas'
    color='purpleblue'

    graph2 = gr.graph_bars_text(df_ventas_linea_mes, metrica, titulo, color)

    st.altair_chart(graph2, use_container_width=False)


    st.markdown(f'**Número de Facturas {linea_selected}**')
    metrica='num'
    titulo='N° Facturas'
    color='yelloworangebrown'

    graph3 = gr.graph_bars_text(df_ventas_linea_mes, metrica, titulo, color)

    st.altair_chart(graph3, use_container_width=False)


    # metrica='monto_dolar'
    # titulo='Ventas en $'
    # columnas='linea:N'

    # graph1 = gr.graph_bars_cols(df_ventas_linea_mes, metrica, titulo, columnas)

    # st.altair_chart(graph1, use_container_width=False)


    # metrica='cantidad'
    # titulo='Volumen de Ventas'
    # columnas='linea:N'

    # graph2 = gr.graph_bars_cols(df_ventas_linea_mes, metrica, titulo, columnas)

    # st.altair_chart(graph2, use_container_width=False)

    # metrica='num'
    # titulo='N° Facturas'
    # columnas='linea:N'

    # graph3 = gr.graph_bars_cols(df_ventas_linea_mes, metrica, titulo, columnas)

    # st.altair_chart(graph3, use_container_width=False)

    df_ventas_prod_linea = df_ventas_año.loc[df_ventas_año.linea.isin(linea_selected),['fecha', 'linea', 'cod', 'producto', 'cantidad', 'monto_dolar', 'num', 'mes_año']]

    df_ventas_prod_linea = lec.leer_metricas(df_ventas_prod_linea, ['linea', 'cod', 'producto']) 

    df_ventas_prod_linea_print = df_ventas_prod_linea.loc[:,['cod', 'producto', 'monto_dolar', 'cantidad', 'num']]
    df_ventas_prod_linea_print.columns = ['Código', 'Producto', 'Ventas en $', 'Volumen de Ventas', 'N° Facturas']
    df_ventas_prod_linea_print = df_ventas_prod_linea_print.sort_values('Ventas en $', ascending=False)

    st.subheader(f'Detalles ventas Productos de la Línea {linea_selected[0]}')
    df = gr.graph_table_select(df_ventas_prod_linea_print)

