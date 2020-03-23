import glob
import os
import subprocess
import tkinter as tk
from tkinter import filedialog, LEFT
from PyPDF2 import PdfFileMerger
import webbrowser
from zipfile import ZipFile

root = tk.Tk()
root.title("Patient Data Walkthrough")

WIDTH = 300
canvas1 = tk.Canvas(root, width=WIDTH, height=300)
title = tk.Label(root, text="Hello, and welcome to the Patient Data Walkthrough!", fg="black", wraplength=WIDTH, font=("Helvetica", 16), padx=20, pady=20)
title.grid(row=0)

status_label = tk.StringVar()
status_label.set('')
def open(file: str):
    webbrowser.open_new(file)


def extract_in_file(folder: str, result_file: str):
    pdf_files = [f for f in glob.iglob(folder + '*/**/*.pdf', recursive=True)]
    if len(pdf_files) == 0:
        status_label.set("No PDF files found in that ZIP file.")
        return
    merger = PdfFileMerger()
    invalid_files = []
    status_label.set(f"Merging {len(pdf_files)} PDFs...")
    for pdf in sorted(pdf_files):
        try:
            merger.append(pdf)
        except:
            invalid_files.append(pdf)
    merger.write(result_file)
    merger.close()
    prefix = f"{len(invalid_files)} invalid PDF(s): {','.join(invalid_files)} .\n" if len(invalid_files) > 0 else ''
    status_label.set(prefix + "Merged " + str(len(pdf_files) - len(invalid_files)) + " PDFs into\n" + result_file)
    open(result_file)

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

merge_button_label = tk.Label(root, text="Step 2: Select the ZIP file of the PDFs:", fg="black", wraplength=250, justify=LEFT)
merge_button_label.grid(column=0, row=2)
merge_button = tk.Button(text='Choose ZIP', command=merge, bg='brown', fg='white')
merge_button.grid(column=1, row=2)

step_4_label = tk.Label(root, text="Step 3: Download the CSV File", fg="black", wraplength=250, justify=LEFT)
step_4_label.grid(column=0, row=5)
step_5_label = tk.Label(root, text="Step 4: Install the Brady Printer software", fg="black", wraplength=250, justify=LEFT)
step_5_label.grid(column=0, row=6)
if __name__ == '__main__':
    root.mainloop()
