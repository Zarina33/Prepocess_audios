import soundfile as sf

# Путь к аудиофайлу
audio_path = "/home/ulan/tts/tacotron2/wavs/m3_1_002.wav"

# Открываем аудиофайл и получаем аудиоволну и частоту дискретизации
audio_data, samplerate = sf.read(audio_path)

min_value = audio_data.min()
max_value = audio_data.max()

print(f"Минимальное значение: {min_value}")
print(f"Максимальное значение: {max_value}")

