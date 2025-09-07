from address_book import AddressBook, Record
import pickle

def inner_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return 'Give me correct name and phone please'
        except IndexError:
            return 'Not enough arguments'
        except AttributeError as e:
            return 'Contact not found'
    return inner

@inner_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@inner_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = 'Contact updated'
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = 'Contact added'
    if phone:
        record.add_phone(phone)
    return message

@inner_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    record.edit_phone(old_phone, new_phone)
    return f'Phone number for {name} was changed to {new_phone}'

@inner_error
def show_phone(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    phone = '; '.join(p.value for p in record.phones)
    return f'{name}: {phone}'

def show_all(book: AddressBook):
    if not book.data:
        return "No contacts found."
    result = []
    for record in book.data.values():
        phones = '; '.join(p.value for p in record.phones) if record.phones else "No phones"
        birthday = record.birthday.value if record.birthday else "No birthday"
        result.append(f'{record.name.value}: Phones: {phones}, Birthday: {birthday}')
    return '\n'.join(result)

@inner_error
def add_birthday(args, book: AddressBook):
    name, birthday, *_ = args
    record = book.find(name)
    record.add_birthday(birthday)
    return f"Birthday for {name} was added."

@inner_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if not record.birthday:
        return f'{name} does not have a birthday'
    return f"{name}'s birthday is {record.birthday.value}"

@inner_error
def birthdays(args, book: AddressBook):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return 'No upcoming birthdays this week'
    result = []
    for user in upcoming:
        result.append(f"{user['name']}: {user['congratulation_date']}")
    return '\n'.join(result)

def save_data(book, filename = 'addressbook.pkl'):
    with open(filename, 'wb') as f:
        pickle.dump(book, f)

def load_data(filename = 'addressbook.pkl'):
    try:
        with open(filename, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()


def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book)
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()