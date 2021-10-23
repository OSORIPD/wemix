from os import times
from numpy import concatenate
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import time
import telegram as tel
import pandas as pd 

path_csv_file_name = "wemixscope_wemixcredit_test.csv"


def data_listing(unit_info, df_info_list):
    # print("unit_info \n",unit_info )        
    
    curr_time = get_time()
    print("curr_time:",curr_time)


    total_supply = get_quantity_credit(unit_info[4].text)
    print("total supply\n",total_supply)

  
    var_supply = total_supply - df_info_list.iloc[-1,1]


    print("var_supply\n",var_supply)


    total_holder = be_int(unit_info[5].text)
    print("total_holder\n",total_holder)

    var_holder = total_holder - df_info_list.iloc[-1,3]
    print("var_holder\n",var_holder)


    total_transfer = get_quantity_transfer(unit_info[6].text)
    print("total_holder\n",total_transfer)

    var_transfer = total_transfer - df_info_list.iloc[-1,5]
    print("var_transfer\n",var_transfer)





    df_info_list.loc[curr_time] = { 'curr_time' : curr_time, 'total_supply' : total_supply, 'var_supply':var_supply, 'total_holder' : total_holder , 'var_holder' : var_holder ,  'total_transfer' : total_transfer ,'var_transfer' : var_transfer }  


    return df_info_list





def get_time():
    timeList = time.localtime()
    timeStr = timeList[0]*10000000000+timeList[1]*100000000+timeList[2]*1000000+timeList[3]*10000+timeList[4]*100+timeList[5]
    print(timeStr)
    return timeStr


def get_quantity_credit(value):
    value = value[:10]
    return be_int(value)

def get_quantity_transfer(value):
    value = value[:16]
    return be_int(value)


def be_int(value):
    value = value.replace(',', '')
    value = value.replace('.', '')
    value = value.replace('T', '')
    value = value.replace('r', '')
    value = value.replace('a', '')
    value = value.replace('n', '')
    value = value.replace('s', '')
    value = value.replace('f', '')
    value = value.replace('e', '')
    value = value.replace('r', '')
    value = value.replace('s', '')


    new_str = ''
    for char in value:
        if char != '.':
            new_str+=char
        else:
            break
    
    return int(new_str)



def do_job():
    bot.sendMessage(chat_id = chat_id, text ='wemixwallet tracing program has been started')

    max_try_count = 10000000
    curr_try_count = 0



    while curr_try_count <  max_try_count:
        curr_try_count+= 1
        print("프로그램 동작 시작 ....", curr_try_count)
        # if curr_try_count % 360 ==0:
        #     bot.sendMessage(chat_id = chat_id, text ='observer??? ?????? ???.. ' +str(curr_try_count))

        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")

        driver = webdriver.Chrome('chromedriver',options=options )
 
 
        driver.implicitly_wait(3)
        driver.get('https://scope.wemixnetwork.com/1002/token/0xc4cc7f623b1da486cb0ec7f6b15dabeb24b67368')

        element = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.CLASS_NAME, "token__info")))
        
        
        html = driver.page_source        
        soup = BeautifulSoup(html, 'html.parser')

        div_token__info =  soup.select("div.token__info > dl > dd ")
         
        try:
            df_info_list = pd.read_csv(path_csv_file_name, index_col =0 )

        except:
            temp_dic = { 'START_LINE' : { 'curr_time' : 0,'total_supply' : 0, 'var_supply':0, 'total_holder' : 0, 'var_holder':0, 'total_transfer' : 0, 'var_transfer':0 }}
            df_info_list =  pd.DataFrame.from_dict(temp_dic, orient ='index')
            #df_info_list= df_info_list.drop('START_LINE')


        df_info_list = data_listing(div_token__info, df_info_list)

        temp_var_supply = df_info_list.iloc[-1,2]
        print( "temp_var_supply " ,temp_var_supply)

        if temp_var_supply>3000:

            mess1 = []
            mess1.append('supply가 ')
            mess1.append(str(temp_var_supply))
            mess1.append(" 만큼 증가했습니다. [현재 유통량: ")
            mess1.append(str(df_info_list.iloc[-1,1]))
            mess1.append("]")
            mess1 = ''.join(mess1)
    
            bot.sendMessage(chat_id = chat_id, text =mess1 )


        if temp_var_supply<-3000:

            mess1 = []
            mess1.append('supply가 ')
            mess1.append(str(temp_var_supply))
            mess1.append(" 만큼 감소했습니다. [현재 유통량: ")
            mess1.append(str(df_info_list.iloc[-1,1]))
            mess1.append("]")
            mess1 = ''.join(mess1)
    
            bot.sendMessage(chat_id = chat_id, text =mess1 )


        driver.close()
        df_info_list.to_csv(path_csv_file_name)


        time.sleep(20)




if __name__ == "__main__":

    bot = tel.Bot(token='2062225545:AAGytzWEbs7_dzQK2aPV5FXjQCG5ucWq8uc')
    chat_id = 2031803571

    try:
        do_job()
    except: 
        bot.sendMessage(chat_id = chat_id, text ='wemixwallet tracing program has been terminated by error')

