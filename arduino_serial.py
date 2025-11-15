import serial

def hilo_arduino(pot_ref, ejecutar_ref, puerto, baudrate):
    try:
        ser = serial.Serial(puerto, baudrate, timeout=0.1)
        print(f"[Serial] Conectado a {puerto}")
    except Exception as e:
        print(f"[Serial] Error: {e}")
        ejecutar_ref[0] = False
        return

    while ejecutar_ref[0]:
        try:
            linea = ser.readline().decode(errors='ignore').strip()
            partes = linea.replace(';', ',').split(',')
            if len(partes) >= 6:
                valores = [max(0, min(1023, int(float(x)))) for x in partes[:6]]
                pot_ref[:] = valores
        except:
            pass

    try: ser.close()
    except: pass
