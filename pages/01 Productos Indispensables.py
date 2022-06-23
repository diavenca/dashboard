import streamlit as st

import pandas as pd

from pathlib import Path
from datetime import date

# Librerías propias
import sources.lectura_datos as lec
import sources.graph as gr
import sources.indispensables as ind

#from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode

# Lectura de datos
BASE_DIR = Path.cwd()
hoy = date.today()
df_ventas = lec.leer_ventas()
df_stock = lec.leer_stock()

st.title('Productos Indispensables')
st.markdown('**Producto Indispensable:** Producto que se vende regularmente, al menos el 75% del tiempo del período estudiado. Producto que no puede faltar.')

st.markdown('**Seleccione uno o varios años para analizar:**')

años = [2021, 2022, 'Todo']

año = st.multiselect(label='', options=años, default='Todo', help = 'Escoja un año para el análisis')

if año==['Todo'] or not año:
    df_ventas_año = df_ventas.loc[:,['fecha', 'cod', 'producto', 'cantidad', 'monto_dolar', 'num', 'mes_año', 'año']]
else:
    df_ventas_año = df_ventas.loc[df_ventas.año.isin(año),['fecha', 'cod', 'producto', 'cantidad', 'monto_dolar', 'num', 'mes_año', 'año']]


fecha_max = df_stock.fecha_stock.max().strftime("%d/%m/%Y")

df_ventas_prod_mes = ind.ventas_prod_mes(df_ventas_año)

df_indispensables = ind.productos_indispensables(df_ventas_prod_mes, df_stock)

df_ventas_indis = ind.ventas_prod_indis(df_ventas_año, df_indispensables)

df_indispensables_print = df_indispensables.copy()
df_indispensables_print.columns = ['Código', 'Producto', 'Stock', 'Promedio Ventas', 'Faltante']
df_indispensables_print = df_indispensables_print.sort_values('Faltante', ascending=True)


col1, col2, col3 = st.columns((1,1,1))
col2.metric('Fecha del Inventario', fecha_max)

st.markdown('**Seleccione uno o varios productos para ver su evolución en el tiempo:**')
df = gr.graph_table_select(df_indispensables_print)

df_indispensables_print.set_index('Código', inplace=True)

df_indispensables_print.to_excel(f"{BASE_DIR / 'data/out/productos_indispensables.xlsx'}")

st.markdown('**Descargue un archivo Excel con la lista de Productos Indispensables:**')
with open("{BASE_DIR / 'data/out/productos_indispensables.xlsx'}", 'rb') as xlsx:
    st.download_button(
        label="Descargar Excel",
        data=xlsx,
        file_name=f'productos_indispensables_{hoy}.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

if not df.empty :

    prod_selected = df['Código'].to_list()

    df_indis = df_ventas_indis.loc[df_ventas_indis.cod.isin(prod_selected),:]

    df_indis = lec.leer_metricas(df_indis, ['mes_año', 'cod', 'producto']) 

    metrica='monto_dolar'
    titulo='Ventas en $'
    columnas='producto:N'
    graph1 = gr.graph_bars_cols(df_indis, metrica, titulo, columnas)
    st.altair_chart(graph1, use_container_width=False)

    metrica='cantidad'
    titulo='Volumen de Ventas'
    columnas='producto:N'
    graph2 = gr.graph_bars_cols(df_indis, metrica, titulo, columnas)
    st.altair_chart(graph2, use_container_width=False)

    metrica='num'
    titulo='N° de Facturas'
    columnas='producto:N'
    graph2 = gr.graph_bars_cols(df_indis, metrica, titulo, columnas)
    st.altair_chart(graph2, use_container_width=False)

    






