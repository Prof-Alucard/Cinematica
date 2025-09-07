import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

# --- Configurações da Página ---
st.set_page_config(layout="wide", page_title="Simulador de Projétil")
st.title("Simulador de Lançamento de Projétil 🎯")

st.write(
    'Este programa interativo permite simular e visualizar o Lançamento Horizontal e Oblíquo de um móvel. '
    'Você pode ajustar o tipo de simulação, a altura (H), a velocidade inicial (v), o ângulo (theta) e a gravidade (g) na barra lateral.'
)

# --- Criação das Colunas para o Layout ---
col1, col2 = st.columns([1, 2])

# --- Coluna da Esquerda: Controles ---
with col1:
    st.header("Controles")
    
    # Adicionar a opção de tipo de lançamento
    modo_lancamento = st.radio(
        "Selecione o tipo de lançamento:",
        ("Oblíquo", "Horizontal")
    )

    # Controles (Sliders)
    altura_inicial = st.slider("Altura Inicial (H, em m)", 0.0, 100.0, 0.0, 0.1)
    velocidade_inicial = st.slider("Velocidade Inicial (vᵢ, em m/s)", 0, 100, 50)
    
    # O slider de ângulo só aparece no modo Oblíquo
    if modo_lancamento == "Oblíquo":
        angulo = st.slider("Ângulo de Lançamento (θ, em °)", 0, 90, 45)
    else:
        angulo = 0 # Ângulo fixo em 0 para lançamento horizontal
    
    gravidade = st.slider("Aceleração da Gravidade (g, em m/s²)", 0.0, 20.0, 9.81, 0.01)

    st.markdown("---")

    # Opções adicionais (checkboxes)
    resistencia_ar = st.checkbox(
        "Resistência do Ar", value=False,
        help="A resistência do ar é uma funcionalidade avançada e não está implementada nesta simulação simples."
    )
    mostrar_vetores = st.checkbox("Mostrar Vetores", value=False)
    
    st.markdown("---")

    # Botões de controle
    btn_iniciar_animacao = st.button("Animação")
    btn_reiniciar = st.button("Reiniciar", help="Reinicia a simulação com os valores padrão ou atuais.")
    
    if btn_reiniciar:
        st.experimental_rerun()

# --- Coluna da Direita: Trajetória e Resultados ---
with col2:
   # st.header("Trajetória e Resultados")

    # Converter ângulo para radianos para o cálculo
    angulo_rad = np.radians(angulo)

    # --- Funções de Cálculo (Mantendo a física básica) ---
    def calcular_trajetoria(v0, ang, g, h0):
        """
        Calcula os pontos da trajetória do projétil.
        Considera a altura inicial h0.
        """
        if g <= 0:
            st.error("A gravidade deve ser maior que zero para calcular a trajetória.")
            return np.array([0]), np.array([h0]), 0, 0, 0, 0, np.array([0]), 0

        # Para lançamento horizontal, o tempo de voo é diferente
        if angulo == 0 and h0 > 0:
            t_voo = np.sqrt(2 * h0 / g)
            t_to_altura_max = 0
            altura_max = h0
            alcance = v0 * t_voo
            x = v0 * t
            y = h0 - 0.5 * g * t**2
        else:
            t_altura_max_p_h0 = v0 * np.sin(ang) / g
            altura_max = h0 + (v0 * np.sin(ang))**2 / (2 * g)
            discriminante = (v0 * np.sin(ang))**2 + 2 * g * h0
            if discriminante < 0:
                st.error("Erro no cálculo do tempo de voo (discriminante negativo).")
                return np.array([0]), np.array([h0]), 0, 0, 0, 0, np.array([0]), 0

            t_voo = (v0 * np.sin(ang) + np.sqrt(discriminante)) / g
            t_to_altura_max = v0 * np.sin(ang) / g

            t = np.linspace(0, t_voo, num=200)

            x = v0 * np.cos(ang) * t
            y = h0 + v0 * np.sin(ang) * t - 0.5 * g * t**2
            
            y[y < 0] = 0
            
            alcance = x[-1] if y[-1] == 0 else max(x)

        t = np.linspace(0, t_voo, num=200)
        x = v0 * np.cos(ang) * t
        y = h0 + v0 * np.sin(ang) * t - 0.5 * g * t**2
        y[y < 0] = 0

        t_to_altura_max = v0 * np.sin(ang) / g
        
        vy_final = v0 * np.sin(ang) - g * t_voo
        vx_final = v0 * np.cos(ang)
        velocidade_final_mag = np.sqrt(vx_final**2 + vy_final**2)

        return x, y, alcance, altura_max, t_to_altura_max, velocidade_final_mag, t, t_voo

    def draw_vectors(ax, pos_x, pos_y, vx, vy, escala_plot_x, escala_plot_y):
        # A nova escala do vetor é uma proporção do tamanho total do gráfico
        # Fator de 0.08 para reduzir o tamanho dos vetores, deixando a visualização mais limpa
        vetor_length = 0.08 * max(escala_plot_x, escala_plot_y, 1)

        # Vetor de velocidade resultante
        ax.arrow(pos_x, pos_y, vx, vy,
                 head_width=0.03 * vetor_length, head_length=0.05 * vetor_length,
                 fc='blue', ec='blue', label='Vetor de Velocidade')
        
        # Componente X do vetor
        ax.arrow(pos_x, pos_y, vx, 0,
                 head_width=0.03 * vetor_length, head_length=0.05 * vetor_length,
                 fc='red', ec='red', ls='--', label='Componente Vx')
        
        # Componente Y do vetor
        ax.arrow(pos_x, pos_y, 0, vy,
                 head_width=0.03 * vetor_length, head_length=0.05 * vetor_length,
                 fc='green', ec='green', ls='--', label='Componente Vy')

        # Adicionar textos para os vetores
        ax.text(pos_x + vx, pos_y + vy, 'V', color='blue', fontsize=12)
        ax.text(pos_x + vx, pos_y, 'Vx', color='red', fontsize=12)
        ax.text(pos_x, pos_y + vy, 'Vy', color='green', fontsize=12)

    # --- Realizar os cálculos ---
    x, y, alcance, altura_max, t_to_altura_max, velocidade_final_mag, t, t_voo = calcular_trajetoria(
        velocidade_inicial, angulo_rad, gravidade, altura_inicial
    )
    
    # --- Plotar o gráfico e a animação ---
    chart_placeholder = st.empty()
    metric_placeholder = st.empty()

    if btn_iniciar_animacao:
        # Loop de animação
        for i in range(len(x)):
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.set_title("Animação da Trajetória")
            ax.set_xlabel("Distância Horizontal (m)")
            ax.set_ylabel("Altura (m)")
            ax.grid(True, linestyle='--', alpha=0.7)
            ax.set_aspect('equal', adjustable='box')
            
            ax.set_xlim(left=0, right=alcance * 1.1)
            ax.set_ylim(bottom=0, top=altura_max * 1.1)

            # Desenha a trilha pontilhada (parte da trajetória já percorrida)
            ax.plot(x[:i], y[:i], 'r--', alpha=0.5, label="Trajetória Completa")
            
            # Desenha o projétil na posição atual
            ax.plot(x[i], y[i], 'o', color='blue', markersize=8)
            
            if mostrar_vetores:
                # Componentes de velocidade no tempo atual
                vx_atual = velocidade_inicial * np.cos(angulo_rad)
                vy_atual = velocidade_inicial * np.sin(angulo_rad) - gravidade * t[i]
                
                draw_vectors(ax, x[i], y[i], vx_atual, vy_atual, ax.get_xlim()[1], ax.get_ylim()[1])

            # Atualiza o gráfico no placeholder
            chart_placeholder.pyplot(fig)
            plt.close(fig) # Fecha a figura para evitar sobrecarga de memória
            
            # Adiciona um pequeno atraso para a animação
            time.sleep(0.01)

    # Plotar o gráfico estático
    else:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(x, y, 'o-', markersize=2, label="Trajetória do Projétil")
        ax.set_title("Gráfico da Trajetória")
        ax.set_xlabel("Distância Horizontal (m)")
        ax.set_ylabel("Altura (m)")
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.set_aspect('equal', adjustable='box')
        ax.legend()
        
        # Ajusta os limites do gráfico dinamicamente
        ax.set_xlim(left=0, right=alcance * 1.1)
        ax.set_ylim(bottom=0, top=altura_max * 1.1)
        
        # Adicionar um ponto de lançamento
        ax.plot(0, altura_inicial, 'o', color='red', markersize=8, label="Ponto de Lançamento")

        if mostrar_vetores:
            # Vetores no ponto de lançamento
            vx_init = velocidade_inicial * np.cos(angulo_rad)
            vy_init = velocidade_inicial * np.sin(angulo_rad)
            draw_vectors(ax, x[0], y[0], vx_init, vy_init, ax.get_xlim()[1], ax.get_ylim()[1])

        chart_placeholder.pyplot(fig)
        
    with metric_placeholder.container():
        st.subheader("Resultados Calculados")
        col_res1, col_res2, col_res3 = st.columns(3)
        with col_res1:
            st.metric(label="Tempo p/ Altura Máx.", value=f"{t_to_altura_max:.2f} s")
        with col_res2:
            st.metric(label="Altura Máxima", value=f"{altura_max:.2f} m")
        with col_res3:
            st.metric(label="Velocidade Final", value=f"{velocidade_final_mag:.2f} m/s")
        
        st.metric(label="Alcance Máximo", value=f"{alcance:.2f} m")
        st.metric(label="Tempo de Voo", value=f"{t_voo:.2f} s")


    st.markdown("---")
    st.markdown("Autor: Prof. Ojeda")

