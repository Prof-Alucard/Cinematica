import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time

# Configuração da página para o Laboratório do Prof. Ojeda
st.set_page_config(page_title="Laboratório de Física - Prof. Ojeda", layout="wide")

# --- MENU LATERAL ---
st.sidebar.title("🔬 Menu de Experimentos")
modulo = st.sidebar.radio("Selecione o tema da aula:", 
                         ["🏠 Início", 
                          "🏃 Cinemática (Encontro)", 
                          "📦 Dinâmica (Força e Atrito)"])

# ---------------------------------------------------------
# TELA INICIAL
# ---------------------------------------------------------
if modulo == "🏠 Início":
    st.title("Bem-vindo ao Laboratório Virtual de Física")
    st.markdown("""
    Este portal foi criado para facilitar a visualização de conceitos abstratos da física.
    
    ### Como usar:
    1. Escolha um dos módulos no **menu lateral à esquerda**.
    2. Ajuste os parâmetros (massa, velocidade, força) nos controles.
    3. Clique no botão **Iniciar** para ver a física acontecer!
    """)
    st.info("💡 Dica: Se a animação travar, tente reduzir o número de passos ou a distância.")

# ---------------------------------------------------------
# MÓDULO: CINEMÁTICA (ENCONTRO)
# ---------------------------------------------------------
elif modulo == "🏃 Cinemática (Encontro)":
    st.title("🏃 Estudo de Encontro de Móveis")
    
    with st.sidebar:
        st.markdown("---")
        st.header("Parâmetros")
        v_a = st.slider("Velocidade do Carro A (m/s)", 1.0, 60.0, 20.0)
        v_b = st.slider("Velocidade do Carro B (m/s)", -60.0, -1.0, -15.0)
        dist_ini = st.slider("Distância entre eles (m)", 50, 500, 200)
        btn_cine = st.button("🏁 Iniciar Simulação")

    # Cálculos
    v_relativa = v_a - v_b
    t_encontro = dist_ini / v_relativa
    p_encontro = v_a * t_encontro

    # Espaços para animação
    met_c = st.empty()
    graf_c = st.empty()

    if btn_cine:
        passos = 30
        for i in range(passos + 1):
            t_atual = (i / passos) * t_encontro
            pos_a = v_a * t_atual
            pos_b = dist_ini + (v_b * t_atual)

            with met_c.container():
                c1, c2, c3 = st.columns(3)
                c1.metric("Tempo", f"{t_atual:.2f} s")
                c2.metric("Posição A", f"{pos_a:.1f} m")
                c3.metric("Posição B", f"{pos_b:.1f} m")

            fig, ax = plt.subplots(figsize=(10, 2))
            ax.axhline(0, color='black', linewidth=1, linestyle='--')
            ax.plot(pos_a, 0, 'go', markersize=15, label="A")
            ax.plot(pos_b, 0, 'ro', markersize=15, label="B")
            ax.set_xlim(-20, dist_ini + 20)
            ax.set_ylim(-1, 1)
            ax.axis('off')
            
            with graf_c.container():
                st.pyplot(fig)
            plt.close(fig)
            time.sleep(0.08)
        st.success(f"Encontro em {t_encontro:.2f}s na posição {p_encontro:.1f}m")

# ---------------------------------------------------------
# MÓDULO: DINÂMICA (ATRITO)
# ---------------------------------------------------------
elif modulo == "📦 Dinâmica (Força e Atrito)":
    st.title("📦 Dinâmica: Leis de Newton e Atrito")
    
    with st.sidebar:
        st.markdown("---")
        st.header("Parâmetros")
        m = st.slider("Massa do Bloco (kg)", 1.0, 50.0, 10.0)
        f_ap = st.slider("Força Aplicada F (N)", 0.0, 400.0, 150.0)
        coef_u = st.slider("Coeficiente de Atrito (µ)", 0.0, 1.0, 0.2)
        d_percurso = st.slider("Distância (m)", 10.0, 400.0, 100.0)
        btn_din = st.button("🚀 Iniciar Bloco")

    # Cálculos
    g = 9.8
    f_atrito = coef_u * m * g
    f_res = f_ap - f_atrito
    
    if f_res > 0:
        a = f_res / m
        t_total = np.sqrt(2 * d_percurso / a)
    else:
        a = 0
        t_total = 0

    met_d = st.empty()
    graf_d = st.empty()

    if btn_din and a > 0:
        passos = 30
        for i in range(passos + 1):
            t_at = (i / passos) * t_total
            dist_at = (a * t_at**2) / 2
            vel_at = a * t_at

            with met_d.container():
                d1, d2, d3 = st.columns(3)
                d1.metric("Aceleração", f"{a:.2f} m/s²")
                d2.metric("Velocidade", f"{vel_at:.1f} m/s")
                d3.metric("Posição", f"{dist_at:.1f} m")

            fig, ax = plt.subplots(figsize=(10, 3))
            ax.axhline(0, color='black', linewidth=2)
            
            # O Bloco (desenhado como um quadrado)
            ax.plot(dist_at, 0.4, 'bs', markersize=30, zorder=3)
            
            # Vetores de Força
            ax.arrow(dist_at, 0.4, 20, 0, head_width=0.1, head_length=5, fc='blue', ec='blue')
            ax.text(dist_at + 25, 0.5, 'F', color='blue', fontweight='bold')
            
            ax.arrow(dist_at - 2, 0.1, -15, 0, head_width=0.1, head_length=5, fc='red', ec='red')
            ax.text(dist_at - 25, 0.2, 'Fat', color='red', fontweight='bold')

            ax.set_xlim(-40, d_percurso + 60)
            ax.set_ylim(-0.5, 1.5)
            ax.axis('off')

            with graf_d.container():
                st.pyplot(fig)
            plt.close(fig)
            time.sleep(0.08)
        st.success("Objetivo alcançado!")
    elif btn_din:
        st.error("Força Resultante nula ou negativa! O bloco permanece em repouso.")
