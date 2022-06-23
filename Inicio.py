# Carga de librerías

import streamlit as st

import pandas as pd

# Librerías propias
import sources.graph as gr
import sources.lectura_datos as lec

# Lectura de datos

df_ventas = lec.leer_ventas()

st.title('Resumen de Ventas Diavenca')

st.markdown('**Seleccione uno o varios años para analizar:**')

años = [2020, 2021, 2022, 'Todo']

año = st.multiselect(label='', options=años, default='Todo', help = 'Escoja un año para el análisis')

if año==['Todo'] or not año:
    df_ventas_año = df_ventas.loc[:,['fecha', 'cantidad', 'monto_dolar', 'num', 'mes_año', 'año', 'tipo']]
else:
    df_ventas_año = df_ventas.loc[df_ventas.año.isin(año),['fecha', 'cantidad', 'monto_dolar', 'num', 'mes_año', 'año', 'tipo']]

# Dataframes para los gráficos y métricas

fecha_min = df_ventas_año.fecha.min().strftime("%d/%m/%Y")
fecha_max = df_ventas_año.fecha.max().strftime("%d/%m/%Y")

df_ventas_mes = lec.leer_metricas(df_ventas_año, 'mes_año') 
df_volum = df_ventas_mes.query('mes_año > "2020-12"')
df_ventas_dia = lec.leer_metricas(df_ventas_año, 'fecha')
df_ventas_tipo = lec.leer_metricas(df_ventas_año, 'tipo')   

# Métricas
ventas_dol = round(df_ventas_año.monto_dolar.sum(),2)
vol_ventas = round(df_ventas_año.cantidad.sum(),2)
n_fact = round(df_ventas_año.num.nunique(),2)

# Medias de las métricas
ventas_dol_med = round(df_ventas_dia.monto_dolar.mean(),2)
vol_ventas_med = round(df_ventas_dia.cantidad.mean(),2)
n_fact_med = round(df_ventas_dia.num.mean(),2)

# Métricas por tipo de venta
ventas_dol_fa = round(df_ventas_tipo.query('tipo=="fa"').monto_dolar.sum(),2)
vol_ventas_fa = round(df_ventas_tipo.query('tipo=="fa"').cantidad.sum(),2)
n_fact_fa = df_ventas_tipo.query('tipo=="fa"').num

ventas_dol_ne = round(df_ventas_tipo.query('tipo=="ne"').monto_dolar.sum(),2)
vol_ventas_ne = round(df_ventas_tipo.query('tipo=="ne"').cantidad.sum(),2)
n_fact_ne = df_ventas_tipo.query('tipo=="ne"').num


st.subheader(f'Período de estudio del {fecha_min} al {fecha_max}')

col1, col2, col3 = st.columns((1,1,1))
col1.metric('Ventas en $', ventas_dol)
col2.metric('Volumen de Ventas', vol_ventas)
col3.metric('N° de Facturas', n_fact)


st.subheader('Evolución de las ventas en el tiempo')
st.markdown('Escoja el período que desea estudiar. Haga zoom sobre el período para ver más detalles')
gr_ts = gr.graph_time_serie(df_ventas_dia)
st.plotly_chart(gr_ts, use_container_width=False)


st.subheader('Promedios diarios')
col1, col2, col3 = st.columns((1,1,1))
col1.metric('Ventas en $', ventas_dol_med)
col2.metric('Volumen de Ventas', vol_ventas_med)
col3.metric('N° de Facturas', n_fact_med)

st.subheader('Ventas en $')
metrica='monto_dolar'
titulo='Ventas en $'
color='goldgreen'

graph1 = gr.graph_bars_text(df_ventas_mes, metrica, titulo, color)

st.altair_chart(graph1, use_container_width=False)


st.subheader('Volumen de Ventas')
metrica='cantidad'
titulo='Volumen de Ventas'
color='purpleblue'

graph2 = gr.graph_bars_text(df_volum, metrica, titulo, color)

st.altair_chart(graph2, use_container_width=False)


st.subheader('Número de Facturas')
metrica='num'
titulo='N° Facturas'
color='yelloworangebrown'

graph3 = gr.graph_bars_text(df_ventas_mes, metrica, titulo, color)

st.altair_chart(graph3, use_container_width=False)


st.subheader('Métricas por Tipo de Venta')
st.markdown('**Faturas**')
col12, col22, col32 = st.columns((1,1,1))
col12.metric('Ventas en $ Facturas', ventas_dol_fa)
col22.metric('Volumen de Ventas Facturas', vol_ventas_fa)
col32.metric('N° de Facturas', n_fact_fa)

st.markdown('**Notas de Entrega**')
col13, col23, col33 = st.columns((1,1,1))
col13.metric('Ventas en $ Notas de Entrega', ventas_dol_ne)
col23.metric('Volumen de Ventas Notas de Entrega', vol_ventas_ne)
col33.metric('N° de Notas de Entrega', n_fact_ne)

