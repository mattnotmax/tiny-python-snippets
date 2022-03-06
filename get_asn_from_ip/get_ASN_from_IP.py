import urllib.request
import json
ip = '8.8.8.8'
url = ('https://api.iptoasn.com/v1/as/ip/' + ip)
hdr = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)' }
req = urllib.request.Request(url, headers=hdr)
response = urllib.request.urlopen(req)
z = response.read().decode('utf-8')
print(json.loads(z)['as_number'])
