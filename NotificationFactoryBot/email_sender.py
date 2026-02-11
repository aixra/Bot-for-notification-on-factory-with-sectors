from __future__ import annotations

import mimetypes
import smtplib
from email.message import EmailMessage

import config


def send_complaint_email(
    request_id: int,
    request_time: str,
    user_name: str,
    sector: str,
    device: str,
    complaint_text: str,
    photo_attachments: list[tuple[str, bytes]],
) -> None:
    if not config.EMAIL_ENABLED:
        return

    message = EmailMessage()
    message["Subject"] = f"Новое обращение №{request_id}"
    message["From"] = config.SMTP_FROM
    message["To"] = config.EMAIL_TO
    message.set_content(
        "\n".join(
            [
                f"Время обращения: {request_time}",
                f"Пользователь: {user_name}",
                f"Участок: {sector}",
                f"Оборудование: {device}",
                f"Текст жалобы: {complaint_text}",
            ]
        )
    )

    for filename, content in photo_attachments:
        mime_type, _ = mimetypes.guess_type(filename)
        maintype, subtype = (mime_type.split("/", 1) if mime_type else ("application", "octet-stream"))
        message.add_attachment(content, maintype=maintype, subtype=subtype, filename=filename)

    with smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT) as smtp:
        if config.SMTP_USE_TLS:
            smtp.starttls()
        if config.SMTP_USERNAME:
            smtp.login(config.SMTP_USERNAME, config.SMTP_PASSWORD)
        smtp.send_message(message)
