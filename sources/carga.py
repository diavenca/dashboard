import pandas as pd

import sources.bd as bd
import sources.carga_ventas as cv
import sources.carga_stock as cs
import sources.carga_tasa_dolar as cd
import sources.email as em

import streamlit as st

def leer_fechas():

    conn = bd.conectarse()
    query = f'SELECT max(max_num), max(max_fecha), tipo FROM control GROUP BY tipo '

    df_ultimos = pd.read_sql_query(query, conn)

    bd.desconectarse(conn)

    return df_ultimos


def tratar_ventas(file):

    result_ok = False

    cd.actualizar_dolar()

    df = cv.read_files(file, 'tipo', 2)

    df = cv.seleccionar_cols(df)

    df = cv.construir_df(df)

    if not cv.probar_existencia(df):

        df = cv.transformar(df)

        df = cv.calcular_monto_dolar(df)

        cv.guardar_datos_bd(df)

        #em.enviar_correo('diavenca.cm@gmail.com', 'diavenca.cm@gmail.com', titulo='Archivo Ventas', file=file)

        result_ok = True

    return result_ok

def tratar_stock(file):

    result_ok = False

    df = cs.read_files(file)
    df = cs.transformar_stock(df)
    cs.guardar_datos_bd(df)

    #st.write(file.name)

    #em.enviar_correo('diavenca.cm@gmail.com', 'diavenca.cm@gmail.com', asunto='Archivo Stock', file=file)

    result_ok = True

    return result_ok