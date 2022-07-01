import streamlit as st

import pandas as pd

# Librerías propias
import sources.graph as gr
import sources.lectura_datos as lec

st.set_page_config(
    page_title='Rendimiento Vendedores', 
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
df_ventas = lec.leer_ventas()

st.title('Vendedores')

st.markdown('**Seleccione uno o varios años para analizar:**')

años = [2020, 2021, 2022, 'Todo']

año_vend = st.multiselect(label='', options=años, default='Todo', help = 'Escoja un año para el análisis')

if año_vend==['Todo'] or not año_vend:
    df_ventas_año = df_ventas.loc[:,['fecha', 'vendedor', 'cantidad', 'monto_dolar', 'num', 'mes_año', 'año']]
else:
    df_ventas_año = df_ventas.loc[df_ventas.año.isin(año_vend),['fecha', 'vendedor', 'cantidad', 'monto_dolar', 'num', 'mes_año', 'año']]


df_vendedor = lec.leer_metricas(df_ventas_año, 'vendedor') 

df_vendedor_print = df_vendedor.loc[:,['vendedor', 'monto_dolar', 'cantidad', 'num']]
df_vendedor_print.columns = ['Vendedor', 'Ventas en $', 'Volumen de Ventas', 'N° Facturas']

st.subheader('Resumen de las métricas de los vendedores para el período seleccionado')
st.markdown('**Seleccione un vendedor para ver el detalle:**')

df = gr.graph_table_select(df_vendedor_print)

st.markdown('**Comparativo de Ventas Mensuales en $ por Vendedor**')

df_ventas_comp = lec.leer_metricas(df_ventas_año, ['mes_año', 'vendedor']) 
metrica='monto_dolar'
titulo='Ventas en $'
met_col='vendedor'

graph_line = gr.graph_lines(df_ventas_comp, metrica, titulo, met_col)

st.altair_chart(graph_line, use_container_width=False)


if not df.empty :

    vend_selected = df['Vendedor'].to_list()

    df_ventas_vend = df_ventas_año.loc[df_ventas_año.vendedor.isin(vend_selected),['fecha', 'vendedor', 'cantidad', 'monto_dolar', 'num', 'mes_año']]

    df_ventas_mes = lec.leer_metricas(df_ventas_vend, ['mes_año', 'vendedor']) 


    st.subheader(f'Ventas en $ para el Vendedor {vend_selected[0]}')
    metrica='monto_dolar'
    titulo='Ventas en $'
    color='goldgreen'

    graph1 = gr.graph_bars_text(df_ventas_mes, metrica, titulo, color)

    st.altair_chart(graph1, use_container_width=False)


    st.subheader(f'Volumen de Ventas para el Vendedor {vend_selected[0]}')
    metrica='cantidad'
    titulo='Volumen de Ventas'
    color='purpleblue'

    graph2 = gr.graph_bars_text(df_ventas_mes, metrica, titulo, color)

    st.altair_chart(graph2, use_container_width=False)


    st.subheader(f'Número de Facturas para el Vendedor {vend_selected[0]}')
    metrica='num'
    titulo='N° Facturas'
    color='yelloworangebrown'

    graph3 = gr.graph_bars_text(df_ventas_mes, metrica, titulo, color)

    st.altair_chart(graph3, use_container_width=False)

    


