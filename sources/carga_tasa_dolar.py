import requests
from bs4 import BeautifulSoup

import re

import pandas as pd
from datetime import date, datetime


import sources.bd as bd

import streamlit as st

hoy = str(date.today())
hoy = datetime.strptime(hoy, '%Y-%m-%d') 

# Leer la página del URL y devolver un objeto BeautifulSoup

def devolver_soup(url):
    # Eliminamos el '/' del final, si existe
    # Da error 403 si se deja
    if url[len(url)-1] == '/':
        url = url[:len(url)-1]
    
    # Obtenemos la página
    try:
        resp = requests.get(url)
    except Exception as e:
        print('Error obteniendo la página. Excepción ',e)
        return url
    
    if resp.status_code != 200:
        print('Error obteniendo la página. Status Code', resp.status_code)
        return url
    
    # Para saber el encoding utilizado por el servidor
    # print(chardet.detect(resp.content))
    
    # Para especificar el tipo de encoding y 
    # obtener correctamente los caracteres acentuados
    resp.encoding = "utf-8"
    contenido = resp.content
    soup = BeautifulSoup(contenido)    

    return soup

# Función general que extrae datos numéricos 
# de una cadena de caracteres. Devuelve un float

# Elimina los "'" y los puntos de mil
# Reemplaza las "," decimales por "."
# Extrae una cifra y la devuelve como float
def extraer_numero(cadena):
    
    result = cadena.replace("'", '').replace('.', '').replace(',', '.')
    
    result = re.findall(r'-?\d+\.?\d*', result)[0]
    
    return float(result)


def leer_pagina(fecha):
    # Extraemos los datos del dólar

    URL='https://monitordolarvenezuela.com/historial#2a'

    soup = devolver_soup(URL)

    # Extraemos la tabla y sus datos
    datos = soup.find('table', attrs={'class':'zui-table'}).find_all('tr')

    # Extraemos la información de cada línea de la tabla
    result = []

    for dato in datos:

        dic = {}
        
        tasas = dato.find_all('td')

        if tasas:

            fecha_aux = tasas[0].text.strip()
            fecha_aux = datetime.strptime(fecha_aux, '%d-%m-%Y') 

            if fecha_aux > fecha:
                dic['fecha'] = fecha_aux
                dic['baja'] = extraer_numero(tasas[1].text.strip())
                dic['alta'] = extraer_numero(tasas[2].text.strip())

                result.append(dic)

    df = pd.DataFrame(result)

    return df


def transformar(df):
    df.fecha = pd.to_datetime(df.fecha)
    df.alta = df.alta.astype(float)
    df.baja = df.baja.astype(float)

    df['tasa_dolar'] = df.apply(lambda row: row['baja'] if row['baja'] else row['alta'], axis = 1)

    return df

def guardar_datos_bd(df):
    conn = bd.conectarse()
    df.to_sql('tasa_dolar', conn, if_exists='append', index = False)
    bd.desconectarse(conn)

def actualizar_dolar():

    conn = bd.conectarse()
    query = 'SELECT max(fecha) FROM tasa_dolar '
    result = bd.ejecutar_consulta(query, conn, False)

    bd.desconectarse(conn)

    fecha = result[0][:10]
    fecha = datetime.strptime(fecha, '%Y-%m-%d') 

    if hoy > fecha: 

        st.write('Actualizar dolar')

        fecha = fecha.strftime('%d-%m-%Y')
        fecha = datetime.strptime(fecha, '%d-%m-%Y') 
    
        df = leer_pagina(fecha)
        df = transformar(df)

        st.dataframe(df)

        guardar_datos_bd(df)
    

