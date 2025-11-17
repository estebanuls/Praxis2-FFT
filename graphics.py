mport matplotlib.pyplot as plt
import numpy as np

def iniciar_graficos(tam_onda, tam_espectro, sr):
    """
    Inicializa las gráficas de forma de onda y espectro.
    Devuelve: fig, linea_onda, linea_espectro
    """
    plt.ion()
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 5))

    linea_onda, = ax1.plot(np.zeros(tam_onda))
    ax1.set_ylim(-1, 1)
    ax1.set_title("Forma de onda")

    # Línea del espectro
    linea_espectro, = ax2.plot(np.zeros(tam_espectro))
    ax2.set_xlim(0, sr/2)
    ax2.set_title("Espectro")

    plt.tight_layout()
    return fig, linea_onda, linea_espectro

def actualizar_graficos(linea_onda, linea_espectro, onda, espectro):
    """
    Actualiza los datos de la forma de onda y del espectro.
    """
    try:
        linea_onda.set_ydata(onda)
        linea_espectro.set_ydata(espectro)
        plt.pause(0.01)
    except Exception as e:
        print(f"[Gráficos] Error al actualizar: {e}")
