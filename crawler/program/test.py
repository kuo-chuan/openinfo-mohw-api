import time

from selenium import webdriver
from selenium.webdriver.common.by import By

import unittest

import logging
logging.basicConfig(format='%(asctime)s %(message)s')
options = webdriver.ChromeOptions()
options.page_load_strategy = 'eager'
options.add_argument("headless")


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.driver = webdriver.Chrome(options=options)
        self.URL = "https://openinfo.mohw.gov.tw/"
        self.driver.get(self.URL)
        self.city = '臺中市'
        city_dict = {'臺北市': 1, '臺中市': 2, '臺南市': 3, '高雄市': 4, '基隆市': 5,
                     '新竹市': 5, '嘉義市': 6, '新北市': 8, '桃園市': 9, '新竹縣': 10,
                     '宜蘭縣': 11, '苗栗縣': 12, '彰化縣': 13, '南投縣': 14, '雲林縣': 15,
                     '嘉義縣': 16, '屏東縣': 17, '澎湖縣': 18, '花蓮縣': 19, '臺東縣': 20,
                     '金門縣': 21, '連江縣': 22}
        self.city_id = city_dict['臺中市']
        self.page = 1
        self.item = 1

    @classmethod
    def tearDownClass(self):
        self.driver.quit()

    def test_01_search(self):
        time.sleep(2)
        if self.city is not None:
            element = self.driver.find_element(By.ID, 'areaDropdown1')
            element.click()
            time.sleep(1)
            element = self.driver.find_element(By.XPATH, f'//*[@id="areaDrop1"]/a[{self.city_id}]')
            element.click()
            time.sleep(1)
        element = self.driver.find_element(By.XPATH, '//*[@id="nav-home"]/div[2]/div/button')
        element.click()
        time.sleep(2)

    def test_02_open_target_tab_01(self):
        element = self.driver.find_element(By.XPATH, f'//*[@id="queryListContainer"]/tr[{self.item}]/td[1]/button')
        element.click()
        time.sleep(2)
        # 醫院基本資料
        print('機構代碼: ', self.driver.find_element(By.ID, 'BAS_AGENCY_ID').text)
        print('權屬別: ', self.driver.find_element(By.ID, 'AUTHOR_NAME').text)
        print('機構名稱: ', self.driver.find_element(By.ID, 'BAS_NAME').text)
        print('機構地址: ', self.driver.find_element(By.ID, 'BAS_ADDR').text)
        print('機構縣市: ', self.driver.find_element(By.ID, 'BAS_ADDR').text[0:3])
        print('身心障礙牙科特別門診: ', self.driver.find_element(By.ID, 'SPC_DENTAL').text)
        print('身心障礙鑑定醫院: ', self.driver.find_element(By.ID, 'HEART_HA').text)
        print('急救責任醫院: ', self.driver.find_element(By.ID, 'EMERGENCY_HOS').text)
        print('24小時急診服務: ', self.driver.find_element(By.ID, 'EMERGENCY_24H').text)
        print('院區: ', self.driver.find_element(By.ID, 'ZONE_NAME').text)
        print('型態別: ', self.driver.find_element(By.ID, 'TYPE_NAME').text)
        print('機構電話: ', self.driver.find_element(By.ID, 'BAS_TEL_NO').text)
        print('負責人: ', self.driver.find_element(By.ID, 'BAS_HAD_NAME').text)
        print('身心障礙牙科門診掛號電話: ', self.driver.find_element(By.ID, 'SPC_DENTAL_TEL').text)
        print('女性整合門診: ', self.driver.find_element(By.ID, 'LADY_COM').text)
        print('急診電話: ', self.driver.find_element(By.ID, 'EMERGENCY_TEL').text)
        # 設置科別
        checked_list = self.driver.find_elements(By.CLASS_NAME, 'form-check-input')
        labels = self.driver.find_elements(By.CLASS_NAME, 'form-check-label')
        SET_SUBJECTS = []
        for check, label in zip(checked_list, labels):
            if check.get_property('checked'):
                SET_SUBJECTS.append(label.text)
        print('設置科別: ', str(SET_SUBJECTS).replace('[', '').replace(']', '').replace("'", ''))
        # 病床設施
        element = self.driver.find_element(By.XPATH, '//*[@id="collapseToggle"]')
        element.click()
        time.sleep(2)
        element = self.driver.find_elements(By.CLASS_NAME, 'text-center')
        index_name = element[0].text
        bed_name = element[1].text
        count = element[2].text
        BED_FACILITIES = []
        for index in range(3, len(element), 3):
            if element[index].text == '':
                break
            elements = {index_name: element[index].text, bed_name: element[index+1].text, count: element[index+2].text}
            BED_FACILITIES.append(elements)
        print('病床設施: ', str(BED_FACILITIES).replace('[', '').replace(']', ''))
        # 醫院人事數
        element = self.driver.find_element(By.XPATH, '//*[@id="collapse2Toggle"]')
        element.click()
        time.sleep(2)
        print('西醫師:', self.driver.find_element(By.XPATH, '//*[@id="DOH_A"]').text)
        print('中醫師:', self.driver.find_element(By.XPATH, '//*[@id="DOH_B"]').text)
        print('牙醫師:', self.driver.find_element(By.XPATH, '//*[@id="DOH_C"]').text)
        print('藥師:', self.driver.find_element(By.XPATH, '//*[@id="DOH_D"]').text)
        print('藥劑師:', self.driver.find_element(By.XPATH, '//*[@id="DOH_E"]').text)
        print('護產人員:', self.driver.find_element(By.XPATH, '//*[@id="DOH_F_G_H_I"]').text)
        print('職能治療師:', self.driver.find_element(By.XPATH, '//*[@id="DOH_R"]').text)
        print('職能治療生:', self.driver.find_element(By.XPATH, '//*[@id="DOH_W"]').text)
        print('醫事檢驗師:', self.driver.find_element(By.XPATH, '//*[@id="DOH_J"]').text)
        print('醫事檢驗生:', self.driver.find_element(By.XPATH, '//*[@id="DOH_K"]').text)
        print('物理治療師:', self.driver.find_element(By.XPATH, '//*[@id="DOH_Q"]').text)
        print('物理治療生:', self.driver.find_element(By.XPATH, '//*[@id="DOH_U"]').text)
        print('醫事放射師:', self.driver.find_element(By.XPATH, '//*[@id="DOH_S"]').text)
        print('醫事放射生:', self.driver.find_element(By.XPATH, '//*[@id="DOH_T"]').text)
        print('諮商心理師:', self.driver.find_element(By.XPATH, '//*[@id="DOH_X"]').text)
        print('臨床心理師:', self.driver.find_element(By.XPATH, '//*[@id="DOH_Y"]').text)
        print('語言治療師:', self.driver.find_element(By.XPATH, '//*[@id="DOH_1"]').text)
        print('聽力師:', self.driver.find_element(By.XPATH, '//*[@id="DOH_3"]').text)
        print('呼吸治療師:', self.driver.find_element(By.XPATH, '//*[@id="DOH_V"]').text)
        print('營養師:', self.driver.find_element(By.XPATH, '//*[@id="DOH_Z"]').text)

    def test_02_open_target_tab_02(self):
        # 健保業務資料 頁面
        element = self.driver.find_element(By.XPATH, '//*[@id="nav-2-tab"]')
        element.click()
        time.sleep(2)
        try:
            elements = {'特約醫院': self.driver.find_element(By.XPATH, '//*[@id="nhi"]/tr/td[1]').text,
                        '全年門診人次': self.driver.find_element(By.XPATH, '//*[@id="nhi"]/tr/td[2]').text,
                        '全年住院人次': self.driver.find_element(By.XPATH, '//*[@id="nhi"]/tr/td[3]').text,
                        '全年急診人次': self.driver.find_element(By.XPATH, '//*[@id="nhi"]/tr/td[4]').text,
                        '平均住院日': self.driver.find_element(By.XPATH, '//*[@id="nhi"]/tr/td[5]').text}
        except:
            elements = {'特約醫院': None,
                        '全年門診人次': None,
                        '全年住院人次': None,
                        '全年急診人次': None,
                        '平均住院日': None}
        finally:
            print('特約醫院: ', elements['特約醫院'])
            print('全年門診人次: ', elements['全年門診人次'])
            print('全年住院人次: ', elements['全年住院人次'])
            print('全年急診人次: ', elements['全年急診人次'])
            print('平均住院日: ', elements['平均住院日'])

    def test_02_open_target_tab_03(self):
        # 評鑑結果 頁面
        element = self.driver.find_element(By.XPATH, '//*[@id="nav-3-tab"]')
        element.click()
        time.sleep(2)
        try:
            print('醫院評鑑結果:', self.driver.find_element(By.XPATH, '//*[@id="haName1"]').text)
        except:
            print('醫院評鑑結果:', None)
        try:
            print('教學醫院評鑑結果:', self.driver.find_element(By.XPATH, '//*[@id="haName2"]').text)
        except:
            print('教學醫院評鑑結果:', None)
        try:
            print('醫院評鑑改善事項數:', self.driver.find_element(By.XPATH, '//*[@id="ret-i"]').text)
            print('已改善及改善中項數:', self.driver.find_element(By.XPATH, '//*[@id="ret-ii"]').text)
            print('改善率:', self.driver.find_element(By.XPATH, '//*[@id="ret-ir"]').text)
        except:
            print('醫院評鑑改善事項數:', None)
            print('已改善及改善中項數:', None)
            print('改善率:', None)

    def test_03_back_to_homepage(self):
        element = self.driver.find_element(By.XPATH, '//*[@id="bnBack"]')
        element.click()
        time.sleep(1)


if __name__ == '__main__':
    test_suite = unittest.defaultTestLoader.discover('crawler/program', pattern='*.py')
