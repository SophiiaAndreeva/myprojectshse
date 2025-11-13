from datetime import datetime

formats = [
    '%A, %B %d, %Y',  # The Moscow Times
    '%A, %d.%m.%y',  # The Guardian
    '%A, %d %B %Y'  # Daily News
]

print("Введите даты в одном из форматов:")
print("1. The Moscow Times: Wednesday, October 2, 2002")
print("2. The Guardian: Friday, 11.10.13")
print("3. Daily News: Thursday, 18 August 1977")
print("Для выхода введите 'exit'")

while True:
    date_str = input("\nВведите дату: ").strip()

    if date_str.lower() == 'exit':
        break

    parsed = None
    for fmt in formats:
        try:
            parsed = datetime.strptime(date_str, fmt)
            break
        except ValueError:
            continue

    if parsed:
        print(parsed)
    else:
        print("Ошибка: неверный формат введения даты")