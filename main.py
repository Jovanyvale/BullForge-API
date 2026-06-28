from fastapi import FastAPI
from pydantic import BaseModel
import resend
from random import randint
import os
from dotenv import load_dotenv
from supabase import create_client, Client
from datetime import datetime, timedelta


load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
supabase: Client = create_client(url, key)

app = FastAPI()

resend.api_key = os.environ["RESEND_API_KEY"]

class EmailRequest(BaseModel):
    email: str

@app.post("/send-code")
def send_code(data: EmailRequest):

    expires_at = (datetime.utcnow() + timedelta(minutes=5)).isoformat()

    code = randint(10000, 99999)

    # try:
    #     response = (
    #     supabase.table("verification_codes")
    #     .get({
    #         "email":data.email,
    #         "code":code,
    #         "expires_at":expires_at
    #         })
    #         .execute()
    #     )

    #     print (response)
    # except Exception as e:
    #     print(e)
    #     return (e)




    params: resend.Emails.SendParams = {
    "from": "BullForge <onboarding@resend.dev>",
    "to": [data.email],
    "subject": "Verification code",
        "html": f"""
        <h1>Your verification code</h1>
        <h2>{code}</h2>
        <p>This code expires in 5 minutes.</p>
        """
    }
    email = resend.Emails.send(params)

    print(email)
    return {
        "success": True
    }