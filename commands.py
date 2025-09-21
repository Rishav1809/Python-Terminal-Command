import os
import shutil
import psutil

def list_files():
    for f in os.listdir():
        print(f)

def change_dir(path):
    try:
        os.chdir(path)
    except FileNotFoundError:
        print("Directory not found.")

def make_dir(dirname):
    try:
        os.mkdir(dirname)
    except Exception as e:
        print("Error:", e)

def remove(path):
    try:
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
    except Exception as e:
        print("Error:", e)

def show_cpu():
    print("CPU Usage:", psutil.cpu_percent(), "%")

def show_mem():
    mem = psutil.virtual_memory()
    print(f"Memory Usage: {mem.percent}% ({mem.used / 1024**2:.2f} MB used)")
