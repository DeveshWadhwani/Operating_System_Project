def create_admin_dialog(self):
    dlg = CreateUserDialog(self.root, title="Create Admin", require_role="admin")
    if dlg.result:
        username, password = dlg.result
        try:
            c = self.conn.cursor()
            c.execute("INSERT INTO users (username,password_hash,role) VALUES (?,?,?)",
                      (username, hash_password(password), "admin"))
            self.conn.commit()
            messagebox.showinfo("Created", "Admin user created")
            log_info(f"Admin created: {username}")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "User already exists")
        except Exception as e:
            log_err("Create admin failed")
            messagebox.showerror("Error", str(e))

def login_dialog(self):
    dlg = LoginDialog(self.root, title="Login")
    if not dlg.result:
        return
    username, password = dlg.result
    c = self.conn.cursor()
    c.execute("SELECT password_hash,role FROM users WHERE username=?", (username,))
    row = c.fetchone()
    if not row:
        messagebox.showerror("Error", "Unknown user")
        return
    phash, role = row
    if hash_password(password) == phash:
        self.user = username
        self.login_btn.config(text=f"User: {username} ({role})")
        self.status_var.set(f"Logged in as {username}")
        log_info(f"User logged in: {username}")
    else:
        messagebox.showerror("Error", "Wrong password")
