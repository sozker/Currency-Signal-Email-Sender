import pandas as pd
import numpy as np
import datetime
import time
from binance.client import Client
from binance.enums import *
import smtplib
import math
import requests
import quandl

#e-mail info
from_address = "sertac.sinyal@gmail.com"
to_address = ["sozker@yahoo.com","hasmir99@hotmail.com","ogansid@hotmail.com","ilkeruyguner@gmail.com","batughan.aydin@gmail.com","guwengul@gmail.com","alpernt1@gmail.com","garabetik@yahoo.com"]


#parameters
margin_kripto_alt = 0.02
margin_kripto_ust = 0.005

margin_doviz = 0.005
margin_parite = 0.002

margin_gold = 0.002

sinyal_arasi_sure = 8*60*60 #8 hours - the period it will wait for sending a signal for the same currency
bekleme_suresi = 3*60 #3 minutes - the period it will wait between each search 

#binance connection
api_key = "u1biOGsY1ss8SH9TGwcwWgEPYR389AmleBqhwNIWz7qqMrb4dpFBfzhkn7IyOcpW"
api_secret = "GKlP514wK71yLrP9PL2kcCTGh75DoxyRtI1tKOx4RVzTRdFvmgfoFvbJZoGVyr9s"
client = Client(api_key, api_secret, {"timeout": 1000})

#just initial data for dataframe
sinyal = pd.DataFrame({'kur':['BTCUSDT'],'zaman':[datetime.datetime.now()]})
sutun = ('time','open','highest','lowest','close','volume','time_end','volume_usd','number_of_trades','open_order_volume','open_order_volume_usd','e')


i = 1

while i>0:
    
    try:

        print(str(datetime.datetime.now()) + " initialized")
        
########################################### CRYPTOCURRENCIES ###########################################

        tickers = pd.DataFrame(client.get_ticker())
        tickers['conv'] = tickers['symbol'].str[-3:]
        tickers['quoteVolume'] = tickers.quoteVolume.astype(float)
        kripto_kurlar = tickers[tickers['conv']=='BTC'].nlargest(50,'quoteVolume')['symbol'].tolist()
        kripto_kurlar.append('BTCUSDT')

        for kur in kripto_kurlar:

            son_sinyalden_gecen_sure = (datetime.datetime.now() - sinyal[sinyal['kur']==kur]['zaman'].max()).seconds

            if math.isnan(son_sinyalden_gecen_sure):
                son_sinyalden_gecen_sure = 1000000
            else: x=0
            
            if son_sinyalden_gecen_sure > sinyal_arasi_sure:

                klines = client.get_historical_klines(kur, Client.KLINE_INTERVAL_1DAY,  "360 days ago UTC")
                df = pd.DataFrame(klines,columns=sutun)
                df['close'] = df.close.astype(float)
                df['highest'] = df.close.astype(float)
                df['lowest'] = df.close.astype(float)

                index_sinir= df.index.max()

                son_fiyat = df[df.index==index_sinir]['close'].min()

                #min prices
                min_1_ay = df[df.index>=(index_sinir-30)]['lowest'].min() * (1+margin_kripto_alt)
                min_2_ay = df[df.index>=(index_sinir-60)]['lowest'].min() * (1+margin_kripto_alt)
                min_3_ay = df[df.index>=(index_sinir-90)]['lowest'].min() * (1+margin_kripto_alt)
                min_4_ay = df[df.index>=(index_sinir-120)]['lowest'].min() * (1+margin_kripto_alt)
                min_5_ay = df[df.index>=(index_sinir-150)]['lowest'].min() * (1+margin_kripto_alt)
                min_6_ay = df[df.index>=(index_sinir-180)]['lowest'].min() * (1+margin_kripto_alt)
                min_7_ay = df[df.index>=(index_sinir-210)]['lowest'].min() * (1+margin_kripto_alt)
                min_8_ay = df[df.index>=(index_sinir-240)]['lowest'].min() * (1+margin_kripto_alt)
                min_9_ay = df[df.index>=(index_sinir-270)]['lowest'].min() * (1+margin_kripto_alt)
                min_10_ay = df[df.index>=(index_sinir-300)]['lowest'].min() * (1+margin_kripto_alt)
                min_11_ay = df[df.index>=(index_sinir-330)]['lowest'].min() * (1+margin_kripto_alt)
                min_12_ay = df[df.index>=(index_sinir-360)]['lowest'].min() * (1+margin_kripto_alt)

                donem = 0
                if son_fiyat < min_1_ay: donem = 1 
                else: x=0
                if son_fiyat < min_2_ay: donem = 2
                else: x=0
                if son_fiyat < min_3_ay: donem = 3
                else: x=0
                if son_fiyat < min_4_ay: donem = 4
                else: x=0
                if son_fiyat < min_5_ay: donem = 5
                else: x=0
                if son_fiyat < min_6_ay: donem = 6
                else: x=0
                if son_fiyat < min_7_ay: donem = 7
                else: x=0
                if son_fiyat < min_8_ay: donem = 8
                else: x=0
                if son_fiyat < min_9_ay: donem = 9
                else: x=0
                if son_fiyat < min_10_ay: donem = 10
                else: x=0
                if son_fiyat < min_11_ay: donem = 11
                else: x=0
                if son_fiyat < min_12_ay: donem = 12
                else: x=0

                if donem >= 1:
                    server = smtplib.SMTP_SSL()
                    server.connect("smtp.gmail.com", 465)
                    server.ehlo()
                    server.login("sertac.sinyal", "147Lahana")
                    subject = "--- "+kur+" son "+str(donem)+" ayin en dusugunde, alim firsati olabilir ---"
                    text = "Merhaba, \n"+kur+" "+str(son_fiyat)+" ile son "+str(donem)+" ayin en dusuk seviyelerinde. Alim firsati olabilir."
                    message = 'Subject: {}\n\n{}'.format(subject, text)
                    server.sendmail(from_address, to_address, message)
                    server.quit()
                    
                    sinyal_ekleme = pd.DataFrame({'kur':[kur],'zaman':[datetime.datetime.now()]})
                    sinyal = pd.concat([sinyal,sinyal_ekleme])
                else: x=0

                #max prices
                max_1_ay = df[df.index>=(index_sinir-30)]['highest'].max() * (1-margin_kripto_ust)
                max_2_ay = df[df.index>=(index_sinir-60)]['highest'].max() * (1-margin_kripto_ust)
                max_3_ay = df[df.index>=(index_sinir-90)]['highest'].max() * (1-margin_kripto_ust)
                max_4_ay = df[df.index>=(index_sinir-120)]['highest'].max() * (1-margin_kripto_ust)
                max_5_ay = df[df.index>=(index_sinir-150)]['highest'].max() * (1-margin_kripto_ust)
                max_6_ay = df[df.index>=(index_sinir-180)]['highest'].max() * (1-margin_kripto_ust)
                max_7_ay = df[df.index>=(index_sinir-210)]['highest'].max() * (1-margin_kripto_ust)
                max_8_ay = df[df.index>=(index_sinir-240)]['highest'].max() * (1-margin_kripto_ust)
                max_9_ay = df[df.index>=(index_sinir-270)]['highest'].max() * (1-margin_kripto_ust)
                max_10_ay = df[df.index>=(index_sinir-300)]['highest'].max() * (1-margin_kripto_ust)
                max_11_ay = df[df.index>=(index_sinir-330)]['highest'].max() * (1-margin_kripto_ust)
                max_12_ay = df[df.index>=(index_sinir-360)]['highest'].max() * (1-margin_kripto_ust)


                donem = 0
                if son_fiyat > max_1_ay: donem = 1 
                else: x=0
                if son_fiyat > max_2_ay: donem = 2
                else: x=0
                if son_fiyat > max_3_ay: donem = 3
                else: x=0
                if son_fiyat > max_4_ay: donem = 4
                else: x=0
                if son_fiyat > max_5_ay: donem = 5
                else: x=0
                if son_fiyat > max_6_ay: donem = 6
                else: x=0
                if son_fiyat > max_7_ay: donem = 7
                else: x=0
                if son_fiyat > max_8_ay: donem = 8
                else: x=0
                if son_fiyat > max_9_ay: donem = 9
                else: x=0
                if son_fiyat > max_10_ay: donem = 10
                else: x=0
                if son_fiyat > max_11_ay: donem = 11
                else: x=0
                if son_fiyat > max_12_ay: donem = 12
                else: x=0

                if donem >= 1:
                    server = smtplib.SMTP_SSL()
                    server.connect("smtp.gmail.com", 465)
                    server.ehlo()
                    server.login("sertac.sinyal", "147Lahana")
                    subject = "--- "+kur+" son "+str(donem)+" ayin en yukseginde, satis firsati olabilir ---"
                    text = "Merhaba, \n"+kur+" "+str(son_fiyat)+" ile son "+str(donem)+" ayin en yuksek seviyelerinde. Satis firsati olabilir."
                    message = 'Subject: {}\n\n{}'.format(subject, text)
                    server.sendmail(from_address, to_address, message)
                    server.quit()
                    
                    sinyal_ekleme = pd.DataFrame({'kur':[kur],'zaman':[datetime.datetime.now()]})
                    sinyal = pd.concat([sinyal,sinyal_ekleme])
                else: x=0

            else: x=0

########################################### FOREIGN CURRENCIES ###########################################

        doviz_kurlari = ['USD','EUR','GBP','EUR/USD']
    
        for kur in doviz_kurlari:
            
            #parameter arrangement
            
            if kur == 'EUR/USD': 
                url='https://www.qnbfinansbank.enpara.com/doviz-kur-bilgileri/doviz-altin-kurlari.aspx'
            else: 
                url='https://www.qnbfinansbank.com/doviz-kur-bilgileri/'

            if kur == 'EUR/USD':
                quandl_string='ECB/EURUSD'
            elif kur == 'USD':
                quandl_string='BOE/XUDLBK75'
            elif kur == 'EUR':
                quandl_string='ECB/EURTRY'
            elif kur == 'GBP':
                quandl_string='BOE/XUDLBK95'
            else: x=0
                
            if kur == 'EUR/USD':
                margin = margin_parite
            else:
                margin = margin_doviz
                
            if kur == 'EUR/USD':
                q = 150
            else:
                q = 75
                
            #last signal detection
            
            son_sinyalden_gecen_sure = (datetime.datetime.now() - sinyal[sinyal['kur']==kur]['zaman'].max()).seconds

            if math.isnan(son_sinyalden_gecen_sure):
                son_sinyalden_gecen_sure = 1000000
            else: x=0
            
            if son_sinyalden_gecen_sure > sinyal_arasi_sure:
                
                response = requests.get(url)
                
                x = response.text.find(kur)
                st = (response.text[x:x+150])
                x = st.find(',')
                kur_11 = float(st[x-1:x])
                kur_12 = float(st[x+1:x+4])
                kur_alis = kur_11+kur_12/1000
                
                x = response.text.find(kur)
                st = (response.text[x+q:x+q+150])
                x = st.find(',')
                kur_21 = float(st[x-1:x])
                kur_22 = float(st[x+1:x+4])
                kur_satis = kur_21+kur_22/1000

                kur_son = (kur_alis + kur_satis) / 2
                
                quandl.ApiConfig.api_key = "fpAxEt1wp2J3uNg2kwK7"
                start = str(datetime.datetime.now().date() - datetime.timedelta(days=180))
                end = str(datetime.datetime.now().date())
                
                df = quandl.get(quandl_string, start_date=start, end_date=end)
                df['Value'] = df.Value.astype(float)
                df = df.reset_index()
                df = df.append({'Date':datetime.datetime.now(), 'Value':kur_son}, ignore_index=True)
                
                #min prices
                min_1_ay = df[df['Date']>=(datetime.datetime.now().date() - datetime.timedelta(days=30))]['Value'].min() * (1+margin)
                min_2_ay = df[df['Date']>=(datetime.datetime.now().date() - datetime.timedelta(days=60))]['Value'].min() * (1+margin)
                min_3_ay = df[df['Date']>=(datetime.datetime.now().date() - datetime.timedelta(days=90))]['Value'].min() * (1+margin)
                min_4_ay = df[df['Date']>=(datetime.datetime.now().date() - datetime.timedelta(days=120))]['Value'].min() * (1+margin)
                min_5_ay = df[df['Date']>=(datetime.datetime.now().date() - datetime.timedelta(days=150))]['Value'].min() * (1+margin)
                min_6_ay = df[df['Date']>=(datetime.datetime.now().date() - datetime.timedelta(days=180))]['Value'].min() * (1+margin)

                donem = 0
                if kur_son < min_1_ay: donem = 1 
                else: x=0
                if kur_son < min_2_ay: donem = 2
                else: x=0
                if kur_son < min_3_ay: donem = 3
                else: x=0
                if kur_son < min_4_ay: donem = 4
                else: x=0
                if kur_son < min_5_ay: donem = 5
                else: x=0
                if kur_son < min_6_ay: donem = 6
                else: x=0                
                
                if donem >= 1:
                    server = smtplib.SMTP_SSL()
                    server.connect("smtp.gmail.com", 465)
                    server.ehlo()
                    server.login("sertac.sinyal", "147Lahana")
                    subject = "--- "+kur+" son "+str(donem)+" ayin en dusugunde, alim firsati olabilir ---"
                    text = "Merhaba, \n"+kur+" "+str(kur_son)+" ile son "+str(donem)+" ayin en dusuk seviyelerinde. Finansbank "+str(kur_alis)+"'ten alip "+str(kur_satis)+"'ten satiyor. Alim firsati olabilir."
                    message = 'Subject: {}\n\n{}'.format(subject, text)
                    server.sendmail(from_address, to_address, message)
                    server.quit()
                    
                    sinyal_ekleme = pd.DataFrame({'kur':[kur],'zaman':[datetime.datetime.now()]})
                    sinyal = pd.concat([sinyal,sinyal_ekleme])
                else: x=0

                #max prices
                max_1_ay = df[df['Date']>=(datetime.datetime.now().date() - datetime.timedelta(days=30))]['Value'].max() * (1-margin)
                max_2_ay = df[df['Date']>=(datetime.datetime.now().date() - datetime.timedelta(days=60))]['Value'].max() * (1-margin)
                max_3_ay = df[df['Date']>=(datetime.datetime.now().date() - datetime.timedelta(days=90))]['Value'].max() * (1-margin)
                max_4_ay = df[df['Date']>=(datetime.datetime.now().date() - datetime.timedelta(days=120))]['Value'].max() * (1-margin)
                max_5_ay = df[df['Date']>=(datetime.datetime.now().date() - datetime.timedelta(days=150))]['Value'].max() * (1-margin)
                max_6_ay = df[df['Date']>=(datetime.datetime.now().date() - datetime.timedelta(days=180))]['Value'].max() * (1-margin)

                donem = 0
                if kur_son > max_1_ay: donem = 1 
                else: x=0
                if kur_son > max_2_ay: donem = 2
                else: x=0
                if kur_son > max_3_ay: donem = 3
                else: x=0
                if kur_son > max_4_ay: donem = 4
                else: x=0
                if kur_son > max_5_ay: donem = 5
                else: x=0
                if kur_son > max_6_ay: donem = 6
                else: x=0       

                if donem >= 1:
                    server = smtplib.SMTP_SSL()
                    server.connect("smtp.gmail.com", 465)
                    server.ehlo()
                    server.login("sertac.sinyal", "147Lahana")
                    subject = "--- "+kur+" son "+str(donem)+" ayin en yukseginde, satis firsati olabilir ---"
                    text = "Merhaba, \n"+kur+" "+str(kur_son)+" ile son "+str(donem)+" ayin en yuksek seviyelerinde. Finansbank "+str(kur_alis)+"'ten alip "+str(kur_satis)+"'ten satiyor. Satis firsati olabilir."
                    message = 'Subject: {}\n\n{}'.format(subject, text)
                    server.sendmail(from_address, to_address, message)
                    server.quit()
                    
                    sinyal_ekleme = pd.DataFrame({'kur':[kur],'zaman':[datetime.datetime.now()]})
                    sinyal = pd.concat([sinyal,sinyal_ekleme])
                else: x=0
                
            else: x=0

########################################### GOLD ###########################################


        #last signal detection
        
        kur = 'GOLD'
    
        son_sinyalden_gecen_sure = (datetime.datetime.now() - sinyal[sinyal['kur']==kur]['zaman'].max()).seconds

        if math.isnan(son_sinyalden_gecen_sure):
            son_sinyalden_gecen_sure = 1000000
        else: x=0

        if son_sinyalden_gecen_sure > sinyal_arasi_sure:

            url = 'http://finans.mynet.com/altin/'
            response = requests.get(url)

            x = response.text.find('Ons Alt')
            st = (response.text[x:x+150])
            x = st.find(',')
            kur_11 = float(st[x-4:x])
            kur_12 = float(st[x+1:x+3])
            kur_alis = kur_11+kur_12/1000

            x = response.text.find('Ons Alt')
            st = (response.text[x+150:x+250])
            x = st.find(',')
            kur_21 = float(st[x-4:x])
            kur_22 = float(st[x+1:x+3])
            kur_satis = kur_21+kur_22/1000

            kur_son = (kur_alis + kur_satis) / 2

            quandl.ApiConfig.api_key = "fpAxEt1wp2J3uNg2kwK7"
            start = str(datetime.datetime.now().date() - datetime.timedelta(days=180))
            end = str(datetime.datetime.now().date())

            df = quandl.get('LBMA/GOLD', start_date=start, end_date=end)
            df = df.reset_index()
            df = df[['Date','USD (AM)']]
            df = df.append({'Date':datetime.datetime.now(), 'USD (AM)':kur_son}, ignore_index=True)

            #min prices
            min_1_ay = df[df['Date']>=(datetime.datetime.now().date() - datetime.timedelta(days=30))]['USD (AM)'].min() * (1+margin_gold)
            min_2_ay = df[df['Date']>=(datetime.datetime.now().date() - datetime.timedelta(days=60))]['USD (AM)'].min() * (1+margin_gold)
            min_3_ay = df[df['Date']>=(datetime.datetime.now().date() - datetime.timedelta(days=90))]['USD (AM)'].min() * (1+margin_gold)
            min_4_ay = df[df['Date']>=(datetime.datetime.now().date() - datetime.timedelta(days=120))]['USD (AM)'].min() * (1+margin_gold)
            min_5_ay = df[df['Date']>=(datetime.datetime.now().date() - datetime.timedelta(days=150))]['USD (AM)'].min() * (1+margin_gold)
            min_6_ay = df[df['Date']>=(datetime.datetime.now().date() - datetime.timedelta(days=180))]['USD (AM)'].min() * (1+margin_gold)

            donem = 0
            if kur_son < min_1_ay: donem = 1 
            else: x=0
            if kur_son < min_2_ay: donem = 2
            else: x=0
            if kur_son < min_3_ay: donem = 3
            else: x=0
            if kur_son < min_4_ay: donem = 4
            else: x=0
            if kur_son < min_5_ay: donem = 5
            else: x=0
            if kur_son < min_6_ay: donem = 6
            else: x=0                

            if donem >= 1:
                server = smtplib.SMTP_SSL()
                server.connect("smtp.gmail.com", 465)
                server.ehlo()
                server.login("sertac.sinyal", "147Lahana")
                subject = "--- "+kur+" son "+str(donem)+" ayin en dusugunde, alim firsati olabilir ---"
                text = "Merhaba, \n"+kur+" "+str(kur_son)+" ile USD karsisinda son "+str(donem)+" ayin en dusuk seviyelerinde. Alim firsati olabilir."
                message = 'Subject: {}\n\n{}'.format(subject, text)
                server.sendmail(from_address, to_address, message)
                server.quit()

                sinyal_ekleme = pd.DataFrame({'kur':[kur],'zaman':[datetime.datetime.now()]})
                sinyal = pd.concat([sinyal,sinyal_ekleme])
            else: x=0

            #max prices
            max_1_ay = df[df['Date']>=(datetime.datetime.now().date() - datetime.timedelta(days=30))]['USD (AM)'].max() * (1-margin_gold)
            max_2_ay = df[df['Date']>=(datetime.datetime.now().date() - datetime.timedelta(days=60))]['USD (AM)'].max() * (1-margin_gold)
            max_3_ay = df[df['Date']>=(datetime.datetime.now().date() - datetime.timedelta(days=90))]['USD (AM)'].max() * (1-margin_gold)
            max_4_ay = df[df['Date']>=(datetime.datetime.now().date() - datetime.timedelta(days=120))]['USD (AM)'].max() * (1-margin_gold)
            max_5_ay = df[df['Date']>=(datetime.datetime.now().date() - datetime.timedelta(days=150))]['USD (AM)'].max() * (1-margin_gold)
            max_6_ay = df[df['Date']>=(datetime.datetime.now().date() - datetime.timedelta(days=180))]['USD (AM)'].max() * (1-margin_gold)

            donem = 0
            if kur_son > max_1_ay: donem = 1 
            else: x=0
            if kur_son > max_2_ay: donem = 2
            else: x=0
            if kur_son > max_3_ay: donem = 3
            else: x=0
            if kur_son > max_4_ay: donem = 4
            else: x=0
            if kur_son > max_5_ay: donem = 5
            else: x=0
            if kur_son > max_6_ay: donem = 6
            else: x=0       

            if donem >= 1:
                server = smtplib.SMTP_SSL()
                server.connect("smtp.gmail.com", 465)
                server.ehlo()
                server.login("sertac.sinyal", "147Lahana")
                subject = "--- "+kur+" son "+str(donem)+" ayin en yukseginde, satis firsati olabilir ---"
                text = "Merhaba, \n"+kur+" "+str(kur_son)+" ile USD karsisinda son "+str(donem)+" ayin en yuksek seviyelerinde. Satis firsati olabilir."
                message = 'Subject: {}\n\n{}'.format(subject, text)
                server.sendmail(from_address, to_address, message)
                server.quit()

                sinyal_ekleme = pd.DataFrame({'kur':[kur],'zaman':[datetime.datetime.now()]})
                sinyal = pd.concat([sinyal,sinyal_ekleme])
            else: x=0

        else: x=0


        time.sleep(bekleme_suresi)

    except:
        pass
