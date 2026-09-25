import smtplib
import os
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# Parse arguments from command line
status = sys.argv[1] if len(sys.argv) > 1 else "Unknown"
repository = sys.argv[2] if len(sys.argv) > 2 else "Unknown Repo"
workflow = sys.argv[3] if len(sys.argv) > 3 else "Unknown Workflow"
artifact_url = sys.argv[4] if len(sys.argv) > 4 else "N/A"

# Retrieve secrets from environment
username = os.getenv("EMAIL_USERNAME")
password = os.getenv("EMAIL_PASSWORD")
smtp_server = os.getenv("EMAIL_SMTP_SERVER")
smtp_port = int(os.getenv("EMAIL_SMTP_PORT", 587))
email_to = os.getenv("EMAIL_TO")

msg = MIMEMultipart("alternative")
msg["Subject"] = f"[{status.upper()}] Playwright Test Execution — {repository}"
msg["From"] = username
msg["To"] = email_to

# Formatted HTML Email Body
status_color = "#28a745" if status.lower() == "success" else "#dc3545"

html_body = f"""
<html>
  <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <h2>Playwright CI Execution Summary</h2>
    <table style="border-collapse: collapse; width: 100%; max-width: 600px;">
      <tr>
        <td style="padding: 8px; font-weight: bold; width: 150px;">Status:</td>
        <td style="padding: 8px; color: {status_color}; font-weight: bold;">{status.upper()}</td>
      </tr>
      <tr>
        <td style="padding: 8px; font-weight: bold;">Repository:</td>
        <td style="padding: 8px;">{repository}</td>
      </tr>
      <tr>
        <td style="padding: 8px; font-weight: bold;">Workflow:</td>
        <td style="padding: 8px;">{workflow}</td>
      </tr>
      <tr>
        <td style="padding: 8px; font-weight: bold;">Artifact Download:</td>
        <td style="padding: 8px;"><a href="{artifact_url}">Download Build Artifacts</a></td>
      </tr>
    </table>
    <p style="margin-top: 20px; font-size: 12px; color: #777;">
      Note: See attached <code>report.html</code> for full test breakdown.
    </p>
  </body>
</html>
"""

msg.attach(MIMEText(html_body, "html"))

# FIX 1 & 2: Check correct path ('reports/report.html') and handle missing file safely
report_path = "reports/report.html"

if os.path.exists(report_path):
    with open(report_path, "rb") as f:
        attachment = MIMEApplication(f.read(), _subtype="html")
        attachment.add_header(
            "Content-Disposition", 
            "attachment", 
            filename="report.html"
        )
        msg.attach(attachment)
else:
    print(f"Warning: {report_path} not found. Sending email without attachment.")

# Send email
with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.starttls()
    server.login(username, password)
    server.sendmail(username, email_to, msg.as_string())

print("Email notification sent successfully.")