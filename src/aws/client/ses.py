import logging
import os

from botocore.exceptions import ClientError

from src.aws import AWSClient


class SES:
    def __init__(
        self,
        recipient: list,
        subject: str = "This a test subject",
        body_text: str = "This is a test",
        heading: str = "This is a test heading",
    ):
        self.client = AWSClient("ses").client
        self.recipient = recipient
        self.body_text = body_text
        self.subject = subject
        self.heading = heading

    def send_mail(self):
        try:
            response = self.client.send_email(
                Destination={
                    "ToAddresses": self.recipient,
                },
                Message={
                    "Body": {
                        "Html": {
                            "Charset": os.environ["CHARSET"],
                            "Data": self.generate_html_body(),
                        },
                        "Text": {
                            "Charset": os.environ["CHARSET"],
                            "Data": self.body_text,
                        },
                    },
                    "Subject": {
                        "Charset": os.environ["CHARSET"],
                        "Data": self.subject,
                    },
                },
                Source=os.environ["SENDER"],
                # If you are not using a configuration set, comment or delete the
                # following line
                # ConfigurationSetName=CONFIGURATION_SET,
            )
        # Display an error if something goes wrong.
        except ClientError as e:
            logging.error(e.response["Error"]["Message"])
        else:
            message_id = response["MessageId"]
            logging.info(f"Email sent! Message ID: {message_id}")

    def generate_html_body(self):
        return f"""<html>
                <head></head>
                <body>
                  <h1>{self.heading}</h1>
                  <p>This email was sent with
                    <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
                    <a href='https://aws.amazon.com/sdk-for-python/'>
                      AWS SDK for Python (Boto)</a>.</p>
                </body>
                </html>
            """
