#!/usr/bin/env python3

import os
import re
import sys
from typing import Any

import requests
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

load_dotenv()
TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

app = FastAPI()


class Lead(BaseModel):
    name: str
    contact: str


def telegram(method: str, data: dict[str, Any] | None = None) -> dict[str, Any]:
    url = f"https://api.telegram.org/bot{TOKEN}/{method}"
    response = requests.post(url, json=data or {}, timeout=10)
    response.raise_for_status()
    return response.json()


def valid_contact(value: str) -> bool:
    telegram_username = r"(?:@|(?:https?://)?t\.me/)[a-z][a-z0-9_]{4,31}/?"
    if re.fullmatch(telegram_username, value, re.IGNORECASE):
        return True

    if not re.fullmatch(r"[+\d\s()\-]+", value):
        return False
    digits = re.sub(r"\D", "", value)
    return bool(re.fullmatch(r"(?:[78]\d{10}|\d{10})", digits))


@app.post("/api/lead")
def lead(data: Lead) -> dict[str, bool]:
    name = data.name.strip()
    contact = data.contact.strip()

    if not name or not contact:
        raise HTTPException(400, "Заполните оба поля.")
    if not valid_contact(contact):
        raise HTTPException(400, "Введите телефон или Telegram.")

    telegram(
        "sendMessage",
        {
            "chat_id": CHAT_ID,
            "text": f"Новая заявка с сайта\n\nИмя: {name}\nТелефон или Telegram: {contact}",
        },
    )
    return {"ok": True}


def show_chats() -> None:
    chats = {}
    for update in telegram("getUpdates", {"limit": 100})["result"]:
        message = update.get("message") or update.get("edited_message")
        if message:
            chat = message["chat"]
            chats[chat["id"]] = chat.get("title") or chat.get("first_name", "")

    if not chats:
        print("Чатов пока нет. Добавьте бота в чат и отправьте там /start")
    for chat_id, title in chats.items():
        print(chat_id, title)


if __name__ == "__main__":
    if "--chats" in sys.argv:
        show_chats()
    else:
        uvicorn.run(app, host="127.0.0.1", port=int(os.environ.get("PORT", "8001")))
