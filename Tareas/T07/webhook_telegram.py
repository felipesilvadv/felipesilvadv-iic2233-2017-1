import requests
#TOKEN = '430672963:AAGNYlLy5V-8teMWFaRaYBgpQQadYfkWFoQ'
TOKEN = "418902447:AAGFDOeddEzhActCd_tCsdhT1tztMW4mSSE"
destination = 'https://shielded-oasis-36199.herokuapp.com/turno'
print(requests.post('https://api.telegram.org/bot{}/setWebhook'.format(TOKEN),
                    data={'url':destination}))
print(requests.get('https://api.telegram.org/bot{}/getWebhookInfo'.format(TOKEN)).json())
                    #data={'url':destination}))
