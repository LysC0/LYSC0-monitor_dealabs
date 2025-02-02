"""
Lys C0 | Dealabs Monitor [v0.4]
"""

import json
import re
from data.script import MAINdealabs

def main():
    try :
        with open('setup.json', 'r') as j:
            data = json.load(j)
            
            dealabs_url = data['dealabs_url']
            webhook = data['settings']['webhook']
            range = data['settings']['range']
            await_time = data['settings']['await_time']
            keyword = data['keywords']

            #############################
            # checking json information #
            #############################

            # dealabs url #
            match = re.match( r'^https:\/\/www\.dealabs\.com\/.*', dealabs_url)
            if not match:
                print('dealabs url not suported -> check setup.json')
                return False

            # webhook #
            match = re.match(r'^https:\/\/discord\.com\/api\/webhooks\/\d+\/[A-Za-z0-9_-]+$', webhook)
            if not match :
                print('webhook url not suported -> chech setup.json')
                return False

            # range #
            if type(range) != int :
                print('range need to be int -> remove : " " | setup.json')
                return False

            # await time #
            if type(await_time) != int :
                print('await_time need to be int -> remove : " " | setup.json')
                return False
            
            ###############
            # run monitor #
            ###############

            bot = MAINdealabs(dealabs_url, range, await_time, keyword, webhook)
            bot.monitor()

    except :
        print('Monitor Stoped | thx')
        return False

if __name__ == '__main__' : 
    main()