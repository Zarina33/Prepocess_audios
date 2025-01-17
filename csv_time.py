import csv
from os.path import join
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from mutagen.flac import FLAC
from mutagen.wave import WAVE

def get_audio_duration(audio_path):
    try:
        if audio_path.endswith('.mp3'):
            audio = MP3(audio_path)
        elif audio_path.endswith('.mp4'):
            audio = MP4(audio_path)
        elif audio_path.endswith('.flac'):
            audio = FLAC(audio_path)
        elif audio_path.endswith('.wav'):
            audio = WAVE(audio_path)
        else:
            print(f"Формат файла {audio_path} не поддерживается.")
            return None

        duration = audio.info.length

        # Форматируем длительность в удобный вид (минуты:секунды)
        formatted_duration = "{:02d}:{:02d}".format(int(duration // 60), int(duration % 60))
        return formatted_duration

    except Exception as e:
        print(f"Ошибка при обработке файла {audio_path}: {e}")
        return None

# Функция для обновления CSV-файла с временем
def update_csv_with_duration(csv_file_path, audio_folder_path):
    updated_rows = []
    with open(csv_file_path, newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            audio_title = row['audio']
            audio_path = join(audio_folder_path, f"{audio_title}")  # Предполагается, что аудиофайлы имеют формат .mp3
            duration = get_audio_duration(audio_path)
            if duration is not None:
                row['время'] = duration
            else:
                row['время'] = 'не найдено или ошибка'
            updated_rows.append(row)

    # Обновляем CSV-файл с добавленной колонкой времени
    with open(csv_file_path, 'w', newline='') as csvfile:
        fieldnames = ['text', 'audio', 'время']
        csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter='\t')  # Указываем разделитель табуляции
        csv_writer.writeheader()
        csv_writer.writerows(updated_rows)

# Пример использования функции
csv_file_path = '/var/www/html/woman.csv'  # Путь к CSV-файлу с названиями аудиофайлов
audio_folder_path = '/var/www/html/female_voice'  # Путь к папке с аудиофайлами

update_csv_with_duration(csv_file_path, audio_folder_path)

