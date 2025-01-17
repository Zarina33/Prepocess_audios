import os
import pandas as pd
from pydub.utils import mediainfo
from pydub import AudioSegment

def get_audio_duration(file_path):
    """
    Function to get the duration of an audio file in seconds.
    """
    audio = AudioSegment.from_file(file_path)
    duration_seconds = len(audio) / 1000.0  # Convert to seconds
    return duration_seconds

def sum_audio_durations(csv_file_path):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)

    total_duration = 0.0

    for index, row in df.iterrows():
        audio_file_url = row['audio']
        if not pd.isnull(audio_file_url):
            # Assuming 'AudioFile' column contains URLs or file paths
            audio_file_path = os.path.join('/var/www/html/female_voice_wav', audio_file_url)
            if os.path.exists(audio_file_path):
                duration = get_audio_duration(audio_file_path)
                total_duration += duration

    return total_duration

csv_file_path = "/var/www/html/woman.csv"
total_duration = sum_audio_durations(csv_file_path)
total_duration_hours = total_duration / 3600
print(f"Суммарная продолжительность аудио в файле: {total_duration_hours:.2f} часов")

