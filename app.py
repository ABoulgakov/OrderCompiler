import os
import streamlit as st
from dotenv import load_dotenv

from connectors.mailbox import test_connection
from init import launch_order_compiler

# --- SETTINGS ---
APP_TITLE = "Agrégateur de commandes"

#load_dotenv()
#password = os.getenv("APP_PASSWORD")
password = st.secrets["APP_PASSWORD"]

# --- PAGE CONFIG ---
st.set_page_config(page_title=APP_TITLE, 
                    page_icon="📦",  
                    layout="wide")

# --- AUTH ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def check_password():
    if st.session_state["password_input"] == password:
        st.session_state.authenticated = True
    else:
        st.warning("Mot de passe incorrect.")

if not st.session_state.authenticated:
    st.title(APP_TITLE)
    st.text_input("Veuillez saisir le mot de passe", type="password", key="password_input", on_change=check_password)
    st.stop()

# --- MAIN APP ---
st.title(APP_TITLE)
st.write("Bienvenue dans l'agrégateur de commande intelligent. Pour charger les commandes de l'email par défaut, cliquer directement sur le bouton.")

email_adress = st.text_input("email adress", "default")
email_password = st.text_input("mot de passe", "default")

if st.button("Récupérer les commandes"):

    mailbox_status = True
    if (email_adress != "default") | (email_password != "default"):
        mailbox_status = test_connection("imap.ionos.fr", email_adress, email_password)
        if mailbox_status:
            st.write(" ✅ Connection à la boîte maile réussie")
        else:
            st.write(" ❌ La connection à la boîte maile a échouée. Pour information il est nécessaire d'avoir une boîte hébergée sur un serveur IONOS.fr")
    
    if mailbox_status | (email_adress=="default"):
        df, nb_clients, nb_orders = launch_order_compiler(email_adress="default", email_password="default")
        st.write(f"Durant les 24 dernières heures, des commandes ont été reçues par {nb_clients} client{'s' if nb_clients > 1 else ''}, \
            pour un total de {nb_orders} commande{'s' if nb_orders > 1 else ''}."
            )
        st.dataframe(df, use_container_width=True)

