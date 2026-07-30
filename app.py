import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Simulador de Física para Ingeniería",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("⚙️ Simulador Interactivo de Física Aplicada")
st.caption("Herramienta computacional para análisis de Cinemática, Dinámica y Aplicaciones de Ingeniería")

# --- CREACIÓN DE PESTAÑAS (MÓDULOS) ---
tab1, tab2, tab3 = st.tabs([
    "🚀 1. Tiro Parabólico", 
    "🏎️ 2. Frenado Vehicular", 
    "📐 3. Plano Inclinado"
])

# ==========================================
# MÓDULO 1: TIRO PARABÓLICO
# ==========================================
with tab1:
    st.header("Módulo 1: Cinemática y Tiro Parabólico")
    st.write("Modifica los parámetros en la barra lateral para simular la trayectoria del proyectil.")
    
    # Controles en la barra lateral
    st.sidebar.markdown("---")
    st.sidebar.subheader("🚀 Parámetros: Tiro Parabólico")
    v0_m1 = st.sidebar.slider("Velocidad Inicial (m/s)", 1.0, 100.0, 35.0, 1.0, key="v0_m1")
    angulo_m1 = st.sidebar.slider("Ángulo de Disparo (°)", 5.0, 85.0, 45.0, 1.0, key="ang_m1")
    g_m1 = st.sidebar.slider("Gravedad (m/s²)", 1.0, 20.0, 9.81, 0.1, key="g_m1")
    
    # Cálculos
    rad_m1 = np.radians(angulo_m1)
    t_vuelo = 2 * v0_m1 * np.sin(rad_m1) / g_m1
    x_max = (v0_m1**2) * np.sin(2 * rad_m1) / g_m1
    y_max = (v0_m1**2) * (np.sin(rad_m1)**2) / (2 * g_m1)
    
    t_vec = np.linspace(0, t_vuelo, 200)
    x_vec = v0_m1 * np.cos(rad_m1) * t_vec
    y_vec = v0_m1 * np.sin(rad_m1) * t_vec - 0.5 * g_m1 * (t_vec**2)
    
    # Métricas
    col1, col2, col3 = st.columns(3)
    col1.metric("📏 Alcance Horizontal Máximo", f"{x_max:.2f} m")
    col2.metric("🏔️ Altura Máxima", f"{y_max:.2f} m")
    col3.metric("⏱️ Tiempo de Vuelo", f"{t_vuelo:.2f} s")
    
    # Gráfica
    fig1, ax1 = plt.subplots(figsize=(9, 4))
    ax1.plot(x_vec, y_vec, color="#1f77b4", lw=2.5, label="Trayectoria Ideal")
    ax1.fill_between(x_vec, y_vec, color="#1f77b4", alpha=0.15)
    ax1.scatter([x_max/2], [y_max], color="red", zorder=5, label=f"Punto Alto ({y_max:.1f} m)")
    ax1.set_title("Trayectoria del Movimiento", fontsize=12, fontweight='bold')
    ax1.set_xlabel("Distancia X (m)")
    ax1.set_ylabel("Altura Y (m)")
    ax1.set_ylim(bottom=0)
    ax1.grid(True, ls="--", alpha=0.6)
    ax1.legend()
    st.pyplot(fig1)

# ==========================================
# MÓDULO 2: FRENADO VEHICULAR
# ==========================================
with tab2:
    st.header("Módulo 2: Dinámica Vehicular y Distancia de Frenado")
    st.write("Calcula la distancia total de detención combinando el tiempo de percepción del conductor y la fricción del pavimento.")
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("🏎️ Parámetros: Vehículo")
    v_kmh = st.sidebar.slider("Velocidad Inicial (km/h)", 10.0, 180.0, 80.0, 5.0)
    t_reaccion = st.sidebar.slider("Tiempo de Reacción (s)", 0.5, 2.5, 1.0, 0.1)
    
    # Selección de condición del pavimento
    terreno = st.sidebar.selectbox(
        "Condición del Asfalto",
        ["Asfalto Seco (Excelente Adherencia)", "Asfalto Mojado (Lluvia)", "Pista Helada / Nieve"]
    )
    
    # Coeficiente de fricción dinámico asignado según el terreno
    if terreno == "Asfalto Seco (Excelente Adherencia)":
        mu = 0.75
    elif terreno == "Asfalto Mojado (Lluvia)":
        mu = 0.40
    else:
        mu = 0.15
        
    g_m2 = 9.81
    v_ms = v_kmh / 3.6  # Conversión de km/h a m/s
    
    # Distancias
    d_reaccion = v_ms * t_reaccion
    d_frenado = (v_ms**2) / (2 * mu * g_m2)
    d_total = d_reaccion + d_frenado
    a_desaceleracion = mu * g_m2  # Desaceleración a = \mu * g
    
    # Métricas
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🧠 Dist. Reacción", f"{d_reaccion:.2f} m")
    col2.metric("🛑 Dist. Frenado Mecánico", f"{d_frenado:.2f} m")
    col3.metric("🚨 Distancia Total Detención", f"{d_total:.2f} m")
    col4.metric("📉 Desaceleración (a)", f"{a_desaceleracion:.2f} m/s²")
    
    # Gráfico comparativo de barras
    fig2, ax2 = plt.subplots(figsize=(8, 3))
    barras = ax2.barh(["Distancia Total"], [d_reaccion], color="#ff7f0e", label="Distancia de Reacción")
    ax2.barh(["Distancia Total"], [d_frenado], left=[d_reaccion], color="#d62728", label="Distancia de Frenado (Fricción)")
    
    ax2.set_xlabel("Metros (m)")
    ax2.set_title(f"Desglose de Detención a {v_kmh} km/h en {terreno}", fontsize=11, fontweight='bold')
    ax2.legend(loc="lower right")
    ax2.grid(True, axis='x', ls="--", alpha=0.5)
    st.pyplot(fig2)

# ==========================================
# MÓDULO 3: PLANO INCLINADO Y FRICCIÓN
# ==========================================
with tab3:
    st.header("Módulo 3: Dinámica en Plano Inclinado")
    st.write("Análisis de descomposición de fuerzas (Fuerza Normal, Fricción y Componentes del Peso).")
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("📐 Parámetros: Plano Inclinado")
    masa = st.sidebar.slider("Masa del Bloque (kg)", 1.0, 100.0, 10.0, 1.0)
    angulo_plano = st.sidebar.slider("Ángulo del Plano (°)", 0.0, 75.0, 25.0, 1.0)
    mu_estatico = st.sidebar.slider("Coeficiente Fricción Estática (μs)", 0.05, 0.90, 0.40, 0.05)
    
    g_m3 = 9.81
    rad_plano = np.radians(angulo_plano)
    
    # Cálculos de fuerzas
    peso = masa * g_m3
    px = peso * np.sin(rad_plano)  # Componente paralela al plano
    py = peso * np.cos(rad_plano)  # Componente perpendicular al plano
    fuerza_normal = py
    friccion_estatica_max = mu_estatico * fuerza_normal
    
    # Condición de movimiento: ¿El bloque se desliza o se queda quieto?
    se_mueve = px > friccion_estatica_max
    if se_mueve:
        aceleracion = (px - friccion_estatica_max) / masa
        estado = "🔴 EL BLOQUE SE DESLIZA (Superó la fricción estática)"
    else:
        aceleracion = 0.0
        estado = "🟢 EL BLOQUE PERMANECE EN REPOSO (En equilibrio estático)"
        
    st.subheader(f"Estado del Sistema: {estado}")
    
    # Métricas
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("⚖️ Peso Total (W)", f"{peso:.1f} N")
    c2.metric("📐 Fuerza Paralela (Px)", f"{px:.1f} N")
    c3.metric("🛑 Fricción Estática Máx", f"{friccion_estatica_max:.1f} N")
    c4.metric("🏃 Aceleración Resultante", f"{aceleracion:.2f} m/s²")
    
    # Diagrama visual simplificado
    fig3, ax3 = plt.subplots(figsize=(6, 3.5))
    
    # Dibujar triángulo del plano
    base = 10
    altura = base * np.tan(rad_plano)
    ax3.plot([0, base, base, 0], [0, 0, altura, 0], color="black", lw=2)
    ax3.fill([0, base, base], [0, 0, altura], color="#e0e0e0")
    
    # Dibujar bloque
    x_bloque = base / 2
    y_bloque = (base / 2) * np.tan(rad_plano)
    ax3.scatter([x_bloque], [y_bloque + 0.3], color="blue", s=400, marker="s", zorder=5, label="Bloque")
    
    ax3.set_title(f"Representación del Plano Inclinado ({angulo_plano}°)", fontsize=11)
    ax3.set_aspect('equal')
    ax3.axis('off')
    st.pyplot(fig3)