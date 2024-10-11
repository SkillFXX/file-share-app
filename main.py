import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from threading import Thread
import os
import flask
from flask import Flask, render_template, send_file, request, redirect, url_for
import socket

class Windows11StyleFileShareApp:
    def __init__(self, master):
        self.master = master
        self.master.title("File Share App")
        self.master.geometry("1000x600")
        self.master.configure(bg="#f0f0f0")

        self.files = []
        self.server_status = "Arrêté"
        self.server_thread = None
        self.app = None
        self.site_name = "File Share"
        self.password = ""

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.configure_styles()

        self.create_widgets()

    def configure_styles(self):
        self.style.configure("W11.TFrame", background="#f0f0f0")
        self.style.configure("W11.TButton", padding=10, font=("Segoe UI", 11), background="#ffffff", borderwidth=0)
        self.style.map("W11.TButton", background=[('active', '#e5e5e5')])
        self.style.configure("W11.TLabel", font=("Segoe UI", 11), background="#f0f0f0")
        self.style.configure("W11Header.TLabel", font=("Segoe UI", 18, "bold"), background="#f0f0f0")
        self.style.configure("W11Status.TLabel", font=("Segoe UI", 10), background="#f0f0f0")
        self.style.configure("W11.TListbox", font=("Segoe UI", 11), background="white", borderwidth=0)
        self.style.configure("W11.TMenubutton", font=("Segoe UI", 11), padding=10)

    def create_widgets(self):
        main_frame = ttk.Frame(self.master, style="W11.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Titre
        ttk.Label(main_frame, text="File Share Application", style="W11Header.TLabel").pack(pady=(0, 20))

        # Frame pour la liste de fichiers
        file_frame = ttk.Frame(main_frame, style="W11.TFrame")
        file_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.file_listbox = tk.Listbox(file_frame, font=("Segoe UI", 11), bg="white", borderwidth=0, highlightthickness=0)
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(file_frame, orient=tk.VERTICAL, command=self.file_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.file_listbox.config(yscrollcommand=scrollbar.set)

        # Boutons pour ajouter/supprimer des fichiers
        btn_frame = ttk.Frame(main_frame, style="W11.TFrame")
        btn_frame.pack(pady=10)

        self.add_btn = ttk.Button(btn_frame, text="Ajouter fichier", command=self.add_file, style="W11.TButton")
        self.add_btn.pack(side=tk.LEFT, padx=5)

        self.remove_btn = ttk.Button(btn_frame, text="Supprimer fichier", command=self.remove_file, style="W11.TButton", state=tk.DISABLED)
        self.remove_btn.pack(side=tk.LEFT, padx=5)

        # Boutons pour contrôler le serveur
        server_frame = ttk.Frame(main_frame, style="W11.TFrame")
        server_frame.pack(pady=10)

        self.start_btn = ttk.Button(server_frame, text="Lancer serveur", command=self.start_server, style="W11.TButton")
        self.start_btn.pack(side=tk.LEFT, padx=5)

        self.stop_btn = ttk.Button(server_frame, text="Arrêter serveur", command=self.stop_server, style="W11.TButton", state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)

        self.update_btn = ttk.Button(server_frame, text="Mettre à jour", command=self.update_server, style="W11.TButton", state=tk.DISABLED)
        self.update_btn.pack(side=tk.LEFT, padx=5)

        # Menu des paramètres
        settings_frame = ttk.Frame(main_frame, style="W11.TFrame")
        settings_frame.pack(pady=10, fill=tk.X)

        self.settings_btn = ttk.Menubutton(settings_frame, text="Paramètres ▼", style="W11.TMenubutton")
        self.settings_btn.pack(side=tk.LEFT)

        self.settings_menu = tk.Menu(self.settings_btn, tearoff=0)
        self.settings_btn['menu'] = self.settings_menu
        self.settings_menu.add_command(label="Nom du site", command=self.set_site_name)
        self.settings_menu.add_command(label="Mot de passe", command=self.set_password)

        # Statut du serveur
        self.status_label = ttk.Label(main_frame, text=f"Statut: {self.server_status}", style="W11Status.TLabel")
        self.status_label.pack(side=tk.BOTTOM, anchor=tk.E, padx=10, pady=10)

        # Bind events
        self.file_listbox.bind('<<ListboxSelect>>', self.on_select)

    def add_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.files.append(file_path)
            self.file_listbox.insert(tk.END, os.path.basename(file_path))
            self.update_button_states()

    def remove_file(self):
        selection = self.file_listbox.curselection()
        if selection:
            index = selection[0]
            self.file_listbox.delete(index)
            self.files.pop(index)
            self.update_button_states()

    def on_select(self, event):
        self.update_button_states()

    def update_button_states(self):
        if self.files:
            self.remove_btn.config(state=tk.NORMAL)
            self.start_btn.config(state=tk.NORMAL)
        else:
            self.remove_btn.config(state=tk.DISABLED)
            self.start_btn.config(state=tk.DISABLED)

        if self.server_status == "En cours":
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            self.update_btn.config(state=tk.NORMAL)
        else:
            self.stop_btn.config(state=tk.DISABLED)
            self.update_btn.config(state=tk.DISABLED)

    def set_site_name(self):
        new_name = simpledialog.askstring("Nom du site", "Entrez le nouveau nom du site:", parent=self.master)
        if new_name:
            self.site_name = new_name

    def set_password(self):
        new_password = simpledialog.askstring("Mot de passe", "Entrez le nouveau mot de passe (laisser vide pour désactiver):", parent=self.master)
        if new_password is not None:  # L'utilisateur n'a pas annulé
            self.password = new_password

    def start_server(self):
        if self.server_status == "Arrêté":
            self.app = Flask(__name__)
            self.setup_routes()
            self.server_thread = Thread(target=self.run_server)
            self.server_thread.start()
            self.server_status = "En cours"
            self.update_status()
            self.update_button_states()

    def stop_server(self):
        if self.server_status == "En cours":
            # Arrêter le serveur Flask (à implémenter)
            self.server_status = "Arrêté"
            self.update_status()
            self.update_button_states()

    def update_server(self):
        if self.server_status == "En cours":
            self.stop_server()
            self.start_server()

    def update_status(self):
        ip = socket.gethostbyname(socket.gethostname())
        self.status_label.config(text=f"Statut: {self.server_status} - IP: {ip}")

    def setup_routes(self):
        @self.app.route('/')
        def home():
            return render_template('index.html', files=self.files, site_name=self.site_name)

        @self.app.route('/download/<path:filename>')
        def download(filename):
            if self.password:
                if request.args.get('password') != self.password:
                    return redirect(url_for('password_page', filename=filename))
            return send_file(filename, as_attachment=True)

        @self.app.route('/password/<path:filename>')
        def password_page(filename):
            return render_template('password.html', filename=filename)

        @self.app.template_filter('basename')
        def basename_filter(path):
            return os.path.basename(path)

    def run_server(self):
        self.app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
    root = tk.Tk()
    app = Windows11StyleFileShareApp(root)
    root.mainloop()