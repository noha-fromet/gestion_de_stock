# connexion à mysql
import mysql.connector
import pandas as pd 
import tkinter as tk
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Laplateforme&13",
    database="boutique"
)

# Creer cursor object
mycursor = conn.cursor()

# creer la table produit si elle n'existe pas
mycursor.execute("""
    CREATE TABLE IF NOT EXISTS produit (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nom VARCHAR(255),
        description TEXT,
        prix INT,
        quantite INT,
        id_categorie INT
    )
""")

# creer la table categorie si elle n'existe pas
mycursor.execute("""
    CREATE TABLE IF NOT EXISTS categorie (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nom VARCHAR(255)
    )
""")

# Insérer des catégories dans la table "categorie"
categories = [('Electronique',), ('Vetements',), ('Alimentation',)]
mycursor.executemany("INSERT INTO categorie (nom) VALUES (%s)", categories)

# Insérer des produits dans la table "produit"
produits = [
    ('Pc', 'Un ordinateur personnel', 1000, 10, 1),
    ('Pantalon', 'Un pantalon en jean', 50, 20, 2),
    ('Fruit', 'Un assortiment de fruits frais', 5, 100, 3)
]
mycursor.executemany("""
    INSERT INTO produit (nom, description, prix, quantite, id_categorie)
    VALUES (%s, %s, %s, %s, %s)
""", produits)

# Valider les modifications dans la base de données
conn.commit()

# Creation de la fenetre
window = tk.Tk()
window.title("Gestion des stocks")
window.geometry("1500x700")

# Creation d'une étiquette et ajoutez à la fenêtre
label = tk.Label(window, text="Bienvenue dans l'application de gestion des stocks!")
label.pack()

def afficher_electronique():
    # Récupérer les produits de la catégorie "Electronique"
    mycursor.execute("""
        SELECT p.*
        FROM produit p
        JOIN categorie c ON p.id_categorie = c.id
        WHERE c.nom = 'Electronique'
    """)
    produits = mycursor.fetchall()

    # Afficher les produits dans l'interface graphique
    for produit in produits:
        label_produit = tk.Label(window, text=str(produit))
        label_produit.pack()

Bouton_elec = tk.Button(window, text="Electronique", width=25, height=10, command=afficher_electronique)
Bouton_elec.pack(anchor="nw")

def afficher_vetements():
    # Récupérer les produits de la catégorie "Vetements"
    mycursor.execute("""
        SELECT p.*
        FROM produit p
        JOIN categorie c ON p.id_categorie = c.id
        WHERE c.nom = 'Vetements'
    """)
    produits = mycursor.fetchall()

    # Afficher les produits dans l'interface graphique
    for produit in produits:
        label_produit = tk.Label(window, text=str(produit))
        label_produit.pack()

Bouton_vet = tk.Button(window, text="Vetements", width=25, height=10, command=afficher_vetements)
Bouton_vet.pack(anchor="n")

def afficher_alimentation():
    # Récupérer les produits de la catégorie "Alimentation"
    mycursor.execute("""
        SELECT p.*
        FROM produit p
        JOIN categorie c ON p.id_categorie = c.id
        WHERE c.nom = 'Alimentation'
    """)
    produits = mycursor.fetchall()

    # Afficher les produits dans l'interface graphique
    for produit in produits:
        label_produit = tk.Label(window, text=str(produit))
        label_produit.pack()

Bouton_alim = tk.Button(window, text="Alimentation", width=25, height=10, command=afficher_alimentation)
Bouton_alim.pack(anchor="ne")

# Fonction pour ajouter un produit
def ajouter_produit():
    # Récupérer les données du formulaire
    nom = entry_nom.get()
    description = entry_description.get()
    prix = entry_prix.get()
    quantite = entry_quantite.get()
    id_categorie = entry_id_categorie.get()

    # Insérer les données dans la table "produit"
    mycursor.execute("""
        INSERT INTO produit (nom, description, prix, quantite, id_categorie)
        VALUES (%s, %s, %s, %s, %s)
    """, (nom, description, prix, quantite, id_categorie))

    # Valider les modifications dans la base de données
    conn.commit()

# Créer un formulaire pour ajouter un produit
label_ajouter = tk.Label(window, text="Ajouter un produit")
label_ajouter.pack()

label_nom = tk.Label(window, text="Nom")
label_nom.pack()
entry_nom = tk.Entry(window)
entry_nom.pack()

label_description = tk.Label(window, text="Description")
label_description.pack()
entry_description = tk.Entry(window)
entry_description.pack()

label_prix = tk.Label(window, text="Prix")
label_prix.pack()
entry_prix = tk.Entry(window)
entry_prix.pack()

label_quantite = tk.Label(window, text="Quantité")
label_quantite.pack()
entry_quantite = tk.Entry(window)
entry_quantite.pack()

label_id_categorie = tk.Label(window, text="ID Catégorie")
label_id_categorie.pack()
entry_id_categorie = tk.Entry(window)
entry_id_categorie.pack()

button_ajouter = tk.Button(window, text="Ajouter", command=ajouter_produit)
button_ajouter.pack()

# Fonction pour supprimer un produit
def supprimer_produit():
    # Récupérer l'ID du produit à supprimer
    id_produit = entry_id_produit.get()

    # Supprimer le produit de la table "produit"
    mycursor.execute("DELETE FROM produit WHERE id = %s", (id_produit,))

    # Valider les modifications dans la base de données
    conn.commit()

# Créer un formulaire pour supprimer un produit
label_supprimer = tk.Label(window, text="Supprimer un produit")
label_supprimer.pack()

label_id_produit = tk.Label(window, text="ID Produit")
label_id_produit.pack()
entry_id_produit = tk.Entry(window)
entry_id_produit.pack()

button_supprimer = tk.Button(window, text="Supprimer", command=supprimer_produit)
button_supprimer.pack()

# Fonction pour modifier un produit
def modifier_produit():
    # Récupérer les données du formulaire
    id_produit = entry_id_produit_modif.get()
    nom = entry_nom_modif.get()
    description = entry_description_modif.get()
    prix = entry_prix_modif.get()
    quantite = entry_quantite_modif.get()
    id_categorie = entry_id_categorie_modif.get()

    # Mettre à jour les données du produit dans la table "produit"
    mycursor.execute("""
        UPDATE produit
        SET nom = %s, description = %s, prix = %s, quantite = %s, id_categorie = %s
        WHERE id = %s
    """, (nom, description, prix, quantite, id_categorie, id_produit))

    # Valider les modifications dans la base de données
    conn.commit()

# Créer un formulaire pour modifier un produit
label_modifier = tk.Label(window, text="Modifier un produit")
label_modifier.pack()

label_id_produit_modif = tk.Label(window, text="ID Produit")
label_id_produit_modif.pack()
entry_id_produit_modif = tk.Entry(window)
entry_id_produit_modif.pack()

label_nom_modif = tk.Label(window, text="Nom")
label_nom_modif.pack()
entry_nom_modif = tk.Entry(window)
entry_nom_modif.pack()

label_description_modif = tk.Label(window, text="Description")
label_description_modif.pack()
entry_description_modif = tk.Entry(window)
entry_description_modif.pack()

label_prix_modif = tk.Label(window, text="Prix")
label_prix_modif.pack()
entry_prix_modif = tk.Entry(window)
entry_prix_modif.pack()

label_quantite_modif = tk.Label(window, text="Quantité")
label_quantite_modif.pack()
entry_quantite_modif = tk.Entry(window)
entry_quantite_modif.pack()

label_id_categorie_modif = tk.Label(window, text="ID Catégorie")
label_id_categorie_modif.pack()
entry_id_categorie_modif = tk.Entry(window)
entry_id_categorie_modif.pack()

button_modifier = tk.Button(window, text="Modifier", command=modifier_produit)
button_modifier.pack()

# Fonction pour filtrer les produits par catégorie
def filtrer_produits():
    # Récupérer la catégorie sélectionnée
    categorie = var_categorie.get()

    # Récupérer les produits de la catégorie sélectionnée
    mycursor.execute("""
        SELECT p.*
        FROM produit p
        JOIN categorie c ON p.id_categorie = c.id
        WHERE c.nom = %s
    """, (categorie,))
    produits = mycursor.fetchall()

    # Afficher les produits dans l'interface graphique
    # ...

# Créer un menu déroulant pour sélectionner une catégorie
label_categorie = tk.Label(window, text="Catégorie")
label_categorie.pack()

var_categorie = tk.StringVar(window)
var_categorie.set("Toutes")

optionmenu_categorie = tk.OptionMenu(window, var_categorie, "Toutes", "Electronique", "Vetements", "Alimentation")
optionmenu_categorie.pack()

button_filtrer = tk.Button(window, text="Filtrer", command=filtrer_produits)
button_filtrer.pack()

# Créer un graphique avec matplotlib
fig = plt.Figure()
ax = fig.add_subplot(111)
ax.plot([1, 2, 3], [1, 2, 3])

# Afficher le graphique dans une fenêtre tkinter
canvas = FigureCanvasTkAgg(fig, master=window)
canvas.draw()
canvas.get_tk_widget().pack()

# Créer un moteur de base de données
engine = create_engine("mysql+mysqlconnector://root:Laplateforme&13@localhost/boutique")

# Lire les données de la base de données dans un DataFrame
df = pd.read_sql("SELECT * FROM produit", engine)


# Exporter les données vers un fichier CSV  
df.to_csv("produits.csv", index=False)



# Executer Tkinter
window.mainloop()

# Fermez le curseur et la connexion
mycursor.close()
conn.close()