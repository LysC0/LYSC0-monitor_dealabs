###########################   ###############################
##    GITHUB : LysC0     ##   ## FILE : dealabs_monitor.py ##
##                       ##   ###############################
##    DEALABS MONITOR    ##   
##                       ##   ###############################
###########################   ## VERSION : [0.4]           ##
###########################   ###############################
    #######        ########
        ###         ###
        ######  #######
            ##  ##
            ######

######################################
import json                         ##
import re                           ##
import time                         ##
######################################
from data.script import MAINdealabs ##
######################################

def main():
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
                time.sleep(10)
                return False

            # webhook #
            match = re.match(r'^https:\/\/discord\.com\/api\/webhooks\/\d+\/[A-Za-z0-9_-]+$', webhook)
            if not match :
                print('webhook url not suported -> chech setup.json')
                time.sleep(10)
                return False

            # range #
            if type(range) != int :
                print('range need to be int -> remove : " " | setup.json')
                time.sleep(10)
                return False

            # await time #
            if type(await_time) != int :
                print('await_time need to be int -> remove : " " | setup.json')
                time.sleep(10)
                return False
            
            ###############
            # run monitor #
            ###############

            bot = MAINdealabs(dealabs_url, range, await_time, keyword, webhook)
            bot.monitor()


############
# run main #
############

if __name__ == '__main__' :
    try :
        main()
    except KeyboardInterrupt :
        print("\n    |\n    '-> Monitor Stoped | Thx -------•")
