import re
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
import os

def parse_mml_file(input_txt, output_dir):
    with open(input_txt, "r", encoding="utf-8") as file:
        data = file.read()

    pattern = re.compile(
        r"MML Command-----([^\n]+);.*?"
        r"NE\s+:\s+([^\n]+)\n"
        r"Report\s+:\s+\+{3}\s+([^\n]+)\s+([0-9\-]+\s+[0-9:]+)\n"
        r"O&M\s+#(\d+)\n"
        r".*?%%/(?:\*[^*]*\*/)?([^\n]+);%%\n"
        r"RETCODE\s+=\s+(\d+)\s+(.*?)\n",
        re.DOTALL
    )

    matches = pattern.findall(data)

    df = pd.DataFrame(matches, columns=[
        "MML_Command", "NE", "Report_NE", "Timestamp", "OM_ID",
        "Full_Command", "Retcode", "Ret_Message"
    ])

    def extract_params(command):
        deviceno = re.search(r'DEVICENO=(\d+)', command)
        subunitno = re.search(r'SUBUNITNO=(\d+)', command)
        tilt = re.search(r'TILT=(\d+)', command)
        return pd.Series([
            deviceno.group(1) if deviceno else None,
            subunitno.group(1) if subunitno else None,
            tilt.group(1) if tilt else None
        ])

    df[['DEVICENO', 'SUBUNITNO', 'TILT']] = df['MML_Command'].apply(extract_params)

    base_name = os.path.splitext(os.path.basename(input_txt))[0]
    output_path = os.path.join(output_dir, f"{base_name}.csv")
    df.to_csv(output_path, index=False)
    return output_path

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        entry_file.delete(0, tk.END)
        entry_file.insert(0, file_path)

def browse_output_dir():
    dir_path = filedialog.askdirectory()
    if dir_path:
        entry_output.delete(0, tk.END)
        entry_output.insert(0, dir_path)

def run_parser():
    input_file = entry_file.get()
    output_dir = entry_output.get()

    if not os.path.isfile(input_file):
        messagebox.showerror("Error", "Please select a valid input .txt file")
        return
    if not os.path.isdir(output_dir):
        messagebox.showerror("Error", "Please select a valid output directory")
        return

    try:
        output_file = parse_mml_file(input_file, output_dir)
        messagebox.showinfo("Success", f"File saved to: {output_file}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI Setup
root = tk.Tk()
root.title("MML Result Parser")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

tk.Label(frame, text="Select MML Result File (.txt):").grid(row=0, column=0, sticky="w")
entry_file = tk.Entry(frame, width=50)
entry_file.grid(row=0, column=1)
tk.Button(frame, text="Browse", command=browse_file).grid(row=0, column=2)

tk.Label(frame, text="Select Output Directory:").grid(row=1, column=0, sticky="w")
entry_output = tk.Entry(frame, width=50)
entry_output.grid(row=1, column=1)
tk.Button(frame, text="Browse", command=browse_output_dir).grid(row=1, column=2)

tk.Button(frame, text="Run", command=run_parser, bg="green", fg="white").grid(row=2, column=1, pady=10)

root.mainloop()
