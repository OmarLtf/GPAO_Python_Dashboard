
# Importation des bibliothèques nécessaires
import dash
import pandas as pd
from dash import dcc, html
from datetime import date
from dash.dependencies import Input, Output
from datetime import datetime
import time
import threading

# Initialisation du tableau de bord Dash 
app = dash.Dash(__name__)

# # Charger le DataFrame depuis le fichier Excel
# df = pd.read_excel('traceability.xlsx')

# # Convertir la colonne 'date_doperation' en objets de date en spécifiant le format
# df['date_doperation'] = pd.to_datetime(df['date_doperation'], format="%d/%m/%Y")

import mysql.connector
# Spécifiez les informations de connexion
host = '197.13.22.187'  # Remplacez par l'adresse de votre serveur MySQL
database = 'pmi_db'
username = 'admin'
password = 'Admin*01'

# Établissez la connexion à la base de données MySQL
conn = mysql.connector.connect(
    host=host,
    user=username,
    password=password,
    database=database
)
def connect_to_database(host, username, password, database):
    return mysql.connector.connect(
        host=host,
        user=username,
        password=password,
        database=database
    )
# # Créez un curseur pour exécuter des requêtes
# cursor = conn.cursor()

# # Exemple : exécutez une requête SQL pour "traceability"
# cursor.execute('SELECT * FROM traceability')  # Remplacez 'traceability' par le nom de votre table
# time.sleep(1)
# # Récupérez les résultats
# rows = cursor.fetchall()

# # Obtenez le nombre de colonnes dans les données
# num_columns = len(rows[0])

# # Créez un DataFrame à partir des résultats en spécifiant le bon nombre de colonnes
# # Supposons que vous avez 11 colonnes, vous devez spécifier les noms de colonnes pour chaque colonne.
# # Par exemple, colonne_0, colonne_1, colonne_2, ..., colonne_10.
# column_names = ['id', 'of', 'emp', 'lot', 'prepare', 'rebut', 'comment', 'userName', 'table', 'matricule', 'date_doperation']
# df = pd.DataFrame(rows, columns=column_names)

# # Exécutez une requête SQL pour obtenir les données de "production" en utilisant des backticks autour de "of"
# cursor.execute('SELECT `of`, `produit` FROM production')
# production_data = cursor.fetchall()

# # Créez un DataFrame pour "production" avec les colonnes "of" et "produit"
# production_columns = ['of', 'produit']
# df_production = pd.DataFrame(production_data, columns=production_columns)

# # Effectuez une fusion (join) entre les DataFrames "df" et "df_production" en utilisant la colonne "of" comme clé de liaison
# df = df.merge(df_production, on='of', how='left')



# # Fermez le curseur et la connexion
# cursor.close()
# conn.close()

# # Maintenant, le DataFrame "df" contient les données de "traceability" avec la colonne "produit" ajoutée.

# # Vous pouvez imprimer "df" ou effectuer d'autres opérations avec les données.

# df['prepare'] = df['prepare'].astype(int)
# df['rebut'] = df['rebut'].astype(int)
# # Convertir la colonne "date_doperation" en format date
# df['date_doperation'] = pd.to_datetime(df['date_doperation'], format='%d/%m/%Y', errors='coerce')

# print(df)


# def callback_on_database_change(host, username, password, database):
#     conn = connect_to_database(host, username, password, database)
#     cursor = conn.cursor()

#     cursor.execute('SELECT * FROM traceability')
#     time.sleep(1)
#     rows = cursor.fetchall()

#     num_columns = len(rows[0])
#     column_names = ['id', 'of', 'emp', 'lot', 'prepare', 'rebut', 'comment', 'userName', 'table', 'matricule', 'date_doperation']
#     df = pd.DataFrame(rows, columns=column_names)

#     cursor.execute('SELECT `of`, `produit` FROM production')
#     production_data = cursor.fetchall()

#     production_columns = ['of', 'produit']
#     df_production = pd.DataFrame(production_data, columns=production_columns)

#     df = df.merge(df_production, on='of', how='left')

#     cursor.close()
#     conn.close()

#     df['prepare'] = df['prepare'].astype(int)
#     df['rebut'] = df['rebut'].astype(int)
#     df['date_doperation'] = pd.to_datetime(df['date_doperation'], format='%d/%m/%Y', errors='coerce')

#     return df

# df = callback_on_database_change(host, username, password, database)

# def update_dataframe_periodically(host, username, password, database, interval=1):
#     global df
#     while True:
#         df = callback_on_database_change(host, username, password, database)
#         print(df)  # or do any other operations with the updated DataFrame
#         time.sleep(interval)


def connect_to_database(host, username, password, database):
    try:
        conn = mysql.connector.connect(
            host=host,
            user=username,
            password=password,
            database=database
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to the database: {err}")
        raise

def callback_on_database_change(host, username, password, database):
    try:
        conn = connect_to_database(host, username, password, database)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM traceability')
        time.sleep(1)
        rows = cursor.fetchall()

        num_columns = len(rows[0])
        column_names = ['id', 'of', 'emp', 'lot', 'prepare', 'rebut', 'comment', 'userName', 'table', 'matricule', 'date_doperation']
        df = pd.DataFrame(rows, columns=column_names)

        cursor.execute('SELECT `of`, `produit` FROM production')
        production_data = cursor.fetchall()

        production_columns = ['of', 'produit']
        df_production = pd.DataFrame(production_data, columns=production_columns)

        df = df.merge(df_production, on='of', how='left')

        df['prepare'] = df['prepare'].astype(int)
        df['rebut'] = df['rebut'].astype(int)
        df['date_doperation'] = pd.to_datetime(df['date_doperation'], format='%d/%m/%Y', errors='coerce')

        return df

    except mysql.connector.Error as err:
        print(f"Error executing query: {err}")
        raise

    finally:
        cursor.close()
        conn.close()


df = callback_on_database_change(host, username, password, database)
def update_dataframe_periodically(host, username, password, database, interval=1):
    global df
    while True:
        try:
            df = callback_on_database_change(host, username, password, database)
            print("##########################################################################################################")
            print(datetime.now())
            print(df)  # or do any other operations with the updated DataFrame

        except Exception as e:
            print(f"Error updating DataFrame: {e}")

        time.sleep(interval)

# Start the update_dataframe_thread in the background
update_dataframe_thread = threading.Thread(target=update_dataframe_periodically, args=(host, username, password, database))
update_dataframe_thread.start()



#************************************************************************************************************************************************************************************
# Données initiales
produit = "Alternateur"
produit_change_time = 200  # Temps en secondes avant de changer de produit

# Callback pour changer le produit toutes les 10 secondes
@app.callback(Output('kpi-title', 'children'), Input('interval-component', 'n_intervals'))
def update_kpi_title(n):
    global produit
    produit = update_produit(n)
    return f"KPI De Production Pm industries : {produit}"

# Définition de la fonction update_produit
def update_produit(n):
    global produit, produit_change_time

    if produit_change_time <= 0:
        if produit == "Alternateur":
            produit = "Démarreur"
        elif produit == "Démarreur":
            produit = "Etrier"
        else:
            produit = "Alternateur"
        produit_change_time = 200  # Réinitialiser le compteur de temps
    else:
        produit_change_time -= 1

    return produit

# Callback pour mettre à jour les sorties
@app.callback(
    Output('demontage-output', 'children'),
    Output('sous_ens-output', 'children'),
    Output('montage-output', 'children'),
    Output('rebut-output', 'children'),
    Output('taux-output', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_outputs(n):
    global produit
    produit = update_produit(n)
    today = date.today().strftime('%Y-%m-%d')

    table_demontage = 'TABLE DE DÉMONTAGE'
    table_sous_ens = 'TABLE DE S-ENSEMBLE'
    table_montage = 'TABLE DE MONTAGE'

    # Filtrer les données en fonction de la valeur actuelle de "produit"
    filtered_data_demontage = df[(df['date_doperation'] == today) & (df['table'] == table_demontage) & (df['produit'] == produit)]
    filtered_data_sous_ens = df[(df['date_doperation'] == today) & (df['table'] == table_sous_ens) & (df['produit'] == produit)]
    filtered_data_montage = df[(df['date_doperation'] == today) & (df['table'] == table_montage) & (df['produit'] == produit)]

    somme_quantite_preparee_demontage = filtered_data_demontage['prepare'].sum()
    somme_quantite_preparee_sous_ens = filtered_data_sous_ens['prepare'].sum()
    somme_quantite_preparee_montage = filtered_data_montage['prepare'].sum()
    somme_quantite_preparee_sous_ens_rebut = filtered_data_sous_ens['rebut'].sum()
    somme_quantite_preparee_montage_rebut = filtered_data_montage['rebut'].sum()

    if somme_quantite_preparee_sous_ens == 0:
        somme_quantite_rebut = 0
    else:
        somme_quantite_rebut = round(((somme_quantite_preparee_sous_ens_rebut + somme_quantite_preparee_montage_rebut) / somme_quantite_preparee_sous_ens) * 100, 2)


    taux = taux_de_rendement(produit, somme_quantite_preparee_montage)

    return f"{somme_quantite_preparee_demontage}", \
           f"{somme_quantite_preparee_sous_ens}", \
           f"{somme_quantite_preparee_montage}", \
           f"{somme_quantite_rebut}%", \
           f"{taux}%"

def taux_de_rendement(produit, somme_quantite_preparee_montage):
    heure_debut = datetime(datetime.now().year, datetime.now().month, datetime.now().day, 8, 0, 0)
    heure_actuelle = datetime.now()
    duree_totale_disponible = (heure_actuelle - heure_debut).total_seconds() / 60
    if somme_quantite_preparee_montage == 0 :
        taux = 0 
    elif produit == "Alternateur":
        nombre_total_unites = 180
        taux = round((somme_quantite_preparee_montage) / ((nombre_total_unites / (60 * 8)) * duree_totale_disponible) * 100,1)
    elif produit == "Demarreur":
        nombre_total_unites = 180
        taux = round((somme_quantite_preparee_montage) / ((nombre_total_unites / (60 * 8)) * duree_totale_disponible) * 100,1)
    else:
        nombre_total_unites = 150
        taux = round((somme_quantite_preparee_montage) / ((nombre_total_unites / (60 * 8)) * duree_totale_disponible) * 100,1)

    return taux

 # Renvoyer la valeur de taux 
#Clacule pour les étiquettes ALT *******************************************************************************************************************************************
# Calculer la somme de la quantité préparée de montage Alt
table_de_montage_alt = 'TABLE DE MONTAGE'  # Assurez-vous que le nom correspond exactement à votre jeu de données
produit_alternateur = 'Alternateur'  # Assurez-vous que le nom du produit correspond exactement à votre jeu de données

filtered_data_montage_alt = df[(df['table'] == table_de_montage_alt) & (df['produit'] == produit_alternateur)]
somme_quantite_preparee_montage_alt = filtered_data_montage_alt['prepare'].sum()

# Calculer la somme de la quantité préparée de démontage Alt
table_de_demontage_alt = 'TABLE DE DÉMONTAGE'  # Assurez-vous que le nom correspond exactement à votre jeu de données

filtered_data_demontage_alt = df[(df['table'] == table_de_demontage_alt) & (df['produit'] == produit_alternateur)]
somme_quantite_preparee_demontage_alt = filtered_data_demontage_alt['prepare'].sum()

# Calculer la somme de la quantité préparée de Sous_Ensemble Alt
table_de_sous_ens_alt = 'TABLE DE S-ENSEMBLE'  # Assurez-vous que le nom correspond exactement à votre jeu de données

filtered_data_sous_ens_alt = df[(df['table'] == table_de_sous_ens_alt) & (df['produit'] == produit_alternateur)]
somme_quantite_preparee_sous_ens_alt = filtered_data_sous_ens_alt['prepare'].sum()

# Calculer la somme de la quantité rebut de Sous_Ensemble Alt
table_de_sous_ens_alt_rebut = 'TABLE DE S-ENSEMBLE'  # Assurez-vous que le nom correspond exactement à votre jeu de données

filtered_data_sous_ens_alt_rebut = df[(df['table'] == table_de_sous_ens_alt_rebut) & (df['produit'] == produit_alternateur)]
somme_quantite_preparee_sous_ens_alt_rebut = filtered_data_sous_ens_alt_rebut['rebut'].sum()

# Calculer la somme de la quantité rebut de montage Alt
table_de_montage_alt_rebut = 'TABLE DE MONTAGE'  # Assurez-vous que le nom correspond exactement à votre jeu de données

filtered_data_montage_alt_rebut = df[(df['table'] == table_de_montage_alt_rebut) & (df['produit'] == produit_alternateur)]
somme_quantite_preparee_montage_alt_rebut = filtered_data_montage_alt_rebut['rebut'].sum()

# Calcul de la quantité bloquée pour le produit Alternateur
produit_alternateur = 'Alternateur'  # Assurez-vous que le nom du produit correspond exactement à votre jeu de données

filtered_data_bloc_alt = df[(df['produit'] == produit_alternateur) & (df['table'] == 'TABLE DE BLOQCAGE')]
somme_quantite_preparee_bloc_alt = filtered_data_bloc_alt['prepare'].sum()


# Calcul de la quantité préparée pour le produit Alternateur dans la table TABLE DE SOUS-TRAITANTS
produit_alternateur = 'Alternateur'  # Assurez-vous que le nom du produit correspond exactement à votre jeu de données
table_de_sous_traitant_alt = 'TABLE DE SOUS-TRAITANTS'  # Assurez-vous que le nom de la table correspond exactement à votre jeu de données

filtered_data_sous_traitant_alt = df[(df['produit'] == produit_alternateur) & (df['table'] == table_de_sous_traitant_alt)]
somme_quantite_preparee_sous_traitant_alt = filtered_data_sous_traitant_alt['prepare'].sum()


# Calculer l'encours brut Alt
encours_brut_alt = (somme_quantite_preparee_demontage_alt)- (somme_quantite_preparee_montage_alt) - (somme_quantite_preparee_montage_alt_rebut) - (somme_quantite_preparee_sous_ens_alt_rebut)

# Calculer l'encours net Alt
encours_net_alt = encours_brut_alt - somme_quantite_preparee_bloc_alt - somme_quantite_preparee_sous_traitant_alt 

#Calculer Att sous_ensemble alt
att_sous_ens_alt = somme_quantite_preparee_demontage_alt-somme_quantite_preparee_sous_ens_alt - somme_quantite_preparee_sous_ens_alt_rebut

#Calculer Att Montage Alt

att_montage_alt = somme_quantite_preparee_sous_ens_alt - somme_quantite_preparee_montage_alt-somme_quantite_preparee_montage_alt_rebut

#Clacule pour les étiquettes Dém
# Calculer la somme de la quantité préparée de montage Dém
table_de_montage_dem = 'TABLE DE MONTAGE'  # Assurez-vous que le nom correspond exactement à votre jeu de données
produit_demarreur = 'Démarreur'  # Assurez-vous que le nom du produit correspond exactement à votre jeu de données

filtered_data_montage_dem = df[(df['table'] == table_de_montage_dem) & (df['produit'] == produit_demarreur)]
somme_quantite_preparee_montage_dem = filtered_data_montage_dem['prepare'].sum()

# Calculer la somme de la quantité préparée de démontage dem
table_de_demontage_dem = 'TABLE DE DÉMONTAGE'  # Assurez-vous que le nom correspond exactement à votre jeu de données

filtered_data_demontage_dem = df[(df['table'] == table_de_demontage_dem) & (df['produit'] == produit_demarreur)]
somme_quantite_preparee_demontage_dem = filtered_data_demontage_dem['prepare'].sum()

# Calculer la somme de la quantité préparée de Sous_Ensemble dem
table_de_sous_ens_dem = 'TABLE DE S-ENSEMBLE'  # Assurez-vous que le nom correspond exactement à votre jeu de données

filtered_data_sous_ens_dem = df[(df['table'] == table_de_sous_ens_dem) & (df['produit'] == produit_demarreur)]
somme_quantite_preparee_sous_ens_dem = filtered_data_sous_ens_dem['prepare'].sum()

# Calculer la somme de la quantité rebut de Sous_Ensemble dem
table_de_sous_ens_dem_rebut = 'TABLE DE S-ENSEMBLE'  # Assurez-vous que le nom correspond exactement à votre jeu de données

filtered_data_sous_ens_dem_rebut = df[(df['table'] == table_de_sous_ens_dem_rebut) & (df['produit'] == produit_demarreur)]
somme_quantite_preparee_sous_ens_dem_rebut = filtered_data_sous_ens_dem_rebut['rebut'].sum()

# Calculer la somme de la quantité rebut de montage dem
table_de_montage_dem_dem_rebut = 'TABLE DE MONTAGE'  # Assurez-vous que le nom correspond exactement à votre jeu de données

filtered_data_montage_dem_rebut = df[(df['table'] == table_de_montage_dem_dem_rebut) & (df['produit'] == produit_demarreur)]
somme_quantite_preparee_montage_dem_rebut = filtered_data_montage_dem_rebut['rebut'].sum()

# Calcul de la quantité bloquée pour le produit dem
produit_demarreur = 'Démarreur'  # Assurez-vous que le nom du produit correspond exactement à votre jeu de données

filtered_data_bloc_dem = df[(df['produit'] == produit_demarreur) & (df['table'] == 'TABLE DE BLOQCAGE')]
somme_quantite_preparee_bloc_dem = filtered_data_bloc_dem['prepare'].sum()


# Calcul de la quantité préparée pour le produit demarreur dans la table TABLE DE SOUS-TRAITANTS
produit_demarreur = 'Démarreur'  # Assurez-vous que le nom du produit correspond exactement à votre jeu de données
table_de_sous_traitant_dem = 'TABLE DE SOUS-TRAITANTS'  # Assurez-vous que le nom de la table correspond exactement à votre jeu de données

filtered_data_sous_traitant_dem = df[(df['produit'] == produit_demarreur) & (df['table'] == table_de_sous_traitant_dem)]
somme_quantite_preparee_sous_traitant_dem = filtered_data_sous_traitant_dem['prepare'].sum()


# Calculer l'encours brut dem
encours_brut_dem = ( somme_quantite_preparee_demontage_dem)-(somme_quantite_preparee_montage_dem)-(somme_quantite_preparee_sous_ens_dem_rebut)-(somme_quantite_preparee_montage_dem_rebut)

# Calculer l'encours net dem
encours_net_dem = encours_brut_dem - (somme_quantite_preparee_bloc_dem) - (somme_quantite_preparee_sous_traitant_dem)

#Calculer Att sous_ensemble dem
att_sous_ens_dem = (somme_quantite_preparee_demontage_dem) - (somme_quantite_preparee_sous_ens_dem) - (somme_quantite_preparee_sous_ens_dem_rebut)

#Calculer Att Montage dem

att_montage_dem = (somme_quantite_preparee_sous_ens_dem) - (somme_quantite_preparee_montage_dem)-(somme_quantite_preparee_montage_dem_rebut)

#Clacule pour les étiquettes ETRIER
# Calculer la somme de la quantité préparée de montage Dém
table_de_montage_ef = 'TABLE DE MONTAGE'  # Assurez-vous que le nom correspond exactement à votre jeu de données
produit_ef = 'Etrier'  # Assurez-vous que le nom du produit correspond exactement à votre jeu de données

filtered_data_montage_ef = df[(df['table'] == table_de_montage_ef) & (df['produit'] == produit_ef)]
somme_quantite_preparee_montage_ef = filtered_data_montage_ef['prepare'].sum()

# Calculer la somme de la quantité préparée de démontage ef
table_de_demontage_ef = 'TABLE DE DÉMONTAGE'  # Assurez-vous que le nom correspond exactement à votre jeu de données

filtered_data_demontage_ef = df[(df['table'] == table_de_demontage_ef) & (df['produit'] == produit_ef)]
somme_quantite_preparee_demontage_ef = filtered_data_demontage_ef['prepare'].sum()

# Calculer la somme de la quantité préparée de Sous_Ensemble ef
table_de_sous_ens_ef = 'TABLE DE S-ENSEMBLE'  # Assurez-vous que le nom correspond exactement à votre jeu de données

filtered_data_sous_ens_ef = df[(df['table'] == table_de_sous_ens_ef) & (df['produit'] == produit_ef)]
somme_quantite_preparee_sous_ens_ef = filtered_data_sous_ens_ef['prepare'].sum()

# Calculer la somme de la quantité rebut de Sous_Ensemble ef
table_de_sous_ens_ef_rebut = 'TABLE DE S-ENSEMBLE'  # Assurez-vous que le nom correspond exactement à votre jeu de données

filtered_data_sous_ens_ef_rebut = df[(df['table'] == table_de_sous_ens_ef_rebut) & (df['produit'] == produit_ef)]
somme_quantite_preparee_sous_ens_ef_rebut = filtered_data_sous_ens_ef_rebut['rebut'].sum()

# Calculer la somme de la quantité rebut de montage ef
table_de_montage_dem_ef_rebut = 'TABLE DE MONTAGE'  # Assurez-vous que le nom correspond exactement à votre jeu de données

filtered_data_montage_ef_rebut = df[(df['table'] == table_de_montage_dem_ef_rebut) & (df['produit'] == produit_ef)]
somme_quantite_preparee_montage_ef_rebut = filtered_data_montage_ef_rebut['rebut'].sum()

# Calcul de la quantité bloquée pour le produit ef
produit_ef = 'Etrier'  # Assurez-vous que le nom du produit correspond exactement à votre jeu de données

filtered_data_bloc_ef = df[(df['produit'] == produit_ef) & (df['table'] == 'TABLE DE BLOQCAGE')]
somme_quantite_preparee_bloc_ef = filtered_data_bloc_ef['prepare'].sum()


# Calcul de la quantité préparée pour le produit ef dans la table TABLE DE SOUS-TRAITANTS
produit_ef = 'Etrier'  # Assurez-vous que le nom du produit correspond exactement à votre jeu de données
table_de_sous_traitant_ef = 'TABLE DE SOUS-TRAITANTS'  # Assurez-vous que le nom de la table correspond exactement à votre jeu de données

filtered_data_sous_traitant_ef = df[(df['produit'] == produit_ef) & (df['table'] == table_de_sous_traitant_ef)]
somme_quantite_preparee_sous_traitant_ef = filtered_data_sous_traitant_ef['prepare'].sum()


# Calculer l'encours brut dem
encours_brut_ef = (somme_quantite_preparee_demontage_ef )-(somme_quantite_preparee_montage_ef )-(somme_quantite_preparee_montage_ef_rebut)-(somme_quantite_preparee_sous_ens_ef_rebut)

# Calculer l'encours net dem
encours_net_ef = (encours_brut_ef)-(somme_quantite_preparee_bloc_ef)-(somme_quantite_preparee_sous_traitant_ef)

#Calculer Att sous_ensemble dem
att_sous_ens_ef = (somme_quantite_preparee_demontage_ef)-(somme_quantite_preparee_sous_ens_ef)-(somme_quantite_preparee_sous_ens_ef_rebut)

#Calculer Att Montage dem

att_montage_ef = (somme_quantite_preparee_sous_ens_ef)-(somme_quantite_preparee_montage_ef)-(somme_quantite_preparee_montage_ef_rebut)


# Callback pour mettre à jour l'heure actuelle
@app.callback(
    Output('heure_actuelle', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_heure_actuelle(n):
    heure_actuelle2 = datetime.now().strftime('%H:%M:%S')  # Obtenez l'heure actuelle
    return f'{heure_actuelle2}'


# Étiquettes en dessous du tableau de bord (verticalement à gauche)
etiquettes_col1 = html.Div(style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'flex-start', 'width': '33.33%', 'margin-left': '20px', 'margin-top': '20px'}, children=[
    html.Div(style={'width': '50px'}),  # Ajouter un espace vide
    html.Div(style={'padding': '10px', 'width': '380px'},className='colonne2', children=[
        html.Div("Atelier Alternateurs", style={'font-size': '24px','font-weight': '600','letter-spacing':'3px', 'color': '#fff'}),
    ]),
    html.Br(),
    html.Div(f"1- Encours Brut : {encours_brut_alt}", style={ 'padding': '10px', 'border-radius': '15px', 'font-size': '24px', 'color': '#EDEBD7', 'width': '380px', 'margin-bottom':'10px'},className='colonne'),
    html.Div(f"2- Encours Net : {encours_net_alt}", style={ 'padding': '10px', 'border-radius': '15px', 'font-size': '24px', 'color': '#EDEBD7', 'width': '380px', 'margin-bottom':'10px'},className='colonne'),
    html.Div(f"3- Attente Sous-Ens : {att_sous_ens_alt}", style={ 'padding': '10px', 'border-radius': '15px', 'font-size': '24px', 'color': '#EDEBD7', 'width': '380px', 'margin-bottom':'10px'},className='colonne'),
    html.Div(f"4- Attente Montage : {att_montage_alt}", style={ 'padding': '10px', 'border-radius': '15px', 'font-size': '24px', 'color': '#EDEBD7', 'width': '380px', 'margin-bottom':'10px'},className='colonne'),
    html.Div(f"5- Bloquage : {somme_quantite_preparee_bloc_alt}", style={'padding': '10px','font-size': '24px', 'color': '#ffefca', 'width': '380px', 'margin-bottom':'10px'},className='colonne'),
    html.Div(f"6- Sous-Traitant : {somme_quantite_preparee_sous_traitant_alt}", style={'padding': '10px', 'font-size': '24px', 'width': '380px'},className='colonne'),
])


etiquettes_col2 = html.Div(style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'flex-start', 'width': '33.33%', 'margin-right': 'auto','margin-left': '30px', 'margin-top': '20px'}, children=[
    html.Div(style={'width': '50px'}),  # Ajouter un espace vide
    html.Div(style={ 'padding': '10px', 'width': '380px'},className='colonne2', children=[
        html.Div("Atelier Démarreurs", style={'font-size': '24px','font-weight': '600','letter-spacing':'3px', 'color': '#fff'}),
    ]),
    html.Br(),
    html.Div(f"1- Encours Brut : {encours_brut_dem}", style={ 'padding': '10px','font-size': '24px', 'width': '380px', 'margin-bottom':'10px'}, className='colonne'),
    html.Div(f"2- Encours Net : {encours_net_dem}", style={'padding': '10px','font-size': '24px','width': '380px', 'margin-bottom':'10px'},className='colonne'),
    html.Div(f"3- Attente Sous-Ens : {att_sous_ens_dem}", style={ 'padding': '10px','font-size': '24px', 'width': '380px', 'margin-bottom':'10px'}, className='colonne'),
    html.Div(f"4- Attente Montage : {att_montage_dem}", style={ 'padding': '10px','font-size': '24px', 'width': '380px', 'margin-bottom':'10px'}, className='colonne'),
    html.Div(f"5- Bloquage : {somme_quantite_preparee_bloc_dem}", style={'padding': '10px','font-size': '24px', 'color': '#ffefca', 'width': '380px', 'margin-bottom':'10px'}, className='colonne'),
    html.Div(f"6- Sous-Traitant : {somme_quantite_preparee_sous_traitant_dem}", style={'padding': '10px','font-size': '24px','width': '380px'}, className='colonne'),
])

etiquettes_col3 = html.Div(style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'flex-start', 'width': '33.33%', 'margin-right': 'auto','margin-left': '30px', 'margin-top': '20px'}, children=[
    html.Div(style={'width': '50px'}),  # Ajouter un espace vide
    html.Div(style={'padding': '10px', 'width': '380px'},className='colonne2', children=[
        html.Div("Atelier Etriers De Frein", style={'font-size': '24px','font-weight': '600','letter-spacing':'3px','color': '#fff', 'width': '380px'}),
    ]),
    html.Br(),
    html.Div(f"1- Encours Brut : {encours_brut_ef}", style={'padding': '10px','font-size': '24px', 'width': '380px', 'margin-bottom':'10px'}, className='colonne'),
    html.Div(f"2- Encours Net : {encours_net_ef}", style={'padding': '10px','font-size': '24px', 'width': '380px', 'margin-bottom':'10px'}, className='colonne'),
    html.Div(f"3- Attente Sous-Ens : {att_sous_ens_ef}", style={'padding': '10px','font-size': '24px','width': '380px', 'margin-bottom':'10px'},className='colonne'),
    html.Div(f"4- Attente Montage : {att_montage_ef}", style={ 'padding': '10px','font-size': '24px', 'width': '380px', 'margin-bottom':'10px'}, className='colonne'),
    html.Div(f"5- Bloquage : {somme_quantite_preparee_bloc_ef}", style={'padding': '10px','font-size': '24px', 'color': '#ffefca', 'width': '380px', 'margin-bottom':'10px'}, className='colonne'),
    html.Div(f"6- Sous-Traitant : {somme_quantite_preparee_sous_traitant_ef}", style={ 'padding': '10px','font-size': '24px','width': '380px'},className='colonne'),

])

# Créez une mise en page de base
app.layout = html.Div([
    html.H1(id='kpi-title', children=f"KPI De Production Pm industries : {produit}"),
    html.Div(id='output-container'),
    html.Div(id='demontage-output'),
    html.Div(id='sous_ens-output'),
    html.Div(id='montage-output'),
    html.Div(id='rebut-output'),
    html.Div(id='taux-output'),
    dcc.Interval(
        id='interval-component',
        interval=0.1*1000,  # in milliseconds
        n_intervals=0
    )
])

app.layout = html.Div([
    # Afficher l'heure actuelle sans libellé
    html.Div([
        dcc.Interval(
            id='interval-component',
            interval=0.1 * 1000,  # en millisecondes
            n_intervals=0
        ),
        html.Div(id='output-container'),
    ]),

    
    dcc.Interval(id='interval-component-2', interval=0.1 * 1000, n_intervals=0),  # Utilisez un autre nom pour cet interval
    html.Div([
        html.Img(src='assets/clock.png', alt='image', className='clock'),
        html.H2("Heure Actuelle", id='heure_actuelle', className='date')
    ], className='custom-div-class'),

    html.H1(id='kpi-title', className='titre'),

    html.Hr(className='line'),

    # Conteneur pour les étiquettes disposées horizontalement
    html.Div(style={'display': 'flex'}, children=[
        html.Div(style={'width': '20px'}),  # Ajouter un espace vide
        html.Div([
            html.H1("Démontage", style={'text-align': 'center', 'font-size': '20px', 'color': '#FFD700', 'margin-bottom': '15px'}),
            html.H1(id='demontage-output', style={'text-align': 'center', 'font-size': '40px', 'color': 'white'}),
        ],
        className='card'
        ),
        html.Div(style={'width': '20px'}),  # Ajouter un espace vide
        html.Div([
            html.H1("Sous-Ensemble", style={'text-align': 'center', 'font-size': '20px', 'color': '#FFD700', 'margin-bottom': '15px'}),
            html.H1(id='sous_ens-output', style={'text-align': 'center', 'font-size': '40px', 'color': 'white'}),
        ],
        className='card'
        ),
        html.Div(style={'width': '20px'}),  # Ajouter un espace vide
        html.Div([
            html.H1("Montage", style={'text-align': 'center', 'font-size': '20px', 'color': '#FFD700', 'margin-bottom': '15px'}),
            html.H1(id='montage-output', style={'text-align': 'center', 'font-size': '40px', 'color': 'white'}),
        ],
        className='card'
        ),
        html.Div(style={'width': '20px'}),  # Ajouter un espace vide
        html.Div([
            html.H1("Taux De Rebut", style={'text-align': 'center', 'font-size': '20px', 'color': '#FFD700', 'margin-bottom': '15px'}),
            html.H1(id='rebut-output', style={'text-align': 'center', 'font-size': '40px', 'color': 'white'}),
        ],
        className='card'
        ),
        html.Div(style={'width': '20px'}),  # Ajouter un espace vide
        html.Div([
            html.H1("Takt Time", style={'text-align': 'center', 'font-size': '20px', 'color': '#FFD700', 'margin-bottom': '15px'}),
            html.H1(id='taux-output', style={'text-align': 'center', 'font-size': '40px', 'color': 'white'}),
        ],
        className='card'
        ),
        html.Div(style={'width': '20px'}),  # Ajouter un espace vide
        html.Div([
            html.H1("Cout", style={'text-align': 'center', 'font-size': '20px', 'color': '#FFD700', 'margin-bottom': '15px'}),
            html.H1("★★★★★", style={'text-align': 'center', 'font-size': '40px', 'color': '#FFD700'}),
        ],
        className='card'
        ),
        html.Div(style={'width': '20px'}),
    ]),
    # Placer les étiquettes en colonnes côte à côte
    html.Div(style={'display': 'flex', 'justify-content': 'center'}, children=[etiquettes_col1, etiquettes_col2, etiquettes_col3]),
    # Placer les étiquettes en colonnes côte à côte

    html.Div(style={'display': 'flex', 'justify-content': 'center'}, children=[
        html.Div(style={'width': '33.33%'}),  # Ajouter un espace vide pour la colonne 1
        html.Div(style={'width': '30%'}),  # Ajouter un espace entre les colonnes 1 et 2
        html.Div(style={'width': '33.33%'}),  # Ajouter un espace vide pour la colonne 2
        html.Div(style={'width': '30%'}),  # Ajouter un espace entre les colonnes 2 et 3
        html.Div(style={'width': '33.33%'}),  # Ajouter un espace vide pour la colonne 3
    ]),
    html.Div([
        html.I("Copyright © 2023 Crafted By Production Sce (B.Y)"),
    ], className='copyr')
])

if __name__ == '__main__':
    app.run_server(debug=True)

