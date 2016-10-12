from wit import Wit

def send(request, response):
    pass
    #print('Sending to user...', response['text'])

def my_action(request):
    pass
    #print('Recieved from user...', request['text'])

handling = raw_input('What do you want to do?')

actions = {
    'send':send,
    'my_action':my_action,
}

client = Wit(access_token='2G6XUDBNKEWLFPJDLKEMTHEIHOSZG7HA')

resp = client.message(handling)
print('Yay, got Wit.ai response: ' + str(resp))
