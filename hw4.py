documents = [
    {'type': 'passport', 'number': '2207 876234', 'name': 'Василий Гупкин'},
    {'type': 'invoice', 'number': '11-2', 'name': 'Геннадий Покемонов'},
    {'type': 'insurance', 'number': '10006', 'name': 'Аристарх Павлов'}
    ]

directories = {
    '1': ['2207 876234', '11-2'],
    '2': ['10006'],
    '3': []
}

def document_owner_name(doc_number: str) -> str | None:
    for document in documents:
        if document['number'] == doc_number:
            return document['name']
    return None
def command_p():
    doc_number = input("Введите номер документа: ")
    owner = document_owner_name(doc_number)
    if owner:
        print(f"Владелец документа: {owner}")
    else:
        print("Документ не найден.")
def main():
    while True:
        command = input("\nВведите команду: ").lower()
        if command == 'p':
            command_p()
        elif command == 'q':
            print("Программа завершена.")
            break
        else:
            print("Неизвестная команда. Введите p или q")
if __name__ == '__main__':
    main()