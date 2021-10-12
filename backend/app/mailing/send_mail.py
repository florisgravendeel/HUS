from fastapi import (
    FastAPI, 
    BackgroundTasks, 
    UploadFile, File, 
    Form, 
    Query,
    Body,
    Depends
)
from starlette.responses import JSONResponse
from starlette.requests import Request
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from pydantic import EmailStr, BaseModel, Field
from typing import List, Dict, Any
from fastapi_mail.email_utils import DefaultChecker
from pathlib import Path

from variables.init_vars import MAIL_USERNAME, MAIL_PASSWORD, MAIL_FROM, MAIL_PORT, MAIL_SERVER



class EmailSchema(BaseModel):
    email: List[EmailStr]
    body: Dict[str, Any]


conf = ConnectionConfig(
    MAIL_USERNAME = MAIL_USERNAME,
    MAIL_PASSWORD = MAIL_PASSWORD,
    MAIL_FROM = MAIL_FROM,
    MAIL_PORT = MAIL_PORT,
    MAIL_SERVER = MAIL_SERVER,
    MAIL_TLS = True,
    MAIL_SSL = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True,
    TEMPLATE_FOLDER = Path(__file__).parent / 'mail_templates'
)

app = FastAPI()


async def simple_send(email: EmailSchema, subject, content) -> JSONResponse:

    message = MessageSchema(
        subject=subject,
        recipients=email.dict().get("email"),  # List of recipients, as many as you can pass 
        body=content,
        subtype="html"
        )

    fm = FastMail(conf)
    try:
        await fm.send_message(message)
    except Exception as e:
        return {"message": str(e)}
    return True


async def send_in_background(
    background_tasks: BackgroundTasks,
    email: EmailSchema,
    subject, content
    ) -> JSONResponse:

    message = MessageSchema(
        subject=subject,
        recipients=email.dict().get("email"),
        body=content
        )

    fm = FastMail(conf)
    try:
        background_tasks.add_task(fm.send_message,message)
    except Exception as e:
        return {"message": str(e)}
    return True


async def send_with_template(email: EmailSchema) -> JSONResponse:

    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=email.dict().get("email"),  # List of recipients, as many as you can pass 
        template_body=email.dict().get("body"),
        )

    fm = FastMail(conf)
    try:
        await fm.send_message(message, template_name="email_template.html") 
    except Exception as e:
        return {"message": str(e)}
    return True