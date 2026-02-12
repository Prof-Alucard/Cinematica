import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time

st.set_page_config(page_title="Simulador de Dinâmica", layout="wide")
st.title("📦 Dinâmica: Força e Atrito")

with st.sidebar:
    st.header("Configurações")
    massa = st.slider("Massa (kg)", 1.0, 50.0, 10.0)
    forca_f = st.slider("Força Aplicada F (N)", 0.0, 300.0, 150.0)
    mu = st.slider("Coeficiente de Atrito (µ)", 0.0, 1.0, 0.2)
    distancia_final = st.slider("Distância do Percurso (m)", 10.0, 500.0, 100.0)
    btn_iniciar = st.button("🚀 Iniciar Deslocamento")

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

metricas_placeholder = st.empty()
espaço_do_grafico = st.empty()

# Mostra as 5 métricas que você queria
with metricas_placeholder.container():
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Atrito", f"{fat_max:.1f} N")
    c2.metric("Aceleração", f"{aceleracao:.2f} m/s²")
    c3.metric("Tempo", "0.00 s")
    c4.metric("Posição", "0.0 m")
    c5.metric("Velocidade", "0.0 m/s")

# Desenho do Gráfico
        fig, ax = plt.subplots(figsize=(12, 3))
        ax.axhline(0, color='black', linewidth=2)
        
        # Bloco (Caixa Azul)
        ax.plot(dist_atual, 0.4, 'bs', markersize=40, zorder=3)
        
        # Seta Força F (Azul)
        ax.arrow(dist_atual, 0.4, 15, 0, head_width=0.1, head_length=4, fc='blue', ec='blue')
        ax.text(dist_atual + 20, 0.4, 'F', color='blue', fontweight='bold')
        
        # Seta Atrito Fat (Vermelha)
        ax.arrow(dist_atual - 3, 0.05, -12, 0, head_width=0.1, head_length=4, fc='red', ec='red')
        ax.text(dist_atual - 20, 0.2, 'Fat', color='red', fontweight='bold')
        
        # Ajustes de Eixo para não cortar as setas
        ax.set_xlim(-25, distancia_final + 40) 
        ax.set_ylim(-0.8, 1.5)
        
        # Estética (Esconde bordas e números do eixo Y)
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.set_yticks([])
        
        # Atualiza o gráfico na tela
        espaço_do_grafico.pyplot(fig)
        plt.close(fig)
        time.sleep(0.1)

    st.success(f"🏁 Chegamos! Percurso de {distancia_final}m concluído.")
elif btn_iniciar:
    st.error("Força insuficiente para vencer o atrito!")
