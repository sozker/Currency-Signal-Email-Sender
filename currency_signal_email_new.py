import pandas as pd
import numpy as np
import datetime
import time
from binance.client import Client
from binance.enums import *
import smtplib
import math
from selenium import webdriver
import os
import shutil

#e-mail info
from_address = "sender@gmail.com"
to_address = ["receiver_1@yahoo.com","receiver_1@hotmail.com"]


#parameters
margin_kripto_alt = 0.02
margin_kripto_ust = 0.002

margin_doviz = 0.002


sinyal_arasi_sure = 8*60*60 #8 hours - the period it will wait for sending a signal for the same currency
bekleme_suresi = 3*60 #3 minutes - the period it will wait between each search 

#binance connection
api_key = "ENTER YOUR API KEY"
api_secret = "ENTER YOUR API SECRET"
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
        kripto_kurlar = tickers[tickers['conv']=='BTC'].nlargest(15,'quoteVolume')['symbol'].tolist()
        kripto_kurlar.append('BTCUSDT')

        for kur in kripto_kurlar:

            ##### last signal detection #####

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
                    server.login("YOUR MAIL ADDRESS", "YOUR PASSWORD")
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
                    server.login("YOUR MAIL ADDRESS", "YOUR PASSWORD")
                    subject = "--- "+kur+" son "+str(donem)+" ayin en yukseginde, satis firsati olabilir ---"
                    text = "Merhaba, \n"+kur+" "+str(son_fiyat)+" ile son "+str(donem)+" ayin en yuksek seviyelerinde. Satis firsati olabilir."
                    message = 'Subject: {}\n\n{}'.format(subject, text)
                    server.sendmail(from_address, to_address, message)
                    server.quit()

                    sinyal_ekleme = pd.DataFrame({'kur':[kur],'zaman':[datetime.datetime.now()]})
                    sinyal = pd.concat([sinyal,sinyal_ekleme])
                else: x=0

            else: x=0

    ########################################### FOREIGN CURRENCIES & STOCKS ###########################################

        driver = webdriver.Chrome(executable_path='C:/Users/Administrator/Desktop/python deneme/chromedriver')
        driver.get('https://www.investing.com/')

        #LOG-IN PROCESS
        login = '//*[@id="userAccount"]/div/a[1]'
        button1 = driver.find_element_by_xpath(login)
        button1.click()

        username = '//*[@id="loginFormUser_email"]'
        box1 = driver.find_element_by_xpath(username)
        box1.send_keys('ENTER YOUR INVESTING.COM USERNAME')

        password = '//*[@id="loginForm_password"]'
        box2 = driver.find_element_by_xpath(password)
        box2.send_keys('ENTER YOUR INVESTING.COM PASSWORD')

        signin = '//*[@id="signup"]/a'
        button2 = driver.find_element_by_xpath(signin)
        button2.click()


        list = ['USD/TRY','EUR/TRY','GBP/TRY','ALTIN/TRY','EUR/USD','ALTIN/USD',
                'BIST_100','GARANTI_BANKASI','TUPRAS','ASELSAN','THY','TURK_TELEKOM','PETKIM','IS_BANKASI_C',
                'SASA','BIM','AKBANK','EREGLI_DEMIR_CELIK','KARDEMIR','SABANCI_HOLDING','HALK_BANKASI','YAPI_KREDI']

        for kur in list:

            ##### parameter arrangement #####

            if kur == 'USD/TRY': url = 'https://www.investing.com/currencies/usd-try-historical-data'
            elif kur == 'EUR/TRY': url = 'https://www.investing.com/currencies/eur-try-historical-data'
            elif kur == 'GBP/TRY': url = 'https://www.investing.com/currencies/gbp-try-historical-data'
            elif kur == 'ALTIN/TRY': url = 'https://www.investing.com/currencies/xau-try-historical-data'
            elif kur == 'EUR/USD': url = 'https://www.investing.com/currencies/eur-usd-historical-data'
            elif kur == 'ALTIN/USD': url = 'https://www.investing.com/currencies/xau-usd-historical-data'
            elif kur == 'BIST_100': url = 'https://www.investing.com/indices/ise-100-historical-data'
            elif kur == 'GARANTI_BANKASI': url = 'https://www.investing.com/equities/garanti-bankasi-historical-data'
            elif kur == 'TUPRAS': url = 'https://www.investing.com/equities/tupras-historical-data'
            elif kur == 'ASELSAN': url = 'https://www.investing.com/equities/aselsan-historical-data'
            elif kur == 'THY': url = 'https://www.investing.com/equities/turk-hava-yollari-historical-data'
            elif kur == 'TURK_TELEKOM': url = 'https://www.investing.com/equities/turk-telekom-historical-data'
            elif kur == 'PETKIM': url = 'https://www.investing.com/equities/petkim-historical-data'
            elif kur == 'IS_BANKASI_C': url = 'https://www.investing.com/equities/is-bankasi-(c)-historical-data'
            elif kur == 'SASA': url = 'https://www.investing.com/equities/sasa-polyester-historical-data'
            elif kur == 'BIM': url = 'https://www.investing.com/equities/bim-magazalar-historical-data'
            elif kur == 'AKBANK': url = 'https://www.investing.com/equities/akbank-historical-data'
            elif kur == 'EREGLI_DEMIR_CELIK': url = 'https://www.investing.com/equities/eregli-demir-celik-historical-data'
            elif kur == 'KARDEMIR': url = 'https://www.investing.com/equities/kardemir-(d)-historical-data'
            elif kur == 'SABANCI_HOLDING': url = 'https://www.investing.com/equities/sabanci-holding-historical-data'
            elif kur == 'HALK_BANKASI': url = 'https://www.investing.com/equities/t.-halk-bankasi-historical-data'
            elif kur == 'YAPI_KREDI': url = 'https://www.investing.com/equities/yapi-ve-kredi-bank.-historical-data'
            else: x = 0

            if kur == 'USD/TRY': file_name = 'USD_TRY Historical Data'
            elif kur == 'EUR/TRY': file_name = 'EUR_TRY Historical Data'
            elif kur == 'GBP/TRY': file_name = 'GBP_TRY Historical Data'
            elif kur == 'ALTIN/TRY': file_name = 'XAU_TRY Historical Data'
            elif kur == 'EUR/USD': file_name = 'EUR_USD Historical Data'
            elif kur == 'ALTIN/USD': file_name = 'XAU_USD Historical Data'
            elif kur == 'BIST_100': file_name = 'BIST 100 Historical Data'
            elif kur == 'GARANTI_BANKASI': file_name = 'GARAN Historical Data'
            elif kur == 'TUPRAS': file_name = 'TUPRS Historical Data'
            elif kur == 'ASELSAN': file_name = 'ASELS Historical Data'
            elif kur == 'THY': file_name = 'THYAO Historical Data'
            elif kur == 'TURK_TELEKOM': file_name = 'TTKOM Historical Data'
            elif kur == 'PETKIM': file_name = 'PETKM Historical Data'
            elif kur == 'IS_BANKASI_C': file_name = 'ISCTR Historical Data'
            elif kur == 'SASA': file_name = 'SASA Historical Data'
            elif kur == 'BIM': file_name = 'BIMAS Historical Data'
            elif kur == 'AKBANK': file_name = 'AKBNK Historical Data'
            elif kur == 'EREGLI_DEMIR_CELIK': file_name = 'EREGL Historical Data'
            elif kur == 'KARDEMIR': file_name = 'KRDMD Historical Data'
            elif kur == 'SABANCI_HOLDING': file_name = 'SAHOL Historical Data'
            elif kur == 'HALK_BANKASI': file_name = 'HALKB Historical Data'
            elif kur == 'YAPI_KREDI': file_name = 'YKBNK Historical Data'
            else: x = 0

            ##### last signal detection #####

            son_sinyalden_gecen_sure = (datetime.datetime.now() - sinyal[sinyal['kur']==kur]['zaman'].max()).seconds

            if math.isnan(son_sinyalden_gecen_sure):
                son_sinyalden_gecen_sure = 1000000
            else: x=0

            if son_sinyalden_gecen_sure > sinyal_arasi_sure:

                driver.get(url)

                #DOWNLOADING DATA
                time_frame = '//*[@id="data_interval"]'
                box3 = driver.find_element_by_xpath(time_frame)
                box3.send_keys('Weekly')

                time.sleep(10)

                download = '//*[@id="column-content"]/div[4]/div/a'
                button3 = driver.find_element_by_xpath(download)
                button3.click()

                time.sleep(10)

                file_path = 'C:/Users/Administrator/Downloads/'
                df = pd.read_csv(file_path+file_name+'.csv')
                df['Price'] = df['Price'].replace(',', '', regex=True)
                df['Price'] = df.Price.astype(float)
                df['High'] = df['High'].replace(',', '', regex=True)
                df['High'] = df.High.astype(float)
                df['Low'] = df['Low'].replace(',', '', regex=True)
                df['Low'] = df.Low.astype(float)
                kur_son = df[df.index==0]['Price'].min()

                #min prices
                min_1_ay = df[df.index<=4]['Low'].min() * (1 + margin_doviz)
                min_2_ay = df[df.index<=8]['Low'].min() * (1 + margin_doviz)
                min_3_ay = df[df.index<=12]['Low'].min() * (1 + margin_doviz)
                min_4_ay = df[df.index<=16]['Low'].min() * (1 + margin_doviz)
                min_5_ay = df[df.index<=20]['Low'].min() * (1 + margin_doviz)
                min_6_ay = df[df.index<=24]['Low'].min() * (1 + margin_doviz)
                min_7_ay = df[df.index<=28]['Low'].min() * (1 + margin_doviz)
                min_8_ay = df[df.index<=32]['Low'].min() * (1 + margin_doviz)
                min_9_ay = df[df.index<=36]['Low'].min() * (1 + margin_doviz)
                min_10_ay = df[df.index<=40]['Low'].min() * (1 + margin_doviz)
                min_11_ay = df[df.index<=44]['Low'].min() * (1 + margin_doviz)
                min_12_ay = df[df.index<=48]['Low'].min() * (1 + margin_doviz)

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
                if kur_son < min_7_ay: donem = 7
                else: x=0  
                if kur_son < min_8_ay: donem = 8
                else: x=0  
                if kur_son < min_9_ay: donem = 9
                else: x=0  
                if kur_son < min_10_ay: donem = 10
                else: x=0  
                if kur_son < min_11_ay: donem = 11
                else: x=0  
                if kur_son < min_12_ay: donem = 12
                else: x=0  

                if donem >= 1:
                    server = smtplib.SMTP_SSL()
                    server.connect("smtp.gmail.com", 465)
                    server.ehlo()
                    server.login("YOUR MAIL ADDRESS", "YOUR PASSWORD")
                    subject = "--- "+kur+" son "+str(donem)+" ayin en dusugunde, alim firsati olabilir ---"
                    text = "Merhaba, \n"+kur+" "+str(kur_son)+" ile son "+str(donem)+" ayin en dusuk seviyelerinde. Alim firsati olabilir."
                    message = 'Subject: {}\n\n{}'.format(subject, text)
                    server.sendmail(from_address, to_address, message)
                    server.quit()

                    sinyal_ekleme = pd.DataFrame({'kur':[kur],'zaman':[datetime.datetime.now()]})
                    sinyal = pd.concat([sinyal,sinyal_ekleme])
                else: x=0

                #max prices
                max_1_ay = df[df.index<=4]['High'].max() * (1 - margin_doviz)
                max_2_ay = df[df.index<=8]['High'].max() * (1 - margin_doviz)
                max_3_ay = df[df.index<=12]['High'].max() * (1 - margin_doviz)
                max_4_ay = df[df.index<=16]['High'].max() * (1 - margin_doviz)
                max_5_ay = df[df.index<=20]['High'].max() * (1 - margin_doviz)
                max_6_ay = df[df.index<=24]['High'].max() * (1 - margin_doviz)
                max_7_ay = df[df.index<=28]['High'].max() * (1 - margin_doviz)
                max_8_ay = df[df.index<=32]['High'].max() * (1 - margin_doviz)
                max_9_ay = df[df.index<=36]['High'].max() * (1 - margin_doviz)
                max_10_ay = df[df.index<=40]['High'].max() * (1 - margin_doviz)
                max_11_ay = df[df.index<=44]['High'].max() * (1 - margin_doviz)
                max_12_ay = df[df.index<=48]['High'].max() * (1 - margin_doviz)

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
                if kur_son > max_7_ay: donem = 7
                else: x=0 
                if kur_son > max_8_ay: donem = 8
                else: x=0 
                if kur_son > max_9_ay: donem = 9
                else: x=0 
                if kur_son > max_10_ay: donem = 10
                else: x=0 
                if kur_son > max_11_ay: donem = 11
                else: x=0 
                if kur_son > max_12_ay: donem = 12
                else: x=0 

                if donem >= 1:
                    server = smtplib.SMTP_SSL()
                    server.connect("smtp.gmail.com", 465)
                    server.ehlo()
                    server.login("YOUR MAIL ADDRESS", "YOUR PASSWORD")
                    subject = "--- "+kur+" son "+str(donem)+" ayin en yukseginde, satis firsati olabilir ---"
                    text = "Merhaba, \n"+kur+" "+str(kur_son)+" ile son "+str(donem)+" ayin en yuksek seviyelerinde. Satis firsati olabilir."
                    message = 'Subject: {}\n\n{}'.format(subject, text)
                    server.sendmail(from_address, to_address, message)
                    server.quit()

                    sinyal_ekleme = pd.DataFrame({'kur':[kur],'zaman':[datetime.datetime.now()]})
                    sinyal = pd.concat([sinyal,sinyal_ekleme])
                else: x=0

                #os.remove(file_path)
                shutil.rmtree(file_path ,ignore_errors=True)

            else: x=0

        driver.close()

        time.sleep(bekleme_suresi)

    except:
        pass
