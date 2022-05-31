from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import date
import mail as Mail

url = 'http://bus.namhae.ac.kr/login/'

f = open('bus.txt', 'r')
text = f.read()
text = text.split('\n')

id = text[0]
pw = text[1]

seatNumList = []

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('disable-gpu')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.implicitly_wait(20)

driver.get(url=url)
driver.find_element(By.ID, 'user_id').send_keys(id)
driver.find_element(By.ID, 'user_pw').send_keys(pw)
driver.find_element(By.ID, 'user_pw').send_keys(Keys.ENTER)

while True:
    url = 'http://bus.namhae.ac.kr/'
    if(driver.current_url == url):
        break
print('{} 로그인 완료!'.format(id))
dateList = date.getBusDay()

index = 0
for dt in dateList:
    url = 'http://bus.namhae.ac.kr/reservation/real-time-reservation/'
    driver.get(url)

    driver.find_element(By.NAME, 'agree2').click()
    selectDate = Select(driver.find_element(By.NAME, 'date1'))
    selectDate.select_by_visible_text(dt)

    selectCourse = Select(driver.find_element(By.NAME, 'ext1'))

    text = ''
    print(dt, end=' ')
    if(index == 0):
        text = '[하교] 창원/김해(하교1차)'
        print('하교버스 예약')
    elif(index == 1):
        text = '[등교] 창원/김해(등교2차)'
        print('등교버스 예약')
        
    selectCourse.select_by_visible_text(text)

    selectBus = Select(driver.find_element(By.NAME, 'ext2'))
    selectBus.select_by_index(4)

    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.seat-wrapper.sold-out')))
    sleep(3)

    soldoutList = []
    seatList = []
    allSeats = driver.find_elements(By.CLASS_NAME, 'seat-wrapper')
    soldOutSeats = driver.find_elements(By.CSS_SELECTOR, '.seat-wrapper.sold-out')
    for seat in allSeats:
        seatNumber = seat.text        
        seatList.append(int(seatNumber))
    for seat in soldOutSeats:
        seatNumber = seat.text        
        soldoutList.append(int(seatNumber))
    resultList = list(set(seatList) - set(soldoutList))
    if(len(resultList) > 0):
        seatNum = resultList[0]
    else:
        seatNum = 0
    driver.find_element(By.ID, 'seat-wrapper-{}'.format(seatNum)).click()
    print('{}번 좌석'.format(seatNum))
    seatNumList.append(seatNum)
    driver.find_element(By.ID, 'submit_btn').click()

    WebDriverWait(driver, 60).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    alert.accept()

    index += 1
driver.quit()

subject = '남해대학교 버스 자동예약'
mailText = '''
[하교]{0} (금) 13:30 좌석번호: {1}\n
[등교]{2} (일) 18:56 좌석번호: {3}
'''.format(dateList[0], seatNumList[0], dateList[1], seatNumList[1])
Mail.Send(subject, mailText)