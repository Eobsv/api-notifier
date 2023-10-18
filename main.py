""" Script gives anybody an email with interesting data. For now there is only data regarding currency exchange rate
I created an .exe file which can be exectued only by me due to necessity to pass confidential data for script to work."""

import requests
import os
import smtplib
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
straight_from_api = f" - 1DKK is {currency_api_response_json['data']['PLN']['value']}PLN \n" \
                    f" - 1DKK is {currency_api_response_json['data']['NOK']['value']}NOK \n" \
                    f" - 1DKK is {currency_api_response_json['data']['EUR']['value']}USD \n" \
                    f" - 1DKK is {currency_api_response_json['data']['USD']['value']}EUR"

# Future variables to be included in email
pln_to_dkk = 1 / currency_api_response_json['data']['PLN']['value']
eur_to_dkk = 1 / currency_api_response_json['data']['EUR']['value']
usd_to_dkk = 1 / currency_api_response_json['data']['USD']['value']
nok_to_dkk = 1 / currency_api_response_json['data']['NOK']['value']

# Future possible print in email
calculated_rates = f"- 1PLN can be bought for {pln_to_dkk}DKK \n" \
                   f"- 1NOK can be bought for {nok_to_dkk}DKK \n" \
                   f"- 1USD can be bought for {usd_to_dkk}DKK \n" \
                   f"- 1EUR can be bought for {eur_to_dkk}DKK "

print(f" From API: \n{straight_from_api} \n"
      f" Calculated: \n{calculated_rates}")

mail_content = f"Hello, \n\n" \
               f"This is a daily currency exchange rates update. \n" \
               f"Here are amount how much 1dkk is worth:\n{straight_from_api} \n\n" \
               f"Here is how much dkk it is necessary to buy one of each currency \n{calculated_rates} \n\n"\
               f"The mail is sent using Python SMTP library. \n" \
               f"Thank You"

subject = "Daily currency update"
body = mail_content
sender = os.environ["SENDER"]
recipients = os.environ["RECIPIENTS"]
password = os.environ["GMAIL_PASSWORD"]


msg = MIMEText(body)
msg['Subject'] = subject
msg['From'] = sender
msg['To'] = recipients

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(sender, password)
server.sendmail(sender, recipients, msg.as_string())
server.quit()


# send_email(subject, body, sender, recipients, password)