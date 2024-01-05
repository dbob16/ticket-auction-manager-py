from .db_engine import session, RegularTicket, RegularBasket, SpecialtyTicket, SpecialtyBasket
from names import get_first_name, get_last_name
from random import randint
from sqlalchemy.sql import func
import ttkbootstrap as ttk 

def stresstest():
    window = ttk.Toplevel(title="TAM Stress Test")
    # Variables
    v_from = ttk.IntVar(window)
    v_to = ttk.IntVar(window)

    # Commands
    def gen_phonenumber():
        str1 = f"{randint(0, 1)}{randint(0, 9)}{randint(0, 9)}-{randint(0, 9)}{randint(0, 9)}{randint(0, 9)}-{randint(0, 9)}{randint(0, 9)}{randint(0, 9)}{randint(0, 9)}"
        return str1

    def cmd_gen_reg_tickets():
        for i in range(v_from.get(), v_to.get()+1):
            try:
                r = RegularTicket(TicketID=i, FirstName=get_first_name(), LastName=get_last_name(), PhoneNumber=gen_phonenumber(), PrefersText=randint(-1, 0))
                session.add(r)
                session.commit()
                print(f"Adding Record {i} {r.FirstName} {r.LastName}")
            except:
                session.rollback()
                print(f"Conflict on {i} detected, rolling back.")

    def cmd_gen_spec_tickets():
        for i in range(v_from.get(), v_to.get()+1):
            try:
                r = SpecialtyTicket(TicketID=i, FirstName=get_first_name(), LastName=get_last_name(), PhoneNumber=gen_phonenumber(), PrefersText=randint(-1, 0))
                session.add(r)
                session.commit()
                print(f"Adding Record {i} {r.FirstName} {r.LastName}")
            except:
                session.rollback()
                print(f"Conflict on {i} detected, rolling back.")

    def cmd_gen_reg_baskets():
        for i in range(v_from.get(), v_to.get()+1):
            tr = session.query(RegularTicket).order_by(func.random()).limit(1).one()
            try:
                r = RegularBasket(BasketID=i, WinningTicket=tr.TicketID)
                session.add(r)
                session.commit()
                print(f"Adding Record {r.BasketID} - {tr.TicketID} {tr.FirstName} {tr.LastName}")
            except:
                session.rollback()
                print(f"Conflict on {i} detected, rolling back")

    def cmd_gen_spec_baskets():
        for i in range(v_from.get(), v_to.get()+1):
            tr = session.query(SpecialtyTicket).order_by(func.random()).limit(1).one()
            try:
                r = SpecialtyBasket(BasketID=i, WinningTicket=tr.TicketID)
                session.add(r)
                session.commit()
                print(f"Adding Record {r.BasketID} - {tr.TicketID} {tr.FirstName} {tr.LastName}")
            except:
                session.rollback()
                print(f"Conflict on {i} detected, rolling back")

    # Frames
    frm_ranger = ttk.LabelFrame(window, text="Range")
    frm_ranger.pack(padx=4, pady=4, fill="x")

    frm_regular = ttk.LabelFrame(window, text="Regular Items")
    frm_regular.pack(padx=4, pady=4, fill="x")

    frm_specialty = ttk.LabelFrame(window, text="Specialty Items")
    frm_specialty.pack(padx=4, pady=4, fill="x")

    # Ranger Frame
    txt_from = ttk.Entry(frm_ranger, textvariable=v_from, width=5)
    txt_from.pack(side="left", padx=4, pady=4)

    txt_to = ttk.Entry(frm_ranger, textvariable=v_to, width=5)
    txt_to.pack(side="left", padx=4, pady=4)

    # Regular Frame
    btn_reg_tickets = ttk.Button(frm_regular, text="Tickets", bootstyle="secondary", command=cmd_gen_reg_tickets)
    btn_reg_tickets.pack(side="left", padx=4, pady=4)

    btn_reg_baskets = ttk.Button(frm_regular, text="Baskets", bootstyle="secondary", command=cmd_gen_reg_baskets)
    btn_reg_baskets.pack(side="left", padx=4, pady=4)

    # Specialty
    btn_spec_tickets = ttk.Button(frm_specialty, text="Tickets", bootstyle="primary", command=cmd_gen_spec_tickets)
    btn_spec_tickets.pack(side="left", padx=4, pady=4)

    btn_spec_baskets = ttk.Button(frm_specialty, text="Baskets", bootstyle="primary", command=cmd_gen_spec_baskets)
    btn_spec_baskets.pack(side="left", padx=4, pady=4)