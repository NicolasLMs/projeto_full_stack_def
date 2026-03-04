from domain.ports.sms_service import SmsService
from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

class TwilioSmsService(SmsService):
    def __init__(self):
        self.client = Client(os.getenv("account_sid"), os.getenv("auth_token"))
        self.service_sid = os.getenv("auth_token_2")
    
    def enviar_verificacao(self, celular):
        self.client.verify.v2.services(self.service_sid) \
            .verifications \
            .create(to=celular, channel='sms')
    
    def verificar_codigo(self, celular, codigo):
        check = self.client.verify.v2.services(self.service_sid) \
            .verification_checks \
            .create(to=celular, code=codigo)
        return check.status == 'approved'
