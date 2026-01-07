import sys
import os
from typing import Callable, Dict

def handle_exit(command: str):
    exit()


def handle_echo(command: str):
    message = command[5:]
    print(message)


def handle_type(command: str):
    message = command[5:]
    builtin_command_strip = [command.strip() for command in builtin_command.keys()]
    if message.strip() in builtin_command_strip:
        print(f"{message} is a shell builtin")
        return

    PATH = os.environ["PATH"]
    for path in PATH.split(os.pathsep):
        if not os.path.exists(path):
            continue

        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            if message == filename and os.path.isfile(file_path) and os.access(file_path, os.X_OK):
                print((f"{message} is {file_path}"))
                return

    print(f"{message}: not found")


builtin_command: Dict[str, Callable] = {
    "exit": handle_exit,
    "echo ": handle_echo,
    "type ": handle_type,
}


def main():
    while True:
        sys.stdout.write("$ ")
        user_command = input()

        for command, command_handler in builtin_command.items():
            if user_command.startswith(command):
                command_handler(user_command)
                break
        else:
            print(f"{user_command}: command not found")


if __name__ == "__main__":
    main()
