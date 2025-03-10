import time, json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from termcolor import colored



#initiate web driver
options = Options()
web = webdriver.Chrome(options=options)

#maximize window
web.maximize_window()


# initialize website cookies & cache
web.get('https://dorar.net/en/ahadith')

time.sleep(1)


# looping through all pages
pagination_start = 1
pagination_end = 91

i = pagination_start

number = 1

JSON = []

while True:

    web.get(f"https://dorar.net/en/ahadith?activeTab=panel-1&page={i}")

    body = web.find_element(By.CSS_SELECTOR, 'body')

    # scroll down & up to trigger lazy load.
    body.send_keys(Keys.END)
    time.sleep(1)
    body.send_keys(Keys.HOME)

    web.execute_script("$('.card article.has-read-more').next().click();") # click 'more...' for all hadiths
    time.sleep(1)

    hadiths_count = web.execute_script("return $('.card article.has-read-more h5').length;") # get number of hadiths per page - for looping purposes

    for x in range(hadiths_count):
        hadith = web.execute_script(f"return $('.card article.has-read-more h5').eq({x}).text().trim();");
        commentary = web.execute_script(f"return $('.card article.has-read-more p.card-text').eq({x}).text().replace('Commentary :', '').trim();");
        dict = {
            "number": number,
            "hadith": f"{hadith}",
            "commentary": f"{commentary}"
            }
        
        JSON.append(dict)
        number+=1

    
    print(colored(f"[PAGE {i}]", "green") + f" {hadiths_count} hadiths")

    if i==pagination_end: break # end loop when last page is reached

    i+=1

file = json.dumps(JSON)

f = open('bukhari.json', 'w')
f.write(file)
f.close()