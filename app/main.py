import subprocess
import sys

from .builtin import builtin_command
from .logger import Logger
from .utils import find_executable, input_with_autocompletion, parse_args, redirect_output


def main():
    executables = find_executable()

    sys.stdout.write("$ ")
    user_command = input_with_autocompletion(sorted(list(builtin_command.keys()) + list(executables.keys())))

    args = parse_args(user_command)
    args, info_path, error_path, dump_mode = redirect_output(args)
    if not args:
        return

    for command, command_handler in builtin_command.items():
        if args[0] == command:
            command_handler(args)
            break
    else:
        if args[0] in executables:
            result = subprocess.run(args, capture_output=True, text=True)
            if result.stdout:
                Logger.info(result.stdout.strip())
            if result.stderr:
                Logger.error(result.stderr.strip())
        else:
            Logger.error(f"{args[0]}: command not found")

    Logger.dump(info_path, error_path, dump_mode)


if __name__ == "__main__":
    while True:
        main()
