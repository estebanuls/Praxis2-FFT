mport matplotlib.pyplot as plt
import numpy as np

def iniciar_graficos(tam_onda, tam_espectro, sr):
    plt.ion()
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 5))

    linea_onda, = ax1.plot(np.zeros(tam_onda), animated=True)
    ax1.set_ylim(-1, 1)
    ax1.set_title("Forma de onda")

    linea_espectro, = ax2.plot(np.zeros(tam_espectro), animated=True)
    ax2.set_xlim(0, sr/2)
    ax2.set_title("Espectro")

    plt.tight_layout()
    fig.canvas.draw()

    # Fondo estático para blit
    fondo_onda = ax1.figure.canvas.copy_from_bbox(ax1.bbox)
    fondo_espec = ax2.figure.canvas.copy_from_bbox(ax2.bbox)

    return fig, linea_onda, linea_espectro, fondo_onda, fondo_espec


def actualizar_graficos(fig, linea_onda, linea_espectro, fondo_onda, fondo_espec, onda, espectro):
    try:
        canvas = fig.canvas

        # Restaurar fondos
        canvas.restore_region(fondo_onda)
        canvas.restore_region(fondo_espec)

        # Actualizar datos
        linea_onda.set_ydata(onda)
        linea_espectro.set_ydata(espectro)

        # Dibujar solo estas líneas (mucho más rápido)
        ax1 = linea_onda.axes
        ax2 = linea_espectro.axes

        ax1.draw_artist(linea_onda)
        ax2.draw_artist(linea_espectro)

        canvas.blit(ax1.bbox)
        canvas.blit(ax2.bbox)

        canvas.flush_events()

    except Exception as e:
        print(f"[Graphics] Error: {e}")
