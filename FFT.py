import sounddevice as sd
import soundfile as sf

AUDIO_PATH = "./audio/base.wav"   # archivo de prueba

def play_audio(path):
    data, samplerate = sf.read(path)
    sd.play(data, samplerate)
    sd.wait()

if __name__ == "__main__":
    print("Reproduciendo audio base...")
    play_audio(AUDIO_PATH)
    print("Fin.")
