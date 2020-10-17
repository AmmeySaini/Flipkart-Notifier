import requests
import urllib3
from bs4 import BeautifulSoup
from pyrogram import Client
import time
import sys
from __banner__.banner import banner
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from dotenv import load_dotenv, find_dotenv, set_key
import os


######## This is only for educational purpose ########
######## I'm not responsible for any loss or damage caused to you ########
######## using this script. ########
######## YOU ARE USING THIS SCRIPT ON YOUR OWN RISK ########

def ordinal(n):
    suffix = ['th', 'st', 'nd', 'rd', 'th', 'th', 'th', 'th', 'th', 'th']

    if n < 0:
        n *= -1

    n = int(n)

    if n % 100 in (11,12,13):
        s = 'th'
    else:
        s = suffix[n % 10]

    return str(n) + s

def main():
    sys.stdout.write(banner())

    time.sleep(0.8)
    ######## Add api_id and api_hash from my.telegram.org ########

    head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    }

    # Check for dotenv file and load into environment
    load_dotenv(find_dotenv())

    chk_list_urls = []
    no = 1

    # True if environment is not set
    input_an = True if os.environ.get("PRODUCT_URLS")=="productA,productB" else False

    # Add urls from dotenv
    if input_an==False:
        chk_list_urls = list(filter(lambda string: string!="", map(lambda url: url.strip(), os.environ.get("PRODUCT_URLS").split(","))))

    while input_an != False:
        inp_urls = input('Paste ' + ordinal(no) + ' url, When you are done adding urls input "next" to start script: ')
        no += 1
        if inp_urls != 'next':
            chk_list_urls.append(inp_urls)
        else:
            # Set product urls in environment
            set_key(find_dotenv(), "PRODUCT_URLS", ",".join(chk_list_urls))
            input_an = False

    if len(chk_list_urls) < 1:
        print('\nInput atleast one url to start')
    else:
        # Get pincode from environment
        pincode = os.environ.get("PINCODE")
        if pincode == "<pincode_here>":
            pincode = input('Enter Your Pincode: ')
            # Set pincode to environment
            set_key(find_dotenv(), "PINCODE", pincode)
        pincode_url = 'https://rome.api.flipkart.com/api/4/page/fetch'
        pincode_data = '{"pageUri":"' + chk_list_urls[0] + '","locationContext":{"pincode":"' + str(pincode) + '"},"pageContext":{"pageNumber":1,"fetchSeoData":true}}'
        
        r2 = requests.post(pincode_url, headers={'X-user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36 FKUA/website/42/website/Desktop',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'}, data=pincode_data, verify=False)
        
        try:       
            jss = r2.json()
            c_sn = jss['SESSION']['sn']
        except:
            print('Some error on server side')
            exit()

        head['Cookie'] = 'SN=' + c_sn
        last_l = len(chk_list_urls)
        while True:
            for index, url in enumerate(chk_list_urls):
                r = requests.get(url, headers=head, verify=False)
                soup = BeautifulSoup(r.content, 'html.parser')

                try:
                    if soup.find('button', class_ = '_2AkmmA _3-iCOr wvj5kH').text == 'NOTIFY ME':
                        title = soup.find('span', class_ = '_35KyD6').text
                        print(title + ' is out of stock')
                        if index == last_l - 1:
                            time.sleep(300)
                        # product is oos
                except:
                    try:
                        if soup.find('button', class_ = '_2AkmmA _2Npkh4 _2MWPVK').text == ' ADD TO CART':
                            title = soup.find('span', class_ = '_35KyD6').text
                            print(title + ' is in stock')
                            # print('in stock')
                            ######## SENDING A MESSAGE TO YOUR TELEGEGRAM ########
                            ######## Get below details from my.telegram.org ########

                            # Please set Telegram API ID and API hash in .env
                            app = Client(
                                "tg_ac",
                                api_id=os.environ.get("TELEGRAM_APP_API_ID"), 
                                api_hash=os.environ.get("TELEGRAM_APP_API_HASH") 
                            )

                            msg = title + ' is in stock. LINK - ' + url ######## You can customize this ########

                            with app:
                                app.send_message(os.environ.get("TELEGRAM_USERNAME"), msg)  ######## Sending msg To @your_tg_username (set urs) ########
                                if index == last_l - 1:
                                    time.sleep(300)
                    except:
                        try:
                            if soup.find('button', class_ = '_2AkmmA _2Npkh4 _2MWPVK _18WSRq')['disabled']:
                                print('disabled')
                        except:
                            print('Please add your Telegram credentials in .env files')
                            exit()

if __name__ == '__main__':
    main()