import numpy as np
import sounddevice as sd
import soundfile as sf
import threading
import time
import mido

from arduino_serial import hilo_arduino
from audio_processing import detectar_picos, crear_estado, procesar_audio
from graphics import iniciar_graficos, actualizar_graficos
from utils import guardar_salida

PUERTO_SERIE = "COM3"
BAUD = 115200
ARCHIVO_WAV = "tu_audio.wav"
SALIDA = "salida.wav"

BLOCK = 2048
HOP = BLOCK // 2
ANCHO = 4.0
MUESTRAS_GRAFICO = 1024

# CARGAR AUDIO

audio, sr = sf.read(ARCHIVO_WAV)
if audio.ndim > 1:
    audio = audio[:, 0]
audio = audio.astype(np.float32)

bins, freqs_global = detectar_picos(audio, sr)
state = crear_estado(audio, sr, BLOCK, HOP, bins, freqs_global)

# Variables globales
pot = [512] * 6
run = [True]


# GRAFICOS (con blitting)
(
    fig,
    linea_onda,
    linea_espectro,
    fondo_onda,
    fondo_espec
) = iniciar_graficos(MUESTRAS_GRAFICO, BLOCK // 2 + 1, sr)

cb_state = {
    "onda": np.zeros(MUESTRAS_GRAFICO),
    "espectro": np.zeros(BLOCK // 2 + 1),
    "buffer": []
}


MIDI_PORT_NAME = "Puerto_Virtual 1"

try:
    outport = mido.open_output(MIDI_PORT_NAME)
    print(f"[MIDI] Puerto abierto: {MIDI_PORT_NAME}")
except Exception as e:
    print(f"[MIDI] Error al abrir puerto: {e}")
    outport = None



def callback(outdata, frames, t, status):
    sal, X = procesar_audio(state, pot, BLOCK, HOP, ANCHO)
    outdata[:, 0] = sal

    # Actualizar buffer para guardar salida
    cb_state["buffer"].append(sal.copy())

    # Update realtime displays
    cb_state["onda"][:len(sal)] = sal
    cb_state["espectro"][:] = np.abs(X)

    # Enviar MIDI (0–5 CC)
    if outport:
        for i, p in enumerate(pot):
            val = int(p / 1023 * 127)
            msg = mido.Message("control_change", control=i, value=val)
            outport.send(msg)



thr = threading.Thread(
    target=hilo_arduino,
    args=(pot, run, PUERTO_SERIE, BAUD),
    daemon=True
)
thr.start()



try:
    with sd.OutputStream(
        channels=1,
        samplerate=sr,
        blocksize=HOP,
        callback=callback
    ):
        print("[Audio] Reproduciendo...")

        while run[0]:
            actualizar_graficos(
                fig,
                linea_onda,
                linea_espectro,
                fondo_onda,
                fondo_espec,
                cb_state["onda"],
                cb_state["espectro"]
            )

            # Mucho más fluido
            time.sleep(0.01)

except KeyboardInterrupt:
    run[0] = False

finally:
    guardar_salida(SALIDA, cb_state["buffer"], sr)
    print("[Main] Terminado")
