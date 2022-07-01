import streamlit as st

import pandas as pd


from datetime import date
import io

# Librerías propias
import sources.lectura_datos as lec
import sources.graph as gr
import sources.indispensables as ind

#from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode

st.set_page_config(
    page_title='Productos Indispensables', 
    page_icon=':bar_chart:', 
    layout="centered", 
    initial_sidebar_state="auto", 
    menu_items={
         'Get Help': None,
         'Report a bug': None,
         'About': '''## Reporte de Ventas de Diavenca 
         
         Aplicación hecha por Diana Chacón Ocariz'''
     }
)

# Lectura de datos
buffer = io.BytesIO()
hoy = date.today()
df_ventas = lec.leer_ventas()
df_stock = lec.leer_stock()

st.title('Productos Indispensables')
st.markdown('**Producto Indispensable:** Producto que se vende regularmente, al menos el 75% del tiempo del período estudiado. Producto que no puede faltar.')

st.markdown('**Seleccione uno o varios años para analizar:**')

años = [2021, 2022, 'Todo']

año_ind = st.multiselect(label='', options=años, default='Todo', help = 'Escoja un año para el análisis')

if año_ind==['Todo'] or not año_ind:
    df_ventas_año = df_ventas.loc[:,['fecha', 'cod', 'producto', 'cantidad', 'monto_dolar', 'num', 'mes_año', 'año']]
else:
    df_ventas_año = df_ventas.loc[df_ventas.año.isin(año_ind),['fecha', 'cod', 'producto', 'cantidad', 'monto_dolar', 'num', 'mes_año', 'año']]


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

with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    # Write each dataframe to a different worksheet.
    df_indispensables_print.to_excel(writer)

    # Close the Pandas Excel writer and output the Excel file to the buffer
    writer.save()

    st.download_button(
        label="Descargar Excel",
        data=buffer,
        file_name=f'productos_indispensables_{hoy}.xlsx',
        mime="application/vnd.ms-excel"
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

    






