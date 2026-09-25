import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import sys

status = sys.argv[1]
repository = sys.argv[2]
workflow = sys.argv[3]
artifact_url = sys.argv[4]

username = os.getenv("EMAIL_USERNAME")
password = os.getenv("EMAIL_PASSWORD")
smtp_server = os.getenv("EMAIL_SMTP_SERVER")
smtp_port = int(os.getenv("EMAIL_SMTP_PORT"))
email_to = os.getenv("EMAIL_TO")

msg = MIMEMultipart()
msg["Subject"] = f"Playwright CI Report — {status}"
msg["From"] = username
msg["To"] = email_to

body = f"""
Execution Status: {status}
Repository: {repository}
Workflow: {workflow}
Artifact URL: {artifact_url}
"""

msg.attach(MIMEText(body, "plain"))

# Attach HTML report
with open("report.html", "rb") as f:
    attachment = MIMEApplication(f.read(), _subtype="html")
    attachment.add_header("Content-Disposition", "attachment", filename="report.html")
    msg.attach(attachment)

with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.starttls()
    server.login(username, password)
    server.sendmail(username, email_to, msg.as_string())
