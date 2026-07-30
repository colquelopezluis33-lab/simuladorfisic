import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

# Configuracion de la pagina
st.set_page_config(page_title="Simulador de Fisica", layout="wide")

# Estilos CSS personalizados para un aspecto profesional y academico
st.markdown("""
    <style>
    .stApp {
        background-color: #f8f9fa;
    }
    h1, h2, h3 {
        color: #2c3e50;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: #e9ecef;
        border-radius: 5px 5px 0px 0px;
        padding: 10px 20px;
        font-weight: 600;
        color: #495057;
        border: 1px solid #dee2e6;
        border-bottom: none;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2c3e50 !important;
        color: #ffffff !important;
    }
    .metric-box {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border-left: 5px solid #3498db;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Funcion para generar descargar de CSV
@st.cache_data
def convertir_df(df):
    return df.to_csv(index=False).encode('utf-8')

# Funcion para configurar la grafica estilo papel milimetrado
def configurar_grafica(ax, xlabel, ylabel, title):
    ax.set_title(title, fontsize=14, fontweight="bold", color="#2c3e50")
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.axhline(0, color='black', linewidth=1.5)
    ax.axvline(0, color='black', linewidth=1.5)
    ax.grid(True, which='major', color='#bdc3c7', linewidth=1.0)
    ax.grid(True, which='minor', color='#ecf0f1', linewidth=0.5, linestyle='-')
    ax.minorticks_on()
    ax.set_facecolor('#ffffff')

# Titulo Principal
st.markdown("<h1>Simulador Interactivo de Cinemática Aplicada</h1>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 18px; color: #7f8c8d;'>desarrrollado en UTEPSA</p>", unsafe_allow_html=True)
st.markdown("---")

# Creacion de Pestañas
tab_mru, tab_mrua, tab_para = st.tabs(["Movimiento Rectilíneo Uniforme (MRU)", "Movimiento Uniformemente Acelerado (MRUA)", "Movimiento Parabólico"])

# ==========================================
# MODULO 1: MRU
# ==========================================
with tab_mru:
    st.markdown("<h3>Análisis de MRU</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("**Calculadora de Variables**")
        incognita_mru = st.selectbox("Seleccione la variable a calcular:", ["Distancia (x)", "Velocidad (v)", "Tiempo (t)"])
        
        if incognita_mru == "Distancia (x)":
            st.latex(r"x = v \cdot t")
            v = st.number_input("Velocidad (m/s)", value=10.0, step=1.0)
            t = st.number_input("Tiempo (s)", min_value=0.1, value=5.0, step=0.5)
            x = v * t
            st.markdown(f"<div class='metric-box'><b>Distancia calculada:</b><br><span style='font-size: 24px; color: #2980b9;'>{x:.2f} m</span></div>", unsafe_allow_html=True)
            
        elif incognita_mru == "Velocidad (v)":
            st.latex(r"v = \frac{x}{t}")
            x = st.number_input("Distancia (m)", value=50.0, step=1.0)
            t = st.number_input("Tiempo (s)", min_value=0.1, value=5.0, step=0.5)
            v = x / t
            st.markdown(f"<div class='metric-box'><b>Velocidad calculada:</b><br><span style='font-size: 24px; color: #2980b9;'>{v:.2f} m/s</span></div>", unsafe_allow_html=True)
            
        elif incognita_mru == "Tiempo (t)":
            st.latex(r"t = \frac{x}{v}")
            x = st.number_input("Distancia (m)", value=50.0, step=1.0)
            v = st.number_input("Velocidad (m/s)", min_value=0.1, value=10.0, step=1.0)
            t = x / v
            st.markdown(f"<div class='metric-box'><b>Tiempo calculado:</b><br><span style='font-size: 24px; color: #2980b9;'>{t:.2f} s</span></div>", unsafe_allow_html=True)

    with col2:
        # Generar datos para la grafica
        t_arr = np.linspace(0, t, 50)
        x_arr = v * t_arr
        
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(t_arr, x_arr, color="#e74c3c", linewidth=2.5)
        configurar_grafica(ax, "Tiempo (s)", "Posición X (m)", "Gráfica Posición vs Tiempo (MRU)")
        st.pyplot(fig)
        
        # Tabla de datos
        df_mru = pd.DataFrame({"Tiempo (s)": np.round(t_arr, 2), "Posición X (m)": np.round(x_arr, 2)})
        st.dataframe(df_mru, use_container_width=True)
        st.download_button("Descargar Tabla CSV", convertir_df(df_mru), "datos_mru.csv", "text/csv")

# ==========================================
# MODULO 2: MRUA
# ==========================================
with tab_mrua:
    st.markdown("<h3>Análisis de MRUA</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("**Calculadora de Variables**")
        incognita_mrua = st.selectbox("Seleccione lo que desea calcular:", ["Velocidad Final y Distancia", "Aceleración y Distancia"])
        
        if incognita_mrua == "Velocidad Final y Distancia":
            st.latex(r"v_f = v_0 + a \cdot t")
            st.latex(r"x = x_0 + v_0 \cdot t + \frac{1}{2} a \cdot t^2")
            v0 = st.number_input("Velocidad Inicial (m/s)", value=0.0, step=1.0, key="v0_mrua1")
            a = st.number_input("Aceleración (m/s²)", value=2.0, step=0.5)
            t_mrua = st.number_input("Tiempo (s)", min_value=0.1, value=5.0, step=0.5, key="t_mrua1")
            
            vf = v0 + (a * t_mrua)
            x_mrua = (v0 * t_mrua) + (0.5 * a * t_mrua**2)
            
            st.markdown(f"<div class='metric-box'><b>Resultados:</b><br>Velocidad Final: <span style='color: #2980b9;'>{vf:.2f} m/s</span><br>Distancia: <span style='color: #2980b9;'>{x_mrua:.2f} m</span></div>", unsafe_allow_html=True)
            
        elif incognita_mrua == "Aceleración y Distancia":
            st.latex(r"a = \frac{v_f - v_0}{t}")
            st.latex(r"x = \frac{v_0 + v_f}{2} \cdot t")
            v0 = st.number_input("Velocidad Inicial (m/s)", value=0.0, step=1.0, key="v0_mrua2")
            vf_input = st.number_input("Velocidad Final (m/s)", value=10.0, step=1.0)
            t_mrua = st.number_input("Tiempo (s)", min_value=0.1, value=5.0, step=0.5, key="t_mrua2")
            
            a = (vf_input - v0) / t_mrua
            x_mrua = ((v0 + vf_input) / 2) * t_mrua
            
            st.markdown(f"<div class='metric-box'><b>Resultados:</b><br>Aceleración: <span style='color: #2980b9;'>{a:.2f} m/s²</span><br>Distancia: <span style='color: #2980b9;'>{x_mrua:.2f} m</span></div>", unsafe_allow_html=True)

    with col2:
        t_arr_a = np.linspace(0, t_mrua, 50)
        x_arr_a = (v0 * t_arr_a) + (0.5 * a * t_arr_a**2)
        v_arr_a = v0 + (a * t_arr_a)
        
        fig2, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
        
        ax1.plot(t_arr_a, x_arr_a, color="#27ae60", linewidth=2.5)
        configurar_grafica(ax1, "Tiempo (s)", "Posición X (m)", "Posición vs Tiempo")
        
        ax2.plot(t_arr_a, v_arr_a, color="#8e44ad", linewidth=2.5)
        configurar_grafica(ax2, "Tiempo (s)", "Velocidad (m/s)", "Velocidad vs Tiempo")
        
        plt.tight_layout()
        st.pyplot(fig2)
        
        df_mrua = pd.DataFrame({"Tiempo (s)": np.round(t_arr_a, 2), "Posición X (m)": np.round(x_arr_a, 2), "Velocidad (m/s)": np.round(v_arr_a, 2)})
        st.dataframe(df_mrua, use_container_width=True)
        st.download_button("Descargar Tabla CSV", convertir_df(df_mrua), "datos_mrua.csv", "text/csv", key="csv_mrua")

# ==========================================
# MODULO 3: MOVIMIENTO PARABOLICO
# ==========================================
with tab_para:
    st.markdown("<h3>Análisis de Movimiento Parabólico</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("**Parámetros Iniciales**")
        v0_p = st.number_input("Velocidad Inicial (m/s)", min_value=1.0, value=20.0, step=1.0)
        angulo = st.number_input("Ángulo de disparo (°)", min_value=1.0, max_value=89.0, value=45.0, step=1.0)
        gravedad = st.radio("Aceleración de la Gravedad (m/s²)", [9.81, 10.0])
        
        # Calculos
        theta_rad = math.radians(angulo)
        v0x = v0_p * math.cos(theta_rad)
        v0y = v0_p * math.sin(theta_rad)
        
        t_vuelo = (2 * v0y) / gravedad
        x_max = (v0_p**2 * math.sin(2 * theta_rad)) / gravedad
        y_max = (v0y**2) / (2 * gravedad)
        
        st.markdown("**Resultados Calculados:**")
        st.latex(r"t_{vuelo} = \frac{2 \cdot v_{0y}}{g}")
        st.markdown(f"<div class='metric-box'><b>Tiempo de vuelo:</b> <span style='color: #2980b9;'>{t_vuelo:.2f} s</span></div>", unsafe_allow_html=True)
        
        st.latex(r"x_{max} = \frac{v_0^2 \cdot \sin(2\theta)}{g}")
        st.markdown(f"<div class='metric-box'><b>Alcance horizontal máximo:</b> <span style='color: #2980b9;'>{x_max:.2f} m</span></div>", unsafe_allow_html=True)
        
        st.latex(r"y_{max} = \frac{v_{0y}^2}{2g}")
        st.markdown(f"<div class='metric-box'><b>Altura máxima:</b> <span style='color: #2980b9;'>{y_max:.2f} m</span></div>", unsafe_allow_html=True)

    with col2:
        t_arr_p = np.linspace(0, t_vuelo, 100)
        x_arr_p = v0x * t_arr_p
        y_arr_p = (v0y * t_arr_p) - (0.5 * gravedad * t_arr_p**2)
        
        fig3, ax3 = plt.subplots(figsize=(8, 4))
        ax3.plot(x_arr_p, y_arr_p, color="#d35400", linewidth=2.5)
        
        # Marcar punto de altura maxima
        idx_ymax = np.argmax(y_arr_p)
        ax3.plot(x_arr_p[idx_ymax], y_arr_p[idx_ymax], marker='o', markersize=8, color="black", label=f"Altura Máx: {y_max:.2f}m")
        ax3.legend()
        
        configurar_grafica(ax3, "Distancia Horizontal X (m)", "Altura Y (m)", "Plano Cartesiano: Trayectoria Parabólica")
        st.pyplot(fig3)
        
        df_para = pd.DataFrame({"Tiempo (s)": np.round(t_arr_p, 2), "Distancia X (m)": np.round(x_arr_p, 2), "Altura Y (m)": np.round(y_arr_p, 2)})
        st.dataframe(df_para, use_container_width=True)
        st.download_button("Descargar Tabla CSV", convertir_df(df_para), "datos_parabolico.csv", "text/csv", key="csv_para") 
       st.markdown(
    """
    <hr>
    <div style="text-align: center; margin-top: 40px; padding: 15px; font-family: Arial, sans-serif; font-size: 13px; color: #444;">
        <p><strong>Proyecto Final de Física - Cinemática</strong></p>
        <p>Desarrollado por: <strong>Luis Emilio Colque Lopez</strong> | Ingeniería Mecánica Automotriz y Agroindustrial - UTEPSA</p>
    </div>
    """,
    unsafe_allow_html=True
)
