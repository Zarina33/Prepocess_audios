import os

dir_path = '/var/www/html/female_voice/'

for filename in os.listdir(dir_path):
    if filename.endswith('.mp3'):
        parts = filename.split('.')
        new_filename = parts[0] + '.mp3'
        old_path = os.path.join(dir_path, filename)
        new_path = os.path.join(dir_path, new_filename)

        # Переименовываем файл
        try:
            os.rename(old_path, new_path)
            print('Файл успешно переименован:', new_filename)
        except Exception as e:
            print('Не удалось переименовать файл:', old_path)
            print('Ошибка:', str(e))

