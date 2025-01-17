import csv

# Открываем существующий CSV файл для чтения и новый CSV файл для записи
with open('/home/ulan/Downloads/man(1).csv', 'r', newline='') as input_file, \
     open('m.csv', 'w', newline='') as output_file:
     
    # Создаем объекты для чтения и записи CSV
    reader = csv.reader(input_file)
    writer = csv.writer(output_file)
    
    for row in reader:
        # Объединяем два столбца в один, разделяя их символом '|'
        combined_value = row[0] + '|' + row[1]
        
        # Записываем объединенное значение в новый CSV файл
        writer.writerow([combined_value])

