import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
import os

load_dotenv()
email_sender = os.getenv("EMAIL_SENDER")
email_sender_password = os.getenv("EMAIL_SENDER_PASS")
email_recipient = os.getenv("EMAIL_USER")

def main():
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    email_user = email_sender
    email_password = email_sender_password

    msg = MIMEMultipart()
    msg['from'] = email_user
    msg['to'] = email_recipient
    msg['Subject'] = "Vagas Indeed"
    body = "Vagas da Semana"
    msg.attach(MIMEText(body, "plain"))

    file_path = "vagas_indeed.csv"

    with open(file_path, "rb") as anexo:
        parte = MIMEBase("application", "octet-stream")
        parte.set_payload(anexo.read())

    encoders.encode_base64(parte)
    parte.add_header("Content-Disposition", f"attachment; filename={file_path}")

    msg.attach(parte)

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email_user, email_password)
        server.sendmail(email_user, email_recipient, msg.as_string())
        server.quit()
        print("Email enviado com sucesso")
    except Exception as e:
        print(f"Erro ao enviar email: {e}")

    try: 
        os.remove(file_path)
        print(f"Arquivo '{file_path}' deletado com sucesso")
    except FileNotFoundError: print(f"Arquivo '{file_path}' não encontrado")

if __name__ == "__main__":
    main()