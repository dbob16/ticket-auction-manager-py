import ttkbootstrap as ttk 
from .db_engine import session, RegularBasket, SpecialtyBasket

def rb_form():
    window = ttk.Toplevel(title="Regular Basket Entry")
    window.focus()

    # Variables
    v_from = ttk.IntVar(window)
    v_to = ttk.IntVar(window)

    v_id = ttk.IntVar(window)
    v_description = ttk.StringVar(window)
    v_donors = ttk.StringVar(window)

    # Commands
    def cmd_tv_refresh():
        for c in tv.get_children():
            tv.delete(c)
        for i in range(v_from.get(), v_to.get()+1):
            try:
                r = session.query(RegularBasket).filter(RegularBasket.BasketID == i).one()
                tv.insert('', index="end", iid=i, values=(i, r.Description, r.Donors))
            except:
                tv.insert('', index="end", iid=i, values=(i, '', ''))

    def cmd_pagerupdate():
        txt_id.config(from_=v_from.get(), to=v_to.get())
        cmd_tv_refresh()
        if v_id.get() < v_from.get():
            v_id.set(v_from.get())
        elif v_id.get() > v_to.get():
            v_id.set(v_to.get())
        cmd_id_update()

    def cmd_id_update():
        tv.selection_set(v_id.get())
        txt_description.focus()

    def cmd_save():
        try:
            r = session.query(RegularBasket).filter(RegularBasket.BasketID == v_id.get()).one()
            r.Description, r.Donors = v_description.get(), v_donors.get()
            session.commit()
        except:
            r = RegularBasket(BasketID=v_id.get(), Description=v_description.get(), Donors=v_donors.get(), WinningTicket=0)
            session.add(r)
            session.commit()
        cmd_tv_refresh()
        cmd_id_update()

    def cmd_dupdown():
        cmd_save()
        vals = (v_description.get(), v_donors.get())
        if v_id.get() < v_to.get():
            v_id.set(v_id.get()+1)
            v_description.set(vals[0]), v_donors.set(vals[1])
            cmd_save()

    def cmd_dupup():
        cmd_save()
        vals = (v_description.get(), v_donors.get())
        if v_id.get() > v_from.get():
            v_id.set(v_id.get()-1)
            v_description.set(vals[0]), v_donors.set(vals[1])
            cmd_save()

    def cmd_movedown():
        if v_id.get() < v_to.get():
            v_id.set(v_id.get()+1)
            cmd_id_update()

    def cmd_moveup():
        if v_id.get() > v_from.get():
            v_id.set(v_id.get()-1)
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

    ttk.Label(frm_entry, text="Description").grid(row=0, column=1, padx=4, pady=4)
    txt_description = ttk.Entry(frm_entry, textvariable=v_description, width=50)
    txt_description.grid(row=1, column=1, padx=4, pady=4)

    ttk.Label(frm_entry, text="Donors").grid(row=0, column=2, padx=4, pady=4)
    txt_donors = ttk.Entry(frm_entry, textvariable=v_donors, width=50)
    txt_donors.grid(row=1, column=2, padx=4, pady=4)

    btn_entry_save = ttk.Button(frm_entry, text="Save - Alt K", bootstyle="secondary", command=cmd_save)
    btn_entry_save.grid(row=0, column=3, padx=4, pady=4, rowspan=2, sticky="ns")

    # Command Widgets
    btn_duplicatedown = ttk.Button(frm_commands, text="Duplicate Down - Alt J", bootstyle="secondary", command=cmd_dupdown)
    btn_duplicatedown.pack(side="left", padx=4, pady=4)

    btn_duplicateup = ttk.Button(frm_commands, text="Duplicate Up - Alt U", bootstyle="secondary", command=cmd_dupup)
    btn_duplicateup.pack(side="left", padx=4, pady=4)

    btn_down = ttk.Button(frm_commands, text="Down - Alt L", bootstyle="secondary", command=cmd_movedown)
    btn_down.pack(side="left", padx=4, pady=4)

    btn_up = ttk.Button(frm_commands, text="Up - Alt O", bootstyle="secondary", command=cmd_moveup)
    btn_up.pack(side="left", padx=4, pady=4)

    # Treeview Widgets
    tv_sb = ttk.Scrollbar(frm_tv, orient="vertical")
    tv_sb.pack(side="right", fill="y")

    tv = ttk.Treeview(frm_tv, columns=("id", "description", "donors"), show="headings", height=22, yscrollcommand=tv_sb.set)
    tv.column("id", width=150), tv.heading("id", text="Basket #")
    tv.column("description", width=500), tv.heading("description", text="Description")
    tv.column("donors", width=500), tv.heading("donors", text="Donors")
    tv.pack(expand=True, fill="both", padx=2, pady=2)

    tv_sb.config(command=tv.yview)

    # Bind Commands
    def bnd_tv_select(_):
        for s in tv.selection():
            r = tv.item(s)['values']
            v_id.set(r[0]), v_description.set(r[1]), v_donors.set(r[2])

    def bnd_save(_):
        cmd_save()

    def bnd_dupdown(_):
        cmd_dupdown()
    
    def bnd_dupup(_):
        cmd_dupup()

    def bnd_movedown(_):
        cmd_movedown()

    def bnd_moveup(_):
        cmd_moveup()
    
    # Bindings
    tv.bind('<<TreeviewSelect>>', bnd_tv_select)
    window.bind('<Alt-k>', bnd_save)
    window.bind('<Alt-j>', bnd_dupdown)
    window.bind('<Alt-u>', bnd_dupup)
    window.bind('<Alt-l>', bnd_movedown)
    window.bind('<Alt-o>', bnd_moveup)

def sb_form():
    window = ttk.Toplevel(title="Specialty Basket Entry")
    window.focus()

    # Variables
    v_from = ttk.IntVar(window)
    v_to = ttk.IntVar(window)

    v_id = ttk.IntVar(window)
    v_description = ttk.StringVar(window)
    v_donors = ttk.StringVar(window)

    # Commands
    def cmd_tv_refresh():
        for c in tv.get_children():
            tv.delete(c)
        for i in range(v_from.get(), v_to.get()+1):
            try:
                r = session.query(SpecialtyBasket).filter(SpecialtyBasket.BasketID == i).one()
                tv.insert('', index="end", iid=i, values=(i, r.Description, r.Donors))
            except:
                tv.insert('', index="end", iid=i, values=(i, '', ''))

    def cmd_pagerupdate():
        txt_id.config(from_=v_from.get(), to=v_to.get())
        cmd_tv_refresh()
        if v_id.get() < v_from.get():
            v_id.set(v_from.get())
        elif v_id.get() > v_to.get():
            v_id.set(v_to.get())
        cmd_id_update()

    def cmd_id_update():
        tv.selection_set(v_id.get())
        txt_description.focus()

    def cmd_save():
        try:
            r = session.query(SpecialtyBasket).filter(SpecialtyBasket.BasketID == v_id.get()).one()
            r.Description, r.Donors = v_description.get(), v_donors.get()
            session.commit()
        except:
            r = SpecialtyBasket(BasketID=v_id.get(), Description=v_description.get(), Donors=v_donors.get(), WinningTicket=0)
            session.add(r)
            session.commit()
        cmd_tv_refresh()
        cmd_id_update()

    def cmd_dupdown():
        cmd_save()
        vals = (v_description.get(), v_donors.get())
        if v_id.get() < v_to.get():
            v_id.set(v_id.get()+1)
            v_description.set(vals[0]), v_donors.set(vals[1])
            cmd_save()

    def cmd_dupup():
        cmd_save()
        vals = (v_description.get(), v_donors.get())
        if v_id.get() > v_from.get():
            v_id.set(v_id.get()-1)
            v_description.set(vals[0]), v_donors.set(vals[1])
            cmd_save()

    def cmd_movedown():
        if v_id.get() < v_to.get():
            v_id.set(v_id.get()+1)
            cmd_id_update()

    def cmd_moveup():
        if v_id.get() > v_from.get():
            v_id.set(v_id.get()-1)
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

    ttk.Label(frm_entry, text="Description").grid(row=0, column=1, padx=4, pady=4)
    txt_description = ttk.Entry(frm_entry, textvariable=v_description, width=50)
    txt_description.grid(row=1, column=1, padx=4, pady=4)

    ttk.Label(frm_entry, text="Donors").grid(row=0, column=2, padx=4, pady=4)
    txt_donors = ttk.Entry(frm_entry, textvariable=v_donors, width=50)
    txt_donors.grid(row=1, column=2, padx=4, pady=4)

    btn_entry_save = ttk.Button(frm_entry, text="Save - Alt K", bootstyle="primary", command=cmd_save)
    btn_entry_save.grid(row=0, column=3, padx=4, pady=4, rowspan=2, sticky="ns")

    # Command Widgets
    btn_duplicatedown = ttk.Button(frm_commands, text="Duplicate Down - Alt J", bootstyle="primary", command=cmd_dupdown)
    btn_duplicatedown.pack(side="left", padx=4, pady=4)

    btn_duplicateup = ttk.Button(frm_commands, text="Duplicate Up - Alt U", bootstyle="primary", command=cmd_dupup)
    btn_duplicateup.pack(side="left", padx=4, pady=4)

    btn_down = ttk.Button(frm_commands, text="Down - Alt L", bootstyle="primary", command=cmd_movedown)
    btn_down.pack(side="left", padx=4, pady=4)

    btn_up = ttk.Button(frm_commands, text="Up - Alt O", bootstyle="primary", command=cmd_moveup)
    btn_up.pack(side="left", padx=4, pady=4)

    # Treeview Widgets
    tv_sb = ttk.Scrollbar(frm_tv, orient="vertical")
    tv_sb.pack(side="right", fill="y")

    tv = ttk.Treeview(frm_tv, columns=("id", "description", "donors"), show="headings", height=22, yscrollcommand=tv_sb.set)
    tv.column("id", width=150), tv.heading("id", text="Basket #")
    tv.column("description", width=500), tv.heading("description", text="Description")
    tv.column("donors", width=500), tv.heading("donors", text="Donors")
    tv.pack(expand=True, fill="both", padx=2, pady=2)

    tv_sb.config(command=tv.yview)

    # Bind Commands
    def bnd_tv_select(_):
        for s in tv.selection():
            r = tv.item(s)['values']
            v_id.set(r[0]), v_description.set(r[1]), v_donors.set(r[2])

    def bnd_save(_):
        cmd_save()

    def bnd_dupdown(_):
        cmd_dupdown()
    
    def bnd_dupup(_):
        cmd_dupup()

    def bnd_movedown(_):
        cmd_movedown()

    def bnd_moveup(_):
        cmd_moveup()
    
    # Bindings
    tv.bind('<<TreeviewSelect>>', bnd_tv_select)
    window.bind('<Alt-k>', bnd_save)
    window.bind('<Alt-j>', bnd_dupdown)
    window.bind('<Alt-u>', bnd_dupup)
    window.bind('<Alt-l>', bnd_movedown)
    window.bind('<Alt-o>', bnd_moveup)