from domain.ports.sms_service import SmsService
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import os
from dotenv import load_dotenv

load_dotenv()

class TwilioSmsService(SmsService):
    def __init__(self):
        account_sid = os.getenv("account_sid")
        auth_token = os.getenv("auth_token")
        self.service_sid = os.getenv("auth_token_2")
        
        if not account_sid or not auth_token or not self.service_sid:
            print("AVISO: Credenciais do Twilio não configuradas no .env")
            self.client = None
        else:
            self.client = Client(account_sid, auth_token)
    
    def enviar_verificacao(self, celular):
        if not self.client:
            print("SMS não enviado: Twilio não configurado")
            return
        
        try:
            self.client.verify.v2.services(self.service_sid) \
                .verifications \
                .create(to=celular, channel='sms')
            print(f"SMS de verificação enviado para {celular}")
        except TwilioRestException as e:
            print(f"Erro Twilio ao enviar SMS: {e.msg}")
            raise
        except Exception as e:
            print(f"Erro ao enviar SMS: {e}")
            raise
    
    def verificar_codigo(self, celular, codigo):
        if not self.client:
            print("Verificação não realizada: Twilio não configurado")
            return False
        
        try:
            check = self.client.verify.v2.services(self.service_sid) \
                .verification_checks \
                .create(to=celular, code=codigo)
            return check.status == 'approved'
        except TwilioRestException as e:
            print(f"Erro Twilio ao verificar código: {e.msg}")
            return False
        except Exception as e:
            print(f"Erro ao verificar código: {e}")
            return False
