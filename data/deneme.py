import requests

url = "https://www.cmegroup.com/CmeWS/mvc/Quotes/ContractsByNumber?productIds=7440&contractsNumber=1&venue=G&type=VOLUME&isProtected&_t=1659130775806"

headers={'user-agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.71"}

r = requests.get(url=url,headers=headers)

print(r.request.headers)

data = r.json()

last = data[0]["last"]
change = data[0]["change"]
perChange = data[0]["percentageChange"]
lastUpdate = data[0]["lastUpdated"]
print(last)

