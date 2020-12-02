from fastapi import Request
from fastapi_mail import FastMail, MessageSchema

from .storage.schemas.users import UserDB
from .settings import get_settings


async def on_after_register(user: UserDB, 
                            request: Request):

    html = """
    <p>Hi, thanks for registering your account at PersonalFinanceTool!</p>
    """


    message = MessageSchema(
        subject="Welcome to PersonalFinanceTool!",
        recipients=[user.email],
        body=html,
        subtype="html"
    )

    settings = get_settings()
    fm = FastMail(settings)
    await fm.send_message(message)


async def on_after_forgot_password(user: UserDB, 
                                   token: str, 
                                   request: Request):

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

    settings = get_settings()
    fm = FastMail(settings)

    await fm.send_message(message)
