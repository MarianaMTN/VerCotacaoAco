import smtplib
import pytz
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os
import pandas as pd 

def send_email(sender_email, sender_password, recipient_email, subject, body, file_path=None, reply_to_email=None):
    """
    Envia um email com um anexo opcional via SMTP do Gmail.

    Args:
        sender_email (str): O email do remetente (ex: seu.email@gmail.com).
        sender_password (str): A Senha de Aplicativo do Gmail.
        recipient_email (str): O email do destinatário.
        subject (str): O assunto do email.
        body (str): O corpo do email (pode ser HTML).
        file_path (str, optional): O caminho para o arquivo de anexo. Defaults to None.
        reply_to_email (str, optional): O email para onde a resposta deve ser enviada. Defaults to None.

    Returns:
        str: Mensagem de sucesso com data e hora do envio, ou levanta uma exceção em caso de falha.
    """

    # 1. Construção da Mensagem
    message = MIMEMultipart()        
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject
    
    # Adiciona o cabeçalho Reply-To para que a resposta vá para o usuário final
    if reply_to_email:
        message['Reply-To'] = reply_to_email
    
    # Corpo do Email (Texto/HTML)
    html_part = MIMEText(body, 'html')
    message.attach(html_part)
    
    # Anexo (Imagem) - Opcional
    if file_path:
        try:
            # Para anexos de imagem (PNG, JPG, JPEG)
            with open(file_path, 'rb') as f:
                image_part = MIMEImage(f.read())
            message.attach(image_part)
        except FileNotFoundError:
            raise FileNotFoundError(f"Arquivo de anexo não encontrado: {file_path}")
        except Exception as e:
            raise Exception(f"Erro ao anexar arquivo: {e}")


    # 2. Envio via SMTP
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
            
            # Geração da mensagem de sucesso
            datetime_br = datetime.now(pytz.timezone('America/Sao_Paulo'))                
            msgRESP = f'Enviado para: {recipient_email} em: {datetime_br.strftime("%d/%m/%Y %H:%M:%S")}'
            return msgRESP
    except smtplib.SMTPAuthenticationError as e:
        # Captura a exceção de autenticação e levanta uma exceção genérica com a mensagem clara.
        raise Exception(f"Falha na autenticação: {e}. Verifique o email e a Senha de Aplicativo do Gmail (use uma Senha de Aplicativo, não a senha normal).")
    except Exception as e:
        # Captura qualquer outro erro de envio.
        raise Exception(f"Erro ao enviar email: {e}")

# Função IsNiver original (mantida para compatibilidade)
def IsNiver(data):
  from datetime import datetime
  c = datetime.now()
  try:
    df = pd.to_datetime(data, format='%m/%d/%Y')
  except ValueError:
    df = pd.to_datetime(data)
    
  d = pd.to_datetime(c,format='%Y-%m-%d')
  if df.month == d.month and df.day == d.day:
    return True
  else:
    return False
