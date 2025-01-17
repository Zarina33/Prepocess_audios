import scipy.io.wavfile as wavfile
import pandas as pd
from scipy import signal

def resample_audio(input_path, output_path, target_sample_rate):
    # Чтение аудиофайла
    sample_rate, audio_data = wavfile.read(input_path)
    
    # Вычисление коэффициента ресемплинга
    resample_factor = target_sample_rate / sample_rate
    
    # Ресемплинг аудио
    resampled_audio = signal.resample(audio_data, int(len(audio_data) * resample_factor))
    
    # Сохранение ресемплированного аудио в файл
    wavfile.write(output_path, target_sample_rate, resampled_audio.astype(audio_data.dtype))

# Пример использования для снижения частоты дискретизации с 48 кГц до 44,1 кГц



csv_file_path = '/home/ulan/Documents/M/man.csv'

# Загрузка данных из CSV-файла с использованием pandas
data = pd.read_csv(csv_file_path)

for index, row in data.iterrows():
	audio = row['data'].split('|')[0]
	out_audio = audio
	audio_path = f'/home/ulan/tts/tacotron2/wavs/{audio}.wav'
    
    
    
	resample_audio(audio_path, f"/home/ulan/tts/tacotron2/changed_audio/{audio}.wav", 44100)

import soundfile as sf
from scipy import signal
from pydub import AudioSegment

def change_audio_format(input_path, output_path, target_sample_rate, target_bitrate):
    # Загрузка аудиофайла
    audio, sample_rate = sf.read(input_path)

    # Изменение частоты дискретизации
    resampled_audio = signal.resample(audio, int(len(audio) * target_sample_rate / sample_rate))

    # Изменение битности на 16 бит
    resampled_audio_16bit = (resampled_audio * 32767).astype('int16')

    # Сохранение аудиофайла с новой частотой дискретизации и битностью
    sf.write(output_path, resampled_audio_16bit, target_sample_rate)

    # Преобразование в AudioSegment для изменения битрейта
    audio_segment = AudioSegment.from_wav(output_path)
    audio_segment.export(output_path, format="wav")

# Целевые значения
target_sample_rate = 16000
target_bitrate = 256

# Использование функции для изменения формата
change_audio_format("input.wav", "output.wav", target_sample_rate, target_bitrate)
    
