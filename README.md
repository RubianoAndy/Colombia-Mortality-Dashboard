# Colombia Mortality Dashboard

<div align="center">
  <img src="public/UnisalleDarkLogoV1.png" alt="Universidad de La Salle" width="150"/>
  
  **Autor:** Andrés Giovanny Rubiano Muñoz "Andy Rubiano"
  **Correo:** arubiano67@unisalle.edu.co
  **Programa:** Maestría en Inteligencia Artificial
  
  <img src="public/assets/images/author/Andy Rubiano.png" alt="Andy Rubiano" width="150" style="border-radius: 50%; margin-top: 15px;"/>
</div>

---

## 📋 Introducción del Proyecto

El **Colombia Mortality Dashboard** es una aplicación web interactiva desarrollada con Dash y Plotly que permite visualizar y analizar datos de mortalidad en Colombia durante el año 2019. Esta herramienta proporciona insights valiosos sobre patrones de mortalidad, causas de muerte y distribución geográfica en el territorio colombiano.

---

## 🎯 Objetivo

Este proyecto busca:

- **Analizar patrones de mortalidad** en Colombia por departamento, municipio, sexo y grupo de edad
- **Identificar causas principales** de muerte y su distribución geográfica
- **Detectar zonas críticas** con mayores tasas de mortalidad
- **Visualizar tendencias temporales** de mortalidad a lo largo de 2019
- **Facilitar el análisis exploratorio** de datos de mortalidad mediante una interfaz intuitiva
- **Apoyar la toma de decisiones** en políticas de salud pública

---

## 📁 Estructura del Proyecto

```
Colombia-Mortality-Dashboard/
├── app.py                          # Aplicación principal Dash
├── requirements.txt                # Dependencias del proyecto
├── README.md                       # Este archivo
│
├── public/                         # Archivos públicos
│   ├── UnisalleDarkLogoV1.png     # Logo de la universidad
│   └── assets/
│       └── images/
│           └── author/
│               └── Andy Rubiano.png # Foto del autor
│
└── utils/                          # Utilidades y datos
    └── data/
        ├── nofetal2019.csv        # Datos de mortalidad no fetal (2019)
        ├── divipola.csv           # División política administrativa (departamentos y municipios)
        └── codigos_muerte.csv     # Catálogo de códigos de causas de muerte (CIE-10)
```

### Descripción de Archivos Principales:

- **app.py**: Contiene la lógica de la aplicación Dash, incluyendo:
  - Carga y procesamiento de datos
  - Mapeos de códigos a nombres
  - Definición de categorías de edad
  - Generación de visualizaciones interactivas
  
- **utils/data/nofetal2019.csv**: Dataset principal con registros de mortalidad
  
- **utils/data/divipola.csv**: Información de divisiones administrativas para mapeo

- **utils/data/codigos_muerte.csv**: Catálogo de clasificación de causas de muerte

---

## 📦 Requisitos

### Dependencias:

| Librería | Versión | Descripción |
|----------|---------|-------------|
| Dash | 4.1.0 | Framework web para dashboards interactivos |
| Plotly | 6.7.0 | Biblioteca de visualización |
| Pandas | 3.0.2 | Análisis y manipulación de datos |
| Gunicorn | 26.0.0 | Servidor WSGI para producción |

### Requisitos del Sistema:

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Navegador web moderno (Chrome, Firefox, Edge, Safari)

---

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/Colombia-Mortality-Dashboard.git
cd Colombia-Mortality-Dashboard
```

### 2. Crear un entorno virtual (recomendado)

**En Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**En macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar la aplicación localmente

```bash
python app.py
```

La aplicación estará disponible en: `http://localhost:8050`

---

## 💻 Software Utilizado

| Tecnología | Versión | Propósito |
|-----------|---------|----------|
| **Python** | 3.8+ | Lenguaje de programación principal |
| **Dash** | 4.1.0 | Framework para crear dashboards interactivos |
| **Plotly** | 6.7.0 | Visualizaciones interactivas |
| **Pandas** | 3.0.2 | Manipulación y análisis de datos |
| **Gunicorn** | 26.0.0 | Servidor web para producción |
| **Git** | Latest | Control de versiones |

---

## 🌐 Despliegue en Render

Este proyecto está configurado para desplegarse fácilmente en **Render**, una plataforma de hosting moderna.

### Pasos para desplegar:

#### 1. Preparación en el repositorio
Asegúrate de tener:
- `requirements.txt` actualizado ✓
- `app.py` en la raíz del proyecto ✓
- `.gitignore` configurado ✓

#### 2. Crear cuenta en Render
- Ve a [render.com](https://render.com)
- Crea una cuenta gratuita
- Conecta tu repositorio de GitHub

#### 3. Crear un nuevo servicio Web

1. Click en **"New +"** → **"Web Service"**
2. Selecciona tu repositorio
3. Configura los siguientes parámetros:

   - **Name**: `colombia-mortality-dashboard`
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:server`
   - **Plan**: Selecciona según necesidades (Free/Paid)

#### 4. Variables de entorno (si aplica)

En caso de necesitar variables de entorno, añádelas en:
Settings → Environment → Add Environment Variable

#### 5. Deploy automático

- El deploy se inicia automáticamente cuando subes cambios a GitHub
- Puedes visualizar logs en tiempo real desde el dashboard de Render
- Tu aplicación estará disponible en: `https://tu-app.render.com`

#### 6. Monitoreo

- Render proporciona métricas de uso
- Monitorea logs para detectar errores
- El servicio se puede pausar/reanudar desde el dashboard

---

## 📊 Visualizaciones

### 1. Mapa Geográfico de Mortalidad por Departamento

**Descripción:** Visualización de puntos geográficos que representa la distribución total de muertes por departamento en Colombia durante 2019.

**Características:**
- Puntos proporcionados al número de casos de mortalidad
- Coordenadas precisas de cada departamento
- Hover interactivo para ver detalles

**Hallazgos:**
- Concentración de mortalidad en regiones con mayor densidad poblacional
- Variación significativa entre departamentos
- Hotspots de mortalidad identificables geográficamente

---

### 2. Línea Temporal: Mortalidad por Mes

**Descripción:** Gráfico de líneas que muestra la tendencia de mortalidad a lo largo de los 12 meses de 2019.

**Características:**
- Visualización mes a mes del total de casos
- Identificación de picos y valles estacionales
- Tendencia general observable

**Hallazgos:**
- Variaciones estacionales en tasas de mortalidad
- Identificación de meses críticos
- Patrones que pueden correlacionar con factores externos

---

### 3. Ciudades más Violentas (Homicidios)

**Descripción:** Gráfico de barras con las 5 ciudades que presentan mayor número de homicidios (códigos X95 en clasificación CIE-10).

**Características:**
- Ranking de municipios por número de homicidios
- Comparativa clara entre ciudades
- Datos enfocados en violencia homicida

**Hallazgos:**
- Zonas de conflicto identificadas
- Diferencias significativas entre municipios
- Necesidad de intervenciones específicas en ciudades críticas

---

### 4. Ciudades con Menor Mortalidad

**Descripción:** Gráfico de pastel (pie chart) que distribuye las 10 ciudades con menor tasa de mortalidad en 2019.

**Características:**
- Visualización proporcional de casos
- Identificación de municipios con mejor indicadores
- Comparativa de distribución

**Hallazgos:**
- Municipios con índices de salud más altos
- Diferencias entre regiones rurales y urbanas
- Posibles modelos a replicar

---

### 5. Tabla de Causas Principales de Muerte

**Descripción:** Tabla interactiva que lista las principales causas de mortalidad clasificadas según CIE-10.

**Características:**
- Ordenamiento por frecuencia
- Códigos CIE-10 con descripciones
- Total de casos por causa

**Hallazgos:**
- Causas naturales dominan el registro
- Variación por grupo demográfico
- Oportunidades de prevención identificadas

---

## 📈 Análisis por Categorías de Edad

El proyecto categoriza la población en grupos de edad con significado epidemiológico:

- **Mortalidad neonatal**: 0-28 días
- **Mortalidad infantil**: 29 días - 1 año
- **Primera infancia**: 1-2 años
- **Niñez**: 3-5 años
- **Adolescencia**: 6-11 años
- **Juventud**: 12-18 años
- **Adultez temprana**: 19-26 años
- **Adultez intermedia**: 27-59 años
- **Vejez**: 60-74 años
- **Longevidad/Centenarios**: 75+ años

---

## 🔍 Fuentes de Datos

- **nofetal2019.csv**: Registros de mortalidad no fetal en Colombia (año 2019)
- **divipola.csv**: Base de datos de división política administrativa
- **codigos_muerte.csv**: Clasificación Internacional de Enfermedades (CIE-10)

---

## 📝 Notas Importantes

- Los datos corresponden exclusivamente al año 2019
- La clasificación de causas sigue estándares CIE-10 internacionales
- Los municipios se identifican mediante códigos DANE
- Las categorías de edad utilizan criterios epidemiológicos estándar
- La aplicación requiere conexión a internet para algunas funciones de Plotly

---

## 🛠️ Desarrollo Futuro

Posibles mejoras y expansiones:

- [ ] Agregar datos de años adicionales para análisis longitudinal
- [ ] Implementar predicciones con Machine Learning
- [ ] Añadir filtros avanzados y búsqueda
- [ ] Generar reportes exportables en PDF
- [ ] Análisis por causas prevenibles
- [ ] Integración con APIs de datos en tiempo real
- [ ] Dashboard mobile responsivo mejorado
- [ ] Análisis de correlaciones con variables socioeconómicas

---

## 📧 Contacto

**Autor:** Andy Rubiano  
**Programa:** Maestría en Inteligencia Artificial  
**Universidad:** Universidad de La Salle

---

## 📄 Licencia

Este proyecto está disponible bajo licencia a especificar. Para más información, contacta al autor.

---

<div align="center">
  
  **Desarrollado con ❤️ | Universidad de La Salle**
  
</div>
