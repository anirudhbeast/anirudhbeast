from __future__ import annotations

import smtplib
from email.message import EmailMessage
import requests


class AlertNotifier:
    def send_email(
        self,
        smtp_host: str,
        smtp_port: int,
        username: str,
        password: str,
        to_email: str,
        subject: str,
        message: str,
    ) -> None:
        if not all([smtp_host, smtp_port, username, password, to_email]):
            return

        email = EmailMessage()
        email["Subject"] = subject
        email["From"] = username
        email["To"] = to_email
        email.set_content(message)

        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(username, password)
            server.send_message(email)

    def send_telegram(self, bot_token: str, chat_id: str, message: str) -> None:
        if not bot_token or not chat_id:
            return
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        requests.post(url, json={"chat_id": chat_id, "text": message}, timeout=10)
