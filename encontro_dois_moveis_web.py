import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

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

    t_max_slider = st.slider('Tempo Máximo da Simulação (t_max em s)', min_value=1.0, max_value=30.0, value=15.0, step=1.0)

# --- Lógica de Encontro ---
# A equação para o encontro é: S_MU = S_MUV
# S₀_MU + v_MU * t = S₀_MUV + v₀_MUV * t + 0.5 * a_MUV * t^2
# Reorganizando para a forma ax^2 + bx + c = 0
# 0.5*a_MUV*t^2 + (v₀_MUV - v_MU)*t + (S₀_MUV - S₀_MU) = 0
a = 0.5 * a_muv
b = v0_muv - v_mu
c = s0_muv - s0_mu

# Usando numpy para resolver a equação do segundo grau
# A função np.roots aceita os coeficientes [a, b, c]
tempos_encontro = np.roots([a, b, c])

# Filtrando os tempos de encontro válidos (reais e não negativos)
tempos_validos = [t.real for t in tempos_encontro if np.isreal(t) and t.real >= 0]
tempos_validos.sort()

# --- Construção do Gráfico ---
st.header("Gráfico de Posição vs. Tempo")

# Define o tempo máximo do gráfico com base nos resultados e no slider
t_max = max(t_max_slider, *tempos_validos) if tempos_validos else t_max_slider
t_grafico = np.linspace(0, t_max, 400)

# Calcula as posições para os gráficos
pos_mu = s0_mu + v_mu * t_grafico
pos_muv = s0_muv + v0_muv * t_grafico + 0.5 * a_muv * t_grafico**2

fig, ax = plt.subplots(figsize=(10, 6))

# Plota as trajetórias
ax.plot(t_grafico, pos_mu, label='Móvel MU', color='blue')
ax.plot(t_grafico, pos_muv, label='Móvel MUV', color='red', linestyle='--')

# Marca o(s) ponto(s) de encontro no gráfico
if tempos_validos:
    st.subheader('Resultados do Encontro:')
    for i, t_encontro in enumerate(tempos_validos):
        # Calcula a posição de encontro usando a equação do MU
        pos_encontro = s0_mu + v_mu * t_encontro
        ax.plot(t_encontro, pos_encontro, 'go', markersize=10, label=f'Encontro {i+1}')
        st.success(f'Encontro em **t = {t_encontro:.2f} s** na posição **S = {pos_encontro:.2f} m**')
else:
    st.info('Os móveis não se encontram no intervalo de tempo selecionado.')

# Configurações do gráfico
ax.set_title('Trajetória dos Móveis ao Longo do Tempo')
ax.set_xlabel('Tempo (s)')
ax.set_ylabel('Posição (m)')
ax.legend()
ax.grid(True)

# Exibe o gráfico no Streamlit
st.pyplot(fig)