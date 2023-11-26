import ttkbootstrap as ttk 
from .db_engine import engine, session, create_tables

def db_settings_window():
    window = ttk.Toplevel(title="DB Settings | TAM")
    window.focus()

    frm_createtables = ttk.LabelFrame(window, text="Create Tables")
    frm_createtables.pack(padx=4, pady=4)

    btn_createtables = ttk.Button(frm_createtables, text="Create Tables", width=15, command=create_tables)
    btn_createtables.pack(padx=4, pady=4)