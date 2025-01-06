from flask import Flask, render_template, request
import sqlite3

# Initialisation de Flask
app = Flask(__name__)

# Fonction pour effectuer la recherche dans la base de données
def rechercher_matricule(matricule):
    conn = sqlite3.connect('entretien24.db')
    cursor = conn.cursor()

    # Recherche dans la table MATRICE
    cursor.execute("SELECT * FROM MATRICE WHERE matricule = ?", (matricule,))
    matrice_result = cursor.fetchone()

    # Recherche dans VIDANGE24
    cursor.execute("SELECT * FROM VIDANGE24 WHERE matricule = ?", (matricule,))
    vidange_result = cursor.fetchall()

    # Recherche dans ENTRETIEN_CURATIF
    cursor.execute("SELECT * FROM ENTRETIEN_CURATIF WHERE matricule = ?", (matricule,))
    entretien_result = cursor.fetchall()

    conn.close()

    return matrice_result, vidange_result, entretien_result

# Route principale
@app.route("/", methods=["GET", "POST"])
def index():
    matrice_result = None
    vidange_result = None
    entretien_result = None

    if request.method == "POST":
        matricule = request.form.get("matricule")  # Récupérer le matricule du formulaire

        if matricule:
            matrice_result, vidange_result, entretien_result = rechercher_matricule(matricule)
        else:
            return render_template("index.html", error="Veuillez entrer un matricule.")

    return render_template("index.html", matrice_result=matrice_result,
                           vidange_result=vidange_result, entretien_result=entretien_result)
# Route pour afficher la table MATRICE
@app.route("/matrice")
def afficher_matrice():
    conn = sqlite3.connect('entretien24.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM MATRICE")
    matrice_donnees = cursor.fetchall()
    conn.close()
    return render_template("matrice.html", donnees=matrice_donnees)

# Route pour afficher la table VIDANGE24
@app.route("/vidange24")
def afficher_vidange24():
    conn = sqlite3.connect('entretien24.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM VIDANGE24")
    vidange_donnees = cursor.fetchall()
    conn.close()
    return render_template("vidange24.html", donnees=vidange_donnees)

# Route pour afficher la table ENTRETIEN_CURATIF
@app.route("/entretien_curatif")
def afficher_entretien_curatif():
    conn = sqlite3.connect('entretien24.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ENTRETIEN_CURATIF")
    entretien_donnees = cursor.fetchall()
    conn.close()
    return render_template("entretien_curatif.html", donnees=entretien_donnees)

if __name__ == "__main__":
    app.run(debug=True)
