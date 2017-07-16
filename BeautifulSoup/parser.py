import requests

req = requests.get('https://beomi.github.io/beomi.github.io_old/')

html = req.text
header = req.headers
status = req.status_code
is_ok = req.ok
print(html)
print(header)
print(status)
print(is_ok)