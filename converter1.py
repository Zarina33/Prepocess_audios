import os
import subprocess

input_folder = "/var/www/html/man_voice"
output_folder = "/var/www/html/man_wav"

# Проверка, существуют ли папки для входных и выходных файлов
if not os.path.exists(input_folder):
    print("Папка с входными файлами не найдена.")
    exit()

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Получение списка файлов .mp3 в папке с входными файлами
mp3_files = [f for f in os.listdir(input_folder) if f.endswith(".mp3")]

# Конвертация файлов
for mp3_file in mp3_files:
    input_path = os.path.join(input_folder, mp3_file)
    filename = os.path.splitext(mp3_file)[0]
    output_filename = filename + ".wav"
    output_path = os.path.join(output_folder, output_filename)

    # Вызов команды FFmpeg для конвертации файла
    subprocess.call(["ffmpeg", "-i", input_path, output_path])

print("Конвертация завершена.")

