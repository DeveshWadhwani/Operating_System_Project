class ItemEditDialog(simpledialog.Dialog):
    def _init_(self, parent, title=None, prefill=None):
        self.prefill = prefill
        super()._init_(parent, title=title)

    def body(self, master):
        ttk.Label(master, text="SKU:").grid(row=0,column=0,sticky=tk.W)
        self.sku = ttk.Entry(master); self.sku.grid(row=0,column=1)
        ttk.Label(master, text="Name:").grid(row=1,column=0,sticky=tk.W)
        self.name = ttk.Entry(master); self.name.grid(row=1,column=1)
        ttk.Label(master, text="Category:").grid(row=2,column=0,sticky=tk.W)
        self.category = ttk.Entry(master); self.category.grid(row=2,column=1)
        ttk.Label(master, text="Unit Price:").grid(row=3,column=0,sticky=tk.W)
        self.price = ttk.Entry(master); self.price.grid(row=3,column=1)
        ttk.Label(master, text="Qty:").grid(row=4,column=0,sticky=tk.W)
        self.qty = ttk.Entry(master); self.qty.grid(row=4,column=1)
        ttk.Label(master, text="Reorder level:").grid(row=5,column=0,sticky=tk.W)
        self.reorder = ttk.Entry(master); self.reorder.grid(row=5,column=1)
        if self.prefill:
            self.sku.insert(0, self.prefill.get("sku") or "")
            self.name.insert(0, self.prefill.get("name") or "")
            self.category.insert(0, self.prefill.get("category") or "")
            self.price.insert(0, str(self.prefill.get("price") or "0"))
            self.qty.insert(0, str(self.prefill.get("qty") or "0"))
            self.reorder.insert(0, str(self.prefill.get("reorder") or "0"))
        return self.name

    def validate(self):
        if not self.name.get().strip():
            messagebox.showerror("Validation","Name required"); return False
        try:
            float(self.price.get()); int(self.qty.get()); int(self.reorder.get())
        except Exception:
            messagebox.showerror("Validation","Invalid numeric value"); return False
        return True

    def apply(self):
        self.result = (self.sku.get().strip(), self.name.get().strip(), self.category.get().strip(),
                       float(self.price.get()), int(self.qty.get()), int(self.reorder.get()))

class ReportDialog(simpledialog.Dialog):
    def _init_(self, parent, title, text, csv_rows=None):
        self.text = text
        self.csv_rows = csv_rows
        super()._init_(parent, title=title)

    def body(self, master):
        txt = tk.Text(master, width=80, height=20)
        txt.pack(fill=tk.BOTH, expand=True)
        txt.insert("1.0", self.text)
        txt.config(state=tk.DISABLED)
        self.txt = txt
        return txt

    def buttonbox(self):
        box = ttk.Frame(self)
        ttk.Button(box, text="Close", command=self.ok).pack(side=tk.RIGHT, padx=5, pady=5)
        if self.csv_rows:
            ttk.Button(box, text="Export CSV", command=self._export_csv).pack(side=tk.RIGHT, padx=5, pady=5)
        box.pack()

    def _export_csv(self):
        fn = filedialog.asksaveasfilename(defaultextension=".csv")
        if not fn:
            return
        try:
            with open(fn, "w", newline='', encoding='utf-8') as f:
                w = csv.writer(f)
                for r in self.csv_rows:
                    w.writerow(r)
            messagebox.showinfo("Exported", f"Exported to {fn}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

class DateRangeDialog(simpledialog.Dialog):
    def body(self, master):
        ttk.Label(master, text="Start date (YYYY-MM-DD):").grid(row=0,column=0)
        self.s = ttk.Entry(master); self.s.grid(row=0,column=1)
        ttk.Label(master, text="End date (YYYY-MM-DD):").grid(row=1,column=0)
        self.e = ttk.Entry(master); self.e.grid(row=1,column=1)
        return self.s
    def validate(self):
        try:
            s = datetime.fromisoformat(self.s.get().strip())
            e = datetime.fromisoformat(self.e.get().strip())
            if s>e:
                messagebox.showerror("Validation","Start must be <= End"); return False
            self.result = (s.date(), e.date())
            return True
        except Exception:
            messagebox.showerror("Validation","Invalid dates"); return False

class LoginDialog(simpledialog.Dialog):
    def body(self, master):
        ttk.Label(master, text="Username:").grid(row=0,column=0)
        self.u = ttk.Entry(master); self.u.grid(row=0,column=1)
        ttk.Label(master, text="Password:").grid(row=1,column=0)
        self.p = ttk.Entry(master, show="*"); self.p.grid(row=1,column=1)
        return self.u
    def apply(self):
        self.result = (self.u.get().strip(), self.p.get())

class CreateUserDialog(simpledialog.Dialog):
    def _init_(self, parent, title=None, require_role=None):
        self.require_role = require_role
        super()._init_(parent, title=title)
    def body(self, master):
        ttk.Label(master, text="Username:").grid(row=0,column=0)
        self.u = ttk.Entry(master); self.u.grid(row=0,column=1)
        ttk.Label(master, text="Password:").grid(row=1,column=0)
        self.p = ttk.Entry(master, show="*"); self.p.grid(row=1,column=1)
        return self.u
    def validate(self):
        if not self.u.get().strip() or not self.p.get():
            messagebox.showerror("Validation","Provide username and password"); return False
        return True
    def apply(self):
        self.result = (self.u.get().strip(), self.p.get())
