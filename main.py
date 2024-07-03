from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import boto3
from dotenv import load_dotenv
import os

load_dotenv()

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")

app = FastAPI()

ses_client = boto3.client(
    'ses', 
    aws_access_key_id=AWS_ACCESS_KEY, 
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY, 
    region_name=AWS_REGION
    )
class EmailContent(BaseModel):
    EmailAddresses: List[str]
    subject: str = "Hello"
    message: str = "Hello this is a test message from AWS SES"

@app.post("/send-email")
async def send_email(email_content: EmailContent):
    try:
        response = ses_client.send_email(
            Source="kvgkrishnamurty@gmail.com",
            Destination={"ToAddresses": email_content.EmailAddresses},
            Message={
                "Subject": {"Data": email_content.subject},
                "Body": {"Text": {"Data": email_content.message}}
            }
        )
        return {"status": "Email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/verify-email")
async def verify_email_addresses(email_content: EmailContent):
    try:
        responses = []
        for email in email_content.EmailAddresses:
            response = ses_client.verify_email_address(EmailAddress=email)
            responses.append(response)
        return {"status": "Email addresses verified successfully", "responses": responses}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))