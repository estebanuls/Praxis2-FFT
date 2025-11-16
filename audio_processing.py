import numpy as np
from utils import db_a_lineal, mapear_ganancia_db, mapear_volumen

def detectar_picos(audio, sr):
    segmento = audio[:min(len(audio), sr * 10)]
    Xg = np.fft.rfft(segmento * np.hanning(len(segmento)))
    magn = np.abs(Xg)
    freqs = np.fft.rfftfreq(len(segmento), 1/sr)
    magn[0] = 0
    bins = np.argsort(magn)[::-1][:5]
    return bins, freqs

def crear_estado(audio, sr, block, hop, bins, freqs):
    return {
        "pos": 0,
        "solapamiento": np.zeros(hop, dtype=np.float32),
        "audio": audio,
        "sr": sr,
        "bins": bins,
        "freqs_global": freqs,
        "ventana": np.hanning(block)
    }

def procesar_audio(state, potenciometros, block, hop, ancho):
    pos = state["pos"]
    audio = state["audio"]
    sr = state["sr"]
    ventana = state["ventana"]

    if pos + block > len(audio):
        pos = 0

    bloque = audio[pos:pos+block]
    if len(bloque) < block:
        bloque = np.pad(bloque, (0, block - len(bloque)))

    bloque_w = bloque * ventana
    X = np.fft.rfft(bloque_w)
    freqs_b = np.fft.rfftfreq(block, 1/sr)

    ganancias = [db_a_lineal(mapear_ganancia_db(potenciometros[i])) for i in range(5)]
    vol = mapear_volumen(potenciometros[5])

    idx = np.arange(len(X))

    for g, bp in zip(ganancias, state["bins"]):
        f_p = state["freqs_global"][bp]
        bin_loc = np.argmin(np.abs(freqs_b - f_p))
        mascara = np.exp(-0.5 * ((idx - bin_loc) / ancho)**2)
        X *= 1 + (g - 1) * mascara

    bloque_p = np.fft.irfft(X, n=block)
    salida = bloque_p[:hop] + state["solapamiento"]
    state["solapamiento"][:] = bloque_p[hop:]
    state["pos"] = pos + hop

    salida *= vol
    if np.max(np.abs(salida)) > 1:
        salida /= np.max(np.abs(salida))

    return salida.astype(np.float32), X
