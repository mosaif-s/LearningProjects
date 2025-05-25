from twilio.rest import Client
account_sid = "hidden"
auth_token = "hidden"
class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def sendMessage(self, message):
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            from_="hidden",
            body=message,
            to="hidden"
        )

