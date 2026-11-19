import os
import smtplib
from email.message import EmailMessage

from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")
@app.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name")
    sender_email = request.form.get("email")
    subject = request.form.get("subject")
    message = request.form.get("message")

    email = EmailMessage()
    email["Subject"] = f"Portfolio Contact: {subject}"
    email["From"] = os.getenv("MAIL_DEFAULT_SENDER")
    email["To"] = os.getenv("MAIL_USERNAME")
    email["Reply-To"] = sender_email

    email.set_content(
        f"""
        New message from your portfolio!

        Name: {name}
        Email: {sender_email}
        Subject: {subject}

        Message:
        {message}
        """
    )

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(
                os.getenv("MAIL_USERNAME"),
                os.getenv("MAIL_PASSWORD")
            )
            server.send_message(email)

        return render_template("success.html")

    except Exception:
        return "Sorry, your message could not be sent. Please try again."


if __name__ == "__main__":
    app.run(debug=True)