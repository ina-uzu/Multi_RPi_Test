import requests
import time
import random

URL = 'http://dd966332.ngrok.io/api/data/'

while True:
    DEVICE_ID = random.randrange(1,10)
    do_val = random.randrange(0,20)
    ph_val = random.randrange(0,7)
    dco2_val = random.randrange(0,5000)
    brix_val =[random.randrange(0,40),format(random.random() + 1, '.2f')]

    data = {'device_id':DEVICE_ID , 'do':do_val, 'ph':ph_val, 'dco2':dco2_val, 'brix_temp':brix_val[0], 'brix_brix':brix_val[1]}
    reponse = requests.post(URL, data = data)
    time.sleep(10)