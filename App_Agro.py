import streamlit as st
import os
from google import genai
from google.genai import types

# 1. configuracion identidad de la pagina
st.set_page_config(
    page_title="Agro Vicente - Sistema de Análisis", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# interfaz 
st.markdown("""
    <style>
    /* Cambiar el fondo de la aplicación */
    .stApp {
        background-color: #f8f9fa;
    }
    /* Estilo para centrar títulos */
    .titulo-principal {
        text-align: center;
        color: #1b4332; /* Verde agro profundo */
        font-family: 'Helvetica Neue', Arial, sans-serif;
        font-weight: 700;
        margin-bottom: 5px;
    }
    .subtitulo-principal {
        text-align: center;
        color: #495057;
        font-family: 'Helvetica Neue', Arial, sans-serif;
        font-size: 1.1rem;
        margin-bottom: 40px;
    }
    /* Encabezados de sección */
    .seccion-header {
        color: #2d6a4f;
        font-family: 'Helvetica Neue', Arial, sans-serif;
        border-bottom: 2px solid #d8f3dc;
        padding-bottom: 8px;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    /* Botón personalizado */
    .stButton>button {
        background-color: #1b4332;
        color: white;
        border-radius: 4px;
        border: none;
        padding: 10px 24px;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #2d6a4f;
        color: white;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# Títulos Centrados
st.markdown("<h1 class='titulo-principal'>AGRO VICENTE</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitulo-principal'>Plataforma de Diagnóstico Tecnológico para Cultivos - Departamento de Santander</p>", unsafe_allow_html=True)



api_key_actual = None


if "api_key" in st.secrets:
    api_key_actual = st.secrets["api_key"]


elif os.path.exists("api_key.txt"):
    with open("api_key.txt", "r") as f:
        api_key_actual = f.read().strip()


# SECCIÓN 1: INGRESO DE VARIABLES DE MEDICIÓN

st.markdown("<h3 class='seccion-header'>1. Parámetros e Información del Cultivo</h3>", unsafe_allow_html=True)

# Organización en columnas optimizadas
col_izq, col_der = st.columns(2)

with col_izq:
    cultivo = st.text_input("Especificar Cultivo:", placeholder="Ej. Plátano Popocho, Tomate, Cacao, Pepino...")
    temperatura = st.number_input("Temperatura Ambiental (°C):", min_value=0.0, max_value=50.0, value=26.0, step=0.1)
    humedad = st.slider("Humedad Relativa (%):", min_value=0, max_value=100, value=65)

with col_der:
    ph = st.number_input("Potencial de Hidrógeno (pH):", min_value=0.0, max_value=14.0, value=6.2, step=0.1)
    ec = st.number_input("Conductividad Eléctrica (EC en mS/cm):", min_value=0.0, max_value=10.0, value=1.8, step=0.1)
    
    # Agrupación de Macronutrientes en subcolumnas
    sub_col1, sub_col2 = st.columns(2)
    with sub_col1:
        nitrogeno = st.number_input("Nitrógeno disponible (N - ppm):", min_value=0, max_value=500, value=60)
    with sub_col2:
        fosforo = st.number_input("Fósforo disponible (P - ppm):", min_value=0, max_value=500, value=35)


# SECCIÓN 2: PROCESAMIENTO Y DIAGNÓSTICO

st.markdown("<h3 class='seccion-header'>2. Evaluación y Reporte Técnico</h3>", unsafe_allow_html=True)

if st.button("Ejecutar Análisis Agronómico"):
    
    # Validaciones de consistencia de datos
    if not cultivo:
        st.error("Error: El campo de especificación del cultivo no puede estar vacío.")
    elif not api_key_actual:
        st.error("Error de Configuración: No se detectó la llave de acceso en el archivo 'api_key.txt'.")
    else:
        # Estructura del reporte de datos estructurados para la IA
        datos_sensores = f"""
        Datos técnicos reportados:
        - Cultivo objetivo: {cultivo}
        - Región geográfica: Departamento de Santander, Colombia
        - Temperatura: {temperatura} °C
        - Humedad Relativa: {humedad} %
        - pH medido: {ph}
        - Conductividad Eléctrica (EC): {ec} mS/cm
        - Concentración de Nitrógeno (N): {nitrogeno} ppm
        - Concentración de Fósforo (P): {fosforo} ppm
        """
        
        # Directriz estricta del comportamiento del sistema
        INSTRUCCION_SISTEMA = """
        Actúa bajo el rol de 'Agro Vicente', un consultor senior e ingeniero agrónomo especialista en agricultura de precisión, sistemas hidropónicos y edafología en las subregiones del departamento de Santander (Mesa de los Santos, Provincia de Soto, Comunera, Mares, etc.).
        
        Tu tarea consiste en procesar las métricas de sensores provistas para cualquier cultivo especificado y generar un reporte técnico formal.
        
        Estructura obligatoria del reporte:
        1. ### EVALUACIÓN DE PARÁMETROS: Contrasta cada una de las variables ingresadas con los requerimientos óptimos de la literatura agronómica para el cultivo en mención. Determina qué variables se encuentran en estado óptimo, crítico o deficitario.
        2. ### DIAGNÓSTICO TÉCNICO: Explica el impacto fisiológico que tienen las anomalías encontradas (ej. cómo afecta un pH inadecuado a la absorción del fósforo o cómo influye la EC en la presión osmótica de las raíces). Ten en cuenta las condiciones climáticas de Santander.
        3. ### PLAN DE ACCIÓN Y RECOMENDACIONES: Provee directrices correctivas claras, detalladas y aplicables (ej. dosificación de soluciones, lixiviación de sales, enmiendas o ajustes térmicos/humedad si aplica).
        
        Mantén un tono estrictamente profesional, analítico y científico. Evita el uso de terminología informal o decoraciones innecesarias.
        """

        try:
            with st.spinner("Procesando datos y generando curvas de análisis..."):
                # Inicialización del cliente con el modelo 
                client = genai.Client(api_key=api_key_actual)
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash',  # Versión con cuotas operativas estables
                    contents=datos_sensores,
                    config=types.GenerateContentConfig(
                        system_instruction=INSTRUCCION_SISTEMA,
                        temperature=0.15  # Máxima precisión técnica, mínima variabilidad
                    )
                )
                
                # Despliegue del informe técnico en pantalla
                st.markdown("---")
                st.info("Informe Técnico Generado Exitosamente")
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"Fallo en la comunicación con el servidor de análisis: {e}")



 
