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
    ProjectDir = tk.StringVar(value = config.load_project_dir(Path.cwd()))
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

    MainWin.columnconfigure(0, weight=1)
    MainWin.rowconfigure(3, weight=1)

    # Title
    ttk.Label(MainWin, text="Create New Project", style="Title.TLabel").grid(
        row=0, column=0, pady=(18, 10)
    )

    # Card container
    card = ttk.Frame(MainWin, padding=16)
    card.grid(row=1, column=0, sticky="ew", padx=18)
    card.columnconfigure(0, weight=1)

    # Form frame inside card
    form = ttk.Frame(card)
    form.grid(row=0, column=0, sticky="ew")
    form.columnconfigure(0, weight=0)  # labels
    form.columnconfigure(1, weight=1)  # inputs expand
    form.columnconfigure(2, weight=0)  # browse button


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

    # Create button 
    btn_row = ttk.Frame(card)
    btn_row.grid(row=1, column=0, sticky="ew", pady=(10, 0))
    btn_row.columnconfigure(0, weight=1)

    create_btn = ttk.Button(btn_row, text="Create Project", style="Primary.TButton")
    create_btn.grid(row=0, column=0, sticky="e")

    # Log 
    ttk.Separator(MainWin).grid(row=2, column=0, sticky="ew", padx=18, pady=(16, 10))

    log_frame = ttk.Frame(MainWin, padding=(18, 0, 18, 18))
    log_frame.grid(row=3, column=0, sticky="nsew")
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
        log_box.insert("end", msg + "\n")
        log_box.see("end")

    def on_create():
        create_btn.config(state="disabled")
        log_box.configure(state="normal")
        try :
            if not ProjectDir.get().strip() :
                messagebox.showerror("Error", "Choose Projects Directory")
                return
            if not Path(ProjectDir.get()).exists() :
                messagebox.showerror("Error", "This directory does not exist")
                return            
            if not ProjectName.get().strip() :
                messagebox.showerror("Error", "Enter Project Name")
                return
            if not MainFileName.get().strip() :
                MainFileName.set(value="main")

            log("Creating project...")
            log(f"Project Type : {Ptype.get()}")
            cp, mfp = c.create_project(ProjectDir.get() , ProjectName.get() ,MainFileName.get())
            log(f"Project created at: {cp}")
            log(f"Main file: {mfp}")
            git_init = c.git_init(cp)
            log(f"Done : {git_init}")
            git_add = c.git_add(cp)
            log(f"Done : {git_add}")
            git_commit = c.git_commit(cp)
            log(f"Done : {git_commit}")
        finally : 
            create_btn.config(state="normal")
            log_box.configure(state="disabled")
            config.update_project_dir(cp.parent)


    browse_btn.config(command=browse_folder)
    create_btn.config(command=on_create)

    MainWin.mainloop()


