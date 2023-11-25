import ttkbootstrap as ttk 
from db_engine import session, RegularTicket, SpecialtyTicket

def rt_form():
    window = ttk.Toplevel(title="Regular Ticket Entry")
    window.focus()

    #Vars
    v_from = ttk.IntVar(window)
    v_to = ttk.IntVar(window)

    v_id = ttk.IntVar(window)
    v_firstname = ttk.StringVar(window)
    v_lastname = ttk.StringVar(window)
    v_phonenumber = ttk.StringVar(window)
    v_preferstext = ttk.IntVar(window)
    v_preferstext.set(0)

    # Commands
    def cmd_tv_refresh():
        for c in tv.get_children():
            tv.delete(c)
        for i in range(v_from.get(), v_to.get()+1):
            try:
                r = session.query(RegularTicket).filter(RegularTicket.TicketID == i).one()
                tv.insert('', index="end", iid=i, values=(i, r.FirstName, r.LastName, r.PhoneNumber, r.pref()))
            except:
                tv.insert('', index="end", iid=i, values=(i, '', '', '', ''))

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
        txt_firstname.focus()

    def cmd_save():
        try:
            r = session.query(RegularTicket).filter(RegularTicket.TicketID == v_id.get()).one()
            r.FirstName, r.LastName, r.PhoneNumber, r.PrefersText = v_firstname.get(), v_lastname.get(), v_phonenumber.get(), v_preferstext.get()
            session.commit()
        except:
            r = RegularTicket(TicketID=v_id.get(), FirstName=v_firstname.get(), LastName=v_lastname.get(), PhoneNumber=v_phonenumber.get(), PrefersText=v_preferstext.get())
            session.add(r)
            session.commit()
        cmd_tv_refresh()
        cmd_id_update()
    
    def cmd_dupdown():
        cmd_save()
        vals = (v_firstname.get(), v_lastname.get(), v_phonenumber.get(), v_preferstext.get())
        if v_to.get() > v_id.get():
            v_id.set(v_id.get()+1)
        v_firstname.set(vals[0]), v_lastname.set(vals[1]), v_phonenumber.set(vals[2]), v_preferstext.set(vals[3])
        cmd_save()
        cmd_id_update()

    def cmd_dupup():
        cmd_save()
        vals = (v_firstname.get(), v_lastname.get(), v_phonenumber.get(), v_preferstext.get())
        if v_id.get() > v_from.get():
            v_id.set(v_id.get()-1)
        v_firstname.set(vals[0]), v_lastname.set(vals[1]), v_phonenumber.set(vals[2]), v_preferstext.set(vals[3])
        cmd_save()
        cmd_id_update()

    def cmd_movedown():
        if v_to.get() > v_id.get():
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

    # Editor Widgets
    ttk.Label(frm_entry, text="ID").grid(row=0, column=0, padx=4, pady=4)
    txt_id = ttk.Spinbox(frm_entry, textvariable=v_id, width=15, command=cmd_id_update)
    txt_id.grid(row=1, column=0, padx=4, pady=4)

    ttk.Label(frm_entry, text="First Name").grid(row=0, column=1, padx=4, pady=4)
    txt_firstname = ttk.Entry(frm_entry, textvariable=v_firstname, width=40)
    txt_firstname.grid(row=1, column=1, padx=4, pady=4)

    ttk.Label(frm_entry, text="Last Name").grid(row=0, column=2, padx=4, pady=4)
    txt_lastname = ttk.Entry(frm_entry, textvariable=v_lastname, width=40)
    txt_lastname.grid(row=1, column=2, padx=4, pady=4)

    ttk.Label(frm_entry, text="Phone Number").grid(row=0, column=3, padx=4, pady=4)
    txt_phonenumber = ttk.Entry(frm_entry, textvariable=v_phonenumber, width=40)
    txt_phonenumber.grid(row=1, column=3, padx=4, pady=4)

    ttk.Label(frm_entry, text="Prefers Text").grid(row=0, column=4, padx=4, pady=4)
    chk_preferstext = ttk.Checkbutton(frm_entry, variable=v_preferstext, onvalue=-1, offvalue=0)
    chk_preferstext.grid(row=1, column=4, padx=4, pady=4)
    
    btn_entry_save = ttk.Button(frm_entry, text="Save - Alt K", bootstyle="secondary", command=cmd_save)
    btn_entry_save.grid(row=0, column=5, padx=4, pady=4, rowspan=2, sticky="ns")

    # Command Widgets
    btn_duplicatedown = ttk.Button(frm_commands, text="Duplicate Down - Alt J", bootstyle="secondary", command=cmd_dupdown)
    btn_duplicatedown.pack(side="left", padx=4, pady=4)

    btn_duplicateup = ttk.Button(frm_commands, text="Duplicate Up - Alt U", bootstyle="secondary", command=cmd_dupup)
    btn_duplicateup.pack(side="left", padx=4, pady=4)

    btn_down = ttk.Button(frm_commands, text="Move Down - Alt L", bootstyle="secondary", command=cmd_movedown)
    btn_down.pack(side="left", padx=4, pady=4)

    btn_up = ttk.Button(frm_commands, text="Move Up - Alt O", bootstyle="secondary", command=cmd_moveup)
    btn_up.pack(side="left", padx=4, pady=4)

    # Treeview Widgets
    tv_sb = ttk.Scrollbar(frm_tv, orient="vertical")
    tv_sb.pack(side="right", fill="y")

    tv = ttk.Treeview(frm_tv, columns=("id", "firstname", "lastname", "phonenumber", "preferstext"), show="headings", height=22, yscrollcommand=tv_sb.set)
    tv.column("id", width=150), tv.heading("id", text="Ticket #")
    tv.column("firstname", width=400), tv.heading("firstname", text="First Name")
    tv.column("lastname", width=400), tv.heading("lastname", text="Last Name")
    tv.column("phonenumber", width=400), tv.heading("phonenumber", text="Phone Number")
    tv.column("preferstext", width=100), tv.heading("preferstext", text="Pref")
    tv.pack(expand=True, fill="both", padx=4, pady=4)
    tv_sb.config(command=tv.yview)

    # Binding Commands
    def bnd_convert(string):
        if string == "TEXT":
            return -1
        else:
            return 0

    def bnd_tv_select(_):
        for s in tv.selection():
            r = tv.item(s)['values']
            v_id.set(r[0]), v_firstname.set(r[1]), v_lastname.set(r[2]), v_phonenumber.set(r[3]), v_preferstext.set(bnd_convert(r[4]))

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

def st_form():
    window = ttk.Toplevel(title="Specialty Ticket Entry")
    window.focus()

    #Vars
    v_from = ttk.IntVar(window)
    v_to = ttk.IntVar(window)

    v_id = ttk.IntVar(window)
    v_firstname = ttk.StringVar(window)
    v_lastname = ttk.StringVar(window)
    v_phonenumber = ttk.StringVar(window)
    v_preferstext = ttk.IntVar(window)
    v_preferstext.set(0)

    # Commands
    def cmd_tv_refresh():
        for c in tv.get_children():
            tv.delete(c)
        for i in range(v_from.get(), v_to.get()+1):
            try:
                r = session.query(SpecialtyTicket).filter(SpecialtyTicket.TicketID == i).one()
                tv.insert('', index="end", iid=i, values=(i, r.FirstName, r.LastName, r.PhoneNumber, r.pref()))
            except:
                tv.insert('', index="end", iid=i, values=(i, '', '', '', ''))

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
        txt_firstname.focus()

    def cmd_save():
        try:
            r = session.query(SpecialtyTicket).filter(SpecialtyTicket.TicketID == v_id.get()).one()
            r.FirstName, r.LastName, r.PhoneNumber, r.PrefersText = v_firstname.get(), v_lastname.get(), v_phonenumber.get(), v_preferstext.get()
            session.commit()
        except:
            r = SpecialtyTicket(TicketID=v_id.get(), FirstName=v_firstname.get(), LastName=v_lastname.get(), PhoneNumber=v_phonenumber.get(), PrefersText=v_preferstext.get())
            session.add(r)
            session.commit()
        cmd_tv_refresh()
        cmd_id_update()
    
    def cmd_dupdown():
        cmd_save()
        vals = (v_firstname.get(), v_lastname.get(), v_phonenumber.get(), v_preferstext.get())
        if v_to.get() > v_id.get():
            v_id.set(v_id.get()+1)
        v_firstname.set(vals[0]), v_lastname.set(vals[1]), v_phonenumber.set(vals[2]), v_preferstext.set(vals[3])
        cmd_save()
        cmd_id_update()

    def cmd_dupup():
        cmd_save()
        vals = (v_firstname.get(), v_lastname.get(), v_phonenumber.get(), v_preferstext.get())
        if v_id.get() > v_from.get():
            v_id.set(v_id.get()-1)
        v_firstname.set(vals[0]), v_lastname.set(vals[1]), v_phonenumber.set(vals[2]), v_preferstext.set(vals[3])
        cmd_save()
        cmd_id_update()

    def cmd_movedown():
        if v_to.get() > v_id.get():
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

    # Editor Widgets
    ttk.Label(frm_entry, text="ID").grid(row=0, column=0, padx=4, pady=4)
    txt_id = ttk.Spinbox(frm_entry, textvariable=v_id, width=15, command=cmd_id_update)
    txt_id.grid(row=1, column=0, padx=4, pady=4)

    ttk.Label(frm_entry, text="First Name").grid(row=0, column=1, padx=4, pady=4)
    txt_firstname = ttk.Entry(frm_entry, textvariable=v_firstname, width=40)
    txt_firstname.grid(row=1, column=1, padx=4, pady=4)

    ttk.Label(frm_entry, text="Last Name").grid(row=0, column=2, padx=4, pady=4)
    txt_lastname = ttk.Entry(frm_entry, textvariable=v_lastname, width=40)
    txt_lastname.grid(row=1, column=2, padx=4, pady=4)

    ttk.Label(frm_entry, text="Phone Number").grid(row=0, column=3, padx=4, pady=4)
    txt_phonenumber = ttk.Entry(frm_entry, textvariable=v_phonenumber, width=40)
    txt_phonenumber.grid(row=1, column=3, padx=4, pady=4)

    ttk.Label(frm_entry, text="Prefers Text").grid(row=0, column=4, padx=4, pady=4)
    chk_preferstext = ttk.Checkbutton(frm_entry, variable=v_preferstext, onvalue=-1, offvalue=0)
    chk_preferstext.grid(row=1, column=4, padx=4, pady=4)
    
    btn_entry_save = ttk.Button(frm_entry, text="Save - Alt K", bootstyle="primary", command=cmd_save)
    btn_entry_save.grid(row=0, column=5, padx=4, pady=4, rowspan=2, sticky="ns")

    # Command Widgets
    btn_duplicatedown = ttk.Button(frm_commands, text="Duplicate Down - Alt J", bootstyle="primary", command=cmd_dupdown)
    btn_duplicatedown.pack(side="left", padx=4, pady=4)

    btn_duplicateup = ttk.Button(frm_commands, text="Duplicate Up - Alt U", bootstyle="primary", command=cmd_dupup)
    btn_duplicateup.pack(side="left", padx=4, pady=4)

    btn_down = ttk.Button(frm_commands, text="Move Down - Alt L", bootstyle="primary", command=cmd_movedown)
    btn_down.pack(side="left", padx=4, pady=4)

    btn_up = ttk.Button(frm_commands, text="Move Up - Alt O", bootstyle="primary", command=cmd_moveup)
    btn_up.pack(side="left", padx=4, pady=4)

    # Treeview Widgets
    tv_sb = ttk.Scrollbar(frm_tv, orient="vertical")
    tv_sb.pack(side="right", fill="y")

    tv = ttk.Treeview(frm_tv, columns=("id", "firstname", "lastname", "phonenumber", "preferstext"), show="headings", height=22, yscrollcommand=tv_sb.set)
    tv.column("id", width=150), tv.heading("id", text="Ticket #")
    tv.column("firstname", width=400), tv.heading("firstname", text="First Name")
    tv.column("lastname", width=400), tv.heading("lastname", text="Last Name")
    tv.column("phonenumber", width=400), tv.heading("phonenumber", text="Phone Number")
    tv.column("preferstext", width=100), tv.heading("preferstext", text="Pref")
    tv.pack(expand=True, fill="both", padx=4, pady=4)
    tv_sb.config(command=tv.yview)

    # Binding Commands
    def bnd_convert(string):
        if string == "TEXT":
            return -1
        else:
            return 0

    def bnd_tv_select(_):
        for s in tv.selection():
            r = tv.item(s)['values']
            v_id.set(r[0]), v_firstname.set(r[1]), v_lastname.set(r[2]), v_phonenumber.set(r[3]), v_preferstext.set(bnd_convert(r[4]))

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