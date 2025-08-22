import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time

# --- Título da página web ---
st.title('Visualizador de Encontro de Móveis')
st.markdown("Analise o encontro de um móvel em **Movimento Uniforme (MU)** com um em **Movimento Uniformemente Variado (MUV)**.")

# --- Barra lateral para entrada de dados ---
with st.sidebar:
    st.header('Parâmetros do MU')
    s0_mu = st.slider('Posição Inicial MU (S₀_MU em m)', min_value=-50.0, max_value=50.0, value=0.0, step=0.5)
    v_mu = st.slider('Velocidade MU (v_MU em m/s)', min_value=-20.0, max_value=20.0, value=5.0, step=0.5)

    st.markdown("---")
    st.header('Parâmetros do MUV')
    s0_muv = st.slider('Posição Inicial MUV (S₀_MUV em m)', min_value=-50.0, max_value=50.0, value=50.0, step=0.5)
    v0_muv = st.slider('Velocidade Inicial MUV (v₀_MUV em m/s)', min_value=-20.0, max_value=20.0, value=-5.0, step=0.5)
    a_muv = st.slider('Aceleração MUV (a_MUV em m/s²)', min_value=-10.0, max_value=10.0, value=1.0, step=0.1)

    t_max = st.slider('Tempo Máximo da Simulação (t_max em s)', min_value=1.0, max_value=30.0, value=15.0, step=1.0)
    velocidade_animacao = st.slider('Velocidade da Animação (segundos)', min_value=0.01, max_value=1.0, value=0.05, step=0.01)

# --- Lógica de Encontro ---
a = 0.5 * a_muv
b = v0_muv - v_mu
c = s0_muv - s0_mu
tempos_encontro = np.roots([a, b, c])
tempos_validos = [t.real for t in tempos_encontro if np.isreal(t) and t.real >= 0]
tempos_validos.sort()

# --- Componentes principais da UI com colunas ---
col_grafico, col_valores = st.columns([3, 1])

with col_grafico:
    st.header("Gráfico de Posição vs. Tempo")
    grafico_placeholder = st.empty()

with col_valores:
    st.header("Valores")
    pos_mu_metric = st.empty()
    st.markdown("---")
    pos_muv_metric = st.empty()
    st.markdown("---")
    tempo_metric = st.empty()
    st.markdown("---")

resultado_container = st.empty()

# Botão para iniciar a animação
if st.button('Iniciar Animação'):
    
    # Prepara o gráfico
    fig, ax = plt.subplots(figsize=(10, 6))
    
    progress_bar = st.progress(0)
    num_steps = 100
    
    # Pre-calcula os limites do gráfico para evitar que a tela "pule"
    t_completo = np.linspace(0, t_max, num_steps + 1)
    pos_completo_mu = s0_mu + v_mu * t_completo
    pos_completo_muv = s0_muv + v0_muv * t_completo + 0.5 * a_muv * t_completo**2
    y_min = min(pos_completo_mu.min(), pos_completo_muv.min())
    y_max = max(pos_completo_mu.max(), pos_completo_muv.max())

    # Loop de animação
    for i in range(num_steps + 1):
        t_atual = t_max * i / num_steps
        
        # Calcula a posição atual de cada móvel
        pos_atual_mu = s0_mu + v_mu * t_atual
        pos_atual_muv = s0_muv + v0_muv * t_atual + 0.5 * a_muv * t_atual**2
        
        # Atualiza a barra de progresso
        progress_bar.progress(i / num_steps)
        
        # Redesenha o gráfico a cada passo
        ax.cla()
        
        # Plota a porção da trajetória percorrida
        tempos_percorridos = np.linspace(0, t_atual, max(2, int(i*0.5)))
        pos_percorrida_mu = s0_mu + v_mu * tempos_percorridos
        pos_percorrida_muv = s0_muv + v0_muv * tempos_percorridos + 0.5 * a_muv * tempos_percorridos**2

        ax.plot(tempos_percorridos, pos_percorrida_mu, label='Móvel MU', color='blue', linewidth=2)
        ax.plot(tempos_percorridos, pos_percorrida_muv, label='Móvel MUV', color='red', linestyle='--', linewidth=2)
        
        # Plota as posições atuais
        ax.plot(t_atual, pos_atual_mu, 'o', color='blue', markersize=10)
        ax.plot(t_atual, pos_atual_muv, 'o', color='red', markersize=10)

        # Ajusta os limites e eixos
        ax.set_xlim(0, t_max)
        ax.set_ylim(y_min - 5, y_max + 5)
        ax.set_title('Trajetória dos Móveis ao Longo do Tempo')
        ax.set_xlabel('Tempo (s)')
        ax.set_ylabel('Posição (m)')
        ax.legend()
        ax.grid(True)

        # Atualiza o gráfico e as métricas nas colunas
        with col_grafico:
            grafico_placeholder.pyplot(fig)
        with col_valores:
            pos_mu_metric.metric(label="Posição MU (m)", value=f"{pos_atual_mu:.2f}")
            pos_muv_metric.metric(label="Posição MUV (m)", value=f"{pos_atual_muv:.2f}")
            tempo_metric.metric(label="Tempo (s)", value=f"{t_atual:.2f}")

        # Controla a velocidade da animação
        time.sleep(velocidade_animacao)

    # Exibe os resultados finais após a animação
    if tempos_validos:
        with resultado_container.container():
            st.subheader('Resultados Finais do Encontro:')
            for t_encontro in tempos_validos:
                pos_encontro = s0_mu + v_mu * t_encontro
                st.success(f'Encontro em **t = {t_encontro:.2f} s** na posição **S = {pos_encontro:.2f} m**')
    else:
        st.info('Os móveis não se encontram no intervalo de tempo selecionado.')

    st.success('Animação concluída!')