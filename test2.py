import requests

PORT=13801
localhost = "localhost"

res = requests.get('http://'+localhost+':'+str(PORT)+'/fortest')
print(res.text)