import os
import scipy.io.wavfile as wavfile
from scipy import signal
import random
import pandas as pd
from sklearn.model_selection import train_test_split
from pydub import AudioSegment
import soundfile as sf

# Путь к исходному файлу CSV
csv_file_path = '/home/ulan/Documents/M/man.csv'

# Процентное соотношение выборок
val_ratio = 0.15
test_ratio = 0.15

# Загрузка данных из CSV-файла с использованием pandas
data = pd.read_csv(csv_file_path)

# Разделение данных на тренировочную, валидационную и тестовую выборки
train_data, temp_data = train_test_split(data, test_size=val_ratio+test_ratio, random_state=42)
val_data, test_data = train_test_split(temp_data, test_size=test_ratio/(val_ratio+test_ratio), random_state=42)

# Пути для сохранения разделенных выборок в txt-файлы
train_txt_path = '/home/ulan/tts/tacotron2/filelists/train.txt'
val_txt_path = '/home/ulan/tts/tacotron2/filelists/validate.txt'
test_txt_path = '/home/ulan/tts/tacotron2/filelists/test.txt'

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


	
def resample_audio(input_path, output_path, target_sample_rate):
    # Чтение аудиофайла
    sample_rate, audio_data = wavfile.read(input_path)
    
    # Вычисление коэффициента ресемплинга
    resample_factor = target_sample_rate / sample_rate
    
    # Ресемплинг аудио
    resampled_audio = signal.resample(audio_data, int(len(audio_data) * resample_factor))
    
    # Сохранение ресемплированного аудио в файл
    wavfile.write(output_path, target_sample_rate, resampled_audio.astype(audio_data.dtype))

# Функция для сохранения данных в txt-файл
def save_to_txt(data, file_path, i):
    with open(file_path, 'w') as f:
        for index, row in data.iterrows():
            line = ','.join([str(value) for value in row]) + '\n'
            audio = row['data'].split('|')[0]
            audio_path = '/home/ulan/tts/tacotron2/wavs1/'+audio+'.wav'
            audio_p = AudioSegment.from_file(audio_path)
            l = len(audio_p)
            if l > 1050:
                stereo_audio = AudioSegment.from_file(audio_path)
                mono_audio = stereo_audio.set_channels(1)
                mono_audio.export('/home/ulan/tts/tacotron2/mono/'+audio+'.wav', format='wav')
                change_audio_format('/home/ulan/tts/tacotron2/mono/'+audio+'.wav', '/home/ulan/tts/tacotron2/wavs/'+audio+'.wav', target_sample_rate, target_bitrate)
                f.write(line)
                

# Сохранение выборок в txt-файлы
save_to_txt(train_data, train_txt_path, 0)
save_to_txt(val_data, val_txt_path, 0)
save_to_txt(test_data, test_txt_path, 0)

