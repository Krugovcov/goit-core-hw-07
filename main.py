from collections import UserDict
from datetime import datetime, timedelta


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Birthday(Field):
    def __init__(self, value):
        try:
            if isinstance(value, str):
                if datetime.strptime(value, "%d.%m.%Y"):
                    parsed_date = datetime.strptime(value, "%d.%m.%Y")
                    self.value = parsed_date
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Phone(Field):
    def __init__(self, number):
        if not isinstance(number, str) or not number.isdigit() or len(number) != 10:
            raise ValueError("The phone number must be a string of 10 digits")
        super().__init__(number)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, number):
        phone = Phone(number)
        self.phones.append(phone)

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def remove_phone(self, number):
        for phone in self.phones:
            if phone.value == number:
                self.phones.remove(phone)
                return True
        return False

    def edit_phone(self, old_number, new_number):
        if self.find_phone(old_number):
            self.add_phone(new_number)
            self.remove_phone(old_number)
            return True
        else:
            raise ValueError(f"Old number {old_number} not found")

    def find_phone(self, number):
        for phone in self.phones:
            if phone.value == number:
                return phone
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise ValueError(f"Record with name {name} not found.")

    def get_upcoming_birthdays(self):
        today = datetime.now()
        upcoming_birthdays = []
        for record in self.data.values():
            if record.birthday:
                this_year_birthday = record.birthday.value.replace(year=today.year)
            if this_year_birthday < today:
                this_year_birthday = this_year_birthday.replace(year=today.year + 1)

            days_until_birthday = (this_year_birthday - today).days

            if 0 <= days_until_birthday <= 7:
                if this_year_birthday.weekday() in (5, 6):  #
                    this_year_birthday += timedelta(days=(7 - this_year_birthday.weekday()))
                upcoming_birthdays.append({
                    "name": record.name.value,
                    "birthday": this_year_birthday.strftime("%d.%m.%Y")
                })
        return upcoming_birthdays

    def __str__(self):
        if not self.data:
            return "The address book is empty."
        return "\n".join(str(record) for record in self.data.values())


# Decorator to handle input errors
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return f"ValueError: {e}"
        except IndexError:
            return "Please provide the correct number of arguments."
        except KeyError:
            return "Contact not found."
        except Exception as e:
            return str(e)

    return inner


@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args


@input_error
def add_contact(args, address_book):
    name, phone = args
    if name in address_book.data:
        raise ValueError(f"Contact with name {name} already exists.")
    record = Record(name)
    record.add_phone(phone)
    address_book.add_record(record)
    return "Contact added."


@input_error
def show_upcoming_birthdays(address_book):
    upcoming = address_book.get_upcoming_birthdays()
    if not upcoming:
        return "No upcoming birthdays."
    return "\n".join([f"{item['name']}: {item['birthday']}" for item in upcoming])


@input_error
def change_contact(args, address_book):
    name, old_phone, new_phone = args  # Extract name, old phone, and new phone
    record = address_book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return "Contact updated."
    else:
        raise KeyError(f"Contact with name {name} not found.")


@input_error
def show_phone(args, address_book):
    name = args[0]  # Extract name
    record = address_book.find(name)
    if record:
        return f"Phone(s) for {name}: {', '.join(phone.value for phone in record.phones)}"
    else:
        raise KeyError


@input_error
def show_all_phones(address_book):
    if not address_book.data:
        return "No contacts available."
    return "\n".join([str(record) for record in address_book.data.values()])


@input_error
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    if not record:
        raise ValueError(f"Contact {name} not found.")
    record.add_birthday(birthday)
    return f"Birthday {birthday} added to contact {name}."


@input_error
def show_birthday(args, address_book):
    name = args[0]
    rest_of_args = args[1:]
    record = address_book.find(name)
    if not record or not record.birthday:
        raise ValueError(f"No birthday found for contact {name}.")
    return f"Birthday of {name}: {record.birthday.value.strftime('%d.%m.%Y')}"


@input_error
def show_upcoming_birthdays(book):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No upcoming birthdays."
    return "\n".join([f"{item['name']}: {item['birthday']}" for item in upcoming])


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = user_input.split(maxsplit=1)
        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args[0].split(), book))
        elif command == "change":
            print(change_contact(args[0].split(), book))
        elif command == "phone":
            print(show_phone(args[0].split(), book))
        elif command == "all":
            print(show_all_phones(book))
        elif command == "add-birthday":
            print(add_birthday(args[0].split(), book))
        elif command == "show-birthday":
            print(show_birthday(args[0].split(), book))
        elif command == "birthdays":
            print(show_upcoming_birthdays(book))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()