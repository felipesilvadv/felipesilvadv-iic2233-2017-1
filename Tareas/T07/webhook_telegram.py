import requests
TOKEN = '430672963:AAGNYlLy5V-8teMWFaRaYBgpQQadYfkWFoQ'
destination = 'https://shielded-oasis-36199.herokuapp.com/Telegram'
#print(requests.post('https://api.telegram.org/bot{}/setWebhook'.format(TOKEN),
 #                   data={'url':destination}))
print(requests.get('https://api.telegram.org/bot{}/getWebhookInfo'.format(TOKEN)).json())
                    #data={'url':destination}))
