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

if __name__ == "__main__":
    app.run(debug=True)
