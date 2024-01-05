import ttkbootstrap as ttk
from .ticketforms import rt_form, st_form
from .basketforms import rb_form, sb_form
from .drawingforms import rd_form, sd_form
from .reportforms import rr_form, sr_form
from .settingforms import db_settings_window
from .stress_test import stresstest

def mainmenu():
    window = ttk.Window(title="Main Menu | Ticket Auction Manager", themename="cyborg")

    # Frames
    frm_mainarea = ttk.Frame(window)
    frm_mainarea.pack()

    frm_tickets = ttk.LabelFrame(frm_mainarea, text="Ticket Entry")
    frm_tickets.grid(row=0, column=0, padx=4, pady=4)

    frm_baskets = ttk.LabelFrame(frm_mainarea, text="Basket Entry")
    frm_baskets.grid(row=0, column=1, padx=4, pady=4)

    frm_drawing = ttk.LabelFrame(frm_mainarea, text="Drawing Forms")
    frm_drawing.grid(row=0, column=2, padx=4, pady=4, rowspan=2, sticky="ns")

    frm_reports = ttk.LabelFrame(frm_mainarea, text="Reports")
    frm_reports.grid(row=1, column=0, padx=4, pady=4, columnspan=2, sticky="we")

    frm_settingsarea = ttk.Frame(window)
    frm_settingsarea.pack(expand=True, fill="x")

    frm_settings = ttk.LabelFrame(frm_settingsarea, text="Settings")
    frm_settings.pack(expand=True, fill="both", padx=4, pady=4)

    # Buttons for ticket entry
    btn_regulartickets = ttk.Button(frm_tickets, text="Regular Tickets", bootstyle="secondary", width=20, command=rt_form)
    btn_regulartickets.pack(expand=True, fill="both", padx=4, pady=4)

    btn_specialtytickets = ttk.Button(frm_tickets, text="Specialty Tickets", bootstyle="primary", width=20, command=st_form)
    btn_specialtytickets.pack(expand=True, fill="both", padx=4, pady=4)

    # Buttons for basket entry
    btn_regularbaskets = ttk.Button(frm_baskets, text="Regular Baskets", bootstyle="secondary", width=20, command=rb_form)
    btn_regularbaskets.pack(expand=True, fill="both", padx=4, pady=4)

    btn_specialtybaskets = ttk.Button(frm_baskets, text="Specialty Baskets", bootstyle="primary", width=20, command=sb_form)
    btn_specialtybaskets.pack(expand=True, fill="both", padx=4, pady=4)

    # Buttons for drawing
    btn_regulardrawing = ttk.Button(frm_drawing, text="Regular Drawing", bootstyle="secondary", width=20, command=rd_form)
    btn_regulardrawing.pack(expand=True, fill="both", padx=4, pady=4)

    btn_specialtydrawing = ttk.Button(frm_drawing, text="Specialty Drawing", bootstyle="primary", width=20, command=sd_form)
    btn_specialtydrawing.pack(expand=True, fill="both", padx=4, pady=4)

    # Buttons for reports
    btn_regularreports = ttk.Button(frm_reports, text="Regular Reports", bootstyle="secondary", command=rr_form)
    btn_regularreports.pack(side="left", expand=True, fill="both", padx=4, pady=4)

    btn_specialtyreports = ttk.Button(frm_reports, text="Specialty Reports", bootstyle="primary", command=sr_form)
    btn_specialtyreports.pack(side="left", expand=True, fill="both", padx=4, pady=4)

    # Buttons for settings
    btn_dbsettings = ttk.Button(frm_settings, text="Database Settings", bootstyle=("warning", "outline"), width=17, command=db_settings_window)
    btn_dbsettings.pack(side="left", padx=4, pady=4)

    btn_stress_test = ttk.Button(frm_settings, text="Stress Test", bootstyle=("warning", "outline"), command=stresstest)
    btn_stress_test.pack(side="left", padx=4, pady=4)

    window.mainloop()