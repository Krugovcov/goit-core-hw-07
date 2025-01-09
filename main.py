def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Enter the argument for the command"
        except IndexError:
            return "Please provide the correct number of arguments"
        except KeyError:
            return "Contact not found."
        except Exception as e:
            return str(e)
    return inner

@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, contacts):
    name, phone = args  
    contacts[name] = phone
    return "Contact added."

@input_error
def change_contact(args, contacts):
    name, phone = args  
    if name in contacts:
        contacts[name] = phone
        return "Contact updated"
    else:
        raise KeyError

@input_error
def show_phone(args, contacts):
    name = args[0]  
    if name in contacts:
        return f"Phone number for {name}: {contacts[name]}"
    else:
        raise KeyError

@input_error
def show_all_phones(contacts):
    if not contacts:
        return "No contacts available."
    return "\n".join([f"{name}: {phone}" for name, phone in contacts.items()])

def main():
    contacts = {}
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all_phones(contacts))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()