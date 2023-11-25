import ttkbootstrap as ttk 
import db_engine

def db_settings_window():
    window = ttk.Toplevel(title="DB Settings | TAM")
    window.focus()

    frm_createtables = ttk.LabelFrame(window, text="Create Tables")
    frm_createtables.pack(padx=4, pady=4)

    btn_createtables = ttk.Button(frm_createtables, text="Create Tables", width=15, command=db_engine.create_tables)
    btn_createtables.pack(padx=4, pady=4)