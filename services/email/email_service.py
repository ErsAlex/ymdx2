

from pydantic import BaseModel
from fastapi.exceptions import HTTPException
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from .settings import OWN_EMAIL, OWN_EMAIL_PASSWORD , SMTP_SSL_ADRESS, SMTP_PORT



class EmailBody(BaseModel):
    to: str
    subject: str
    message: str
    
    
async def send_email(body: EmailBody):
    try:
        msg = MIMEText(body.message, "html")
        msg['Subject'] = body.subject
        msg['From'] = f'<{OWN_EMAIL}>'
        msg['To'] = body.to

        port = 465


        server = SMTP_SSL(SMTP_SSL_ADRESS, SMTP_PORT)
        server.login(OWN_EMAIL, OWN_EMAIL_PASSWORD)

        server.send_message(msg)
        server.quit()
        return "Success"

    except Exception as e:
        raise HTTPException(status_code=500, detail=e)