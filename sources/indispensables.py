import pandas as pd

import streamlit as st
 

# Calcula la cantidad de producto vendido cada mes del período
def ventas_prod_mes(df_ventas):

    df_prod = df_ventas.query('fecha > "2020-12-31"').loc[:,['fecha', 'cod', 'producto', 'cantidad', 'monto_dolar']]
    
    df_prod['mes_año'] = df_prod.fecha.dt.strftime('%m-%Y')

    df_ventas_prod_mes = df_prod.pivot_table(index='cod',
                                                columns='mes_año',
                                                fill_value=0,
                                                aggfunc={'cantidad':sum})

    df_ventas_prod_mes['total_ventas'] = df_ventas_prod_mes.sum(axis = 1)

    return df_ventas_prod_mes


# Calculamos cuantos meses del período cada producto tuvo ventas
# Difinimos como un producto indispensable aquel que tiene ventas regulares
# por ejemplo el 75% de los meses del período

def __calculo_mes_con_ventas(row):
    # -1 para descontar la columna total_ventas
    total = -1
    
    for column in row: 
        if column:
            total = total + 1
    
    return total


def productos_indispensables(df_ventas_prod_mes, df_stock):

    df_ventas_prod_mes['mes_ventas'] = df_ventas_prod_mes.apply(lambda row: __calculo_mes_con_ventas(row), 
                                                axis = 1)

    min_meses = (df_ventas_prod_mes.shape[1] - 1) * .75

    df_ventas_prod_mes = df_ventas_prod_mes[ df_ventas_prod_mes['mes_ventas'] > min_meses ]


    df_promed_ventas_prod = df_ventas_prod_mes.total_ventas/df_ventas_prod_mes.mes_ventas
    df_promed_ventas_prod = df_promed_ventas_prod.reset_index()
    df_promed_ventas_prod.columns=['cod', 'promedio']
    df_promed_ventas_prod.promedio = round(df_promed_ventas_prod.promedio)

    df_indispensables = df_stock[df_stock.cod.isin(df_ventas_prod_mes.index)]
    df_indispensables = pd.merge(df_indispensables, df_promed_ventas_prod, on='cod')
    df_indispensables['faltan'] = df_indispensables.stock - df_indispensables.promedio 
    df_indispensables = df_indispensables.loc[:,['cod', 'producto', 'stock', 'promedio', 'faltan']]

    return df_indispensables


# Ventas (volumnen y en $) por mes de los productos indispensables
def ventas_prod_indis(df_ventas, df_indispensables):

    df_prod = df_ventas.query('fecha > "2020-12-31"').loc[:,['fecha', 'mes_año', 'cod', 'producto', 'cantidad', 'monto_dolar', 'num']]
    
    df_ventas_indis = df_prod[df_prod.cod.isin(df_indispensables.cod)]

    return df_ventas_indis


