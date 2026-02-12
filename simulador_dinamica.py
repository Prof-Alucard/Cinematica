import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time

# Configuração inicial
st.set_page_config(page_title="Simulador de Dinâmica", layout="wide")
st.title("📦 Dinâmica: Força e Atrito")

# Sidebar
with st.sidebar:
    st.header("Configurações")
    massa = st.slider("Massa (kg)", 1.0, 50.0, 10.0)
    forca_f = st.slider("Força Aplicada F (N)", 0.0, 300.0, 150.0)
    mu = st.slider("Coeficiente de Atrito (µ)", 0.0, 1.0, 0.2)
    distancia_final = st.slider("Distância do Percurso (m)", 10.0, 500.0, 100.0)
    btn_iniciar = st.button("🚀 Iniciar Deslocamento")

# Cálculos Físicos
gravidade = 9.8
peso = massa * gravidade
fat_max = mu * peso
forca_resultante = forca_f - fat_max

if forca_resultante > 0:
    aceleracao = forca_resultante / massa
    tempo_total = np.sqrt(2 * distancia_final / aceleracao)
else:
    aceleracao = 0
    tempo_total = 0

# Espaços reservados para atualização
metricas_placeholder = st.empty()
espaço_do_grafico = st.empty()

# Simulação
if btn_iniciar and aceleracao > 0:
    passos = 50  # Ajustado para fluidez na web
    for i in range(passos + 1):
        t_atual = (i / passos) * tempo_total
        dist_atual = (aceleracao * t_atual**2) / 2
        vel_atual = aceleracao * t_atual

        # 1. Atualiza Métricas
        with metricas_placeholder.container():
            mc1, mc2, mc3, mc4, mc5 = st.columns(5)
            mc1.metric("Atrito", f"{fat_max:.1f} N")
            mc2.metric("Aceleração", f"{aceleracao:.2f} m/s²")
            mc3.metric("Tempo", f"{t_atual:.2f} s")
            mc4.metric("Posição", f"{dist_atual:.1f} m")
            mc5.metric("Velocidade", f"{vel_atual:.1f} m/s")

        # 2. Desenha Gráfico
        fig, ax = plt.subplots(figsize=(12, 3))
        ax.axhline(0, color='black', linewidth=2)
        
        # Bloco
        ax.plot(dist_atual, 0.4, 'bs', markersize=40, zorder=3)
        
        # Seta e Texto F
        ax.arrow(dist_atual, 0.4, 15, 0, head_width=0.1, head_length=4, fc='blue', ec='blue')
        ax.text(dist_atual + 20, 0.4, 'F', color='blue', fontweight='bold')
        
        # Seta e Texto Fat
        ax.arrow(dist_atual - 3, 0.05, -12, 0, head_width=0.1, head_length=4, fc='red', ec='red')
        ax.text(dist_atual - 20, 0.2, 'Fat', color='red', fontweight='bold')
        
        # Ajustes de visualização
        ax.set_xlim(-25, distancia_final + 40)
        ax.set_ylim(-0.8, 1.5)
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.set_yticks([])
        
        espaço_do_grafico.pyplot(fig)
        plt.close(fig)
        time.sleep(0.1) # Tempo de espera para sincronizar com a internet

    st.success(f"🏁 Chegamos! Percurso de {distancia_final}m concluído.")
elif btn_iniciar:
    st.error("Força aplicada é menor ou igual ao atrito. O bloco não se move!")
