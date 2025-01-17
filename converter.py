import os
import subprocess

input_folder = "/var/www/html/female_voice_wav_add"
output_folder = "/var/www/html/female_voice_wav"

# Проверка, существуют ли папки для входных и выходных файлов
if not os.path.exists(input_folder):
    print("Папка с входными файлами не найдена.")
    exit()

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Получение списка файлов .wav в папке с входными файлами
wav_files = [f for f in os.listdir(input_folder) if f.endswith(".wav")]

# Конвертация файлов
for wav_file in wav_files:
    input_path = os.path.join(input_folder, wav_file)
    filename = os.path.splitext(wav_file)[0]
    output_filename = filename + ".mp3"
    output_path = os.path.join(output_folder, output_filename)

    # Вызов команды FFmpeg для конвертации файла
    subprocess.call(["ffmpeg", "-i", input_path, output_path])

print("Конвертация завершена.")

