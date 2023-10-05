import numpy as np
from scipy.io import wavfile
import re
sample_rate = 44100  # サンプリング周波数 (Hz)
def Beep3(wave,frequency1, frequency2, frequency3, duration):
    fundamental_amplitude = 0.5    # 第1フォルマントの振幅
    formant2_amplitude = 0.3    # 第2フォルマントの振幅
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    fundamental_wave = fundamental_amplitude * np.sin(2 * np.pi * frequency1 * t)
    formant2_wave = formant2_amplitude * np.sin(2 * np.pi * frequency2 * t)
    formant3_wave = formant2_amplitude * np.sin(2 * np.pi * frequency3 * t)
    
    final_wave = fundamental_wave + formant2_wave + formant3_wave

    final_wave_int = np.int16(final_wave * 32767)
    return np.append(wave, final_wave)


def VML(text:str):
    waves = np.array([])
    for i in text.split("\n"):
        line = i.replace("\n","")
        re_line = re.sub(r"F([0-9]{2,4}),([0-9]{2,4}),([0-9]{2,4}):S([0-9]*\.[0-9]{1,12});", r"\1 \2 \3 \4", line)
        print("["+re_line+"]")
        re_line_sp = re_line.split(" ")
        waves = Beep3(waves, int(re_line_sp[0]), int(re_line_sp[1]), int(re_line_sp[2]),float(re_line_sp[3]) )
    return waves
def VML_WAV(text, filename):
    wavfile.write(filename, sample_rate, VML(text))

if __name__ == "__main__":
    VML_WAV("F440,440,440:S1.0;", "IUIIAAEEO.wav")