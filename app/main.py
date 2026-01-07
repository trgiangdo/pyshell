import sys


def main():
    while True:
        sys.stdout.write("$ ")
        command = input()

        if command == "exit":
            exit()
        if command.startswith("echo "):
            message = command[5:]
            print(message)
            continue

        print(f"{command}: command not found")


if __name__ == "__main__":
    main()
