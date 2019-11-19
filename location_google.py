from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
def distance_google(location_from, location_where):
    l_from = location_from
    l_where = location_where
    driver = webdriver.Chrome()
    driver.get('https://www.google.ru/maps/')

    itinerary = driver.find_element_by_xpath('//*[@id="searchbox-directions"]')
    itinerary.click() #допилить чтоб драйвер не ждал загрузку всей страницы
    time.sleep(5)

    departure_input = driver.find_element_by_xpath('//*[@id="sb_ifc51"]/input')
    departure_input.send_keys(l_from)
    time.sleep(3)

    destination_input = driver.find_element_by_xpath('//*[@id="sb_ifc52"]/input')
    destination_input.send_keys(l_where)
    time.sleep(3)
    destination_input.send_keys(Keys.ENTER)
    time.sleep(10)
    t = driver.find_element_by_xpath('//*[@id="section-directions-trip-0"]/div[2]/div[1]/div[1]/div[2]/div')
    print(t.text)
    input()

    '''
    departure_input = driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[1]/div[1]/div/div/div/div/div/div/div[1]/div/div/div[3]/div/form/div[2]/div/div/div[1]/div/div[2]/div/span/span[1]/input')
    departure_input.click()
    departure_input.send_keys(l_from)
    time.sleep(10.0)
    input()

    destination_input = driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[1]/div[1]/div/div/div/div/div/div/div[1]/div/div/div[3]/div/form/div[2]/div/div/div[2]/div/div[2]/div/span/span[1]/input')
    destination_input.send_keys(l_where)
    time.sleep(10.0)
    input()
    
    distance = 
    return ('Расстояние между {} {} {}'.format(distance,l_from,l_where))
    '''
distance_google('альметьевск', 'казань')