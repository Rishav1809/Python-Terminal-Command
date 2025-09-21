# -------------------------------
# Python Command Terminal with AI Features
# -------------------------------

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from commands import list_files, change_dir, make_dir, remove, show_cpu, show_mem
import os
import shutil
from dotenv import load_dotenv
import openai

# -------------------------------
# Load OpenAI API Key
# -------------------------------
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# -------------------------------
# Command List and Auto-Completion
# -------------------------------
commands_list = ['ls', 'cd', 'pwd', 'mkdir', 'rm', 'cpu', 'mem', 'exit']
command_completer = WordCompleter(commands_list, ignore_case=True)
session = PromptSession(completer=command_completer)

# -------------------------------
# AI Command Handler
# -------------------------------
def ai_command(prompt):
    """Send prompt to OpenAI and return interpreted command."""
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Convert this natural language command into a Python terminal command: {prompt}",
            max_tokens=100,
            temperature=0
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print("AI Error:", e)
        return None

# -------------------------------
# Local Natural Language Parser (Fallback)
# -------------------------------
def parse_natural_command(command):
    """Fallback parser for basic natural commands."""
    command = command.lower().strip()
    
    if "create folder" in command:
        folder_name = command.split("create folder")[-1].strip().split()[0]
        make_dir(folder_name)
        return

    if "remove" in command:
        target = command.split("remove")[-1].strip().split()[0]
        remove(target)
        return

    if "move" in command and "into" in command:
        parts = command.split("move")[-1].strip().split()
        if len(parts) >= 3:
            src = parts[0]
            dest = parts[2]
            if os.path.exists(src) and os.path.exists(dest):
                shutil.move(src, os.path.join(dest, os.path.basename(src)))
                print(f"Moved {src} into {dest}")
            else:
                print("Source or destination does not exist.")
        return

    print(f"Command not recognized: {command}")

# -------------------------------
# Execute a single command (for Streamlit)
# -------------------------------
def execute_command(user_input):
    """Executes a command and returns the output as string."""
    from io import StringIO
    import sys

    # Capture printed output
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()

    try:
        cmd_parts = user_input.split()
        cmd = cmd_parts[0]
        args = cmd_parts[1:]

        if cmd == 'ls':
            list_files()
        elif cmd == 'cd':
            if args:
                change_dir(args[0])
            else:
                print("Usage: cd <directory>")
        elif cmd == 'pwd':
            print(os.getcwd())
        elif cmd == 'mkdir':
            if args:
                make_dir(args[0])
            else:
                print("Usage: mkdir <directory>")
        elif cmd == 'rm':
            if args:
                remove(args[0])
            else:
                print("Usage: rm <file/dir>")
        elif cmd == 'cpu':
            show_cpu()
        elif cmd == 'mem':
            show_mem()
        elif cmd == 'exit':
            print("Exiting terminal...")
        else:
            ai_result = ai_command(user_input)
            if ai_result:
                print(f"AI suggests: {ai_result}")
                parse_natural_command(ai_result)
            else:
                parse_natural_command(user_input)

    except Exception as e:
        print(f"Error: {str(e)}")

    # Restore stdout
    sys.stdout = old_stdout
    return mystdout.getvalue()

# -------------------------------
# Main Terminal Loop
# -------------------------------
def main():
    print("Welcome to Python Command Terminal!")
    print("Available commands:")
    print("  ls                : List files in current directory")
    print("  cd <dir>          : Change directory")
    print("  pwd               : Show current directory")
    print("  mkdir <dir>       : Create a new directory")
    print("  rm <file/dir>     : Remove a file or directory")
    print("  cpu               : Show CPU usage")
    print("  mem               : Show memory usage")
    print("  exit              : Exit the terminal")
    print("\nYou can also type natural language commands like 'create folder test' or 'move file.txt into test'.")
    
    while True:
        try:
            user_input = session.prompt(f"{os.getcwd()} >> ").strip()
            if not user_input:
                continue

            output = execute_command(user_input)
            print(output)

            if user_input.lower() == "exit":
                break

        except KeyboardInterrupt:
            print("\nUse 'exit' to quit")
        except EOFError:
            print("\nExiting terminal...")
            break

if __name__ == "__main__":
    main()
