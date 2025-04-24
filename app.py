import os
import streamlit as st
from dotenv import load_dotenv
from init import launch_order_compiler

# --- SETTINGS ---
APP_TITLE = "Agrégateur de commandes"

load_dotenv()
password = os.getenv("APP_PASSWORD")

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
st.write("Bienvenue dans l'agrégateur de commande intelligent.")

if st.button("Récupérer les commandes"):
    df, nb_clients, nb_orders = launch_order_compiler()
    st.write(f"Des commandes ont été reçues par {nb_clients} client{'s' if nb_clients > 1 else ''}, \
            pour un total de {nb_orders} commande{'s' if nb_orders > 1 else ''}."
            )
    st.dataframe(df, use_container_width=True)

