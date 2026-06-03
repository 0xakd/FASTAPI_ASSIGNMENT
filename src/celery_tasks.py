from celery import Celery
from src.mail import mail, create_message
from asgiref.sync import async_to_sync

c_app = Celery()

c_app.config_from_object("src.config")


@c_app.task()
def send_email(recipients: list[str], subject: str, body: str):
    try:

        # 🔍 DEBUG

        print("TYPE:", type(recipients))

        print("VALUE:", recipients)

        # ✅ Safety fix

        if isinstance(recipients, str):

            recipients = [recipients]

        if not isinstance(recipients, list):

            raise ValueError("Recipients must be a list")

        # ✅ create message

        message = create_message(

            recipients=recipients,

            subject=subject,

            body=body

        )

        # ✅ send mail

        async_to_sync(mail.send_message)(message)

        print("✅ Email sent")

    except Exception as e:

        print("❌ EMAIL ERROR:", e)



    # message = create_message(recipients=recipients, subject=subject, body=body)

    # async_to_sync(mail.send_message)(message)
    # print("Email sent")