from flask import Flask, render_template, request, flash, redirect, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Remplacez par une clé secrète pour utiliser flash messages

# Route pour la page d'accueil
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/agence')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/services')
def service():
    return render_template('service.html')

@app.route('/sendmail', methods=['POST'])
def send_mail():
    name = request.form.get('name')
    user_email = request.form.get('email')
    subject = request.form.get('subject')
    message = request.form.get('message')

    # Validation des données
    if not all([name, user_email, subject, message]):
        flash('Please fill out all fields.', 'error')
        return redirect('/contact')

    try:
        send_email(name, user_email, subject, message)
        flash('Message sent successfully!', 'success')
        return redirect('/contact')
    except Exception as e:
        flash(f'An error occurred: {e}', 'error')
        return redirect('/contact')

def send_email(name, user_email, subject, message):
    sender_email = user_email  # L'email saisi par l'utilisateur
    receiver_email = "contact@equilibre.media"  # Adresse du destinataire
    smtp_username = "henry.gossou17@gmail.com"  # Adresse e-mail utilisée pour l'authentification SMTP
    smtp_password = "nxbi bsyk nvfo ipgm"  # Mot de passe de l'email d'authentification

    # Créer l'objet du message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = f"Nouveau message de {name}: {subject}"

    # Contenu du message
    body = f"Vous avez reçu un nouveau message via votre site web:\n\nNom: {name}\nEmail: {user_email}\nObjet: {subject}\n\nMessage:\n{message}"
    msg.attach(MIMEText(body, 'plain'))

    # Connexion au serveur SMTP et envoi de l'email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Activer la sécurité (TLS)
            server.login(smtp_username, smtp_password)  # Se connecter avec les informations d'authentification
            text = msg.as_string()
            server.sendmail(sender_email, receiver_email, text)  # Envoyer l'email
        print(f"Email envoyé de {sender_email} à {receiver_email}")
    except smtplib.SMTPException as e:
        print(f"Erreur lors de l'envoi de l'email: {e}")
        raise

if __name__ == '__main__':
    app.run(debug=True)
