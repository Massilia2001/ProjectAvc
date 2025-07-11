# Importation des bibliothèques nécessaires
from flask import Flask, render_template, request, send_file, flash, redirect, url_for
import psycopg2
import pandas as pd
from io import BytesIO
from fpdf import FPDF
from datetime import datetime
import joblib
import numpy as np

# Initialisation de l'application Flask
app = Flask(__name__)
app.secret_key = 'ton_secret_key'

# Configuration de la base PostgreSQL
DB_CONFIG = {
    'dbname': 'stroke_db',
    'user': 'postgres',
    'password': 'root',
    'host': 'localhost',
    'port': '5432'
}

# Fonction pour se connecter à la base de données
def connect_db():
    return psycopg2.connect(**DB_CONFIG)

# Fonction pour récupérer les patients filtrés
def get_filtered_patients(genre=None, work=None, age_range=None, residence=None):
    conn = connect_db()
    cur = conn.cursor()

    query = """
        SELECT id, gender, age, hypertension, heart_disease, work_type, residence_type, stroke
        FROM patients WHERE stroke = TRUE
    """
    filters = []
    values = []

    if genre:
        filters.append("gender = %s")
        values.append(genre)
    if work:
        filters.append("work_type = %s")
        values.append(work)
    if age_range and "-" in age_range:
        min_age, max_age = age_range.split("-")
        filters.append("age BETWEEN %s AND %s")
        values.extend([min_age, max_age])
    if residence:
        filters.append("residence_type = %s")
        values.append(residence)

    if filters:
        query += " AND " + " AND ".join(filters)

    query += " ORDER BY id"
    cur.execute(query, tuple(values))
    data = cur.fetchall()
    conn.close()
    return data

# Fonction pour récupérer les patients en DataFrame (pour export)
def get_patients_df(genre=None, work=None, age_range=None, residence=None):
    conn = connect_db()

    query = """
        SELECT id AS "ID", gender AS "Genre", age AS "Âge",
               hypertension AS "Hypertension", heart_disease AS "Cardiaque",
               work_type AS "Travail", residence_type AS "Résidence", stroke AS "AVC"
        FROM patients WHERE stroke = TRUE
    """
    filters = []
    values = []

    if genre:
        filters.append("gender = %s")
        values.append(genre)
    if work:
        filters.append("work_type = %s")
        values.append(work)
    if age_range and "-" in age_range:
        min_age, max_age = age_range.split("-")
        filters.append("age BETWEEN %s AND %s")
        values.extend([min_age, max_age])
    if residence:
        filters.append("residence_type = %s")
        values.append(residence)

    if filters:
        query += " AND " + " AND ".join(filters)

    query += " ORDER BY id"
    df = pd.read_sql(query, conn, params=values)
    conn.close()
    return df

# Page d'accueil
@app.route("/")
def index():
    patients = get_filtered_patients()
    return render_template("index.html", patients=patients, total=len(patients),
                           genre=None, work=None, age_range=None, residence=None)

# Route pour filtrer
@app.route("/filter")
def filter_patients():
    genre = request.args.get("genre")
    work = request.args.get("work")
    age_range = request.args.get("age_range")
    residence = request.args.get("residence")

    patients = get_filtered_patients(genre, work, age_range, residence)
    return render_template("index.html", patients=patients, total=len(patients),
                           genre=genre, work=work, age_range=age_range, residence=residence)

# Export CSV
@app.route("/export")
def export_csv():
    genre = request.args.get("genre")
    work = request.args.get("work")
    age_range = request.args.get("age_range")
    residence = request.args.get("residence")

    df = get_patients_df(genre, work, age_range, residence)
    csv_io = BytesIO()
    df.to_csv(csv_io, index=False, encoding='utf-8')
    csv_io.seek(0)

    filename = f"patients_avc_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    return send_file(csv_io, as_attachment=True, download_name=filename, mimetype='text/csv')

# Export PDF
@app.route("/export_pdf")
def export_pdf():
    genre = request.args.get("genre")
    work = request.args.get("work")
    age_range = request.args.get("age_range")
    residence = request.args.get("residence")

    df = get_patients_df(genre, work, age_range, residence)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Liste des patients AVC filtrés", ln=True, align='C')
    pdf.set_font("Arial", size=10)

    col_width = 190 / len(df.columns)
    for col in df.columns:
        pdf.cell(col_width, 10, txt=col, border=1)
    pdf.ln()

    for _, row in df.iterrows():
        for item in row:
            pdf.cell(col_width, 10, txt=str(item), border=1)
        pdf.ln()

    output = BytesIO()
    pdf.output(output)
    output.seek(0)

    filename = f"patients_avc_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    return send_file(output, download_name=filename, as_attachment=True)

# Ajouter un patient
@app.route("/add", methods=["GET", "POST"])
def add_patient():
    if request.method == "POST":
        gender = request.form.get("gender")
        age = request.form.get("age")
        hypertension = request.form.get("hypertension") == "oui"
        heart_disease = request.form.get("heart_disease") == "oui"
        work_type = request.form.get("work_type")
        residence_type = request.form.get("residence_type")
        stroke = request.form.get("stroke") == "oui"

        if not gender or not age or not work_type or not residence_type:
            flash("Veuillez remplir tous les champs obligatoires.", "warning")
            return redirect(url_for('add_patient'))

        try:
            age_int = int(age)
        except ValueError:
            flash("L'âge doit être un nombre entier.", "warning")
            return redirect(url_for('add_patient'))

        try:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO patients (gender, age, hypertension, heart_disease, work_type, residence_type, stroke)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (gender, age_int, hypertension, heart_disease, work_type, residence_type, stroke))
            conn.commit()
            conn.close()
            flash("Patient ajouté avec succès !", "success")
            return redirect(url_for('index'))
        except Exception as e:
            flash(f"Erreur lors de l'ajout du patient : {e}", "danger")
            return redirect(url_for('add_patient'))

    return render_template("add_patient.html")

# Modifier un patient
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_patient(id):
    conn = connect_db()
    cur = conn.cursor()

    if request.method == "POST":
        gender = request.form.get("gender")
        age = request.form.get("age")
        hypertension = request.form.get("hypertension") == "oui"
        heart_disease = request.form.get("heart_disease") == "oui"
        work_type = request.form.get("work_type")
        residence_type = request.form.get("residence")
        stroke = request.form.get("stroke") == "oui"

        try:
            cur.execute("""
                UPDATE patients
                SET gender = %s, age = %s, hypertension = %s,
                    heart_disease = %s, work_type = %s,
                    residence_type = %s, stroke = %s
                WHERE id = %s
            """, (gender, age, hypertension, heart_disease, work_type, residence_type, stroke, id))
            conn.commit()
            flash("Patient mis à jour avec succès.", "success")
            return redirect(url_for('index'))
        except Exception as e:
            flash(f"Erreur lors de la mise à jour : {e}", "danger")
            return redirect(url_for('edit_patient', id=id))

    cur.execute("SELECT id, gender, age, hypertension, heart_disease, work_type, residence_type, stroke FROM patients WHERE id = %s", (id,))
    patient = cur.fetchone()
    conn.close()

    if not patient:
        flash("Patient introuvable.", "danger")
        return redirect(url_for('index'))

    return render_template("edit_patient.html", patient=patient)

# Supprimer un patient
@app.route("/delete/<int:id>", methods=["POST"])
def delete_patient(id):
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM patients WHERE id = %s", (id,))
        conn.commit()
        conn.close()
        flash("Patient supprimé avec succès.", "success")
    except Exception as e:
        flash(f"Erreur lors de la suppression : {e}", "danger")
    return redirect(url_for("index"))

# Chargement du modèle
model = joblib.load("model.pkl")
expected_columns = joblib.load("model_columns.pkl")

@app.route("/predict", methods=["GET", "POST"])
def predict_avc():
    if request.method == "POST":
        try:
            age = float(request.form.get("age"))
            avg_glucose_level = float(request.form.get("avg_glucose_level"))
            bmi = float(request.form.get("bmi"))
            hypertension = 1 if request.form.get("hypertension") == "oui" else 0
            heart_disease = 1 if request.form.get("heart_disease") == "oui" else 0
            gender = (request.form.get("gender") or "").lower()
            work_type = (request.form.get("work_type") or "").lower()
            residence_type = (request.form.get("residence") or "").lower()
            ever_married = (request.form.get("ever_married") or "").lower()
            smoking_status = (request.form.get("smoking_status") or "").lower()

            input_dict = {
                "gender": gender,
                "age": age,
                "hypertension": hypertension,
                "heart_disease": heart_disease,
                "ever_married": ever_married,
                "work_type": work_type,
                "residence_type": residence_type,
                "avg_glucose_level": avg_glucose_level,
                "bmi": bmi,
                "smoking_status": smoking_status
            }
            input_df = pd.DataFrame([input_dict])
            input_df = pd.get_dummies(input_df)

            for col in expected_columns:
                if col not in input_df.columns:
                    input_df[col] = 0

            input_df = input_df[expected_columns]

            prediction = model.predict(input_df)[0]
            prob = model.predict_proba(input_df)[0][1] * 100

            message = f"Résultat : {'AVC probable' if prediction == 1 else 'Risque faible'} (probabilité : {prob:.2f}%)"
            flash(message, "success")
        except Exception as e:
            flash(f"Erreur lors de la prédiction : {e}", "danger")
            return redirect(url_for("predict_avc"))

    return render_template("predict.html")

if __name__ == "__main__":
    app.run(debug=True)
