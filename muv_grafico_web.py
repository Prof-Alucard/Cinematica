import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time

# --- Título da página web ---
import streamlit as st
st.write(f"<span style='font-size: 30px;'>Visualizador de Movimento Uniformemente Variado (M.U.V.)</span>", unsafe_allow_html=True)
st.write('Este é um simulador interativo para visualizar a trajetória de um objeto em Movimento Uniformemente Variado. Ajuste a posição inicial, a velocidade inicial, a aceleraçao e o o tempo na barra lateral esquerda e clique em (Ininiar Animaçao).')


#import streamlit as st
#st.write(f"<span style='font-size: 26px;'>Gráfico de Posição vs. Tempo</span>", unsafe_allow_html=True)

"""
Autor: Prof Ojeda
"""

import streamlit as st
#st.markdown("<h1 style='text-align: center; margin-top: -50px;'>Visualizador de Movimento Uniformemente Variado (M.U.V.)</h1>", unsafe_allow_html=True)

#st.title('Visualizador de Movimento Uniformemente Variado (M.U.V.)', size=24)

# --- Barra lateral para entrada de dados ---
with st.sidebar:
    st.header('Parâmetros do Movimento')
    s0 = st.slider('Posição Inicial (S₀ em m)', min_value=-50.0, max_value=50.0, value=0.0, step=0.5)
    v0 = st.slider('Velocidade Inicial (v₀ em m/s)', min_value=-20.0, max_value=20.0, value=5.0, step=0.5)
    a = st.slider('Aceleração (a em m/s²)', min_value=-10.0, max_value=10.0, value=1.0, step=0.1)
    t_max = st.slider('Tempo Final (t em s)', min_value=1.0, max_value=20.0, value=10.0, step=0.5)
    velocidade_animacao = st.slider('Velocidade da Animação (segundos)', min_value=0.01, max_value=1.0, value=0.1, step=0.01)

# --- Criação das Colunas Principais ---
col_grafico, col_contadores = st.columns([4, 1])

# Local para o gráfico e os contadores
with col_grafico:
    grafico_placeholder = st.empty()

with col_contadores:
    st.write("### Valores")
    posicao_metric = st.empty()
    st.markdown("---")
    tempo_metric = st.empty()
    st.markdown("---")

# Botão para iniciar a animação
if st.button('Iniciar Animação'):
    
    # Prepara o gráfico
    fig, ax = plt.subplots(figsize=(4, 6))
    
    # Inicia a animação em um loop
    num_steps = 100
    progress_bar = st.progress(0)

    for i in range(num_steps + 1):
        t_atual = t_max * i / num_steps
        
        # --- EQUAÇÃO DO M.U.V. ---
        posicao_atual = s0 + v0 * t_atual + 0.5 * a * t_atual**2

        progress_bar.progress(i / num_steps)
        
        ax.cla()
        
        # Redesenha os limites e eixos
        # ax.set_title('Movimento do Ponto ao Longo do Tempo')  # Esta linha foi removida/comentada
        ax.set_xlabel('Tempo (s)')
        ax.set_ylabel('Posição (m)')
        ax.grid(True)
        ax.set_xlim(0, t_max)
        
        # Calcula os limites do eixo Y com base na trajetória
        t_completo = np.linspace(0, t_max, 100)
        posicoes_completas = s0 + v0 * t_completo + 0.5 * a * t_completo**2
        y_min = posicoes_completas.min() - 5
        y_max = posicoes_completas.max() + 5
        ax.set_ylim(y_min, y_max)
        
        ax.axhline(0, color='black', linewidth=0.5)
        ax.axvline(0, color='black', linewidth=0.5)
        
        # Desenha a linha de trajetória
        tempos_trajetoria = np.linspace(0, t_atual, 100)
        posicoes_trajetoria = s0 + v0 * tempos_trajetoria + 0.5 * a * tempos_trajetoria**2
        ax.plot(tempos_trajetoria, posicoes_trajetoria, color='blue', linestyle='--', linewidth=1)
        
        # Desenha o ponto atual
        ax.plot(t_atual, posicao_atual, 'ro', markersize=10, label='Ponto Atual')

        # Atualiza o gráfico e os contadores
        posicao_metric.metric(label="Posição (m)", value=f"{posicao_atual:.2f}")
        tempo_metric.metric(label="Tempo (s)", value=f"{t_atual:.2f}")
        
        grafico_placeholder.pyplot(fig)
        
        time.sleep(velocidade_animacao)

    st.success('Animação concluída!')