from pydub import AudioSegment
import os

def get_audio_duration(audio_file):
    audio = AudioSegment.from_file(audio_file)
    return audio.duration_seconds

def sum_audio_durations(audio_folder):
    total_duration = 0

    for filename in os.listdir(audio_folder):
        if filename.endswith('.mp3') or filename.endswith('.wav'):
            audio_file_path = os.path.join(audio_folder, filename)
            total_duration += get_audio_duration(audio_file_path)

    return total_duration
 # Замените 'путь_к_папке_с_аудиофайлами' на реальный путь к папке с вашими аудиофайлами
folder_path = '/home/ulan/Documents/female_voices'
total_duration = sum_audio_durations(folder_path)
total_duration =total_duration/3600
print(f"Общая длительность аудио в папке: {total_duration:.2f} hours")
