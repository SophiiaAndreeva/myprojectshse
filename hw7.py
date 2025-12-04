def main():
   """Главная функция"""
   input_file = "web_clients_correct-старое.csv"
   output_file = "homework.txt"

   try:
        lines = read_csv_file(input_file) # Загрузка
        customers = parse_csv_data(lines) # Парсинг

        descriptions = [] # Список описаний каждого покупателя
        for customer in customers:
            description = create_description(customer)
            descriptions.append(description)

        write_output_file(descriptions, output_file) # Запись описаний в файл
        print(f"Сгенерировано {len(descriptions)} описаний. Файл сохранен: {output_file}")

   except FileNotFoundError:
        print("Ошибка: файл 'web_clients_correct-старое.csv' не найден!")

def read_csv_file(filepath):
    """Чтение csv-файла"""
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.readlines()

def parse_csv_data(lines):
    """Парсинг данных"""
    if not lines: # Проверяю, что файл не пустой
        return []

    headers = [head.strip() for head in lines[0].strip().split(',')] # Беру заголовки с 0 строки

    customers = [] # Список с данными покупателей
    for line in lines[1:]:
        values = line.strip().split(',')  # разделяю по запятым каждую строчку

        customer = {} # словарь с данными для 1 покупателя
        for i in range(len(headers)):
            customer[headers[i]] = values[i]
        customers.append(customer)
    return customers

def create_description(customer):
    """Создание описания для одного покупателя"""
    gender_info = get_gender_info(customer['sex'], customer['age']) # получаю инфо по полу и возрасту
    device_rus = transform_device_type(customer['device_type']) # Тип устройства перевожу на руссский

    region = customer['region'] # собиарю инфо о регионе
    if region == '-':
        region_text = "Регион покупки не указан."
    else:
        region_text = f"Регион, из которого совершалась покупка: {region}."

    description = ( # Делаю описание по шаблону
        f"Пользователь {customer['name']} {gender_info['pronoun']} пола, "
        f"{customer['age']} {gender_info['age_word']} {gender_info['verb']} покупку на "
        f"{customer['bill']} у.е. с {device_rus} браузера {customer['browser']}. "
        f"{region_text}"
    )
    return description

def get_gender_info(sex, age):
    """Определение окончания пола"""
    age_str = str(age).strip() # Перевожу возраст в строку

    if age_str == '0.67': # Обрабатываю ошибку из файла :)
        age_int = 67
    else:
        try:
            age_int = int(float(age_str.replace(',', '.'))) # Первеожу 0,67 в 0.67, а затем в int
        except (ValueError, TypeError):
            age_int = 0

    if sex == 'female':
        return {
            'pronoun': 'женского',
            'verb': 'совершила',
            'age_word': get_correct_age_word(age_int)
        }
    else:
        return {
            'pronoun': 'мужского',
            'verb': 'совершил',
            'age_word': get_correct_age_word(age_int)
        }

def get_correct_age_word(age):
    """Определение написания слова 'Год'"""
    if 11 <= age % 100 <= 19: # Исключения для "лет"
        return "лет"
    elif age % 10 == 1: # Исключения для "год"
        return "год"
    elif 2 <= age % 10 <= 4:
        return "года"
    else:
        return "лет"

def transform_device_type(device):
    """Перевод типа устройства на русский язык"""
    device_translation = {
        'mobile': 'мобильного',
        'tablet': 'планшета',
        'desktop': 'компьютера',
        'laptop': 'ноутбука',
    }
    return device_translation.get(device, device)

def write_output_file(descriptions, output_path):
    """Запись в файл"""
    with open(output_path, 'w', encoding='utf-8') as file:
        for description in descriptions:
            file.write(description + '\n\n') # Между записями делаю пустую строчку

if __name__ == "__main__":   # эту строчку написала при помощи интернета
    main()







