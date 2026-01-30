import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
from tkinter import messagebox
from . import core as c
from .utilities import config
from pathlib import Path

def run_app():

    MainWin = tk.Tk()
    MainWin.title("Dev Tool")
    MainWin.geometry("820x720")
    MainWin.minsize(760, 620)

    Ptype = tk.StringVar()
    ProjectDir = tk.StringVar(value=config.load_project_dir(Path.cwd()))
    ProjectName = tk.StringVar(value="Untitled")
    MainFileName = tk.StringVar(value="main")

    style = ttk.Style(MainWin)
    style.theme_use("clam")

    style.configure("Title.TLabel", font=("Arial", 20, "bold"))
    style.configure("Section.TLabel", font=("Arial", 12, "bold"))
    style.configure("Field.TLabel", font=("Arial", 11))
    style.configure("Primary.TButton", font=("Arial", 11, "bold"), padding=(12, 6))
    style.configure("TButton", padding=(10, 5))
    style.configure("TEntry", padding=(6, 4))
    style.configure("TCombobox", padding=(6, 4))
    style.configure("TCheckbutton", font=("Arial", 11), padding=(4, 6))


    MainWin.columnconfigure(0, weight=1)
    MainWin.rowconfigure(4, weight=1) 

    # Title
    ttk.Label(MainWin, text="Create New Project", style="Title.TLabel").grid(
        row=0, column=0, pady=(18, 10)
    )

    cards = ttk.Frame(MainWin)
    cards.grid(row=1, column=0, sticky="ew", padx=18)
    cards.columnconfigure(0, weight=1)
    cards.columnconfigure(1, weight=1)


    card1 = ttk.Frame(cards, padding=16)
    card1.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
    card1.columnconfigure(0, weight=1)
    
    form = ttk.Frame(card1)
    form.grid(row=0, column=0, sticky="ew")
    form.columnconfigure(0, weight=0) 
    form.columnconfigure(1, weight=1)  
    form.columnconfigure(2, weight=0)

    # Project type
    ttk.Label(form, text="Type of Project", style="Field.TLabel").grid(
        row=0, column=0, sticky="w", padx=(0, 10), pady=(0, 10)
    )
    ProjectType = ttk.Combobox(
        form,
        width=40,
        textvariable=Ptype,
        state="readonly",
        values=("Python",),
    )
    ProjectType.grid(row=0, column=1, columnspan=2, sticky="ew", pady=(0, 10))
    ProjectType.current(0)

    # Projects directory
    ttk.Label(form, text="Projects Directory", style="Field.TLabel").grid(
        row=1, column=0, sticky="w", padx=(0, 10), pady=(0, 10)
    )
    dir_entry = ttk.Entry(form, textvariable=ProjectDir)
    dir_entry.grid(row=1, column=1, sticky="ew", pady=(0, 10))

    browse_btn = ttk.Button(form, text="Browse")
    browse_btn.grid(row=1, column=2, sticky="e", padx=(10, 0), pady=(0, 10))

    # Project name
    ttk.Label(form, text="Project Name", style="Field.TLabel").grid(
        row=2, column=0, sticky="w", padx=(0, 10), pady=(0, 10)
    )
    ttk.Entry(form, textvariable=ProjectName).grid(
        row=2, column=1, columnspan=2, sticky="ew", pady=(0, 10)
    )

    # Main file name
    ttk.Label(form, text="Main File Name", style="Field.TLabel").grid(
        row=3, column=0, sticky="w", padx=(0, 10), pady=(0, 6)
    )
    ttk.Entry(form, textvariable=MainFileName).grid(
        row=3, column=1, columnspan=2, sticky="ew", pady=(0, 6)
    )

    card2 = ttk.Frame(cards, padding=16)
    card2.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
    card2.columnconfigure(0, weight=1)

    #Options
    ttk.Label(card2, text="Options", style="Section.TLabel").grid(
        row=0, column=0, sticky="w", pady=(0, 10)
    )
    # git init

    use_git = tk.BooleanVar(value = True)
    gitCheck = ttk.Checkbutton(card2 , variable = use_git ,text = "Git Initialize" , takefocus = 0, style= "TCheckbutton")
    gitCheck.grid(row = 1 , column = 0 , sticky = "w")


    btn_row = ttk.Frame(MainWin)
    btn_row.grid(row=2, column=0, sticky="ew", padx=18, pady=(12, 0))
    btn_row.columnconfigure(0, weight=1)

    create_btn = ttk.Button(btn_row, text="Create Project", style="Primary.TButton")
    create_btn.grid(row=0, column=0, sticky="e")

    # Log separator
    ttk.Separator(MainWin).grid(row=3, column=0, sticky="ew", padx=18, pady=(16, 10))

    # Log frame
    log_frame = ttk.Frame(MainWin, padding=(18, 0, 18, 18))
    log_frame.grid(row=4, column=0, sticky="nsew")
    log_frame.columnconfigure(0, weight=1)
    log_frame.rowconfigure(1, weight=1)

    ttk.Label(log_frame, text="Log", style="Section.TLabel").grid(
        row=0, column=0, sticky="w", pady=(0, 8)
    )

    log_box = tk.Text(log_frame, height=12, wrap="word")
    log_box.grid(row=1, column=0, sticky="nsew")

    scroll = ttk.Scrollbar(log_frame, orient="vertical", command=log_box.yview)
    scroll.grid(row=1, column=1, sticky="ns")
    log_box.configure(yscrollcommand=scroll.set)
    log_box.configure(state="disabled")

    config.config_setup()

    def browse_folder():
        path = filedialog.askdirectory()
        if path:
            ProjectDir.set(path)

    def log(msg: str):
        log_box.configure(state="normal")
        log_box.insert("end", msg + "\n")
        log_box.see("end")
        log_box.configure(state="disabled")

    def on_create():
        create_btn.config(state="disabled")
        cp = None
        try:
            if not ProjectDir.get().strip():
                messagebox.showerror("Error", "Choose Projects Directory")
                return
            if not Path(ProjectDir.get()).exists():
                messagebox.showerror("Error", "This directory does not exist")
                return
            if not ProjectName.get().strip():
                messagebox.showerror("Error", "Enter Project Name")
                return
            if not MainFileName.get().strip():
                MainFileName.set(value="main")

            log("Creating project...")
            log(f"Project Type : {Ptype.get()}")
            cp, mfp = c.create_project(ProjectDir.get(), ProjectName.get(), MainFileName.get() , use_git.get())
            log(f"Project created at: {cp}")
            log(f"Main file: {mfp}")

        finally:
            create_btn.config(state="normal")
            if cp is not None:
                config.update_project_dir(cp.parent)

    browse_btn.config(command=browse_folder)
    create_btn.config(command=on_create)

    MainWin.mainloop()
