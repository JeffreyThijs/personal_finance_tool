from fastapi import Request

from .storage.schemas.users import UserDB
from .settings import mail_settings
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig


async def on_after_register(user: UserDB, request: Request):
    
    html = """
    <p>Hi, thanks for registering your account at PersonalFinanceTool!</p> 
    """
    
    message = MessageSchema(
        subject="Welcome to PersonalFinanceTool!",
        recipients=[user.email],
        body=html,
        subtype="html"
    )
    
    fm = FastMail(mail_settings)
    await fm.send_message(message)


async def on_after_forgot_password(user: UserDB, token: str, request: Request):
    
    origin = request.headers.get("Origin", None)
    if not origin:
        return
    
    reset_url = f"{origin}/reset-password?token={token}"
    
    html = f"""
    <p>Hi, reset your password <a href="{reset_url}">here</a>.</p> 
    """
    
    message = MessageSchema(
        subject="Password reset",
        recipients=[user.email],
        body=html,
        subtype="html"
    )
    
    fm = FastMail(mail_settings)
    
    await fm.send_message(message)
