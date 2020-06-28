from flask import Flask, render_template, jsonify, request
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import requests

app = Flask(__name__)

from pymongo import MongoClient          
client = MongoClient('localhost', 27017)  
# client = MongoClient('mongodb://test:test@localhost', 27017) 
db = client.dbsparta                      

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://new.land.naver.com/',headers=headers) # ???
soup = BeautifulSoup(data.text, 'html.parser')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/region', methods=['POST'])
def read_region():
   seoul_gu_receive = request.form['seoul_gu_give']
   seoul_dong_receive = request.form['seoul_dong_give']

   # 웹 브라우저를 띄우지 않는 headless chrome 옵션
   # chrome_options = webdriver.ChromeOptions() 
   # chrome_options.add_argument('headless')
   # chrome_options.add_argument('--disable-gpu')
   # chrome_options.add_argument('lang=ko_KR')
   # driver = webdriver.Chrome('C:\chromedriver_win32\chromedriver.exe', chrome_options=chrome_options)

   driver = webdriver.Chrome('C:\chromedriver_win32\chromedriver.exe')
   driver.implicitly_wait(3)
   driver.get('https://new.land.naver.com/')
   driver.find_element_by_xpath("//div[@class='filter_area filter_area--apart']//button[2]").click() # 아파트분양권 체크해제
   driver.find_element_by_xpath("//div[@class='filter_area filter_area--apart']//button[3]").click() # 재건축 체크해제 
   driver.find_element_by_xpath("//div[@class='map_controls_wrap']//a[1]").click() #개발 체크해제
   driver.implicitly_wait(2)  

   driver.find_element_by_xpath("//div[@class='filter_region_inner']//a//span[1]").click() #지역선택(도) 
   driver.find_element_by_xpath("//ul[@class='area_list--district']//li[1]").click() # 서울시 선택 
   time.sleep(1)

   gu_names = driver.find_element_by_css_selector(".area_list--district").find_elements_by_tag_name("li")
   count_gu = 0
   for gu_n in gu_names:
      gu = gu_n.text
      c1 = count_gu + 1
      if seoul_gu_receive == gu :
         driver.find_element_by_xpath("//ul[@class='area_list--district']//li['c1']").click() # ??? li[숫자]인식불가 (강남구)
         break
   
   time.sleep(2)

   dong_names = driver.find_element_by_css_selector(".area_list--district").find_elements_by_tag_name("li")
   print(dong_names)
   count_dong = 0
   for dong_n in dong_names:
      dong = dong_n.text
      print(dong)
      c2 = count_dong + 1
      if seoul_dong_receive == dong : 
         driver.find_element_by_xpath("//ul[@class='area_list--district']//li[1]").click() # ??? li[숫자]인식불가 (개포동)
         break

   driver.find_element_by_xpath("//ul[@class='area_list--complex']//li[1]").click() # lg자이 선택 

   # soup 사용하여 단지정보 불러옴, data = requests.get('https://new.land.naver.com/ 확인필요 

   apt_title = soup.select('div.complex_title > h3').text # 아파트명 db에 저장 
   apt_num = soup.select('info_table_wrap > tbody > tr > td[1]') # 세대수 
   db.apt.insert_one({
      'apt_title_db': apt_title,
      'apt_num_db': apt_num
   })
   complext_list = soup.select('#articleListArea')

   for c_list in complext_list:
      item_name = c_list.select_one('item_inner > a > item_title').text
      price = c_list.select_one('item_inner > a > price_line').text
      info = c_list.select_one('item_inner > a > info_area > p > span').text 

      db.apt.insert_one({
         'item_db': item_name,
         'price_db': price,
         'info_db': info
      })

@app.route('/region', methods=['GET'])
def data_region():
    aptcontext = list(db.apt.find({}, {'_id': False}))
    data = {
        'result': 'success',
        'aptcontext': aptcontext,
    }
    return jsonify(data)
    # ({'result':'success', 'msg': '이 요청은 GET!'})

if __name__ == '__main__':  
   app.run('0.0.0.0', port=5000, debug=True)