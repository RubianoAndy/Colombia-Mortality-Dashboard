from dash import html

SIDEBAR_BG          = '#002D57'
SIDEBAR_ACTIVE_BG   = '#FFCD00'
SIDEBAR_ACTIVE_TEXT = '#002D57'
SIDEBAR_TEXT        = '#FFFFFF'
SIDEBAR_MUTED       = '#7A99B8'

MAIN_BG     = '#E6E6E6'
CARD_BG     = '#FFFFFF'
CARD_BORDER = '#E1E5EE'
SHADOW      = '0 2px 12px rgba(0,0,0,0.07)'

TITLE_COLOR = '#002D57'
TEXT_COLOR  = '#3D4A5C'
TEXT_MUTED  = '#94A3B8'

GOLD   = '#FFCD00'
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

dd_style = {
    'backgroundColor': '#01376B',
    'border': '1px solid rgba(255,255,255,0.18)',
    'borderRadius': '6px',
    'color': SIDEBAR_TEXT,
    'fontSize': '12px',
}
dd_container_style = {'marginBottom': '18px'}

def title_cfg(text):
    """
    Crea la configuración de título para gráficos de Plotly.
    
    Genera un diccionario con la configuración de fuente y color para títulos
    de gráficos, asegurando consistencia de estilo en todo el dashboard.
    
    Parámetros
    ----------
    text : str
        Texto del título del gráfico.
    
    Retorna
    -------
    dict
        Configuración de título con fuente, tamaño y color.
    """
    
    return dict(text=text, font=dict(size=14, color=TITLE_COLOR, weight=600))


def kpi_card(icon, value, label, card_id=None):
    """
    Crea una tarjeta KPI (Indicador Clave de Rendimiento) con ícono, valor y etiqueta.
    
    Construye un componente HTML que muestra un KPI con un ícono emoji, un valor
    numérico grande y una etiqueta descriptiva, con estilos consistentes.
    
    Parámetros
    ----------
    icon : str
        Ícono o emoji a mostrar en la tarjeta.
    value : str o int
        Valor numérico del KPI.
    label : str
        Etiqueta descriptiva del KPI.
    card_id : str, opcional
        ID HTML para el elemento del valor (permite actualización dinámica).
    
    Retorna
    -------
    html.Div
        Componente Dash HTML con la tarjeta KPI estilizada.
    """

    return html.Div([
        html.Div(icon, style={'fontSize': '26px', 'marginBottom': '10px'}),
        html.Div(value, id=card_id, style={
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
    """
    Envuelve contenido en un contenedor con estilo de tarjeta del dashboard.

    Parámetros
    ----------
    children : any
        Contenido Dash que se renderizará dentro de la tarjeta.
    flex : int o float, opcional
        Valor CSS flex para controlar el ancho relativo. Por defecto 1.
    padding : bool, opcional
        Si es True, aplica padding interno de 20px. Por defecto False.
    min_w : str, opcional
        Ancho mínimo CSS de la tarjeta (p. ej. '300px'). Por defecto '0'.

    Retorna
    -------
    html.Div
        Componente Dash HTML estilizado como tarjeta.
    """

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
