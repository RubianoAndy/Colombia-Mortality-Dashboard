import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output

from src.theme import (
    BASE_LAYOUT, title_cfg,
    BLUE, RED, ORANGE, GOLD, GREEN, PURPLE,
    CARD_BORDER, SEX_COLORS,
)
from src.data import df, colombia_geojson, cod_map, cod3_map, cat_order

def register_callbacks(app):
    """
    Registra todos los callbacks interactivos de la aplicación Dash.
    
    Configura las funciones callback que actualizan el dashboard en respuesta
    a cambios en los filtros de municipio y mes, generando dinámicamente
    KPIs, gráficos y tablas basados en los datos filtrados.
    
    Parámetros
    ----------
    app : dash.Dash
        Instancia de la aplicación Dash.
    """

    @app.callback(
        Output('filter-municipio', 'value'),
        Output('filter-mes', 'value'),
        Input('btn-clear', 'n_clicks'),
        prevent_initial_call=True,
    )
    def clear_filters(_):
        """
        Limpia los filtros de municipio y mes.
        
        Callback activado al presionar el botón 'Limpiar filtros'.
        Restablece los valores de ambos filtros a listas vacías.
        
        Parámetros
        ----------
        _ : int
            Número de clics del botón (no se utiliza).
        
        Retorna
        -------
        tuple
            Tupla con dos listas vacías para municipio y mes.
        """
        return [], []

    @app.callback(
        Output('kpi-total',         'children'),
        Output('kpi-homicidios',    'children'),
        Output('kpi-departamentos', 'children'),
        Output('kpi-municipios',    'children'),

        Output('fig-map',      'figure'),
        Output('fig-line',     'figure'),
        Output('fig-violent',  'figure'),
        Output('fig-pie',      'figure'),
        Output('table-causes', 'data'),
        Output('table-causes', 'tooltip_data'),
        Output('fig-stacked',  'figure'),
        Output('fig-hist',     'figure'),

        Input('filter-municipio', 'value'),
        Input('filter-mes',       'value'),
    )

    def update_all(sel_municipios, sel_meses):
        dff = df.copy()
        if sel_municipios:
            dff = dff[dff['MUNICIPIO'].isin(sel_municipios)]
        if sel_meses:
            dff = dff[dff['MES'].isin(sel_meses)]

        total_muertes       = len(dff)
        homicidios_df       = dff[dff['COD_MUERTE'].str.startswith('X95', na=False)]
        total_homicidios    = len(homicidios_df)
        total_departamentos = dff['COD_DEPARTAMENTO'].nunique()
        total_municipios    = dff['COD_DANE'].nunique()

        kpi_total = f'{total_muertes:,}'
        kpi_hom   = f'{total_homicidios:,}'
        kpi_dept  = str(total_departamentos)
        kpi_mun   = str(total_municipios)

        dept_deaths = dff.groupby(['COD_DEPARTAMENTO', 'DEPARTAMENTO']).size().reset_index(name='Total_Muertes')
        dept_deaths['DPTO'] = dept_deaths['COD_DEPARTAMENTO'].astype(str).str.zfill(2)

        fig_map = px.choropleth_map(
            dept_deaths,
            geojson=colombia_geojson,
            locations='DPTO',
            featureidkey='properties.DPTO',
            color='Total_Muertes',
            hover_name='DEPARTAMENTO',
            hover_data={'Total_Muertes': True, 'DPTO': False},
            color_continuous_scale=['#C8E6FA', BLUE, '#0B3D6B'],
            zoom=4.5,
            center={'lat': 4.5, 'lon': -74},
            map_style='carto-positron',
            opacity=0.75,
        )
        fig_map.update_layout(**BASE_LAYOUT,
            title=title_cfg('Distribución de Muertes por Departamento — Colombia 2019'),
            margin=dict(l=10, r=10, t=55, b=10),
            height=500,
            coloraxis_colorbar=dict(title='Muertes', tickfont=dict(size=10)),
        )

        monthly = dff.groupby(['MES', 'MES_NOMBRE']).size().reset_index(name='Total_Muertes').sort_values('MES')

        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(
            x=monthly['MES_NOMBRE'], y=monthly['Total_Muertes'],
            mode='lines+markers',
            line=dict(color=BLUE, width=3),
            marker=dict(size=9, color=BLUE, line=dict(width=2, color='white')),
            fill='tozeroy',
            fillcolor='rgba(68,114,196,0.12)',
            hovertemplate='<b>%{x}</b><br>Total muertes: %{y:,.0f}<extra></extra>',
        ))
        fig_line.update_layout(**BASE_LAYOUT,
            title=title_cfg('Total de Muertes por Mes — Colombia 2019'),
            xaxis=dict(title='', showgrid=False, linecolor=CARD_BORDER, tickangle=-30),
            yaxis=dict(title='Total de Muertes', gridcolor='#F1F5F9', linecolor=CARD_BORDER),
            margin=dict(l=55, r=20, t=55, b=60),
            height=380,
        )

        cities_violent = (homicidios_df.groupby('MUNICIPIO').size()
                          .reset_index(name='Homicidios')
                          .dropna(subset=['MUNICIPIO'])
                          .sort_values('Homicidios', ascending=False)
                          .head(5))

        fig_violent = px.bar(
            cities_violent, x='MUNICIPIO', y='Homicidios',
            color_discrete_sequence=[RED], text='Homicidios',
        )
        fig_violent.update_traces(texttemplate='%{text:,}', textposition='outside', marker_line_width=0)
        fig_violent.update_layout(**BASE_LAYOUT,
            title=title_cfg('5 Ciudades Más Violentas — Homicidios (X95)'),
            xaxis=dict(title='', showgrid=False, linecolor=CARD_BORDER),
            yaxis=dict(title='Total Homicidios', gridcolor='#F1F5F9', linecolor=CARD_BORDER),
            margin=dict(l=55, r=20, t=55, b=55),
            height=380,
            showlegend=False,
        )

        city_deaths = dff.groupby('MUNICIPIO').size().reset_index(name='Total_Muertes')
        city_deaths  = city_deaths[city_deaths['Total_Muertes'] > 0]
        cities_low   = city_deaths.sort_values('Total_Muertes', ascending=True).head(10)

        fig_pie = px.pie(
            cities_low, values='Total_Muertes', names='MUNICIPIO',
            color_discrete_sequence=[BLUE, ORANGE, GOLD, GREEN, RED,
                                      PURPLE, '#16A085', '#F39C12', '#1ABC9C', '#E74C3C'],
        )
        fig_pie.update_traces(textinfo='label+value', textposition='inside',
                              textfont=dict(size=11))
        fig_pie.update_layout(**BASE_LAYOUT,
            title=title_cfg('10 Ciudades con Menor Índice de Mortalidad'),
            margin=dict(l=20, r=20, t=55, b=20),
            height=380,
            legend=dict(font=dict(size=10), orientation='v'),
        )

        cause_counts = dff.groupby('COD_MUERTE').size().reset_index(name='Total_Casos')
        cause_counts['Nombre'] = cause_counts['COD_MUERTE'].map(cod_map)
        mask = cause_counts['Nombre'].isna()
        cause_counts.loc[mask, 'Nombre'] = cause_counts.loc[mask, 'COD_MUERTE'].str[:3].map(cod3_map)
        cause_counts.loc[cause_counts['Nombre'].isna(), 'Nombre'] = 'Sin descripción'
        top10 = cause_counts.sort_values('Total_Casos', ascending=False).head(10).copy()
        top10 = top10.rename(columns={'COD_MUERTE': 'Código'})
        top10['Ranking'] = range(1, len(top10) + 1)
        top10 = top10[['Ranking', 'Código', 'Nombre', 'Total_Casos']]

        table_data   = top10.to_dict('records')
        tooltip_data = [
            {col: {'value': str(row[col]), 'type': 'markdown'} for col in top10.columns}
            for _, row in top10.iterrows()
        ]

        sex_dept = dff.groupby(['DEPARTAMENTO', 'SEXO_NOMBRE']).size().reset_index(name='Total_Muertes')

        fig_stacked = px.bar(
            sex_dept, x='DEPARTAMENTO', y='Total_Muertes',
            color='SEXO_NOMBRE', barmode='stack',
            color_discrete_map=SEX_COLORS,
        )

        fig_stacked.update_layout(**BASE_LAYOUT,
            title=title_cfg('Total de Muertes por Sexo en Cada Departamento'),
            xaxis=dict(title='', showgrid=False, tickangle=-45, linecolor=CARD_BORDER),
            yaxis=dict(title='Total de Muertes', gridcolor='#F1F5F9', linecolor=CARD_BORDER),
            margin=dict(l=55, r=20, t=55, b=110),
            height=460,
            legend=dict(title='Sexo', orientation='h', y=1.08, x=0.5, xanchor='center'),
        )

        age_hist = dff.groupby('CATEGORIA_EDAD').size().reset_index(name='Total_Muertes')
        age_hist['CATEGORIA_EDAD'] = pd.Categorical(
            age_hist['CATEGORIA_EDAD'], categories=cat_order, ordered=True)
        age_hist = age_hist.sort_values('CATEGORIA_EDAD').reset_index(drop=True)

        fig_hist = px.bar(
            age_hist, x='CATEGORIA_EDAD', y='Total_Muertes',
            color='Total_Muertes',
            color_continuous_scale=['#C8E6FA', BLUE, '#0B3D6B'],
            text='Total_Muertes',
        )

        fig_hist.update_traces(texttemplate='%{text:,}', textposition='outside', marker_line_width=0)
        
        fig_hist.update_layout(**BASE_LAYOUT,
            title=title_cfg('Distribución de Muertes por Grupo de Edad'),
            xaxis=dict(title='', showgrid=False, tickangle=-45, linecolor=CARD_BORDER),
            yaxis=dict(title='Total de Muertes', gridcolor='#F1F5F9', linecolor=CARD_BORDER),
            margin=dict(l=55, r=20, t=55, b=120),
            height=460,
            showlegend=False,
            coloraxis_showscale=False,
        )

        return (
            kpi_total, kpi_hom, kpi_dept, kpi_mun,
            fig_map, fig_line, fig_violent, fig_pie,
            table_data, tooltip_data,
            fig_stacked, fig_hist,
        )
