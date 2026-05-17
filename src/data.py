import os
import json
import base64
import pandas as pd

_SRC_DIR   = os.path.dirname(__file__)
_BASE_DIR  = os.path.dirname(_SRC_DIR)
DATA_DIR   = os.path.join(_BASE_DIR, 'utils', 'data')
PUBLIC_DIR = os.path.join(_BASE_DIR, 'public')


def encode_image(path):
    """
    Codifica una imagen en base64 para incrustarla en HTML.
    
    Lee el archivo de imagen de la ruta especificada, lo convierte a base64
    y genera una cadena de datos de URI compatible con navegadores web.
    
    Parámetros
    ----------
    path : str
        Ruta absoluta o relativa al archivo de imagen.
    
    Retorna
    -------
    str
        Cadena de datos URI (data:image/[formato];base64,[datos]) o cadena vacía
        si el archivo no existe.
    """
    
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

meses = {
    1: 'Enero',    2: 'Febrero',   3: 'Marzo',     4: 'Abril',
    5: 'Mayo',     6: 'Junio',     7: 'Julio',      8: 'Agosto',
    9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre',
}
df['MES_NOMBRE'] = df['MES'].map(meses)

cod_map  = cod.dropna(subset=['Codigo4']).set_index('Codigo4')['Desc4'].to_dict()
cod3_map = cod.dropna(subset=['Codigo3']).drop_duplicates('Codigo3').set_index('Codigo3')['Desc3'].to_dict()

edad_cats = {
    'Mortalidad neonatal':      [0, 1, 2, 3, 4],
    'Mortalidad infantil':      [5, 6],
    'Primera infancia':         [7, 8],
    'Niñez':                    [9, 10],
    'Adolescencia':             [11],
    'Juventud':                 [12, 13],
    'Adultez temprana':         [14, 15, 16],
    'Adultez intermedia':       [17, 18, 19],
    'Vejez':                    [20, 21, 22, 23, 24],
    'Longevidad / Centenarios': [25, 26, 27, 28],
    'Edad desconocida':         [29],
}
edad_reverse = {c: cat for cat, codes in edad_cats.items() for c in codes}
df['CATEGORIA_EDAD'] = df['GRUPO_EDAD1'].map(edad_reverse)
cat_order = list(edad_cats.keys())

dept_coords = {
    91: (-1.44, -71.57),  5: (6.88, -75.83),   8: (10.66, -75.00),
    11: (4.65, -74.08),  13: (8.67, -74.03),  15: (5.89, -73.36),
    17: (5.30, -75.36),  18: (1.37, -75.61),  19: (2.45, -76.82),
    20: (9.34, -73.52),  23: (8.35, -75.73),  25: (5.03, -74.03),
    27: (5.69, -76.66),  41: (2.53, -75.53),  44: (11.35, -72.09),
    47: (10.19, -74.15), 50: (3.27, -73.08),  52: (1.60, -78.09),
    54: (7.95, -72.50),  63: (4.46, -75.67),  66: (4.99, -75.70),
    68: (6.95, -73.13),  70: (8.81, -75.39),  73: (3.89, -75.23),
    76: (3.80, -76.64),  81: (7.08, -70.76),  85: (5.34, -72.39),
    86: (1.15, -76.65),  88: (12.58, -81.72), 94: (2.58, -68.23),
    95: (2.57, -72.64),  97: (1.25, -70.23),  99: (4.44, -69.29),
}

with open(os.path.join(DATA_DIR, 'Colombia.geo.json'), encoding='utf-8') as _f:
    colombia_geojson = json.load(_f)

dept_codes = {str(feat['properties']['DPTO']): feat['properties']['NOMBRE_DPT']
              for feat in colombia_geojson['features']}

municipios_options = sorted([
    {'label': m, 'value': m}
    for m in df['MUNICIPIO'].dropna().unique()
], key=lambda x: x['label'])

meses_options = [
    {'label': meses[i], 'value': i}
    for i in sorted(meses.keys())
]
