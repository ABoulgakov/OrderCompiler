def prep_single_client_string(orders_dict, client_name):

    client_recap_str = """
        ******************************************
            """

    for mail in orders_dict[client_name]:
        client_recap_str += "Mail subject: " + mail["subject"]
        client_recap_str += """ 
            """
        client_recap_str += "Time: " + mail["time"]
        client_recap_str += """ 
            """
        client_recap_str += mail["body"]
        client_recap_str += """ 
        ******************************************
            """

    return client_recap_str


def get_single_client_instructions(client_name):
    return f"""
    Je suis exportateur de produits alimentaires et tu travailles pour moi. 
    Ci-dessous se trouvent des emails séparés par des "******************************************". 
    Il s'agit de commandes du client {client_name}. 
    J'ai besoin que tu lises attentivement ces emails et que tu remplisses pour chaque produit commandé une liste python.
    Pour chaque produit, cette liste contient un dictionnaire dont les clés sont "Heure", "Client", "Commande", "Quantité".
    Cette liste servira de récapitulatif des commandes.
    Tu peux corriger les fautes d'orthographe
    Pour la quantité, tu dois préciser l'unité (kg, grammes, caisses, sacs, etc). 
    Ta réponse doit être le contenu de la liste entre crochets, et strictement rien d'autre.
    Si le contenu des mails ne concerne pas des commandes, alors renvoie une liste vide.
    
    """

def get_instructions():
    return """
Je suis exportateur de produits alimentaires et tu travailles pour moi. Ci-dessous se trouvent des emails séparés par des "****" reçus cette nuit. 
Il s'agit de commandes de nos clients. J'ai besoin que tu lises attentivement ces emails et que tu remplisses pour chaque aliment commandé une liste python.
Pour chaque aliment, cette liste contient un dictionnaire dont les clés sont "Heure", "Client", "Commande", "Quantité".
Si un client désire modifie sa commande, alors tu dois modifier le dictionnaire correspondant sa commande initiale.
Pour le contenu de la commande, tu peux corriger les fautes d'orthographe.
Pour la quantité, tu dois préciser l'unité (kg, grammes, caisses, sacs, etc). 
Ta réponse doit être le contenu de la liste entre crochets et strictement rien d'autre.
"""

def get_exceptions():
    return """
Attention:
- quand un client parle d'avocats, il parle généralement de caisses d'avocats
- quand un client parle de côtes de porc, il parle généralement d'une caisse de côtes de porc

"""

def get_test_emails():
    return """
Voici les emails:

****
18:05
Bonjour, 

pour demain, deux avocats, une cote de pocr et 2kg de jambon

Merci, 
Halal Kebab


****
21:33
Hello, 

Please can you send some more porc chops, three please

Cheers, 
Ronald


****
21:34
Bonjour la team OAK, comment allez vous ? 

Pourriez vous nous faire parvenir une caisse d'avocats ainsi que 9kilogrammes de pate à pizza et 10kg de viande hachée de boeuf ? 

Bien à vous, 
Adam Restaurant

****
01:45
FInalement ce sera plutot 7kg de jambon 

Merci, 
Halal Kebab


"""