import json
import time
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ========== CONFIG ==========
URL = "http://localhost:8000"
CONFIG_PATH = "../data/config.json"
LOG_PATH = "../data/bot.log"

# ========== SETUP LOGGING ==========
os.makedirs("../data", exist_ok=True)

def log(msg):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    full_msg = f"{timestamp} {msg}"
    print(full_msg)
    with open(LOG_PATH, "a") as f:
        f.write(full_msg + "\n")

# Réinitialisation fichier de logs
with open(LOG_PATH, "w") as f:
    f.write("=== LOG DU BOT ===\n")

# ========== CHARGEMENT CONFIG ==========
with open(CONFIG_PATH, "r") as f:
    config = json.load(f)
log(f"📤 Configuration demandée par GUI : {config}")

# ========== LANCEMENT DU NAVIGATEUR ==========
driver = webdriver.Chrome()
driver.get(URL)

log("⏳ En attente de l'ouverture des ventes...")
while True:
    try:
        acheter_btn = driver.find_element(By.ID, "acheter")
        if acheter_btn.is_displayed():
            log("🎯 Bouton détecté !")
            acheter_btn.click()
            break
    except:
        pass

# ========== ATTENTE DU FORMULAIRE ==========
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "categories-container"))
)

# ========== DÉTECTION DES CATÉGORIES ==========
time.sleep(1.5)  # petit délai pour s'assurer que le JS ait injecté les éléments
category_blocks = driver.find_elements(By.CLASS_NAME, "category")
log(f"🔎 {len(category_blocks)} blocs de catégorie détectés.")

available_categories = {}

for block in category_blocks:
    try:
        name = block.find_element(By.CLASS_NAME, "header").find_elements(By.TAG_NAME, "span")[0].text.strip()
        is_disabled = "disabled" in block.get_attribute("class")
        available_categories[name] = {
            "element": block,
            "available": not is_disabled
        }
    except Exception as e:
        log(f"⚠️ Erreur lors de l'analyse d'un bloc : {e}")

log("📋 Catégories détectées dans le DOM :")
for cat, info in available_categories.items():
    log(f" - {cat} → {'dispo' if info['available'] else 'épuisée'}")

# ========== AJOUT DE TICKETS ==========
def add_tickets(cat_name, qty):
    block = available_categories[cat_name]["element"]
    header = block.find_element(By.CLASS_NAME, "header")
    toggle = header.find_element(By.CLASS_NAME, "toggle")
    if toggle.text == "➤":
        toggle.click()
        time.sleep(0.2)
    plus_btn = block.find_element(By.CLASS_NAME, "plus")
    for _ in range(qty):
        plus_btn.click()
        time.sleep(0.1)
    log(f"✅ {qty} billet(s) ajoutés en '{cat_name}'")

# ========== TRAITEMENT DES DEMANDES ==========
selection_faite = False
taken_summary = {}

for cat_name, details in config.items():
    qty = details.get("qty", 0)
    fallback = details.get("fallback", "").strip()

    if available_categories.get(cat_name, {}).get("available", False):
        log(f"🎟️ Sélection principale : {qty} en {cat_name}")
        add_tickets(cat_name, qty)
        taken_summary[cat_name] = taken_summary.get(cat_name, 0) + qty
        selection_faite = True
    elif fallback and available_categories.get(fallback, {}).get("available", False):
        log(f"⚠️ {cat_name} épuisée → fallback vers {fallback}")
        add_tickets(fallback, qty)
        taken_summary[fallback] = taken_summary.get(fallback, 0) + qty
        selection_faite = True
    else:
        log(f"❌ Demande impossible pour '{cat_name}' (ni fallback)")

# ========== CONCLUSION ==========
if not selection_faite:
    log("🚫 Aucun billet sélectionnable. Fin du bot.")
else:
    log("✅ Sélection complète.")
    try:
        driver.find_element(By.NAME, "nom").send_keys("Dupont")
        driver.find_element(By.NAME, "prenom").send_keys("Jean")
        driver.find_element(By.NAME, "email").send_keys("jean.dupont@example.com")
        driver.find_element(By.NAME, "cb").send_keys("4111111111111111")
        driver.find_element(By.NAME, "cvv").send_keys("123")

        expiration = driver.find_element(By.NAME, "expiration")
        driver.execute_script("arguments[0].value = arguments[1]", expiration, "2026-05")

        driver.find_element(By.XPATH, "//form/button").click()
        log("📤 Formulaire soumis avec succès.")
    except Exception as e:
        log(f"❌ Erreur lors du remplissage du formulaire : {e}")
        log("📦 Résumé des billets ajoutés :")
        for cat, q in taken_summary.items():
            log(f"➡️ {q} billet(s) en '{cat}'")

input("🕵️‍♂️ Appuie sur Entrée pour fermer le navigateur...")
driver.quit()
