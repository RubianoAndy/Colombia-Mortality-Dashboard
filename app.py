import dash
from dash import dcc, html, dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os
import base64

BASE_DIR   = os.path.dirname(__file__)
DATA_DIR   = os.path.join(BASE_DIR, 'utils/data')
PUBLIC_DIR = os.path.join(BASE_DIR, 'public')

def encode_image(path):
    if not os.path.exists(path):
        return ''
    with open(path, 'rb') as f:
        enc = base64.b64encode(f.read()).decode('ascii')
    ext = os.path.splitext(path)[1].lstrip('.').lower()
    if ext == 'jpg':
        ext = 'jpeg'
    return f'data:image/{ext};base64,{enc}'

LOGO_SRC   = encode_image(os.path.join(PUBLIC_DIR, 'UnisalleDarkLogoV1.png'))
AUTHOR_SRC = encode_image(os.path.join(PUBLIC_DIR, 'assets', 'images', 'author', 'Andy Rubiano.png'))

df  = pd.read_csv(os.path.join(DATA_DIR, 'nofetal2019.csv'))
div = pd.read_csv(os.path.join(DATA_DIR, 'divipola.csv'))
cod = pd.read_csv(os.path.join(DATA_DIR, 'codigos_muerte.csv'))

dept_map = div.drop_duplicates('COD_DEPARTAMENTO').set_index('COD_DEPARTAMENTO')['DEPARTAMENTO'].to_dict()
df['DEPARTAMENTO'] = df['COD_DEPARTAMENTO'].map(dept_map)

mun_map = div.set_index('COD_DANE')['MUNICIPIO'].to_dict()
df['MUNICIPIO'] = df['COD_DANE'].map(mun_map)

sex_map = {1: 'Masculino', 2: 'Femenino', 3: 'Indeterminado'}
df['SEXO_NOMBRE'] = df['SEXO'].map(sex_map)

meses = {1:'Enero',2:'Febrero',3:'Marzo',4:'Abril',5:'Mayo',6:'Junio',
         7:'Julio',8:'Agosto',9:'Septiembre',10:'Octubre',11:'Noviembre',12:'Diciembre'}
df['MES_NOMBRE'] = df['MES'].map(meses)

cod_map  = cod.dropna(subset=['Codigo4']).set_index('Codigo4')['Desc4'].to_dict()
cod3_map = cod.dropna(subset=['Codigo3']).drop_duplicates('Codigo3').set_index('Codigo3')['Desc3'].to_dict()

edad_cats = {
    'Mortalidad neonatal':      [0,1,2,3,4],
    'Mortalidad infantil':      [5,6],
    'Primera infancia':         [7,8],
    'Niñez':                    [9,10],
    'Adolescencia':             [11],
    'Juventud':                 [12,13],
    'Adultez temprana':         [14,15,16],
    'Adultez intermedia':       [17,18,19],
    'Vejez':                    [20,21,22,23,24],
    'Longevidad / Centenarios': [25,26,27,28],
    'Edad desconocida':         [29],
}
edad_reverse = {c: cat for cat, codes in edad_cats.items() for c in codes}
df['CATEGORIA_EDAD'] = df['GRUPO_EDAD1'].map(edad_reverse)

cat_order = list(edad_cats.keys())

# 1. MAP data
dept_deaths = df.groupby(['COD_DEPARTAMENTO','DEPARTAMENTO']).size().reset_index(name='Total_Muertes')
dept_coords = {
    91:(-1.44,-71.57),  5:(6.88,-75.83),  8:(10.66,-75.00),
    11:(4.65,-74.08),  13:(8.67,-74.03),  15:(5.89,-73.36),
    17:(5.30,-75.36),  18:(1.37,-75.61),  19:(2.45,-76.82),
    20:(9.34,-73.52),  23:(8.35,-75.73),  25:(5.03,-74.03),
    27:(5.69,-76.66),  41:(2.53,-75.53),  44:(11.35,-72.09),
    47:(10.19,-74.15), 50:(3.27,-73.08),  52:(1.60,-78.09),
    54:(7.95,-72.50),  63:(4.46,-75.67),  66:(4.99,-75.70),
    68:(6.95,-73.13),  70:(8.81,-75.39),  73:(3.89,-75.23),
    76:(3.80,-76.64),  81:(7.08,-70.76),  85:(5.34,-72.39),
    86:(1.15,-76.65),  88:(12.58,-81.72), 94:(2.58,-68.23),
    95:(2.57,-72.64),  97:(1.25,-70.23),  99:(4.44,-69.29),
}
dept_deaths['LAT'] = dept_deaths['COD_DEPARTAMENTO'].map(lambda x: dept_coords.get(x,(0,0))[0])
dept_deaths['LON'] = dept_deaths['COD_DEPARTAMENTO'].map(lambda x: dept_coords.get(x,(0,0))[1])

# 2. LINE: deaths by month
monthly = df.groupby(['MES','MES_NOMBRE']).size().reset_index(name='Total_Muertes').sort_values('MES')

# 3. BAR: 5 most violent cities (X95)
homicidios = df[df['COD_MUERTE'].str.startswith('X95', na=False)]
cities_violent = (homicidios.groupby('MUNICIPIO').size()
                  .reset_index(name='Homicidios')
                  .dropna(subset=['MUNICIPIO'])
                  .sort_values('Homicidios', ascending=False)
                  .head(5))

# 4. PIE: 10 cities with lowest mortality
city_deaths = df.groupby('MUNICIPIO').size().reset_index(name='Total_Muertes')
city_deaths  = city_deaths[city_deaths['Total_Muertes'] > 0]
cities_low   = city_deaths.sort_values('Total_Muertes', ascending=True).head(10)

# 5. TABLE: top 10 causes
cause_counts = df.groupby('COD_MUERTE').size().reset_index(name='Total_Casos')
cause_counts['Nombre'] = cause_counts['COD_MUERTE'].map(cod_map)
mask = cause_counts['Nombre'].isna()
cause_counts.loc[mask, 'Nombre'] = cause_counts.loc[mask, 'COD_MUERTE'].str[:3].map(cod3_map)
cause_counts.loc[cause_counts['Nombre'].isna(), 'Nombre'] = 'Sin descripción'
top10_causes = cause_counts.sort_values('Total_Casos', ascending=False).head(10).copy()
top10_causes = top10_causes.rename(columns={'COD_MUERTE': 'Código'})
top10_causes['Ranking'] = range(1, 11)
top10_causes = top10_causes[['Ranking','Código','Nombre','Total_Casos']]

# 6. STACKED BAR: deaths by sex per department
sex_dept = df.groupby(['DEPARTAMENTO','SEXO_NOMBRE']).size().reset_index(name='Total_Muertes')

# 7. HISTOGRAM BAR: deaths by age category
age_hist = df.groupby('CATEGORIA_EDAD').size().reset_index(name='Total_Muertes')
age_hist['CATEGORIA_EDAD'] = pd.Categorical(age_hist['CATEGORIA_EDAD'], categories=cat_order, ordered=True)
age_hist = age_hist.sort_values('CATEGORIA_EDAD').reset_index(drop=True)

total_muertes       = len(df)
total_homicidios    = len(homicidios)
total_departamentos = df['COD_DEPARTAMENTO'].nunique()
total_municipios    = df['COD_DANE'].nunique()

SIDEBAR_BG          = '#1B2B3A'
SIDEBAR_ACTIVE_BG   = '#F5C518'
SIDEBAR_ACTIVE_TEXT = '#1B2B3A'
SIDEBAR_TEXT        = '#FFFFFF'
SIDEBAR_MUTED       = '#7A99B8'

MAIN_BG     = '#EFF2F7'
CARD_BG     = '#FFFFFF'
CARD_BORDER = '#E1E5EE'
SHADOW      = '0 2px 12px rgba(0,0,0,0.07)'

TITLE_COLOR = '#1B2B3A'
TEXT_COLOR  = '#3D4A5C'
TEXT_MUTED  = '#94A3B8'

GOLD   = '#F5C518'
BLUE   = '#4472C4'
ORANGE = '#ED7D31'
RED    = '#C0392B'
GREEN  = '#27AE60'
PURPLE = '#8E44AD'

SEX_COLORS = {'Masculino': BLUE, 'Femenino': ORANGE, 'Indeterminado': GOLD}
FONT = '"Segoe UI", Arial, sans-serif'

BASE_LAYOUT = dict(
    paper_bgcolor=CARD_BG,
    plot_bgcolor=CARD_BG,
    font=dict(color=TEXT_COLOR, family=FONT, size=12),
)

def title_cfg(text):
    return dict(text=text, font=dict(size=14, color=TITLE_COLOR, weight=600))


# FIG 1: Map — Distribución de muertes por departamento
fig_map = px.scatter_mapbox(
    dept_deaths, lat='LAT', lon='LON',
    size='Total_Muertes', color='Total_Muertes',
    hover_name='DEPARTAMENTO',
    hover_data={'Total_Muertes': True, 'LAT': False, 'LON': False},
    color_continuous_scale=['#C8E6FA', BLUE, '#0B3D6B'],
    size_max=50, zoom=4.5,
    center={'lat': 4.5, 'lon': -74},
    mapbox_style='carto-positron',
)
fig_map.update_layout(**BASE_LAYOUT,
    title=title_cfg('Distribución de Muertes por Departamento — Colombia 2019'),
    margin=dict(l=10, r=10, t=55, b=10),
    height=500,
    coloraxis_colorbar=dict(title='Muertes', tickfont=dict(size=10)),
)

# FIG 2: Line — Total de muertes por mes
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

# FIG 3: Bar — 5 ciudades más violentas (X95)
fig_violent = px.bar(
    cities_violent, x='MUNICIPIO', y='Homicidios',
    color_discrete_sequence=[RED],
    text='Homicidios',
)
fig_violent.update_traces(texttemplate='%{text:,}', textposition='outside', marker_line_width=0)
fig_violent.update_layout(**BASE_LAYOUT,
    title=title_cfg('5 Ciudades Más Violentas — Homicidios (Código X95)'),
    xaxis=dict(title='', showgrid=False, linecolor=CARD_BORDER),
    yaxis=dict(title='Total Homicidios', gridcolor='#F1F5F9', linecolor=CARD_BORDER),
    margin=dict(l=55, r=20, t=55, b=55),
    height=380,
    showlegend=False,
)

# FIG 4: Pie — 10 ciudades con menor índice de mortalidad
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

# FIG 5: Stacked bar — muertes por sexo por departamento
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

# FIG 6: Bar — distribución de muertes por grupo de edad
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

app = dash.Dash(__name__, title='Mortalidad Colombia 2019', suppress_callback_exceptions=True)
server = app.server

SIDEBAR_WIDTH = '220px'

def nav_item(label, active=False):
    return html.Div(label, style={
        'padding': '11px 18px',
        'color': SIDEBAR_ACTIVE_TEXT if active else SIDEBAR_TEXT,
        'backgroundColor': SIDEBAR_ACTIVE_BG if active else 'transparent',
        'cursor': 'pointer',
        'fontSize': '13px',
        'fontWeight': '700' if active else '400',
        'borderRadius': '0',
        'margin': '3px 12px',
        'letterSpacing': '0.2px',
    })

def kpi_card(icon, value, label):
    return html.Div([
        html.Div(icon, style={'fontSize': '26px', 'marginBottom': '10px'}),
        html.Div(value, style={
            'fontSize': '26px', 'fontWeight': '700',
            'color': TITLE_COLOR, 'lineHeight': '1',
        }),
        html.Div(label, style={
            'fontSize': '10px', 'color': TEXT_MUTED, 'marginTop': '6px',
            'textTransform': 'uppercase', 'letterSpacing': '0.8px', 'fontWeight': '600',
        }),
    ], style={
        'backgroundColor': CARD_BG,
        'borderRadius': '0',
        'border': f'1px solid {CARD_BORDER}',
        'padding': '20px 24px',
        'flex': '1',
        'boxShadow': SHADOW,
        'minWidth': '155px',
        'fontFamily': FONT,
    })

def card(children, flex=1, padding=False, min_w='0'):
    style = {
        'flex': str(flex),
        'minWidth': min_w,
        'backgroundColor': CARD_BG,
        'borderRadius': '0',
        'border': f'1px solid {CARD_BORDER}',
        'boxShadow': SHADOW,
        'overflow': 'hidden',
    }
    if padding:
        style['padding'] = '20px'
    return html.Div(children, style=style)

app.layout = html.Div([

    # SIDEBAR
    html.Div([
        html.Div([
            html.Img(src=LOGO_SRC, style={
                'width': '82%', 'maxWidth': '165px',
                'display': 'block', 'margin': '0 auto',
            }) if LOGO_SRC else html.Div([
                html.P('UNIVERSIDAD', style={'color': SIDEBAR_TEXT, 'fontSize': '11px',
                                             'margin': '0', 'fontWeight': '700',
                                             'letterSpacing': '1px', 'textAlign': 'center'}),
                html.P('DE LA SALLE', style={'color': GOLD, 'fontSize': '13px',
                                             'margin': '2px 0 0 0', 'fontWeight': '900',
                                             'letterSpacing': '1px', 'textAlign': 'center'}),
            ]),
        ], style={
            'padding': '20px 16px 18px',
            'borderBottom': '1px solid rgba(255,255,255,0.1)',
            'flexShrink': '0',
        }),

        html.Div([
            html.Div([
                html.Img(src=AUTHOR_SRC, style={
                    'width': '48px', 'height': '48px', 'borderRadius': '50%',
                    'objectFit': 'cover', 'border': f'2px solid {GOLD}',
                    'marginRight': '10px', 'flexShrink': '0',
                }) if AUTHOR_SRC else html.Div(style={
                    'width': '48px', 'height': '48px', 'borderRadius': '50%',
                    'backgroundColor': GOLD, 'marginRight': '10px', 'flexShrink': '0',
                }),
                html.Div([
                    html.P('Andy Rubiano', style={'color': SIDEBAR_TEXT, 'margin': '0',
                                                  'fontSize': '13px', 'fontWeight': '600'}),
                    html.P('Analista de Datos', style={'color': SIDEBAR_MUTED,
                                                       'margin': '0', 'fontSize': '11px'}),
                ]),
            ], style={'display': 'flex', 'alignItems': 'center'}),
        ], style={
            'padding': '14px 20px',
            'borderTop': '1px solid rgba(255,255,255,0.1)',
            'marginTop': 'auto',
            'flexShrink': '0',
        }),

    ], style={
        'width': SIDEBAR_WIDTH,
        'minWidth': SIDEBAR_WIDTH,
        'backgroundColor': SIDEBAR_BG,
        'display': 'flex',
        'flexDirection': 'column',
        'height': '100vh',
        'position': 'fixed',
        'top': '0',
        'left': '0',
        'zIndex': '100',
        'overflowY': 'auto',
        'overflowX': 'hidden',
        'fontFamily': FONT,
        'boxSizing': 'border-box',
    }),

    # MAIN CONTENT
    html.Div([

        # Title banner
        html.Div([
            html.H1('MORTALIDAD EN COLOMBIA — 2019', style={
                'margin': '0', 'fontSize': '22px', 'fontWeight': '800',
                'color': TITLE_COLOR, 'letterSpacing': '0.8px',
            }),
            html.P('Por Andy Rubiano  ·  Fuente: DANE — Estadísticas Vitales EEVV', style={
                'color': TEXT_MUTED, 'margin': '5px 0 0 0', 'fontSize': '13px',
            }),
        ], style={
            'backgroundColor': CARD_BG, 'padding': '22px 32px',
            'borderBottom': f'1px solid {CARD_BORDER}',
            'boxShadow': '0 1px 4px rgba(0,0,0,0.05)', 'fontFamily': FONT,
        }),

        html.Div([
            html.Div([
                kpi_card('📊', f'{total_muertes:,}',      'Total Defunciones'),
                kpi_card('⚠️',  f'{total_homicidios:,}',  'Homicidios (X95)'),
                kpi_card('🏛️', f'{total_departamentos}',  'Departamentos'),
                kpi_card('🏙️', f'{total_municipios}',     'Municipios'),
            ], style={'display': 'flex', 'gap': '16px', 'marginBottom': '20px', 'flexWrap': 'wrap'}),

            card(dcc.Graph(figure=fig_map, config={'scrollZoom': True, 'displayModeBar': False}),
                 flex=1),
            html.Div(style={'marginBottom': '20px'}),

            html.Div([
                card(dcc.Graph(figure=fig_line,    config={'displayModeBar': False}), flex=6),
                card(dcc.Graph(figure=fig_violent, config={'displayModeBar': False}), flex=4),
            ], style={'display': 'flex', 'gap': '16px', 'marginBottom': '20px'}),

            html.Div([
                card(dcc.Graph(figure=fig_pie, config={'displayModeBar': False}), flex=4),

                card([
                    html.H3('Top 10 Causas de Muerte en Colombia 2019', style={
                        'color': TITLE_COLOR, 'fontSize': '14px', 'fontWeight': '600',
                        'margin': '0 0 14px 0', 'fontFamily': FONT,
                    }),
                    dash_table.DataTable(
                        data=top10_causes.to_dict('records'),
                        columns=[
                            {'name': '#',               'id': 'Ranking'},
                            {'name': 'Código',          'id': 'Código'},
                            {'name': 'Causa de Muerte', 'id': 'Nombre'},
                            {'name': 'Casos',           'id': 'Total_Casos', 'type': 'numeric',
                             'format': dash_table.FormatTemplate.money(0).symbol(
                                 dash_table.Format.Symbol.no)},
                        ],
                        style_header={
                            'backgroundColor': '#F8FAFC', 'color': TITLE_COLOR,
                            'fontWeight': '700', 'border': f'1px solid {CARD_BORDER}',
                            'fontSize': '11px', 'padding': '10px 12px', 'fontFamily': FONT,
                        },
                        style_cell={
                            'backgroundColor': CARD_BG, 'color': TEXT_COLOR,
                            'border': f'1px solid {CARD_BORDER}', 'fontSize': '11px',
                            'padding': '9px 12px', 'textAlign': 'left',
                            'maxWidth': '240px', 'overflow': 'hidden',
                            'textOverflow': 'ellipsis', 'fontFamily': FONT,
                        },
                        style_data_conditional=[
                            {'if': {'row_index': 'odd'}, 'backgroundColor': '#F8FAFC'},
                            {'if': {'column_id': 'Total_Casos'},
                             'textAlign': 'right', 'fontWeight': '700', 'color': BLUE},
                            {'if': {'column_id': 'Ranking'},
                             'textAlign': 'center', 'width': '36px', 'color': TEXT_MUTED,
                             'fontWeight': '600'},
                        ],
                        tooltip_data=[
                            {col: {'value': str(row[col]), 'type': 'markdown'}
                             for col in top10_causes.columns}
                            for _, row in top10_causes.iterrows()
                        ],
                        tooltip_duration=None,
                        style_table={'overflowX': 'auto'},
                        page_size=10,
                    ),
                ], flex=6, padding=True),

            ], style={'display': 'flex', 'gap': '16px', 'marginBottom': '20px', 'alignItems': 'stretch'}),

            card(dcc.Graph(figure=fig_stacked, config={'displayModeBar': False})),
            html.Div(style={'marginBottom': '20px'}),

            card(dcc.Graph(figure=fig_hist, config={'displayModeBar': False})),
            html.Div(style={'marginBottom': '20px'}),

            html.Div([
                html.P(
                    'Fuente: DANE — Estadísticas Vitales EEVV 2019  ·  Desarrollado con Python, Dash y Plotly',
                    style={'color': TEXT_MUTED, 'textAlign': 'center',
                           'fontSize': '11px', 'margin': '0', 'fontFamily': FONT},
                ),
            ], style={'borderTop': f'1px solid {CARD_BORDER}', 'padding': '14px 0 6px'}),

        ], style={'padding': '24px 32px'}),

    ], style={
        'marginLeft': SIDEBAR_WIDTH,
        'backgroundColor': MAIN_BG,
        'minHeight': '100vh',
        'fontFamily': FONT,
    }),

], style={
    'fontFamily': FONT,
})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)
