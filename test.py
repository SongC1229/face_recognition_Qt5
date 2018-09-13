import requests
url = "http://192.168.1.6/pwm.cgi?status=0"
res = requests.get(url)
print(res)
