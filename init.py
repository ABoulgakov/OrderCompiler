import os
from dotenv import load_dotenv
import pandas as pd

from connectors.mailbox import *
from connectors.gpt import call_gpt
from manager.queries import *
from manager.emails import *

def launch_order_compiler():

  print("***** 🚨 Début de la tâche 🚨 *****")

  # Get environment variables
  load_dotenv()
  gpt_key = os.getenv("OPENAI_API_KEY")
  imap_server = os.getenv("IMAP_SERVER")
  email_adress = os.getenv("EMAIL_USER")
  email_password = os.getenv("EMAIL_PASS")

  # Access mailbox content
  print("*** Récupération des emails ***")
  fetch_emails(imap_server, email_adress, email_password)

  # Email preprocessing
  print("*** Préparation des emails ***")
  orders_dict = prep_orders_json()
  print(f"Nombre d'expéditeurs trouvés: {len(orders_dict)}")

  # Feed emails to chat GPT client by client and store orders as dictionnaries in a single list variable
  print("*** Lancement des requêtes à l'IA ***")
  all_orders_list = []

  for client in orders_dict.keys():
    query = get_single_client_instructions(client) + get_exceptions() + prep_single_client_string(orders_dict, client)
    client_orders_list = call_gpt(gpt_key, query)
    print(f"✅ Emails du client {client} traités: {len(client_orders_list)} commandes")
    all_orders_list.extend(client_orders_list or [])

  # Turn orders list to dataframe and display it
  print("*** 📦 Récapitulatif des commandes reçues ***")
  all_orders_df = pd.DataFrame(all_orders_list)
  all_orders_df.index += 1
  print(all_orders_df)
  nb_clients = all_orders_df["Client"].nunique()
  nb_orders = len(all_orders_df)

  return all_orders_df, nb_clients, nb_orders

if __name__=="__main__":
  launch_order_compiler()

  # checker température pour réduire l'entropie.. possible sur gpt 4o mini ? 
  # selectionner des mails sur une période donnée  ? 



