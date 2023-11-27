import ttkbootstrap as ttk 
from .db_engine import session, RegularTicket, RegularBasket, SpecialtyTicket, SpecialtyBasket

def rd_form():
    window = ttk.Toplevel(title="Regular Drawing Form")
    window.focus()

    # Variables
    v_from = ttk.IntVar(window)
    v_to = ttk.IntVar(window)

    v_id = ttk.IntVar(window)
    v_winningticket = ttk.IntVar(window)

    # Commands
    def cmd_tv_refresh():
        for c in tv.get_children():
            tv.delete(c)
        for i in range(v_from.get(), v_to.get()+1):
            try:
                rb = session.query(RegularBasket).filter(RegularBasket.BasketID == i).one()
                rt = session.query(RegularTicket).filter(RegularTicket.TicketID == rb.WinningTicket).one()
                tv.insert('', index="end", iid=i, values=(i, rb.WinningTicket, f"{rt.LastName}, {rt.FirstName}: {rt.PhoneNumber} {rt.pref()}"))
            except:
                tv.insert('', index="end", iid=i, values=(i, 0, 'No Basket Entry Yet'))

    def cmd_pagerupdate():
        cmd_tv_refresh()
        txt_id.config(from_=v_from.get(), to=v_to.get())
        if v_id.get() < v_from.get():
            v_id.set(v_from.get())
        if v_id.get() > v_to.get():
            v_id.set(v_to.get())
        cmd_id_update()

    def cmd_id_update():
        tv.selection_set(v_id.get())
        txt_winningticket.focus()

    def cmd_movedown():
        if v_id.get() < v_to.get():
            cmd_save()
            v_id.set(v_id.get()+1)
            cmd_id_update()
    
    def cmd_moveup():
        if v_id.get() > v_from.get():
            cmd_save()
            v_id.set(v_id.get()-1)
            cmd_id_update()

    def cmd_save():
        try:
            r = session.query(RegularBasket).filter(RegularBasket.BasketID == v_id.get()).one()
            r.WinningTicket = v_winningticket.get()
            session.commit()
        except:
            r = RegularBasket(BasketID=v_id.get(), Description='', Donors='', WinningTicket=v_winningticket.get())
            session.add(r)
            session.commit()
        cmd_tv_refresh()
        cmd_id_update()

    # Frames
    frm_pager = ttk.LabelFrame(window, text="Range Control")
    frm_pager.pack(padx=4, pady=4, expand=False, fill="x")

    frm_entry = ttk.LabelFrame(window, text="Record Editor")
    frm_entry.pack(padx=4, pady=4, expand=False, fill="x")

    frm_commands = ttk.LabelFrame(window, text="Commands")
    frm_commands.pack(padx=4, pady=4, expand=False, fill="x")

    frm_tv = ttk.LabelFrame(window, text="View Page")
    frm_tv.pack(padx=4, pady=4, expand=True, fill="both")

    # Pager Widgets
    txt_from = ttk.Entry(frm_pager, textvariable=v_from, width=15)
    txt_from.pack(side="left", padx=4, pady=4)

    ttk.Label(frm_pager, text=" - ").pack(side="left", padx=4, pady=4)

    txt_to = ttk.Entry(frm_pager, textvariable=v_to, width=15)
    txt_to.pack(side="left", padx=4, pady=4)

    btn_pgr_update = ttk.Button(frm_pager, text="Update", bootstyle="secondary", command=cmd_pagerupdate)
    btn_pgr_update.pack(side="left", padx=4, pady=4)

    # Entry Widgets
    ttk.Label(frm_entry, text="ID").grid(row=0, column=0, padx=4, pady=4)
    txt_id = ttk.Spinbox(frm_entry, textvariable=v_id, width=15, command=cmd_id_update)
    txt_id.grid(row=1, column=0, padx=4, pady=4)

    ttk.Label(frm_entry, text="Winning Ticket").grid(row=0, column=1, padx=4, pady=4)
    txt_winningticket = ttk.Entry(frm_entry, textvariable=v_winningticket, width=17)
    txt_winningticket.grid(row=1, column=1, padx=4, pady=4)

    btn_entry_save = ttk.Button(frm_entry, text="Save - Alt K", bootstyle="secondary", command=cmd_save)
    btn_entry_save.grid(row=0, column=2, padx=4, pady=4, rowspan=2, sticky="ns")

    # Command Widgets
    btn_down = ttk.Button(frm_commands, text="Down - Alt L", bootstyle="secondary", command=cmd_movedown)
    btn_down.pack(side="left", padx=4, pady=4)

    btn_up = ttk.Button(frm_commands, text="Up - Alt O", bootstyle="secondary", command=cmd_moveup)
    btn_up.pack(side="left", padx=4, pady=4)

    # TV Widgets
    tv_sb = ttk.Scrollbar(frm_tv, orient="vertical")
    tv_sb.pack(side="right", fill="y")

    tv = ttk.Treeview(frm_tv, columns=("id", "winningticket", "winner"), show="headings", yscrollcommand=tv_sb.set, height=22)
    tv.column("id", width=150), tv.heading("id", text="ID")
    tv.column("winningticket", width=170), tv.heading("winningticket", text="Winning Ticket")
    tv.column("winner", width=700), tv.heading("winner", text="Winner")
    tv.pack(padx=2, pady=2, expand=True, fill="both")

    tv_sb.config(command=tv.yview)

    # Bind Commands
    def bnd_tv_select(_):
        for s in tv.selection():
            r = tv.item(s)['values']
            v_id.set(r[0]), v_winningticket.set(r[1])

    def bnd_save(_):
        cmd_save()

    def bnd_movedown(_):
        cmd_movedown()

    def bnd_moveup(_):
        cmd_moveup()
    
    # Bindings
    tv.bind('<<TreeviewSelect>>', bnd_tv_select)
    window.bind('<Alt-k>', bnd_save)
    window.bind('<Alt-l>', bnd_movedown)
    window.bind('<Alt-o>', bnd_moveup)

def sd_form():
    window = ttk.Toplevel(title="Specialty Drawing Form")
    window.focus()

    # Variables
    v_from = ttk.IntVar(window)
    v_to = ttk.IntVar(window)

    v_id = ttk.IntVar(window)
    v_winningticket = ttk.IntVar(window)

    # Commands
    def cmd_tv_refresh():
        for c in tv.get_children():
            tv.delete(c)
        for i in range(v_from.get(), v_to.get()+1):
            try:
                rb = session.query(SpecialtyBasket).filter(SpecialtyBasket.BasketID == i).one()
                rt = session.query(SpecialtyTicket).filter(SpecialtyTicket.TicketID == rb.WinningTicket).one()
                tv.insert('', index="end", iid=i, values=(i, rb.WinningTicket, f"{rt.LastName}, {rt.FirstName}: {rt.PhoneNumber} {rt.pref()}"))
            except:
                tv.insert('', index="end", iid=i, values=(i, 0, 'No Basket Entry Yet'))

    def cmd_pagerupdate():
        cmd_tv_refresh()
        txt_id.config(from_=v_from.get(), to=v_to.get())
        if v_id.get() < v_from.get():
            v_id.set(v_from.get())
        if v_id.get() > v_to.get():
            v_id.set(v_to.get())
        cmd_id_update()

    def cmd_id_update():
        tv.selection_set(v_id.get())
        txt_winningticket.focus()

    def cmd_movedown():
        if v_id.get() < v_to.get():
            cmd_save()
            v_id.set(v_id.get()+1)
            cmd_id_update()
    
    def cmd_moveup():
        if v_id.get() > v_from.get():
            cmd_save()
            v_id.set(v_id.get()-1)
            cmd_id_update()

    def cmd_save():
        try:
            r = session.query(SpecialtyBasket).filter(SpecialtyBasket.BasketID == v_id.get()).one()
            r.WinningTicket = v_winningticket.get()
            session.commit()
        except:
            r = SpecialtyBasket(BasketID=v_id.get(), Description='', Donors='', WinningTicket=v_winningticket.get())
            session.add(r)
            session.commit()
        cmd_tv_refresh()
        cmd_id_update()

    # Frames
    frm_pager = ttk.LabelFrame(window, text="Range Control")
    frm_pager.pack(padx=4, pady=4, expand=False, fill="x")

    frm_entry = ttk.LabelFrame(window, text="Record Editor")
    frm_entry.pack(padx=4, pady=4, expand=False, fill="x")

    frm_commands = ttk.LabelFrame(window, text="Commands")
    frm_commands.pack(padx=4, pady=4, expand=False, fill="x")

    frm_tv = ttk.LabelFrame(window, text="View Page")
    frm_tv.pack(padx=4, pady=4, expand=True, fill="both")

    # Pager Widgets
    txt_from = ttk.Entry(frm_pager, textvariable=v_from, width=15)
    txt_from.pack(side="left", padx=4, pady=4)

    ttk.Label(frm_pager, text=" - ").pack(side="left", padx=4, pady=4)

    txt_to = ttk.Entry(frm_pager, textvariable=v_to, width=15)
    txt_to.pack(side="left", padx=4, pady=4)

    btn_pgr_update = ttk.Button(frm_pager, text="Update", bootstyle="primary", command=cmd_pagerupdate)
    btn_pgr_update.pack(side="left", padx=4, pady=4)

    # Entry Widgets
    ttk.Label(frm_entry, text="ID").grid(row=0, column=0, padx=4, pady=4)
    txt_id = ttk.Spinbox(frm_entry, textvariable=v_id, width=15, command=cmd_id_update)
    txt_id.grid(row=1, column=0, padx=4, pady=4)

    ttk.Label(frm_entry, text="Winning Ticket").grid(row=0, column=1, padx=4, pady=4)
    txt_winningticket = ttk.Entry(frm_entry, textvariable=v_winningticket, width=17)
    txt_winningticket.grid(row=1, column=1, padx=4, pady=4)

    btn_entry_save = ttk.Button(frm_entry, text="Save - Alt K", bootstyle="primary", command=cmd_save)
    btn_entry_save.grid(row=0, column=2, padx=4, pady=4, rowspan=2, sticky="ns")

    # Command Widgets
    btn_down = ttk.Button(frm_commands, text="Down - Alt L", bootstyle="primary", command=cmd_movedown)
    btn_down.pack(side="left", padx=4, pady=4)

    btn_up = ttk.Button(frm_commands, text="Up - Alt O", bootstyle="primary", command=cmd_moveup)
    btn_up.pack(side="left", padx=4, pady=4)

    # TV Widgets
    tv_sb = ttk.Scrollbar(frm_tv, orient="vertical")
    tv_sb.pack(side="right", fill="y")

    tv = ttk.Treeview(frm_tv, columns=("id", "winningticket", "winner"), show="headings", yscrollcommand=tv_sb.set, height=22)
    tv.column("id", width=150), tv.heading("id", text="ID")
    tv.column("winningticket", width=170), tv.heading("winningticket", text="Winning Ticket")
    tv.column("winner", width=700), tv.heading("winner", text="Winner")
    tv.pack(padx=2, pady=2, expand=True, fill="both")

    tv_sb.config(command=tv.yview)

    # Bind Commands
    def bnd_tv_select(_):
        for s in tv.selection():
            r = tv.item(s)['values']
            v_id.set(r[0]), v_winningticket.set(r[1])

    def bnd_save(_):
        cmd_save()

    def bnd_movedown(_):
        cmd_movedown()

    def bnd_moveup(_):
        cmd_moveup()
    
    # Bindings
    tv.bind('<<TreeviewSelect>>', bnd_tv_select)
    window.bind('<Alt-k>', bnd_save)
    window.bind('<Alt-l>', bnd_movedown)
    window.bind('<Alt-o>', bnd_moveup)