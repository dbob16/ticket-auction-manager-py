from .db_engine import session, RegularTicket, RegularBasket, SpecialtyTicket, SpecialtyBasket
from jinja2 import Environment, FileSystemLoader
import ttkbootstrap as ttk 

def rr_form():
    window = ttk.Toplevel(title="Regular Report Generator")

    # Variables
    v_eventname = ttk.StringVar(window)

    # Commands
    def cmd_bn_all():
        env = Environment(loader=FileSystemLoader("templates"))
        template = env.get_template("main_template.html")
        cur_title = "Regular Basket Winners - All"
        cur_headings = ("Winner", "Basket #", "Ticket #", "Description", "Preference")
        results = session.query(RegularBasket, RegularTicket).join(RegularTicket).filter(RegularBasket.WinningTicket > 0).all()
        results_list = []
        for b, t in results:
            cur_record = []
            cur_record.append(f"{t.LastName}, {t.FirstName}: {t.PhoneNumber}")
            cur_record.append(b.BasketID)
            cur_record.append(b.WinningTicket)
            cur_record.append(b.Description)
            cur_record.append(t.pref())
            cur_record = tuple(cur_record)
            results_list.append(cur_record)
        results_list.sort()
        report = template.render(title=cur_title, headings=cur_headings, data=results_list)
        with open("reports/regular-all-winners-name.html", "w") as f:
            f.write(report)

    def cmd_bn_text():
        env = Environment(loader=FileSystemLoader("templates"))
        template = env.get_template("main_template.html")
        cur_title = "Regular Basket Winners - Text Preference"
        cur_headings = ("Winner", "Basket #", "Ticket #", "Description")
        results = session.query(RegularBasket, RegularTicket).join(RegularTicket).filter(RegularBasket.WinningTicket > 0, RegularTicket.PrefersText == -1).all()
        results_list = []
        for b, t in results:
            cur_record = []
            cur_record.append(f"{t.LastName}, {t.FirstName}: {t.PhoneNumber}")
            cur_record.append(b.BasketID)
            cur_record.append(b.WinningTicket)
            cur_record.append(b.Description)
            cur_record = tuple(cur_record)
            results_list.append(cur_record)
        results_list.sort()
        report = template.render(title=cur_title, headings=cur_headings, data=results_list)
        with open("reports/regular-text-winners-name.html", "w") as f:
            f.write(report)

    def cmd_bn_call():
        env = Environment(loader=FileSystemLoader("templates"))
        template = env.get_template("main_template.html")
        cur_title = "Regular Basket Winners - Call Preference"
        cur_headings = ("Winner", "Basket #", "Ticket #", "Description")
        results = session.query(RegularBasket, RegularTicket).join(RegularTicket).filter(RegularBasket.WinningTicket > 0, RegularTicket.PrefersText == 0).all()
        results_list = []
        for b, t in results:
            cur_record = []
            cur_record.append(f"{t.LastName}, {t.FirstName}: {t.PhoneNumber}")
            cur_record.append(b.BasketID)
            cur_record.append(b.WinningTicket)
            cur_record.append(b.Description)
            cur_record = tuple(cur_record)
            results_list.append(cur_record)
        results_list.sort()
        report = template.render(title=cur_title, headings=cur_headings, data=results_list)
        with open("reports/regular-call-winners-name.html", "w") as f:
            f.write(report)

    def cmd_bnum_all():
        env = Environment(loader=FileSystemLoader("templates"))
        template = env.get_template("main_template.html")
        cur_title = "Basket # Regular Winners - All"
        cur_headings = ("Basket #", "Ticket #", "Winner", "Description", "Preference")
        results = session.query(RegularBasket, RegularTicket).join(RegularTicket).filter(RegularBasket.WinningTicket > 0).all()
        results_list = []
        for b, t in results:
            cur_record = []
            cur_record.append(b.BasketID)
            cur_record.append(b.WinningTicket)
            cur_record.append(f"{t.LastName}, {t.FirstName}: {t.PhoneNumber}")
            cur_record.append(b.Description)
            cur_record.append(t.pref())
            cur_record = tuple(cur_record)
            results_list.append(cur_record)
        results_list.sort()
        report = template.render(title=cur_title, headings=cur_headings, data=results_list)
        with open("reports/regular-all-winners-basketnum.html", "w") as f:
            f.write(report)
    
    def cmd_bnum_text():
        env = Environment(loader=FileSystemLoader("templates"))
        template = env.get_template("main_template.html")
        cur_title = "Basket # Regular Winners - Text Preference"
        cur_headings = ("Basket #", "Ticket #", "Winner", "Description")
        results = session.query(RegularBasket, RegularTicket).join(RegularTicket).filter(RegularBasket.WinningTicket > 0, RegularTicket.PrefersText == -1).all()
        results_list = []
        for b, t in results:
            cur_record = []
            cur_record.append(b.BasketID)
            cur_record.append(b.WinningTicket)
            cur_record.append(f"{t.LastName}, {t.FirstName}: {t.PhoneNumber}")
            cur_record.append(b.Description)
            cur_record = tuple(cur_record)
            results_list.append(cur_record)
        results_list.sort()
        report = template.render(title=cur_title, headings=cur_headings, data=results_list)
        with open("reports/regular-text-winners-basketnum.html", "w") as f:
            f.write(report)

    def cmd_bnum_call():
        env = Environment(loader=FileSystemLoader("templates"))
        template = env.get_template("main_template.html")
        cur_title = "Basket # Regular Winners - Call Preference"
        cur_headings = ("Basket #", "Ticket #", "Winner", "Description")
        results = session.query(RegularBasket, RegularTicket).join(RegularTicket).filter(RegularBasket.WinningTicket > 0, RegularTicket.PrefersText == 0).all()
        results_list = []
        for b, t in results:
            cur_record = []
            cur_record.append(b.BasketID)
            cur_record.append(b.WinningTicket)
            cur_record.append(f"{t.LastName}, {t.FirstName}: {t.PhoneNumber}")
            cur_record.append(b.Description)
            cur_record = tuple(cur_record)
            results_list.append(cur_record)
        results_list.sort()
        report = template.render(title=cur_title, headings=cur_headings, data=results_list)
        with open("reports/regular-call-winners-basketnum.html", "w") as f:
            f.write(report)

    # Frames
    frm_byname = ttk.LabelFrame(window, text="By Winner Name")
    frm_byname.grid(row=0, column=0, padx=4, pady=4, sticky="nsew")

    frm_bynum = ttk.LabelFrame(window, text="By Basket Number")
    frm_bynum.grid(row=1, column=0, padx=4, pady=4, sticky="nsew")

    # By Name Frame
    btn_bn_all = ttk.Button(frm_byname, text="All Winners", bootstyle="secondary", command=cmd_bn_all)
    btn_bn_all.pack(side="left", padx=4, pady=4)

    btn_bn_preftext = ttk.Button(frm_byname, text="Prefers Texts", bootstyle="secondary", command=cmd_bn_text)
    btn_bn_preftext.pack(side="left", padx=4, pady=4)

    btn_bn_prefcall = ttk.Button(frm_byname, text="Prefers Calls", bootstyle="secondary", command=cmd_bn_call)
    btn_bn_prefcall.pack(side="left", padx=4, pady=4)

    # By Basket Number Frame
    btn_bnum_all = ttk.Button(frm_bynum, text="All Winners", bootstyle="secondary", command=cmd_bnum_all)
    btn_bnum_all.pack(side="left", padx=4, pady=4)

    btn_bnum_preftext = ttk.Button(frm_bynum, text="Prefers Texts", bootstyle="secondary", command=cmd_bnum_text)
    btn_bnum_preftext.pack(side="left", padx=4, pady=4)

    btn_bnum_prefcall = ttk.Button(frm_bynum, text="Prefers Calls", bootstyle="secondary", command=cmd_bnum_call)
    btn_bnum_prefcall.pack(side="left", padx=4, pady=4)

def sr_form():
    window = ttk.Toplevel(title="Specialty Report Generator")

    # Variables
    v_eventname = ttk.StringVar(window)

    # Commands
    def cmd_bn_all():
        env = Environment(loader=FileSystemLoader("templates"))
        template = env.get_template("main_template.html")
        cur_title = "Specialty Basket Winners - All"
        cur_headings = ("Winner", "Basket #", "Ticket #", "Description", "Preference")
        results = session.query(SpecialtyBasket, SpecialtyTicket).join(SpecialtyTicket).filter(SpecialtyBasket.WinningTicket > 0).all()
        results_list = []
        for b, t in results:
            cur_record = []
            cur_record.append(f"{t.LastName}, {t.FirstName}: {t.PhoneNumber}")
            cur_record.append(b.BasketID)
            cur_record.append(b.WinningTicket)
            cur_record.append(b.Description)
            cur_record.append(t.pref())
            cur_record = tuple(cur_record)
            results_list.append(cur_record)
        results_list.sort()
        report = template.render(title=cur_title, headings=cur_headings, data=results_list)
        with open("reports/specialty-all-winners-name.html", "w") as f:
            f.write(report)

    def cmd_bn_text():
        env = Environment(loader=FileSystemLoader("templates"))
        template = env.get_template("main_template.html")
        cur_title = "Specialty Basket Winners - Text Preference"
        cur_headings = ("Winner", "Basket #", "Ticket #", "Description")
        results = session.query(SpecialtyBasket, SpecialtyTicket).join(SpecialtyTicket).filter(SpecialtyBasket.WinningTicket > 0, SpecialtyTicket.PrefersText == -1).all()
        results_list = []
        for b, t in results:
            cur_record = []
            cur_record.append(f"{t.LastName}, {t.FirstName}: {t.PhoneNumber}")
            cur_record.append(b.BasketID)
            cur_record.append(b.WinningTicket)
            cur_record.append(b.Description)
            cur_record = tuple(cur_record)
            results_list.append(cur_record)
        results_list.sort()
        report = template.render(title=cur_title, headings=cur_headings, data=results_list)
        with open("reports/specialty-text-winners-name.html", "w") as f:
            f.write(report)

    def cmd_bn_call():
        env = Environment(loader=FileSystemLoader("templates"))
        template = env.get_template("main_template.html")
        cur_title = "Specialty Basket Winners - Call Preference"
        cur_headings = ("Winner", "Basket #", "Ticket #", "Description")
        results = session.query(SpecialtyBasket, SpecialtyTicket).join(SpecialtyTicket).filter(SpecialtyBasket.WinningTicket > 0, SpecialtyTicket.PrefersText == 0).all()
        results_list = []
        for b, t in results:
            cur_record = []
            cur_record.append(f"{t.LastName}, {t.FirstName}: {t.PhoneNumber}")
            cur_record.append(b.BasketID)
            cur_record.append(b.WinningTicket)
            cur_record.append(b.Description)
            cur_record = tuple(cur_record)
            results_list.append(cur_record)
        results_list.sort()
        report = template.render(title=cur_title, headings=cur_headings, data=results_list)
        with open("reports/specialty-call-winners-name.html", "w") as f:
            f.write(report)

    def cmd_bnum_all():
        env = Environment(loader=FileSystemLoader("templates"))
        template = env.get_template("main_template.html")
        cur_title = "Basket # Specialty Winners - All"
        cur_headings = ("Basket #", "Ticket #", "Winner", "Description", "Preference")
        results = session.query(SpecialtyBasket, SpecialtyTicket).join(SpecialtyTicket).filter(SpecialtyBasket.WinningTicket > 0).all()
        results_list = []
        for b, t in results:
            cur_record = []
            cur_record.append(b.BasketID)
            cur_record.append(b.WinningTicket)
            cur_record.append(f"{t.LastName}, {t.FirstName}: {t.PhoneNumber}")
            cur_record.append(b.Description)
            cur_record.append(t.pref())
            cur_record = tuple(cur_record)
            results_list.append(cur_record)
        results_list.sort()
        report = template.render(title=cur_title, headings=cur_headings, data=results_list)
        with open("reports/specialty-all-winners-basketnum.html", "w") as f:
            f.write(report)
    
    def cmd_bnum_text():
        env = Environment(loader=FileSystemLoader("templates"))
        template = env.get_template("main_template.html")
        cur_title = "Basket # Specialty Winners - Text Preference"
        cur_headings = ("Basket #", "Ticket #", "Winner", "Description")
        results = session.query(SpecialtyBasket, SpecialtyTicket).join(SpecialtyTicket).filter(SpecialtyBasket.WinningTicket > 0, SpecialtyTicket.PrefersText == -1).all()
        results_list = []
        for b, t in results:
            cur_record = []
            cur_record.append(b.BasketID)
            cur_record.append(b.WinningTicket)
            cur_record.append(f"{t.LastName}, {t.FirstName}: {t.PhoneNumber}")
            cur_record.append(b.Description)
            cur_record = tuple(cur_record)
            results_list.append(cur_record)
        results_list.sort()
        report = template.render(title=cur_title, headings=cur_headings, data=results_list)
        with open("reports/specialty-text-winners-basketnum.html", "w") as f:
            f.write(report)

    def cmd_bnum_call():
        env = Environment(loader=FileSystemLoader("templates"))
        template = env.get_template("main_template.html")
        cur_title = "Basket # Specialty Winners - Call Preference"
        cur_headings = ("Basket #", "Ticket #", "Winner", "Description")
        results = session.query(SpecialtyBasket, SpecialtyTicket).join(SpecialtyTicket).filter(SpecialtyBasket.WinningTicket > 0, SpecialtyTicket.PrefersText == 0).all()
        results_list = []
        for b, t in results:
            cur_record = []
            cur_record.append(b.BasketID)
            cur_record.append(b.WinningTicket)
            cur_record.append(f"{t.LastName}, {t.FirstName}: {t.PhoneNumber}")
            cur_record.append(b.Description)
            cur_record = tuple(cur_record)
            results_list.append(cur_record)
        results_list.sort()
        report = template.render(title=cur_title, headings=cur_headings, data=results_list)
        with open("reports/specialty-call-winners-basketnum.html", "w") as f:
            f.write(report)

    # Frames
    frm_byname = ttk.LabelFrame(window, text="By Winner Name")
    frm_byname.grid(row=0, column=0, padx=4, pady=4, sticky="nsew")

    frm_bynum = ttk.LabelFrame(window, text="By Basket Number")
    frm_bynum.grid(row=1, column=0, padx=4, pady=4, sticky="nsew")

    # By Name Frame
    btn_bn_all = ttk.Button(frm_byname, text="All Winners", bootstyle="primary", command=cmd_bn_all)
    btn_bn_all.pack(side="left", padx=4, pady=4)

    btn_bn_preftext = ttk.Button(frm_byname, text="Prefers Texts", bootstyle="primary", command=cmd_bn_text)
    btn_bn_preftext.pack(side="left", padx=4, pady=4)

    btn_bn_prefcall = ttk.Button(frm_byname, text="Prefers Calls", bootstyle="primary", command=cmd_bn_call)
    btn_bn_prefcall.pack(side="left", padx=4, pady=4)

    # By Basket Number Frame
    btn_bnum_all = ttk.Button(frm_bynum, text="All Winners", bootstyle="primary", command=cmd_bnum_all)
    btn_bnum_all.pack(side="left", padx=4, pady=4)

    btn_bnum_preftext = ttk.Button(frm_bynum, text="Prefers Texts", bootstyle="primary", command=cmd_bnum_text)
    btn_bnum_preftext.pack(side="left", padx=4, pady=4)

    btn_bnum_prefcall = ttk.Button(frm_bynum, text="Prefers Calls", bootstyle="primary", command=cmd_bnum_call)
    btn_bnum_prefcall.pack(side="left", padx=4, pady=4)