import requests
import urllib3
from bs4 import BeautifulSoup
from pyrogram import Client
import time
import sys
from __constants.constants import *
from __banner__.banner import banner
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


######## This is only for educational purpose ########
######## I'm not responsible for any loss or damage caused to you ########
######## using this script. ########
######## YOU ARE USING THIS SCRIPT ON YOUR OWN RISK ########


def main():

    sys.stdout.write(banner())

    time.sleep(0.8)
    ######## Add Your Links Before Running This Script in __constants/constants.py (chk_list) ########
    ######## Also add api_id and api_hash from my.telegram.org ########
    last_l = len(chk_list)

    while True:
        for index, url in enumerate(chk_list):
            r = requests.get(url, headers=head, verify=False)
            soup = BeautifulSoup(r.content, 'html.parser')

            try:
                if soup.find('button', class_ = '_2AkmmA _3-iCOr wvj5kH').text == 'NOTIFY ME':
                    title = soup.find('span', class_ = '_35KyD6').text
                    print(title + ' is oos')
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

                        app = Client(
                            "tg_ac",
                            api_id=1234567, ######## YOUR API_ID ########
                            api_hash="xxxxxxxxxx" ######## YOUR API_HASH ########
                        )

                        msg = title + ' is in stock LINK - ' + url ######## You can customize this ########

                        with app:
                            app.send_message("your_tg_username", msg)  ######## Sending msg To @your_tg_username (set urs) ########
                            if index == last_l - 1:
                                time.sleep(300)
                except:
                    if soup.find('button', class_ = '_2AkmmA _2Npkh4 _2MWPVK _18WSRq')['disabled']:
                        print('disabled')

if __name__ == '__main__':
    main()