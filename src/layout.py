from dash import dcc, html, dash_table

from src.theme import (
    SIDEBAR_BG, SIDEBAR_TEXT, SIDEBAR_MUTED, GOLD,
    MAIN_BG, CARD_BG, CARD_BORDER, TITLE_COLOR, TEXT_MUTED, BLUE,
    FONT, dd_style, dd_container_style,
    kpi_card, card,
)
from src.data import LOGO_SRC, AUTHOR_SRC, municipios_options, meses_options

SIDEBAR_WIDTH = '240px'

layout = html.Div([
    html.Div([
        html.Div([
            html.A(
                href='https://lasalle.edu.co/',
                target='_blank',
                rel='noopener noreferrer',
                style={'cursor': 'pointer', 'display': 'block'},
                children=html.Img(src=LOGO_SRC, style={
                    'width': '82%', 'maxWidth': '165px',
                    'display': 'block', 'margin': '0 auto',
                })
            ) if LOGO_SRC else html.Div([
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

            html.Div('FILTROS', style={
                'color': SIDEBAR_MUTED,
                'fontSize': '10px',
                'fontWeight': '700',
                'letterSpacing': '1.4px',
                'marginBottom': '14px',
            }),

            html.Div([
                html.Label('🏙️  Ciudad / Municipio', style={
                    'color': SIDEBAR_TEXT,
                    'fontSize': '11px',
                    'fontWeight': '600',
                    'display': 'block',
                    'marginBottom': '6px',
                    'letterSpacing': '0.3px',
                }),
                dcc.Dropdown(
                    id='filter-municipio',
                    options=municipios_options,
                    value=[],
                    multi=True,
                    placeholder='Todos los municipios',
                    searchable=True,
                    clearable=True,
                    style=dd_style,
                    className='sidebar-dropdown',
                ),
            ], style=dd_container_style),

            html.Div([
                html.Label('📅  Mes', style={
                    'color': SIDEBAR_TEXT,
                    'fontSize': '11px',
                    'fontWeight': '600',
                    'display': 'block',
                    'marginBottom': '6px',
                    'letterSpacing': '0.3px',
                }),
                dcc.Dropdown(
                    id='filter-mes',
                    options=meses_options,
                    value=[],
                    multi=True,
                    placeholder='Todos los meses',
                    searchable=False,
                    clearable=True,
                    style=dd_style,
                    className='sidebar-dropdown',
                ),
            ], style=dd_container_style),

            html.Button(
                '✕  Limpiar filtros',
                id='btn-clear',
                n_clicks=0,
                style={
                    'width': '100%',
                    'padding': '8px 0',
                    'backgroundColor': 'transparent',
                    'color': SIDEBAR_MUTED,
                    'border': '1px solid rgba(255,255,255,0.12)',
                    'borderRadius': '6px',
                    'cursor': 'pointer',
                    'fontSize': '11px',
                    'fontWeight': '600',
                    'letterSpacing': '0.4px',
                    'marginTop': '4px',
                    'fontFamily': FONT,
                    'transition': 'all 0.2s',
                },
            ),

        ], style={
            'padding': '20px 18px',
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
                    html.P('Analista de datos', style={'color': SIDEBAR_MUTED,
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

    html.Div([
        html.Div([
            html.H1('MORTALIDAD EN COLOMBIA — 2019', style={
                'margin': '0', 'fontSize': '22px', 'fontWeight': '800',
                'color': TITLE_COLOR, 'letterSpacing': '0.8px',
            }),
            html.P('Por Andy Rubiano | Fuente: DANE — Estadísticas Vitales EEVV', style={
                'color': TEXT_MUTED, 'margin': '5px 0 0 0', 'fontSize': '13px',
            }),
        ], style={
            'backgroundColor': CARD_BG, 'padding': '22px 32px',
            'borderBottom': f'1px solid {CARD_BORDER}',
            'boxShadow': '0 1px 4px rgba(0,0,0,0.05)', 'fontFamily': FONT,
        }),

        html.Div([

            html.Div([
                kpi_card('📊', '', 'Total Defunciones',   card_id='kpi-total'),
                kpi_card('⚠️',  '', 'Homicidios (X95)',   card_id='kpi-homicidios'),
                kpi_card('🏛️', '', 'Departamentos',       card_id='kpi-departamentos'),
                kpi_card('🏙️', '', 'Municipios',          card_id='kpi-municipios'),
            ], style={'display': 'flex', 'gap': '16px', 'marginBottom': '20px', 'flexWrap': 'wrap'}),

            card(dcc.Graph(id='fig-map', config={'scrollZoom': True, 'displayModeBar': False}),
                 flex=1),
            html.Div(style={'marginBottom': '20px'}),

            html.Div([
                card(dcc.Graph(id='fig-line',    config={'displayModeBar': False}), flex=6),
                card(dcc.Graph(id='fig-violent', config={'displayModeBar': False}), flex=4),
            ], style={'display': 'flex', 'gap': '16px', 'marginBottom': '20px'}),

            html.Div([
                card(dcc.Graph(id='fig-pie', config={'displayModeBar': False}), flex=4),

                card([
                    html.H3('Top 10 Causas de Muerte en Colombia 2019', style={
                        'color': TITLE_COLOR, 'fontSize': '14px', 'fontWeight': '600',
                        'margin': '0 0 14px 0', 'fontFamily': FONT,
                    }),
                    dash_table.DataTable(
                        id='table-causes',
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
                            'backgroundColor': CARD_BG, 'color': TEXT_MUTED,
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
                        tooltip_duration=None,
                        style_table={'overflowX': 'auto'},
                        page_size=10,
                    ),
                ], flex=6, padding=True),

            ], style={'display': 'flex', 'gap': '16px', 'marginBottom': '20px', 'alignItems': 'stretch'}),

            card(dcc.Graph(id='fig-stacked', config={'displayModeBar': False})),
            html.Div(style={'marginBottom': '20px'}),

            card(dcc.Graph(id='fig-hist', config={'displayModeBar': False})),
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

], style={'fontFamily': FONT})
