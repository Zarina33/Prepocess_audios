import soundfile as sf

# Путь к аудиофайлу
audio_path = "/home/ulan/tts/tacotron2/wavs/m3_1_002.wav"

# Открываем аудиофайл и получаем информацию о нем
audio_info = sf.info(audio_path)

# Получение битности из параметров аудиофайла
bit_depth = audio_info.subtype[-2:]  # Получаем последние два символа из subtype

print(f"Битность: {bit_depth} бит")

