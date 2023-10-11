import requests
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Constants
API_CURRENCY_ENDPOINT = "https://api.currencyapi.com/v3/"
API_KEY_CURRENCY = os.environ["API_KEY_CURRENCY"]

# Parameters for currency API
params = {
    "apikey": API_KEY_CURRENCY,
    "base_currency": "DKK",
    "currencies": "PLN,EUR,USD,NOK",
}

# API Requests
currency_api_response = requests.get(API_CURRENCY_ENDPOINT + "latest", params)

# Processing Response
currency_api_response_json = currency_api_response.json()

# Future messages for email
straight_from_api = f"DKK TO PLN {currency_api_response_json['data']['PLN']['value']} \n" \
                    f"DKK to NOK {currency_api_response_json['data']['NOK']['value']} \n" \
                    f"DKK to EUR {currency_api_response_json['data']['EUR']['value']} \n" \
                    f"DKK TO USD {currency_api_response_json['data']['USD']['value']}"

# Future variables to be included in email
pln_to_dkk = 1 / currency_api_response_json['data']['PLN']['value']
eur_to_dkk = 1 / currency_api_response_json['data']['EUR']['value']
usd_to_dkk = 1 / currency_api_response_json['data']['USD']['value']
nok_to_dkk = 1 / currency_api_response_json['data']['NOK']['value']

# Future possible print in email
caluclated_rates = f"- PLN to DKK {pln_to_dkk}\n" \
                   f"- NOK to DKK {nok_to_dkk}\n" \
                   f"- USD to DKK {usd_to_dkk}\n" \
                   f"- EUR to DKK {eur_to_dkk}"

print(f" From API: \n {straight_from_api} \n"
      f" Calculated: \n {caluclated_rates}")

mail_content = f"Hello, \n\n" \
               f"This is a daily currency exchange rates update. \n" \
               f"Here are amount how much 1dkk is worth:\n{caluclated_rates} \n\n" \
               f"Here is how many dkk are in different currencies \n{straight_from_api} \n\n"\
               f"The mail is sent using Python SMTP library. \n" \
               f"Thank You"

subject = "Daily currency update"
body = mail_content
sender = "d.eobsv@gmail.com"
recipients = ["michal.kunkel+eobsv@gmail.com", """place for second recipent in \"...\" """]
password = os.environ["GMAIL_PASSWORD"]

#
msg = MIMEText(body)
msg['Subject'] = subject
msg['From'] = sender
msg['To'] = ', '.join(recipients)
# with smtplib.SMTP('smtp.gmail.com', 567) as smtp_server:
#    smtp_server.login(sender, password)
#    smtp_server.sendmail(sender, recipients, msg.as_string())

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(sender, password)
# msg = MIMEText('send my python', 'plain', 'utf-8')
server.sendmail(sender, 'michal.kunkel+eobsv@gmail.com', msg.as_string())
server.quit()

# with smtplib.SMTP('smtp.gmail.com', 587) as server:
#     server.login(sender, password)
#     msg = MIMEText
print("Message sent!")


# send_email(subject, body, sender, recipients, password)