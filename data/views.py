import asyncio
from pyppeteer import launch
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup

def getValues(link):
    USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
    LANGUAGE = 'en-US,en;q=0.5'
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    html = session.get(link).text
    return html
# Create your views here.

def exchange(request):
    amount = request.GET.get('amount')
    if amount:
        html = getValues('https://bigpara.hurriyet.com.tr/altin/altin-ons-fiyati/')
        soup = BeautifulSoup(html,'html.parser')
        ons = soup.find_all('span','value up')[0].text
        ons = ons.replace('.','')
        ons = ons.replace(',','.')
        html = getValues('https://bigpara.hurriyet.com.tr/doviz/dolar/')
        soup = BeautifulSoup(html,'html.parser')
        dollar = soup.find_all('span','value up')[0].text
        dollar = dollar.replace(',','.')
        liras = (float(ons)/31.10)*float(dollar)*float(amount)
        return render(request,'exchange.html',{'liras':liras,'amount':amount})

    return render(request,'exchange.html')

def index(request):
    if request.method == "POST":
        if "getAluminiumTables" in request.POST:
            labels = []
            prices = []
            data = []
            html = getValues('https://www.westmetall.com/en/markdaten.php?action=table&field=LME_Al_cash')
            soup = BeautifulSoup(html,'html.parser')
            table_div = soup.find('div' , {'class': 'section'})
            table_body = table_div.find('tbody')
            rows = table_body.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                data.append([ele for ele in cols if ele])
            i = 0
            data = [x for x in data if x]
            for one_data in data:
                one_data = data[i][0]
                labels.append(one_data)
                i += 1
            i = 0
            for one_data in data:
                one_data = data[i][3]
                one_data = one_data.replace(',','.')
                prices.append(one_data)
                i += 1      
            return render(request,'index.html',{'labels':labels[:30],'prices':prices[:30]})

        if "getCompareTables" in request.POST:
            html = getValues('https://metalavm.com/aluminyum')
            soup = BeautifulSoup(html,'html.parser')
            div = soup.find('div' , {'class': 'product-grid no-padding no-margin'})
            metalAvmprices = div.find_all('span','price-new')
            metalAvmlabels = div.find_all('div','name')
            metalAvmprices = [x.text for x in metalAvmprices]
            metalAvmprices = [x.replace(',','.') for x in metalAvmprices]
            metalAvmprices = [x.replace("\xa0/kg","") for x in metalAvmprices]
            metalAvmlabels = [x.text for x in metalAvmlabels]
            metalAvmlabels = metalAvmlabels[:4]

            html = getValues('https://www.metalreyonu.com.tr/urunler/aluminyum-cubuk')
            soup = BeautifulSoup(html,'html.parser')
            div = soup.find('ul' , {'class': 'anaurunlistesi'})
            metalReyprices = div.find_all('span',id='fiyatid')
            metalReylabels = div.find_all('h5','anauruntitle')
            metalReyprices = [x.text for x in metalReyprices]
            metalReyprices = [x.replace(',','.') for x in metalReyprices]
            metalReyprices = [x.replace(" TL/kg","") for x in metalReyprices]
            metalReylabels = [x.text for x in metalReylabels]

            metalReylabel = []
            metalReyprice = []
            i = 0
            for label in metalReylabels:
                i += 1
                if " 8 mm" in label or " 6 mm" in label or " 10 mm" in label or " 12 mm" in label:
                    metalReylabel.append(label)
                    metalReyprice.append(metalReyprices[i])
            return render(request,'index.html',{'metalAvmlabels':metalAvmlabels,'metalAvmprices':metalAvmprices,"metalReylabels":metalReylabel,"metalReyprices":metalReyprice})

        if "getFuture" in request.POST:
            url = "https://www.cmegroup.com/CmeWS/mvc/Quotes/ContractsByNumber?productIds=7440&contractsNumber=1&venue=G&type=VOLUME&isProtected&_t=1659130775806"
            headers={'user-agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.71"}
            r = requests.get(url=url,headers=headers)
            data = r.json()
            last = data[0]["last"]
            change = data[0]["change"]
            perChange = data[0]["percentageChange"]
            lastUpdate = data[0]["lastUpdated"]
            lastUpdate = lastUpdate.replace("T"," ")
            print(lastUpdate)
            return render(request,"index.html",{"last":last,"change":change,"perChange":perChange,"lastUpdate":lastUpdate})


    return render(request,"index.html")
