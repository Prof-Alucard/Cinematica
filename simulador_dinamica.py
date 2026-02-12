import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time

# Configuração da Página
st.set_page_config(page_title="Laboratório de Física - Prof. Ojeda", layout="wide")

# --- MENU LATERAL ---
st.sidebar.title("🔬 Módulos de Física")
modulo = st.sidebar.radio("Selecione o simulador:", ["Dinâmica (Atrito)", "Cinemática (Encontro)"])

# ==========================================
# MÓDULO: DINÂMICA
# ==========================================
if modulo == "Dinâmica (Atrito)":
    st.title("📦 Dinâmica: Força e Atrito")
    st.markdown("Estudo do movimento retilíneo sob influência de forças e atrito cinético.")

    with st.sidebar:
        st.markdown("---")
        st.header("Configurações")
        massa = st.slider("Massa (kg)", 1.0, 50.0, 10.0)
        forca_f = st.slider("Força Aplicada F (N)", 0.0, 300.0, 150.0)
        mu = st.slider("Coeficiente de Atrito (µ)", 0.0, 1.0, 0.2)
        distancia_final = st.slider("Distância do Percurso (m)", 10.0, 500.0, 100.0)
        btn_iniciar = st.button("🚀 Iniciar Simulação")

    # Cálculos
    g = 9.8
    fat_max = mu * massa * g
    f_res = forca_f - fat_max
    acel = f_res / massa if f_res > 0 else 0
    t_total = np.sqrt(2 * distancia_final / acel) if acel > 0 else 0

    metricas = st.empty()
    grafico = st.empty()

    # Mostra métricas iniciais
    with metricas.container():
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Atrito", f"{fat_max:.1f} N")
        c2.metric("Aceleração", f"{acel:.2f} m/s²")
        c3.metric("Tempo", "0.00 s")
        c4.metric("Posição", "0.0 m")
        c5.metric("Velocidade", "0.0 m/s")

    if btn_iniciar and acel > 0:
        passos = 30
        for i in range(passos + 1):
            t = (i / passos) * t_total
            d = (acel * t**2) / 2
            v = acel * t

            with metricas.container():
                mc1, mc2, mc3, mc4, mc5 = st.columns(5)
                mc1.metric("Atrito", f"{fat_max:.1f} N")
                mc2.metric("Aceleração", f"{acel:.2f} m/s²")
                mc3.metric("Tempo", f"{t:.2f} s")
                mc4.metric("Posição", f"{d:.1f} m")
                mc5.metric("Velocidade", f"{v:.1f} m/s")

            fig, ax = plt.subplots(figsize=(12, 3))
            ax.axhline(0, color='black', linewidth=2)
            ax.plot(d, 0.4, 'bs', markersize=40, zorder=3)
            ax.arrow(d, 0.4, 15, 0, head_width=0.1, head_length=4, fc='blue', ec='blue')
            ax.text(d + 20, 0.4, 'F', color='blue', fontweight='bold')
            ax.arrow(d - 3, 0.05, -12, 0, head_width=0.1, head_length=4, fc='red', ec='red')
            ax.text(d - 20, 0.2, 'Fat', color='red', fontweight='bold')
            ax.set_xlim(-25, distancia_final + 40)
            ax.set_ylim(-0.8, 1.5)
            ax.axis('off')
            grafico.pyplot(fig)
            plt.close(fig)
            time.sleep(0.1)
        st.success("Simulação Concluída!")
    elif btn_iniciar:
        st.error("Equilíbrio ou Repouso: Força F insuficiente para vencer o atrito!")

# ==========================================
# MÓDULO: CINEMÁTICA
# ==========================================
else:
    st.title("🏃 Cinemática: Encontro de Móveis")
    st.markdown("Estudo do tempo e posição onde dois objetos se cruzam.")

    with st.sidebar:
        st.markdown("---")
        st.header("Configurações de Encontro")
        v1 = st.slider("Velocidade Móvel A (m/s)", 1.0, 50.0, 20.0)
        v2 = st.slider("Velocidade Móvel B (m/s)", -50.0, -1.0, -15.0)
        dist_inicial = st.slider("Distância Inicial (m)", 50.0, 500.0, 200.0)
        btn_encontro = st.button("🏁 Simular Encontro")

    # Cálculo do encontro (Vrel = V1 - V2)
    # Como V2 é negativo, Vrel = V1 + |V2|
    v_rel = v1 - v2
    t_encontro = dist_inicial / v_rel
    p_encontro = v1 * t_encontro

    grafico_cin = st.empty()
    met_cin = st.empty()

    if btn_encontro:
        passos_c = 30
        for i in range(passos_c + 1):
            t_c = (i / passos_c) * t_encontro
            p1 = v1 * t_c
            p2 = dist_inicial + (v2 * t_c)

            with met_cin.container():
                col1, col2, col3 = st.columns(3)
                col1.metric("Tempo", f"{t_c:.2f} s")
                col2.metric("Posição A", f"{p1:.1f} m")
                col3.metric("Posição B", f"{p2:.1f} m")

            fig, ax = plt.subplots(figsize=(12, 3))
            ax.axhline(0, color='gray', linestyle='--')
            ax.plot(p1, 0, 'go', label="Móvel A", markersize=15)
            ax.plot(p2, 0, 'ro', label="Móvel B", markersize=15)
            ax.set_xlim(-10, dist_inicial + 10)
            ax.set_ylim(-1, 1)
            ax.legend()
            grafico_cin.pyplot(fig)
            plt.close(fig)
            time.sleep(0.1)
        st.success(f"Encontro no instante {t_encontro:.2f}s na posição {p_encontro:.1f}m")
