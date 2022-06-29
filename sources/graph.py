import pandas as pd

# Librerías para graficar 
import altair as alt
import plotly.express as px

from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode


# Funciones para crear gráficos con Altair


# graf_barras_ventas_dol
# Crea un gráfico de barras de ventas en $ en función de diferentes
# intervalos de tiempo
#
# Parámetros: 
#     df: DataFrame a utilizar
#     x: Datos para el eje de las x. Generalmente es el intervalo de tiempo
#     tooltip: Lista con los parámetros del tooltip
#     titulo: Título del gráfico
#     dx: Entero para ajustar horizontalmente la posición del texto sobre las barras


def graph_bars_text(df, met, titulo, color_scheme):

    metrica = 'sum(' + met + '):Q'

    x=alt.X('yearmonth(fecha):T', title='Mes y Año', axis = alt.Axis(labelAngle=0, labelFontSize=14))
    y=alt.Y(metrica, title = titulo, scale=alt.Scale(zero=False), 
                    axis = alt.Axis(grid=True, titleAnchor='middle', titleAngle = 270, labelFontSize=12))

    color=alt.Color(metrica, scale=alt.Scale(scheme=color_scheme),
                    legend=alt.Legend(title=titulo))

    tooltip=[alt.Tooltip('yearmonth(fecha):T', title='Mes y Año'),
            alt.Tooltip(metrica, title=titulo, format=',.5')]

    barras = alt.Chart(df).mark_bar().encode(
                    x=x,
                    y=y,
                    color=color,
                    tooltip=tooltip,
                    ).properties(#title=titulo,
                            width=800, 
                            height=400
                    )

    textos = barras.mark_text(dx=18, dy=-10, fill='black').encode(
            text = alt.Text(metrica, format=',.5', title = titulo)
                    )

    med = 'mean(' + met + '):Q'

    media = alt.Chart(df).mark_rule(color='red').encode(
                                    y=med, 
                                    tooltip=[alt.Tooltip(med, title='Media', format=',.5')])


    grafico_final = barras + textos + media

    return grafico_final




def graph_bars_cols(df, met, titulo, columns):

    metrica = 'sum(' + met + '):Q'

    x=alt.X('yearmonth(fecha):T', title='Mes y Año', axis = alt.Axis(labelAngle=0, labelFontSize=14))
    y=alt.Y(metrica, title = titulo, scale=alt.Scale(zero=False), 
                    axis = alt.Axis(grid=True, titleAnchor='middle', titleAngle = 270, labelFontSize=12))

    color=alt.Color(columns, legend=alt.Legend(title=titulo))

    tooltip=[alt.Tooltip('yearmonth(fecha):T', title='Mes y Año'),
                # alt.Tooltip('cod', title='Código'), 
                # alt.Tooltip('producto', title='Producto'), 
                alt.Tooltip(metrica, title=titulo, format=',.4',)]

    barras = alt.Chart(df).mark_bar().encode(
                    x=x,
                    y=y,
                    color=color,
                    column=alt.Column(columns, title=''),
                    tooltip=tooltip,
                    ).properties(#title=titulo,
                            width=300, 
                            height=300
                    )

   
    return barras


def graph_map(df):
    mapa = alt.Chart(df).mark_rect().encode(
            x=alt.X('dia_mes:O', title='Días del mes', axis = alt.Axis(labelAngle=0, labelFontSize=14)),
            y=alt.Y('yearmonth(fecha):T', title = 'Mes y Año', scale=alt.Scale(zero=False), 
            axis = alt.Axis(grid=True, titleAnchor='middle', titleAngle = 270, labelFontSize=10)),
            color=alt.Color(
                'sum(monto_dolar):Q', scale=alt.Scale(scheme='goldgreen'), legend=alt.Legend(title="Ventas en $")),
            tooltip=[
                alt.Tooltip('dia_mes:O', title='Día'),
                alt.Tooltip('yearmonth(fecha):T', title='Mes y Año'),
                alt.Tooltip('sum(monto_dolar):Q', format=',.5', title='Ventas en $')]
            ).properties(title='Ventas en $ por Día del Mes',
                        width=800, 
                        height=300
            ).configure_title(
                fontSize = 16,
                anchor = 'middle',
            ).interactive()

    return mapa


def graph_time_serie(df):

    # Gráfico interactivo serie temporal
    # ==============================================================================

    fig = px.line(
        data_frame = df,
        x      = 'fecha',
        y      = 'monto_dolar',
        labels = {
            'fecha': 'Fecha',
            'monto_dolar': 'Ventas en $',
        },
        hover_data={'fecha': '|%B %d, %Y'},
        width  = 900,
        height = 500
    )

    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=7, label="1 Semana", step="day", stepmode="backward"),
                dict(count=1, label="1 Mes", step="month", stepmode="backward"),
                dict(count=3, label="3 Meses", step="month", stepmode="backward"),
                dict(count=6, label="6 Meses", step="month", stepmode="backward"),
                dict(count=1, label="Este Año", step="year", stepmode="todate"),
                dict(count=1, label="1 Año", step="year", stepmode="backward"),
                dict(label="Todo", step="all")
            ])
        )
    )


    return fig



def graph_table_select(df):

    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
    gb.configure_side_bar() #Add a sidebar
    gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
    gridOptions = gb.build()

    grid_response = AgGrid(
        df,
        gridOptions=gridOptions,
        data_return_mode='AS_INPUT', 
        update_mode='MODEL_CHANGED', 
        fit_columns_on_grid_load=True,
        theme='blue', #Add theme color to the table
        enable_enterprise_modules=True,
        height=400, 
        reload_data=True
    )

    selected = grid_response['selected_rows'] 

    df_sel = pd.DataFrame(selected) #Pass the selected rows to a new dataframe df

    return df_sel



def graph_lines(df, met, titulo, met_col):

    metrica = 'sum(' + met + '):Q'
    met_color = met_col + ':N'

    x=alt.X('yearmonth(fecha):T', title='Mes y Año', axis = alt.Axis(labelAngle=0, labelFontSize=14))
    
    # Definimos la selección para hacer el gráfico interactivo
    # Cuando el mouse se acerca a la línea de un producto, 
    # esta aumenta de grosor
    highlight = alt.selection(type='single', on='mouseover',
                            fields=[met_col], nearest=True)


    base = alt.Chart(df).mark_line().encode(
        x = x,
        y = alt.Y(metrica, title = titulo, scale=alt.Scale(zero=False), 
                axis = alt.Axis(grid=True, titleAnchor='middle', titleAngle = 270, labelFontSize=10)),
        color = alt.Color(met_color), 
        tooltip = [alt.Tooltip('yearmonth(fecha):T', title='Mes y Año'),
                alt.Tooltip(met_col, title=met_col), 
                alt.Tooltip(metrica, title=titulo, format=',.6',)]
    )


    points = base.mark_circle().encode(
        opacity=alt.value(0.5)
    ).add_selection(
        highlight
    ).properties(
        title = titulo,
        width=900
    )

    # Permite cambiar el aspecto de las líneas cuando el ratón se acerca
    # Se utiliza la negación de la selección ~highlight para evitar
    # que el gráfico tenga las líneas resaltadas al cargar
    lines = base.mark_line().encode(
        size=alt.condition(~highlight, alt.value(1), alt.value(3))
    )

    grafico = alt.layer(
        points,
        lines
        ).interactive()

    return grafico

