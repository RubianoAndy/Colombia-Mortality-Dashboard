"""
app.py
------
Punto de entrada de la aplicación Dash.

Inicializa la aplicación Dash con Plotly, configura el servidor, establece el layout
y registra todos los callbacks para la interactividad del dashboard de mortalidad en Colombia.

Para ejecutar la aplicación: http://localhost:8050/
"""

from src.dashboard import app, server

__all__ = ['app', 'server']

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)
