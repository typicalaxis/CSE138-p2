import requests

localhost = "localhost" # Docker Toolbox users should use Docker's ip address here
port = 13801
url = 'http://{}:{}/kvs'.format(localhost, port)
url2 = 'http://{}:{}/fortest'.format(localhost, port)

respsonse = requests.get(url, json={'key': "testkey", 'val': "testval"})
print(respsonse.text)

respsonse = requests.get(url2)
print(respsonse.text)
