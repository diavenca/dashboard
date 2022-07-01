import pandas as pd
import datetime 

import sources.bd as bd

import streamlit as st


# Lectura de los archivos y creación de un DF con todos los datos

def probar_existencia(df):
    conn = bd.conectarse()

    existe = True
    hoy = datetime.datetime.now()

    min_num = str(df.num.min())
    max_num = str(df.num.max())
    
    min_fecha = str(df.fecha_comp.min())
    max_fecha = str(df.fecha_comp.max())
    tipo = str(df.tipo.min())

    query = f'SELECT max(max_num), max(max_fecha) FROM control WHERE tipo = "{tipo}"'

    result = bd.ejecutar_consulta(query, conn, False)

    # st.write('tipo', tipo)
    # st.write('max(max_num)', result[0])
    # st.write('max(max_fecha)', result[1])
    # st.write('max(min_num)', min_num)
    # st.write('min_fecha', min_fecha)

    # if result[0] < min_num and result[1] < min_fecha:
    if result[1] < min_fecha:
        existe = False

        query = f'INSERT INTO control VALUES("{hoy}","{min_num}", "{max_num}","{min_fecha}", "{max_fecha}", "{tipo}")'
        bd.ejecutar(query, conn)
        
    bd.desconectarse(conn)

    return existe

    
def read_files(file, col, long):

    df = pd.read_excel(file)
    
    info_file = file.name[:long]
    df[col] = info_file

    return df

def seleccionar_cols(df):

    df_aux = df[~df.Número.str.contains('Totales')]

    cols = ['num', 'reng', 'fecha_comp', 'cliente', 'vendedor', 'almacen', 'cantidad','und', 'precio', 'base', 'iva', 'otros', 'neto', 'tipo']
    df_aux.columns = cols
    df_aux = df_aux.loc[:,['num', 'fecha_comp', 'vendedor', 'cantidad', 'neto', 'tipo']]

    return df_aux

def construir_df(df):
    result = []

    cod = ''
    prod = ''

    for index, row in df.iterrows(): 
        if len(row['num']) <= 5 :
            cod = row['num']
            prod = row['fecha_comp']
        else:
            dic = {}
            dic['num'] = row['num']
            dic['fecha_comp'] = row['fecha_comp']
            dic['vendedor'] = row['vendedor']
            dic['cod'] = cod
            dic['producto'] = prod
            dic['cantidad'] = row['cantidad']
            dic['monto'] = row['neto']   
            dic['tipo'] = row['tipo'] 
            
            result.append(dic)

    return pd.DataFrame(result)

def transformar(df):

    def columna_num(año, num, tipo):
        año = str(año)[0:4]
        result = str(año) + '-' + str(num) + '-' + str(tipo)
        return result

    # Transformamos los tipos de columnas para que se guarden con el tipo correcto
    # Creamos la columna fecha con solo la fecha, sin tiempo. Será utilizada más adelante

    df.vendedor = df.vendedor.astype(int)
    df.fecha_comp = pd.to_datetime(df.fecha_comp)
    df['fecha'] = pd.to_datetime(df.fecha_comp.dt.date)
    df.cantidad = round(df.cantidad, 2)

    df.num = df.apply(lambda row: columna_num(row.fecha, row.num, row.tipo), axis = 1)

    return df

def calcular_monto_dolar(df):
    conn = bd.conectarse()

    min = df.fecha.min()
    query = 'SELECT fecha, tasa_dolar FROM tasa_dolar WHERE fecha >= "' + str(min) + '"'
    df_dolar = pd.read_sql_query(query, conn)
    df_dolar.fecha = pd.to_datetime(df_dolar.fecha)

    bd.desconectarse(conn)

    df = pd.merge(df, df_dolar, on='fecha')

    df['monto_dolar'] = df.apply(lambda row: row['monto'] / row['tasa_dolar'], axis = 1)
    df.monto_dolar = round(df.monto_dolar, 2)

    return df          

def guardar_datos_bd(df):
    conn = bd.conectarse()
    df.to_sql('ventas', conn, if_exists='append', index = False)
    bd.desconectarse(conn)

    
