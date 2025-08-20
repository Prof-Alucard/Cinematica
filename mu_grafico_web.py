import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time

# Título da página web
st.title('Visualizador de Movimento Uniforme (M.U.)')

# --- Barra lateral para entrada de dados ---
with st.sidebar:
    st.header('Parâmetros do Movimento')
    s0 = st.slider('Posição Inicial (S₀ em m)', min_value=-50.0, max_value=50.0, value=0.0, step=0.5)
    v = st.slider('Velocidade (v em m/s)', min_value=-20.0, max_value=20.0, value=5.0, step=0.5)
    t_max = st.slider('Tempo Final (t em s)', min_value=1.0, max_value=20.0, value=10.0, step=0.5)
    velocidade_animacao = st.slider('Velocidade da Animação (segundos)', min_value=0.01, max_value=1.0, value=0.1, step=0.01)

# --- Criação das Colunas Principais ---
col_grafico, col_contadores = st.columns([0.7, 0.3])

# Local para o gráfico e os contadores
with col_grafico:
    st.header("Gráfico de Posição vs. Tempo")
    grafico_placeholder = st.empty()

with col_contadores:
    st.header("Valores")
    posicao_metric = st.empty()
    st.markdown("---")
    tempo_metric = st.empty()
    st.markdown("---")

# Botão para iniciar a animação
if st.button('Iniciar Animação'):
    
    # Prepara o gráfico
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Inicia a animação em um loop
    num_steps = 100
    progress_bar = st.progress(0)

    for i in range(num_steps + 1):
        t_atual = t_max * i / num_steps
        posicao_atual = s0 + v * t_atual

        progress_bar.progress(i / num_steps)
        
        # --- CORREÇÃO AQUI ---
        # Limpa o gráfico para desenhar o novo estado
        ax.cla()
        
        # Redesenha os limites e eixos
        ax.set_title('Movimento do Ponto ao Longo do Tempo')
        ax.set_xlabel('Tempo (s)')
        ax.set_ylabel('Posição (m)')
        ax.grid(True)
        ax.set_xlim(0, t_max)
        y_min = min(s0, s0 + v * t_max) - 5
        y_max = max(s0, s0 + v * t_max) + 5
        ax.set_ylim(y_min, y_max)
        ax.axhline(0, color='black', linewidth=0.5)
        ax.axvline(0, color='black', linewidth=0.5)
        
        # Desenha a linha de trajetória
        tempos_trajetoria = np.linspace(0, t_atual, 100)
        posicoes_trajetoria = s0 + v * tempos_trajetoria
        ax.plot(tempos_trajetoria, posicoes_trajetoria, color='blue', linestyle='--', linewidth=1)
        
        # Desenha o ponto atual
        ax.plot(t_atual, posicao_atual, 'ro', markersize=10, label='Ponto Atual')

        # Atualiza o gráfico e os contadores
        posicao_metric.metric(label="Posição (m)", value=f"{posicao_atual:.2f}")
        tempo_metric.metric(label="Tempo (s)", value=f"{t_atual:.2f}")
        
        grafico_placeholder.pyplot(fig)
        
        time.sleep(velocidade_animacao)

    st.success('Animação concluída!')