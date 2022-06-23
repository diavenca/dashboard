import pandas as pd

# Librerías propias
import sources.bd as bd


def leer_ventas():
    conn = bd.conectarse()
    query = 'SELECT * FROM ventas '

    df = pd.read_sql_query(query, conn)

    bd.desconectarse(conn)

    df.fecha_comp = pd.to_datetime(df.fecha_comp)
    df.fecha = pd.to_datetime(df.fecha_comp.dt.date)

    df.monto_dolar = round(df.monto_dolar,2)
    df.cantidad = round(df.cantidad,2)

    df['año'] = df.fecha.dt.year
    df['mes_año'] = pd.to_datetime(df.fecha.dt.strftime('%m-%Y'))

    return df


def leer_stock():
    conn = bd.conectarse()
    query = 'SELECT * FROM stock'

    df = pd.read_sql_query(query, conn)

    bd.desconectarse(conn)

    df.fecha_stock = pd.to_datetime(df.fecha_stock)
    df.stock = round(df.stock,2)

    return df


def leer_sin_ventas():
    conn = bd.conectarse()
    query = 'select * from stock where cod not in (select cod from ventas)'

    df = pd.read_sql_query(query, conn)

    bd.desconectarse(conn)

    df.fecha_stock = pd.to_datetime(df.fecha_stock)
    df.stock = round(df.stock,2)

    return df



# Calcula la cantidad de producto vendido cada mes del período
def leer_metricas(df, ind):

    if 'fecha' in ind:
        df_aux = df.pivot_table(index=ind,
                                aggfunc={'monto_dolar': sum,
                                        'cantidad': sum,
                                        'num':'nunique'},
                                fill_value=0)
    else:
        df_aux = df.pivot_table(index=ind,
                                aggfunc={'monto_dolar': sum,
                                        'cantidad': sum,
                                        'num':'nunique',
                                        'fecha':max},
                                fill_value=0)


    df_aux.monto_dolar = round(df_aux.monto_dolar,2)
    df_aux.cantidad = round(df_aux.cantidad,2)
    
    return df_aux.reset_index()

