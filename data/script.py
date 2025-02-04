###########################
##    GITHUB : LysC0     ##   
##                       ##
##    DEALABS MONITOR    ##
##        [v0.4]         ## 
###########################
###########################
    #######        ########
        ###         ###
        ###############

##################################################
import requests                                 ##
import json                                     ##
import time                                     ##
import os                                       ##
##################################################
from bs4 import BeautifulSoup                   ##
##################################################
from data.random_agent import random_user_agent ##
##################################################

class MAINdealabs:
    """
    monitor dealabs by LysCO
    """
    def __init__(self, url, range, await_time, keyword, webhook) -> None:
        self.url = url 
        self.range = range 
        self.await_time = await_time
        self.keyword = keyword
        self.webhook = webhook

        global headers, stock
        headers = {
            "user-agent" : random_user_agent(),
            "referer" : self.url
        }
        stock = [{'' : ''}]

    ##############
    ## Monitor ##
    ##############
    def monitor(self):
        f = -1
        x = 0
        while range(self.range):
            try :
                # getting site page #
                session = requests.Session()
                rsp = session.get(
                    url=self.url,
                    headers=headers,
                    timeout=10
                )
                if rsp.status_code == 200 :
                        # parse json info #
                        soup = BeautifulSoup(rsp.text, 'html.parser')
                        a = 0
                        found_last = False
                        while range(int(100)) :
                            try :
                                js = soup.find_all('div', class_='js-vue2')[a] #last product
                                json_data = js.get('data-vue2')
                                info = json.loads(json_data)
                                j = info['props']['thread']
                                found_last = True
                                break
                            except :
                                a += 1
                        
                        if found_last :
                            # all info #
                            self.title = j.get('title')
                            self.site_link = j.get('link')
                            self.price = f"{j.get('price')}€"
                            self.old_price = 'none' if j.get('nextBestPrice') == 0 else f"{j.get('nextBestPrice')}€"
                            self.dealabs_link = soup.find('a', class_='js-thread-title').get('href').strip()
                            self.voucher_code = 'none' if j.get('voucherCode') == '' else j.get('voucherCode') 
                            self.thread_id = j.get('threadId')
                            
                            # get img #

                            rsp = session.get(self.dealabs_link, headers=headers)
                            soup = BeautifulSoup(rsp.text, 'html.parser')
                            img = soup.find('div', class_='threadItemCard-img')
                            self.img = img.find('img').get('src').strip()
                            
                            # json payload #

                            payload = {'title' : self.title, 'site_link' : self.site_link, 
                                    'price' : self.price, 'old_price' : self.old_price, 
                                    'dealabs_link' : self.dealabs_link, 'voucher_code' : self.voucher_code,
                                    'thread_id' : self.thread_id, 'img' : self.img}
                            
                            # compare | monitor part #
                        
                            for i in stock :
                                    if i.get('title') == self.title: #increment stock
                                        break

                            if i.get('title') == self.title: #same product
                                    stock.append(payload)#save product in stock
                                    x += 1

                                    #display instance
                                    self.instance(f, x, self.range)

                                    #await
                                    time.sleep(int(self.await_time))

                            else : #new product 
                                    print(f'product found : {self.title}') 
                                    stock.append(payload)#save product in stock
                                    f += 1
                                    x += 1

                                    #send webhook
                                    self.webhook_sender(
                                                title=self.title, 
                                                dealabs_link=self.dealabs_link, 
                                                site_link=self.site_link, 
                                                img=self.img, 
                                                price=self.price, 
                                                old_price=self.old_price, 
                                                thread_id=self.thread_id, 
                                                voucher_code=self.voucher_code
                                    )

                                    #display instance
                                    self.instance(f, x, self.range)

                                    #await
                                    time.sleep(int(self.await_time))  
                        else :
                            print('Error Getting Last Div | Retrying..')     
                else :
                    print('Error Getting Page | Retrying..')
            except requests.exceptions.Timeout:
                print('Timeout Error | Retrying..')
            except Exception as e:
                print('Main Error : '+e)
    
    #############
    ## Webhook ##
    #############
    def webhook_sender(self, title, dealabs_link, site_link, img, price, old_price, thread_id, voucher_code):
        color = 864410
        found = ''
        try :
            for items in self.keyword :
                    if items.lower() in title.lower():
                        color = 55813
                        found = f'\n- keyword found : {items.lower()}'
                        break
        except :
            pass

        embed = {
            'title' : f'**Monitor dealabs .me**',
            'url' : self.dealabs_link,
            "description" :f"- monitor dealabs\n- id : {thread_id}{found}",
            "color": color,
            "type" : "rich",
            "fields": [
                {"name": "**__PRODUCT NAME__**", "value": title, "inline": False},
                {"name": "**__PRICE / OLD PRICE__**", "value": f'{price} / {old_price}', "inline": False},
                {"name": "**__DEALABS URL__**", "value": '[product dealabs page]' + '(' + dealabs_link + ')', "inline": False},
                {"name": "**__VOUCHER CODE__**", "value": voucher_code, "inline" : False},
                {"name": "**__SITE URL__**", "value": '[product page site]' + '(' + site_link + ')', "inline" : False},
            ],
            
            "thumbnail" : {
                "url" : img
            }
        }  
        
        payload = {
            "content": "",
            "embeds": [embed]
        }

        response = requests.post(self.webhook, data=json.dumps(payload), headers={"Content-Type": "application/json"})

        if response.status_code == 204:
            pass
        else:
            print("\033[1;31mWebhook error :", response.status_code)

    ##############
    ## Instance ##
    ##############
    def instance(self, found, x, range):
        os.system('cls')
        c_time = time.strftime('%H:%M:%S')
        print(f"""
 ______________________________
|    DEALABS MONITOR v0.4      |
|           LysC0              |
|______________________________|
| ++ found : [{found}]            
|-------------------------------
| ++ range : [{x}/{range}]        
|-------------------------------
| ++ time : [{c_time}]            
|-------------------------------""")

if __name__ == '__main__' :
    #bot = MAINdealabs('https://www.dealabs.com/', 19000, 2, '', 'https://discord.com/api/webhooks/1154193477819695175/lXjz_mO_oxiNDgXqBYh3Rr69LRpgUuTLBLBhnjKYUAaGMbRIjpLu8IdbdSVBm1n7Cc5f')
    #bot.monitor()
    pass