from selenium import webdriver
from bs4 import BeautifulSoup
import time
import telegram
import pandas as pd 

path_csv_file_name = "tx_list_rere.csv"



def data_listing(tr_list, df_tx_list, bot, chat_id):

    for tr in tr_list : 
        tx_hash = tr.select_one(".CroppedTxWithLink").text
        block_num = be_int(tr.select_one(".Table__td.TxListDesktop__blockNumber.TxListDesktop__blockNumberTd").text)
        tx_time = tr.select_one(".Tooltip__tooltip.Tooltip__tooltip--bottom").text
        tx_in_out = tr.select_one(".InOut__arrow").text
        tx_from = tr.select_one(".CroppedTxWithLink__link.CroppedTxWithLink__link--success").text
        tx_to = tr.select_one(".CroppedTxWithLink__link.CroppedTxWithLink__link--dimmed").text
        tx_type = tr.select_one(".Tooltip__tooltip.Tooltip__tooltip--bottom-left").text
        tx_amount = be_int(tr.select(".ValueWithUnit__value.ValueWithUnit__value--table")[0].text)
        tx_fee = tr.select(".ValueWithUnit__value.ValueWithUnit__value--table")[2].text
        
        
        if tx_in_out == 'OUT':
            tx_amount = tx_amount*-1
        else:
            pass
        
        if tx_amount > 90000 and tx_hash not in df_tx_list.index:
            #do.. some action
            # print(block_num)
            # print(tx_hash)
            # print(tx_type)
            # print(tx_amount)
            # print(tx_fee)
            bot.sendMessage(chat_id = chat_id, text ='observer가 뭔가 중대한 거래를 발견했습니다.(유입)')
            bot.sendMessage(chat_id = chat_id, text =tx_time+ "/ " + str(block_num) + "/ " + str(tx_amount) )


        # if tx_amount < -20000 and tx_hash not in df_tx_list.index:
        #     bot.sendMessage(chat_id = chat_id, text ='observer가 뭔가 중대한 거래를 발견했습니다.(인출)')
        #     bot.sendMessage(chat_id = chat_id, text =tx_time+ "/ " + str(block_num) + "/ " + str(tx_amount) )


        if tx_hash not in df_tx_list.index:
            df_tx_list.loc[tx_hash] = { 'block_num' : block_num, 'tx_time' : tx_time, 'tx_from' : tx_from , 'tx_to' : tx_to, 'tx_amount' :tx_amount , 'tx_fee' : tx_fee }  

    return df_tx_list





def be_int(value):
    value = value.replace(',', '')

    new_str = ''
    for char in value:
        if char != '.':
            new_str+=char
        else:
            break
    
    return int(new_str)



def do_job():

    # 우선 테스트 봇이니까 가장 마지막으로 bot에게 말을 건 사람의 id를 지정해줄게요.
    # 만약 IndexError 에러가 난다면 봇에게 메시지를 아무거나 보내고 다시 테스트해보세요.

    max_try_count = 10000000
    curr_try_count = 0



    while curr_try_count <  max_try_count:
        curr_try_count+= 1
        print("크롤링 수행 중 ",curr_try_count,"회 차")
        
        # if curr_try_count % 360 ==0:
        #     bot.sendMessage(chat_id = chat_id, text ='observer는 열일 중.. ' +str(curr_try_count))

        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")

        #driver = webdriver.Chrome('/Users/heine/Downloads/chromedriver_win32/chromedriver',chrome_options=options )
        driver = webdriver.Chrome('chromedriver',options=options )

 
        driver.implicitly_wait(3)
        driver.get('https://scope.klaytn.com/account/0x2968c66f14308673c12812febfa58cfe87c4e5a8?tabId=txList')
        html = driver.page_source

        
        soup = BeautifulSoup(html, 'html.parser')

        div_Table__tr = soup.select(".Table__tr")

        try:
            df_tx_list = pd.read_csv(path_csv_file_name, index_col =0 )

        except:
            temp_dic = { 'dummy' : { 'block_num' : 0,'tx_time' : 0, 'tx_from' : 0 , 'tx_to' :0, 'tx_amount' : 0 , 'tx_fee' : 0}  }
            df_tx_list =  pd.DataFrame.from_dict(temp_dic, orient ='index')
            df_tx_list= df_tx_list.drop('dummy')


        #df_tx_list = data_listing(div_Table__tr, df_tx_list, bot, chat_id )
        # print(df_tx_list)


        driver.close()
        df_tx_list.to_csv(path_csv_file_name)

        time.sleep(30)




if __name__ == "__main__":

    do_job()


