import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

os.makedirs("../data", exist_ok=True)

root = tk.Tk()
root.title("🎟️ Configuration des billets")
root.geometry("600x500")

tk.Label(root, text="Choisissez vos catégories, quantités et fallback", font=("Arial", 14)).pack(pady=10)

categories = ["Cat Or", "Cat 1", "Cat 2", "Cat 3", "Fosse", "Fosse Or"]

ligne_container = tk.Frame(root)
ligne_container.pack()

all_lignes = []

def ajouter_ligne():
    frame = tk.Frame(ligne_container)
    frame.pack(pady=5)

    cat_var = tk.StringVar()
    cat_menu = ttk.Combobox(frame, values=categories, textvariable=cat_var, width=15, state="readonly")
    cat_menu.set(categories[0])
    cat_menu.pack(side=tk.LEFT, padx=5)

    qty_var = tk.IntVar(value=1)
    qty_spin = tk.Spinbox(frame, from_=1, to=8, width=5, textvariable=qty_var)
    qty_spin.pack(side=tk.LEFT, padx=5)

    fb_var = tk.StringVar()
    fb_menu = ttk.Combobox(frame, values=categories, textvariable=fb_var, width=15, state="readonly")
    fb_menu.set("")  # Fallback vide par défaut
    fb_menu.pack(side=tk.LEFT, padx=5)

    all_lignes.append((cat_var, qty_var, fb_var))

# Ajouter la première ligne par défaut
ajouter_ligne()

btn_add = tk.Button(root, text="➕ Ajouter une ligne", command=ajouter_ligne)
btn_add.pack(pady=10)

def valider():
    config = {}
    for cat_var, qty_var, fb_var in all_lignes:
        cat = cat_var.get()
        qty = qty_var.get()
        fb = fb_var.get()
        if cat:
            config[cat] = {"qty": qty, "fallback": fb}

    if not config:
        messagebox.showwarning("Aucune sélection", "Veuillez ajouter au moins une catégorie.")
        return

    try:
        with open("../data/config.json", "w") as f:
            json.dump(config, f, indent=2)
        messagebox.showinfo("✅ Succès", "Configuration enregistrée ! Le bot va démarrer.")
        root.destroy()
    except Exception as e:
        messagebox.showerror("❌ Erreur", f"Impossible d'enregistrer : {e}")

tk.Button(root, text="Lancer le bot", command=valider, bg="#4CAF50", fg="white").pack(pady=20)

root.mainloop()
