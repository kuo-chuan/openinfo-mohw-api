from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

import os
import time
from fire import Fire

import pandas as pd
import logging
logging.basicConfig(format='%(asctime)s %(message)s')

options = webdriver.ChromeOptions()
options.page_load_strategy = 'none'
options.add_argument('blink-settings=imagesEnabled=false')
options.add_argument('--disable-images')
options.add_argument("headless")
path = os.path.join('datastore')
city_dic = {'臺北市': 1, '臺中市': 2, '臺南市': 3, '高雄市': 4, '基隆市': 5,
            '新竹市': 5, '嘉義市': 6, '新北市': 8, '桃園市': 9, '新竹縣': 10,
            '宜蘭縣': 11, '苗栗縣': 12, '彰化縣': 13, '南投縣': 14, '雲林縣': 15,
            '嘉義縣': 16, '屏東縣': 17, '澎湖縣': 18, '花蓮縣': 19, '臺東縣': 20,
            '金門縣': 21, '連江縣': 22}
kind_dic = {'地區醫院': 1, '區域醫院': 2, '醫學中心': 3}


def main(**parmas):
    logging.warning(f'載入網頁與設定!')
    city = parmas.get('city', '所有')
    basname = parmas.get('basname', '')
    basid = parmas.get('basid', '')
    kind = parmas.get('kind', '')
    page = parmas.get('page', 1)
    url = "https://openinfo.mohw.gov.tw/"
    chrome = webdriver.Chrome(options=options)
    chrome.get(url)
    time.sleep(2)
    if city != '所有':
        areaDropdown1 = chrome.find_element(By.ID, 'areaDropdown1')
        areaDropdown1.click()
        time.sleep(0.1)
        areaDrop1 = chrome.find_element(By.XPATH, f'//*[@id="areaDrop1"]/a[{city_dic[city]}]')
        areaDrop1.click()
        time.sleep(0.1)
    if basname != '':
        basName1 = chrome.find_element(By.XPATH, '//*[@id="basName1"]')
        basName1.clear()
        basName1.send_keys(basname)
    if basid != '':
        basAgencyId1 = chrome.find_element(By.XPATH, '//*[@id="basAgencyId1"]')
        basAgencyId1.clear()
        basAgencyId1.send_keys(basid)
    if kind != '':
        kindDropdown1 = chrome.find_element(By.ID, 'kindDropdown1')
        kindDropdown1.click()
        time.sleep(0.1)
        kindDrop1 = chrome.find_element(By.XPATH, f'//*[@id="kindDrop1"]/a[{kind_dic[kind]}]')
        kindDrop1.click()
        time.sleep(0.1)
    button = chrome.find_element(By.XPATH, '//*[@id="nav-home"]/div[2]/div/button')
    button.click()
    time.sleep(1)
    logging.warning(f'開始抓取{city}的醫院名單!')
    process_stop = 0
    if page < 0:
        page = 1
    while process_stop == 0:
        main_information = []
        for i in range(1, 6):
            if page > 1:
                try:
                    next = chrome.find_element(By.XPATH, '//*[@id="next"]/a/span')
                except:
                    process_stop = 1
                currentPage = chrome.find_element(By.XPATH, '//*[@id="currentPage"]')
                currentPage.clear()
                currentPage.send_keys(page)
                jump = chrome.find_element(By.XPATH, '//*[@id="jump"]')
                jump.click()
                time.sleep(0.5)

            # 醫院基本資料 頁面
            try:
                query = chrome.find_element(By.XPATH, f'//*[@id="queryListContainer"]/tr[{i}]/td[1]/button')
                query.click()
            except:
                process_stop = 1
                break
            time.sleep(1)

            BAS_ADDR = chrome.find_element(By.ID, 'BAS_ADDR').text
            BAS_CITY = BAS_ADDR[0:3]
            df = pd.DataFrame([{'機構代碼': chrome.find_element(By.ID, 'BAS_AGENCY_ID').text,
                                '權屬別': chrome.find_element(By.ID, 'AUTHOR_NAME').text,
                                '機構縣市': BAS_CITY,
                                '機構名稱': chrome.find_element(By.ID, 'BAS_NAME').text,
                                '機構地址': BAS_ADDR,
                                '身心障礙牙科特別門診': chrome.find_element(By.ID, 'SPC_DENTAL').text,
                                '身心障礙鑑定醫院': chrome.find_element(By.ID, 'HEART_HA').text,
                                '急救責任醫院': chrome.find_element(By.ID, 'EMERGENCY_HOS').text,
                                '24小時急診服務': chrome.find_element(By.ID, 'EMERGENCY_24H').text,
                                '院區': chrome.find_element(By.ID, 'ZONE_NAME').text,
                                '型態別': chrome.find_element(By.ID, 'TYPE_NAME').text,
                                '機構電話': chrome.find_element(By.ID, 'BAS_TEL_NO').text,
                                '負責人': chrome.find_element(By.ID, 'BAS_HAD_NAME').text,
                                '身心障礙牙科門診掛號電話': chrome.find_element(By.ID, 'SPC_DENTAL_TEL').text,
                                '女性整合門診': chrome.find_element(By.ID, 'LADY_COM').text,
                                '急診電話': chrome.find_element(By.ID, 'EMERGENCY_TEL').text}])
            # 設置科別
            checked_list = chrome.find_elements(By.CLASS_NAME, 'form-check-input')
            labels = chrome.find_elements(By.CLASS_NAME, 'form-check-label')
            SET_SUBJECTS = []
            for check, label in zip(checked_list, labels):
                if check.get_property('checked'):
                    SET_SUBJECTS.append(label.text)
            df['設置科別'] = str(SET_SUBJECTS).replace('[', '').replace(']', '').replace("'", '')

            # 病床設施
            collapseToggle = chrome.find_element(By.XPATH, '//*[@id="collapseToggle"]')
            collapseToggle.click()
            time.sleep(1)
            tds = chrome.find_elements(By.CLASS_NAME, 'text-center')
            index_name = tds[0].text
            bed_name = tds[1].text
            count = tds[2].text
            BED_FACILITIES = []
            for index in range(3, len(tds), 3):
                if tds[index].text == '':
                    break
                dic = {index_name: tds[index].text, bed_name: tds[index+1].text, count: tds[index+2].text}
                BED_FACILITIES.append(dic)

            df['病床設施'] = str(BED_FACILITIES).replace('[', '').replace(']', '')

            # 醫院人事數
            collapseToggle = chrome.find_element(By.XPATH, '//*[@id="collapse2Toggle"]')
            collapseToggle.click()
            time.sleep(1)
            df['西醫師'] = chrome.find_element(By.XPATH, '//*[@id="DOH_A"]').text
            df['中醫師'] = chrome.find_element(By.XPATH, '//*[@id="DOH_B"]').text
            df['牙醫師'] = chrome.find_element(By.XPATH, '//*[@id="DOH_C"]').text
            df['藥師'] = chrome.find_element(By.XPATH, '//*[@id="DOH_D"]').text
            df['藥劑師'] = chrome.find_element(By.XPATH, '//*[@id="DOH_E"]').text
            df['護產人員'] = chrome.find_element(By.XPATH, '//*[@id="DOH_F_G_H_I"]').text
            df['職能治療師'] = chrome.find_element(By.XPATH, '//*[@id="DOH_R"]').text
            df['職能治療生'] = chrome.find_element(By.XPATH, '//*[@id="DOH_W"]').text
            df['醫事檢驗師'] = chrome.find_element(By.XPATH, '//*[@id="DOH_J"]').text
            df['醫事檢驗生'] = chrome.find_element(By.XPATH, '//*[@id="DOH_K"]').text
            df['物理治療師'] = chrome.find_element(By.XPATH, '//*[@id="DOH_Q"]').text
            df['物理治療生'] = chrome.find_element(By.XPATH, '//*[@id="DOH_U"]').text
            df['醫事放射師'] = chrome.find_element(By.XPATH, '//*[@id="DOH_S"]').text
            df['醫事放射生'] = chrome.find_element(By.XPATH, '//*[@id="DOH_T"]').text
            df['諮商心理師'] = chrome.find_element(By.XPATH, '//*[@id="DOH_X"]').text
            df['臨床心理師'] = chrome.find_element(By.XPATH, '//*[@id="DOH_Y"]').text
            df['語言治療師'] = chrome.find_element(By.XPATH, '//*[@id="DOH_1"]').text
            df['聽力師'] = chrome.find_element(By.XPATH, '//*[@id="DOH_3"]').text
            df['呼吸治療師'] = chrome.find_element(By.XPATH, '//*[@id="DOH_V"]').text
            df['營養師'] = chrome.find_element(By.XPATH, '//*[@id="DOH_Z"]').text

            # 健保業務資料 頁面
            query = chrome.find_element(By.XPATH, '//*[@id="nav-2-tab"]')
            query.click()
            time.sleep(1)
            try:
                df['特約醫院'] = chrome.find_element(By.XPATH, '//*[@id="nhi"]/tr/td[1]').text
                df['全年門診人次'] = chrome.find_element(By.XPATH, '//*[@id="nhi"]/tr/td[2]').text
                df['全年住院人次'] = chrome.find_element(By.XPATH, '//*[@id="nhi"]/tr/td[3]').text
                df['全年急診人次'] = chrome.find_element(By.XPATH, '//*[@id="nhi"]/tr/td[4]').text
                df['平均住院日'] = chrome.find_element(By.XPATH, '//*[@id="nhi"]/tr/td[5]').text
            except:
                df['特約醫院'] = None
                df['全年門診人次'] = None
                df['全年住院人次'] = None
                df['全年急診人次'] = None
                df['平均住院日'] = None

            # 評鑑結果 頁面
            query = chrome.find_element(By.XPATH, '//*[@id="nav-3-tab"]')
            query.click()
            time.sleep(1)
            try:
                df['醫院評鑑結果'] = chrome.find_element(By.XPATH, '//*[@id="haName1"]').text
            except:
                df['醫院評鑑結果'] = None
            try:
                df['教學醫院評鑑結果'] = chrome.find_element(By.XPATH, '//*[@id="haName2"]').text
            except:
                df['教學醫院評鑑結果'] = None
            try:
                df['醫院評鑑改善事項數'] = chrome.find_element(By.XPATH, '//*[@id="ret-i"]').text
                df['已改善及改善中項數'] = chrome.find_element(By.XPATH, '//*[@id="ret-ii"]').text
                df['改善率'] = chrome.find_element(By.XPATH, '//*[@id="ret-ir"]').text
            except:
                df['醫院評鑑改善事項數'] = None
                df['已改善及改善中項數'] = None
                df['改善率'] = None

            main_information.append(df)
            chrome.back()
            time.sleep(1)
        result = pd.concat(main_information, ignore_index=True)
        result.to_csv(f'{path}/openinfo_mohw_page{page}.csv')
        logging.warning(f'第{page}頁已完成!')
        page += 1
    logging.warning(f'{city}醫院名單抓取已完成!')
    logging.warning(f'整合{city}醫院名單!')
    doc_list = os.listdir(path)
    result = []
    remove_list = []
    for doc in doc_list:
        if 'openinfo_mohw_page' in doc:
            df = pd.read_csv(f'{path}/{doc}', index_col=0)
            result.append(df)
            remove_list.append(doc)
    result = pd.concat(result, ignore_index=True)
    result.to_csv(f'{path}/{city}{basname}{basid}{kind}醫院評鑑資訊.csv')
    for doc in remove_list:
        os.remove(f'{path}/{doc}')


if __name__ == '__main__':
    Fire(main)
