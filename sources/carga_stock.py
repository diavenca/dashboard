import pandas as pd
from datetime import date

import sources.bd as bd

def read_files(file):

    hoy = date.today()

    df = pd.read_excel(file)
    
    df['fecha'] = hoy

    return df

def transformar_stock(df):

    df_aux = df.copy()
    cols = ['cod', 'producto', 'linea', 'stock', 'stock2', 'ajuste', 'fecha_stock']
    df_aux.columns = cols
    df_aux = df_aux.loc[:,['cod', 'producto', 'linea', 'stock', 'fecha_stock']]

    df_aux.dropna(inplace=True)
    df_aux.cod = df_aux.cod.astype(str)
    df_aux.fecha_stock = pd.to_datetime(df_aux.fecha_stock)
    df_aux.producto = df_aux.apply(lambda row: row['producto'].strip(), axis = 1)
    df_aux.linea = df_aux.apply(lambda row: row['linea'].strip(), axis = 1)

    return df_aux

def guardar_datos_bd(df):
    conn = bd.conectarse()
    df.to_sql('stock', conn, if_exists='replace', index = False)
    bd.desconectarse(conn)

