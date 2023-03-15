import os
import zipfile
import shutil
import time
import tkinter as tk
from tkinter import filedialog
from threading import Thread

def extract_files():
    source_folder = source_entry.get()
    destination_folder = destination_entry.get()
    skip_files = skip_files_var.get()

    while thread.do_run:

        zip_files = [f for f in os.listdir(source_folder) if f.endswith('.zip')]

        for zip_file in zip_files:
            zip_file_path = os.path.join(source_folder, zip_file)
            extract_folder_name = os.path.splitext(zip_file)[0]
            extract_folder_path = os.path.join(destination_folder, extract_folder_name)

            if os.path.exists(extract_folder_path):
                if skip_files:
                    log_var.set(f"Skipped extracting {zip_file}")
                    continue
                else:
                    new_folder_name = extract_folder_name
                    i = 1
                    while os.path.exists(os.path.join(destination_folder, new_folder_name)):
                        new_folder_name = f"{extract_folder_name} ({i})"
                        i += 1
                    extract_folder_path = os.path.join(destination_folder, new_folder_name)

            log_var.set(f"Extracting {zip_file}")
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(extract_folder_path)

            os.remove(zip_file_path)
            log_var.set(f"Moved {zip_file} to {extract_folder_path}")

        time.sleep(1)

def start_extraction():
    global thread
    thread = Thread(target=extract_files)
    thread.do_run = True
    thread.start()

def stop_extraction():
    global thread
    thread.do_run = False
    thread.join()

root = tk.Tk()
root.wm_attributes("-topmost", 1)
root.geometry("500x300")
root.title("Movement")

source_label = tk.Label(root, text="Source Folder: ")
source_label.grid(row=0, column=0)

source_entry = tk.Entry(root)
source_entry.grid(row=0, column=1)

def select_source_folder():
    folder_path = filedialog.askdirectory()
    source_entry.delete(0, tk.END)
    source_entry.insert(0, folder_path)

source_button = tk.Button(root, text="Select", command=select_source_folder)
source_button.grid(row=0, column=2)

destination_label = tk.Label(root, text="Destination Folder: ")
destination_label.grid(row=1, column=0)

destination_entry = tk.Entry(root)
destination_entry.grid(row=1, column=1)

def select_destination_folder():
    folder_path = filedialog.askdirectory()
    destination_entry.delete(0, tk.END)
    destination_entry.insert(0, folder_path)

destination_button = tk.Button(root, text="Select", command=select_destination_folder)
destination_button.grid(row=1, column=2)

skip_files_var = tk.BooleanVar()
skip_files_var.set(True)

skip_files_checkbutton = tk.Checkbutton(root, text="Skip files with same name", variable=skip_files_var)
skip_files_checkbutton.grid(row=2, column=1)

log_var = tk.StringVar()
log_var.set("")
log_label = tk.Label(root, textvariable=log_var)
log_label.grid(row=3, columnspan=3)

start_button = tk.Button(root, text="Start", command=start_extraction)
start_button.grid(row=4, column=0)

stop_button = tk.Button(root, text="Stop", command=stop_extraction)
stop_button.grid(row=4, column=1)

root.mainloop()
