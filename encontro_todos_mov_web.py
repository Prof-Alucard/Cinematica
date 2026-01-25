import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time

# --- Título da página web ---
import streamlit as st
st.write(f"<span style='font-size: 30px;'>Visualizador do encontro de dois moveis</span>", unsafe_allow_html=True)
st.write('Este programa interativo, permite simular e visualizar o encontro entre dois móveis. Você pode ajustar a barra lateral à esquerda e escolher o tipo de simulação entre (M.U.-M.U.), (M.U.-M.U.V.) e (M.U.V.-M.U.V.), definindo os valores de posição inicial, velocidade inicial, aceleração e tempo e clicar em (Iniciar Simulação).')

"""
Autor: Prof Ojeda
"""




#st.title('Visualizador de Encontro de Móveis')
#st.markdown("Analise o encontro de dois móveis em **Movimento Uniforme (MU)** ou **Movimento Uniformemente Variado (MUV)**.")

# --- Barra lateral para entrada de dados ---
with st.sidebar:
    # Seleção do tipo de movimento para o Móvel 1
    st.header('Móvel 1')
    tipo_movimento_1 = st.selectbox('Tipo de Movimento', ['MU', 'MUV'], key='movel1')
    s0_1 = st.slider('Posição Inicial (S₀ em m)', min_value=-50.0, max_value=50.0, value=0.0, step=0.5, key='s0_1')
    v_1 = st.slider('Velocidade Inicial (v₀ em m/s)', min_value=-20.0, max_value=20.0, value=5.0, step=0.5, key='v_1')
    if tipo_movimento_1 == 'MUV':
        a_1 = st.slider('Aceleração (a em m/s²)', min_value=-10.0, max_value=10.0, value=1.0, step=0.1, key='a_1')
    else:
        a_1 = 0.0

    st.markdown("---")

    # Seleção do tipo de movimento para o Móvel 2
    st.header('Móvel 2')
    tipo_movimento_2 = st.selectbox('Tipo de Movimento', ['MU', 'MUV'], key='movel2')
    s0_2 = st.slider('Posição Inicial (S₀ em m)', min_value=-50.0, max_value=50.0, value=50.0, step=0.5, key='s0_2')
    v_2 = st.slider('Velocidade Inicial (v₀ em m/s)', min_value=-20.0, max_value=20.0, value=-5.0, step=0.5, key='v_2')
    if tipo_movimento_2 == 'MUV':
        a_2 = st.slider('Aceleração (a em m/s²)', min_value=-10.0, max_value=10.0, value=1.0, step=0.1, key='a_2')
    else:
        a_2 = 0.0

    t_max = st.slider('Tempo Máximo da Simulação (t_max em s)', min_value=1.0, max_value=30.0, value=15.0, step=1.0)
    velocidade_animacao = st.slider('Velocidade da Animação (segundos)', min_value=0.01, max_value=1.0, value=0.05, step=0.01)

# --- Lógica de Encontro ---
# Equação para o encontro: (s0_1 + v_1*t + 0.5*a_1*t²) = (s0_2 + v_2*t + 0.5*a_2*t²)
# Rearranjando para a forma ax² + bx + c = 0
a = 0.5 * (a_1 - a_2)
b = v_1 - v_2
c = s0_1 - s0_2
tempos_encontro = np.roots([a, b, c])
tempos_validos = [t.real for t in tempos_encontro if np.isreal(t) and t.real >= 0]
tempos_validos.sort()

# --- Componentes principais da UI com colunas ---
col_grafico, col_valores = st.columns([3, 1])

with col_grafico:
  #  st.header("Gráfico de Posição vs. Tempo")
    grafico_placeholder = st.empty()

with col_valores:
    st.write("Valores")
    pos_1_metric = st.empty()
    st.markdown("---")
    pos_2_metric = st.empty()
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
    
    # Pre-calcula os limites do gráfico
    t_completo = np.linspace(0, t_max, num_steps + 1)
    pos_completo_1 = s0_1 + v_1 * t_completo + 0.5 * a_1 * t_completo**2
    pos_completo_2 = s0_2 + v_2 * t_completo + 0.5 * a_2 * t_completo**2
    y_min = min(pos_completo_1.min(), pos_completo_2.min())
    y_max = max(pos_completo_1.max(), pos_completo_2.max())

    # Loop de animação
    for i in range(num_steps + 1):
        t_atual = t_max * i / num_steps
        
        # Calcula a posição atual de cada móvel
        pos_atual_1 = s0_1 + v_1 * t_atual + 0.5 * a_1 * t_atual**2
        pos_atual_2 = s0_2 + v_2 * t_atual + 0.5 * a_2 * t_atual**2
        
        # Atualiza a barra de progresso
        progress_bar.progress(i / num_steps)
        
        # Redesenha o gráfico a cada passo
        ax.cla()
        
        # Plota a porção da trajetória percorrida
        tempos_percorridos = np.linspace(0, t_atual, max(2, int(i*0.5)))
        pos_percorrida_1 = s0_1 + v_1 * tempos_percorridos + 0.5 * a_1 * tempos_percorridos**2
        pos_percorrida_2 = s0_2 + v_2 * tempos_percorridos + 0.5 * a_2 * tempos_percorridos**2

        ax.plot(tempos_percorridos, pos_percorrida_1, label='Móvel 1', color='blue', linewidth=2)
        ax.plot(tempos_percorridos, pos_percorrida_2, label='Móvel 2', color='red', linestyle='--', linewidth=2)
        
        # Plota as posições atuais
        ax.plot(t_atual, pos_atual_1, 'o', color='blue', markersize=10)
        ax.plot(t_atual, pos_atual_2, 'o', color='red', markersize=10)

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
            pos_1_metric.metric(label="Posição Móvel 1 (m)", value=f"{pos_atual_1:.2f}")
            pos_2_metric.metric(label="Posição Móvel 2 (m)", value=f"{pos_atual_2:.2f}")
            tempo_metric.metric(label="Tempo (s)", value=f"{t_atual:.2f}")


# Cálculo do tempo de encontro (exemplo para MU)
t_enc = (s0_2 - s0_1) / (v1 - v2)
s_enc = s0_1 + v1 * t_enc

# Marcar no gráfico
plt.scatter(t_enc, s_enc, color='green', s=100, label='Ponto de Encontro')
plt.annotate(f'Encontro: {s_enc:.2f}m', (t_enc, s_enc), textcoords="offset points", xytext=(0,10), ha='center')
        

        
        # Controla a velocidade da animação
        time.sleep(velocidade_animacao)

    # Exibe os resultados finais após a animação
    if tempos_validos:
        with resultado_container.container():
            st.subheader('Resultados Finais do Encontro:')
            for t_encontro in tempos_validos:
                pos_encontro = s0_1 + v_1 * t_encontro + 0.5 * a_1 * t_encontro**2
                st.success(f'Encontro em **t = {t_encontro:.2f} s** na posição **S = {pos_encontro:.2f} m**')
    else:
        st.info('Os móveis não se encontram no intervalo de tempo selecionado.')

    st.success('Animação concluída!')
