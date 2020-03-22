import glob
import os
import subprocess
import tkinter as tk
from tkinter import filedialog, LEFT
from PyPDF2 import PdfFileMerger
import webbrowser
from zipfile import ZipFile

root = tk.Tk()
root.title("Verily Patient Data Printer")

WIDTH = 300
canvas1 = tk.Canvas(root, width=WIDTH, height=300)
title = tk.Label(root, text="Hello, and welcome to the Verily Patient Data Printer!", fg="black", wraplength=WIDTH, font=("Helvetica", 16), padx=20, pady=20)
title.grid(row=0)

status_label = tk.StringVar()
status_label.set('')
def open(file: str):
    webbrowser.open_new(file)


def extract_in_file(folder: str, result_file: str):
    pdf_files = [f for f in glob.iglob(folder + '**/*.pdf', recursive=True)]
    if len(pdf_files) == 0:
        status_label.set("No PDF files found in that ZIP file.")
        return
    merger = PdfFileMerger()
    for pdf in pdf_files:
        merger.append(pdf)
    merger.write(result_file)
    merger.close()
    status_label.set("Merged " + str(len(pdf_files)) + " PDFs into\n" + result_file)

    step_3_label = tk.Label(root, text="Step 3: Open and print the merged PDF: ", fg="black", wraplength=250, justify=LEFT)
    step_3_label.grid(column=0, row=4)
    open_button = tk.Button(text='Open PDF', command=lambda: open(result_file), bg='brown', fg='white')
    open_button.grid(column=1, row=4)

def merge():
    file_selected = filedialog.askopenfilename(filetypes=[("ZIP Files", ".zip")])
    if not file_selected:
        return
    folder_selected = os.path.dirname(file_selected)
    with ZipFile(file_selected, 'r') as zipObj:
        # Extract all the contents of zip file in different directory
        zipObj.extractall(folder_selected + '/pdfs')

    result_file = folder_selected + "/merged.pdf"
    if os.path.exists(result_file):
        os.remove(result_file)

    extract_in_file(folder_selected + "/pdfs", result_file)

status = tk.Label(root, textvariable=status_label, fg="green", wraplength=250)
status.grid(column=0, row=3)

step_1_label = tk.Label(root, text="Step 1: Download the ZIP file", fg="black", wraplength=250, justify=LEFT)
step_1_label.grid(column=0, row=1)

merge_button_label = tk.Label(root, text="Step 2: Select the ZIP file:", fg="black", wraplength=250, justify=LEFT)
merge_button_label.grid(column=0, row=2)
merge_button = tk.Button(text='Choose ZIP', command=merge, bg='brown', fg='white')
merge_button.grid(column=1, row=2)

step_4_label = tk.Label(root, text="Step 4: Download the CSV File", fg="black", wraplength=250, justify=LEFT)
step_4_label.grid(column=0, row=6)
step_5_label = tk.Label(root, text="Step 5: Install the Brady Printer software", fg="black", wraplength=250, justify=LEFT)
step_5_label.grid(column=0, row=7)
if __name__ == '__main__':
    root.mainloop()
