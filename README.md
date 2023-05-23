# [醫院評鑑資訊專區API](https://openinfo.mohw.gov.tw/)

---
API提供完整的醫院基本資料、健保業務資料與評鑑結果。

---

## 使用說明

```
# 功能測試
python -m unittest crawler/program/test.py

# 爬取網頁
python crawler/program/run.py
python crawler/program/run.py --city 臺中市 --kind 醫學中心
```
#### 參數說明
`--city`
縣市別

`--basname`
醫事機構名稱

`--basid`
醫事機構代碼

`--kind`
特約類別

`--page`
開始抓取頁數

--------
#### 縣市列表

北部:
`臺北市`, `新北市`, `新竹縣`, `桃園市`, `基隆市`, `新竹市`, `宜蘭縣`

中部:
`臺中市`, `彰化縣`, `南投縣`, `苗栗縣`, `雲林縣`

南部:
`臺南市`, `高雄市`, `嘉義市`, `嘉義縣`, `屏東縣`

東部: `臺東縣`, `花蓮縣`

外島:
`澎湖縣`, `金門縣`, `連江縣`
--------
#### 特約列表

`地區醫院`,
`區域醫院`,
`醫學中心`

--------
## 資料格式

```
機構代碼: float64
權屬別: object
機構縣市: object
機構名稱: object
機構地址: object
身心障礙牙科特別門診: object
身心障礙鑑定醫院: object
急救責任醫院: object
24小時急診服務: object
院區: object
型態別: object
機構電話: object
負責人: object
身心障礙牙科門診掛號電話: object
女性整合門診: object
急診電話: object
設置科別: object
病床設施: object
西醫師: int64
中醫師:  int64
牙醫師: int64
藥師: int64
藥劑師: int64
護產人員: int64
職能治療師: int64
職能治療生: int64
醫事檢驗師: int64
醫事檢驗生: int64
物理治療師: int64
物理治療生: int64
醫事放射師: int64
醫事放射生: int64
諮商心理師: int64
臨床心理師: int64
語言治療師: int64
聽力師: int64
呼吸治療師: int64
營養師: int64
特約醫院: object
全年門診人次: float64
全年住院人次: float64
全年急診人次: float64
平均住院日: float64
醫院評鑑結果: object
教學醫院評鑑結果: object
醫院評鑑改善事項數: object
已改善及改善中項數: object
改善率: object
```
```
# 範例
head example.csv
```
### 醫院基本資料

<table>
  <tr>
    <td>機構代碼</td>
    <td>權屬別</td>
    <td>機構名稱</td>
    <td>機構地址</td>
    <td>機構縣市</td>
    <td>院區</td>
    <td>型態別</td>
    <td>機構電話</td>
    <td>負責人</td>
    <td>身心障礙牙科特別門診</td>
    <td>身心障礙鑑定醫院</td>
    <td>急救責任醫院</td>
    <td>24小時急診服務</td>
    <td>身心障礙牙科門診掛號電話</td>
    <td>女性整合門診</td>
    <td>急診電話</td>
  </tr>
  <tr>
    <td>0617060018</td>
    <td>榮民醫院</td>
    <td>臺中榮民總醫院</td>
    <td>臺中市西屯區臺灣大道4段1650號</td>
    <td>臺中市</td>
    <td>本院</td>
    <td>綜合醫院</td>
    <td>04 23592525</td>
    <td>陳適安</td>
    <td>是</td>
    <td>是</td>
    <td>是</td>
    <td>是</td>
    <td>否</td>
    <td>是</td>
    <td>是</td>
  </tr>
</table>

<table>
  <tr>
    <td>設置科別</td>
    <td>病床設施</td>
  </tr>
  <tr>
    <td>'家庭醫學科, 內科, 外科, 兒科, 婦產科, 骨科...'
    <td>"{'項次': '1', '病床名稱': '急性一般病床', '病床數': '975'}, {'項次': '2', '病床名稱': '精神急性一般病床', '病床數': '70'}, {'項次': '3', '病床名稱': '正壓隔離病床', '病床數': '14'}..."</td>
  </tr>
</table>

### 醫院人事數

<table>
    <tr>
        <td>西醫師</td>
        <td>中醫師</td>
        <td>牙醫師</td>
        <td>藥師</td>
        <td>藥劑師</td>
        <td>護產人員</td>
        <td>職能治療師</td>
        <td>職能治療生</td>
        <td>醫事檢驗師</td>
        <td>醫事檢驗生</td>
        <td>物理治療師</td>
        <td>物理治療生</td>
        <td>醫事放射師</td>
        <td>醫事放射生</td>
        <td>諮商心理師</td>
        <td>臨床心理師</td>
        <td>語言治療師</td>
        <td>聽力師</td>
        <td>呼吸治療師</td>
        <td>營養師</td>
    </tr>
    <tr>
        <td>866</td>
        <td>15</td>
        <td>43</td>
        <td>126</td>
        <td>0</td>
        <td>2216</td>
        <td>14</td>
        <td>0</td>
        <td>193</td>
        <td>1</td>
        <td>24</td>
        <td>0</td>
        <td>151</td>
        <td>0</td>
        <td>4</td>
        <td>10</td>
        <td>6</td>
        <td>4</td>
        <td>29</td>
        <td>22</td>
    </tr>
</table>

### 健保業務資料

<table>
  <tr>
    <td>特約醫院</td>
    <td>全年門診人次</td>
    <td>全年住院人次</td>
    <td>全年急診人次</td>
    <td>平均住院日</td>
  </tr>
  <tr>
    <td>醫學中心</td>
    <td>1694377</td>
    <td>60392</td>
    <td>55347</td>
    <td>7</td>
  </tr>
</table>

### 醫院評鑑結果

<table>
  <tr>
    <td>醫院評鑑結果</td>
    <td>教學醫院評鑑結果</td>
    <td>醫院評鑑改善事項數</td>
    <td>已改善及改善中項數</td>
    <td>改善率</td>
  </tr>
  <tr>
    <td>醫院評鑑優等（醫學中心）</td>
    <td>醫師及醫事人員類教學醫院評鑑合格（醫學中心）</td>
    <td>1</td>
    <td>1</td>
    <td>100%</td>
  </tr>
</table>