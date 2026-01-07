import subprocess
import sys
import os
from typing import Callable, Dict


def find_executable(command: str) -> str:
    PATH = os.environ["PATH"]
    for path in PATH.split(os.pathsep):
        if not os.path.exists(path):
            continue

        file_path = os.path.join(path, command)
        if os.access(file_path, os.X_OK):
            return file_path

    return ""


def handle_exit(command: str):
    exit()


def handle_echo(command: str):
    message = command[5:]
    print(message)


def handle_type(command: str):
    message = command[5:]
    if message.strip() in builtin_command:
        print(f"{message} is a shell builtin")
        return

    if exec_path := find_executable(message):
        print((f"{message} is {exec_path}"))
        return

    print(f"{message}: not found")


def handle_pwd(command: str):
    print(os.getcwd())


builtin_command: Dict[str, Callable] = {
    "exit": handle_exit,
    "echo": handle_echo,
    "type": handle_type,
    "pwd": handle_pwd,
}


def main():
    while True:
        sys.stdout.write("$ ")
        user_command = input()
        args = user_command.split(" ")

        for command, command_handler in builtin_command.items():
            if args[0] == command:
                command_handler(user_command)
                break
            elif find_executable(args[0]):
                result = subprocess.run(args, capture_output=True, text=True)
                if result.stdout:
                    print(result.stdout.strip())
                if result.stderr:
                    print(result.stderr.strip())
                break
        else:
            print(f"{args[0]}: command not found")


if __name__ == "__main__":
    main()
