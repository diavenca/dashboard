# Carga de librerías

import streamlit as st

import pandas as pd

# Librerías propias
import sources.carga as cr

st.set_page_config(
    page_title='Carga de Datos', 
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

st.title('Cargar Nuevos Datos')

st.subheader('Cargar Datos Ventas')

st.markdown('''Seleccione los archivos con los nuevos datos de las **Ventas**.

Son 2 archivos:
- Facturas (el nombre debe comenzar por "fa")
- Notas de Entrega (el nombre debe comenzar por "ne". Recuerde convertir los montos que están en COP)

Recuerde buscar los reportes en el Profit, que sean las ventas a partir de la última fecha y guardar los reportes como **Excel Solo Datos**.

Estas son las fechas de las últimas ventas guardadas:
''')

df_ultimos = cr.leer_fechas()
df_ultimos.columns=['N° Factura', 'Fecha', 'Tipo de Venta']

st.write(df_ultimos)

files = st.file_uploader('Cargar Archivos Ventas', type=['xls'], key='up_ventas', accept_multiple_files=True, help='Cargue los archivos con las últimas ventas')

if files:

    if st.button('Procesar Datos', key='pr_ventas'):

        for file in files:

            if  cr.tratar_ventas(file):
                st.success(f"Los datos del archivo {file} han sido integrados exitosamente")
            else:
                st.error(f"Los datos del archivo {file} ya han sido integrados")


st.subheader('Cargar Datos Stock')

st.markdown('Seleccione el archivo con los datos del **Stock**.')


files = st.file_uploader('Cargar Archivo Stock', type=['xls'], key='up_stock', accept_multiple_files=True, help='Cargue los archivos con las últimas ventas')

if files:

    if st.button('Procesar Datos', key='pr_stock'):

        for file in files:

            if  cr.tratar_stock(file):
                st.success(f"Los datos del archivo {file} han sido integrados exitosamente")
            else:
                st.error(f"Los datos del archivo {file} ya han sido integrados")

