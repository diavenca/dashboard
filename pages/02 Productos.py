from datetime import date
import io

import streamlit as st

import pandas as pd

# Librerías propias
import sources.graph as gr
import sources.lectura_datos as lec

st.set_page_config(
    page_title='Análisis Productos', 
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


st.title('Productos')

st.markdown('**Seleccione el producto que desea analizar:**')

productos = df_stock.producto.to_list()
productos.append('- Seleccione un producto -')
productos.sort()

prod = st.selectbox(label='', options=productos, help = 'Escoja un Producto para el análisis')

df_sin_ventas_print = lec.leer_sin_ventas()
df_sin_ventas_print.columns = ['Código', 'Producto', 'Línea', 'Stock', 'Fecha Stock']
df_sin_ventas_print = df_sin_ventas_print.sort_values('Stock', ascending=False)

df_sin_ventas_print.set_index('Código', inplace=True)

st.markdown('''**Descargue un archivo Excel con la lista de Productos Sin Ventas:** 

Se trata de todos los productos que no se han vendido al menos desde el 2020.''')

with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    # Write each dataframe to a different worksheet.
    df_sin_ventas_print.to_excel(writer)

    # Close the Pandas Excel writer and output the Excel file to the buffer
    writer.save()

    st.download_button(
        label="Descargar Excel",
        data=buffer,
        file_name=f'productos_sin_ventas_{hoy}.xlsx',
        mime="application/vnd.ms-excel"
    )


if prod != '- Seleccione un producto -':
    df_ventas_prod = df_ventas.loc[df_ventas.producto.isin([prod]),:]

    if not df_ventas_prod.empty:

        df_ventas_prod = lec.leer_metricas(df_ventas_prod, ['mes_año', 'cod', 'producto']) 
        
        # metrica='monto_dolar'
        # titulo='Ventas en $'
        # columnas='producto:N'
        # graph1 = gr.graph_bars_cols(df_ventas_prod, metrica, titulo, columnas)
        # st.altair_chart(graph1, use_container_width=False)

        # metrica='cantidad'
        # titulo='Volumen de Ventas'
        # columnas='producto:N'
        # graph2 = gr.graph_bars_cols(df_ventas_prod, metrica, titulo, columnas)
        # st.altair_chart(graph2, use_container_width=False)

        # metrica='num'
        # titulo='N° de Facturas'
        # columnas='producto:N'
        # graph2 = gr.graph_bars_cols(df_ventas_prod, metrica, titulo, columnas)
        # st.altair_chart(graph2, use_container_width=False)


        st.markdown(f'**Ventas en $ {prod}**')
        metrica='monto_dolar'
        titulo='Ventas en $'
        color='goldgreen'

        graph1 = gr.graph_bars_text(df_ventas_prod, metrica, titulo, color)

        st.altair_chart(graph1, use_container_width=False)


        st.markdown(f'**Volumen de Ventas {prod}**')
        metrica='cantidad'
        titulo='Volumen de Ventas'
        color='purpleblue'

        graph2 = gr.graph_bars_text(df_ventas_prod, metrica, titulo, color)

        st.altair_chart(graph2, use_container_width=False)


        st.markdown(f'**Número de Facturas {prod}**')
        metrica='num'
        titulo='N° Facturas'
        color='yelloworangebrown'

        graph3 = gr.graph_bars_text(df_ventas_prod, metrica, titulo, color)

        st.altair_chart(graph3, use_container_width=False)

    else:
        st.error(f"No hay datos de ventas para {prod}")



