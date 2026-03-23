import os
import re
import random
from dotenv import load_dotenv
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

load_dotenv()


class TwilioSmsService:

    def __init__(self):

        self.account_sid = os.getenv("account_sid")
        self.auth_token = os.getenv("auth_token")
        self.template_sid = os.getenv("auth_token_3")

        if not all([self.account_sid, self.auth_token, self.template_sid]):
            raise ValueError("Credenciais Twilio não configuradas")

        self.client = Client(self.account_sid, self.auth_token)

        self.codigos = {}

    def limpar_numero(self, celular: str):

        apenas_numeros = re.sub(r"\D", "", celular)

        if not apenas_numeros.startswith("55"):
            apenas_numeros = "55" + apenas_numeros

        return f"+{apenas_numeros}"

    def enviar_verificacao(self, celular: str):

        numero = self.limpar_numero(celular)

        codigo = random.randint(100000, 999999)

        try:

            message = self.client.messages.create(
                from_="whatsapp:+14155238886",
                to=f"whatsapp:{numero}",
                content_sid=self.template_sid,
                content_variables=f'{{"1": "{codigo}"}}'
            )

            self.codigos[numero] = codigo

            print(f"Código enviado para {numero}")
            return message.sid

        except TwilioRestException as e:

            print(f"Erro Twilio: {e.msg}")
            raise

    def verificar_codigo(self, celular: str, codigo: str):

        numero = self.limpar_numero(celular)

        codigo_salvo = self.codigos.get(numero)

        if not codigo_salvo:
            print("Nenhum código enviado")
            return False

        if str(codigo_salvo) == str(codigo):

            print("Código válido")
            del self.codigos[numero]
            return True

        print("Código incorreto")
        return False