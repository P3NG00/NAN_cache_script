from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import sys


url_gc = "https://www.geocaching.com/geocache/"
url = "https://witzabout.com/NAN/"
char_mapping = {
    "A": "1", "B": "2", "C": "3", "D": "4", "E": "5", "F": "6", "G": "7", "H": "8", "I": "9",
    "J": "1", "K": "2", "L": "3", "M": "4", "N": "5", "O": "6", "P": "7", "Q": "8", "R": "9",
    "S": "1", "T": "2", "U": "3", "V": "4", "W": "5", "X": "6", "Y": "7", "Z": "8",
    "a": "0", "b": "1", "c": "2", "d": "3", "e": "4", "f": "5", "g": "6", "h": "7", "i": "8", "j": "9",
    "k": "1", "l": "2", "m": "3", "n": "4", "o": "5", "p": "6", "q": "7", "r": "8", "s": "9",
    "t": "1", "u": "2", "v": "3", "w": "4", "x": "5", "y": "6", "z": "7"
}


if len(sys.argv) != 2:
    print("Usage: python convert.py <gc code>")
    sys.exit(1)

# get input string
gc = sys.argv[1]

# use output in selenium
driver_options = webdriver.EdgeOptions()
driver_options.add_argument("headless")
driver_options.add_argument("disable-gpu")
driver_options.add_argument("log-level=3")
driver = webdriver.Edge(driver_options)

try:
    # go to geocache page
    driver.get(url_gc + gc)
    # get cache title
    cache_title = driver.find_element(By.XPATH, '//*[@id="ctl00_ContentBody_CacheName"]').text[4:]
    if len(cache_title) > 12:
        cache_title = cache_title[:12]
    # convert title to code
    output_string = ""
    for c in cache_title:
        if c in char_mapping:
            output_string += char_mapping[c]
        else:
            output_string += c
    # get code from gc
    code = []
    for secret in driver.find_element(By.XPATH, '//*[@id="ctl00_ContentBody_LongDescription"]').find_elements(By.TAG_NAME, "img"):
        code.append(secret.get_attribute("src")[28:30])
    # go to site
    driver.get(url)
    # input code
    driver.find_element(By.XPATH, "/html/body/form/input").send_keys(output_string + Keys.RETURN)
    # read table
    table_rows = driver.find_element(By.XPATH, "/html/body/table/tbody").find_elements(By.TAG_NAME, "tr")
    header_values = [ None ]
    translation_values = {}
    for row in table_rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        # first row
        if row == table_rows[0]:
            for i in range(1, 8):
                header_values.append(int(cols[i].text))
        # all subsequent rows
        else:
            num = int(cols[0].text)
            for i in range(1, 8):
                id = cols[i].find_element(By.TAG_NAME, "img").get_attribute("src")[33:35]
                translation_values[id] = header_values[i] + num
    # iterate over code and get translation
    translation = ""
    for c in code:
        translation += str(translation_values[c])
    # print output
    print("Code: " + output_string)
    print(translation)
    print(f"{translation[0:2]}.{translation[2:5]} & {translation[5:7]}.{translation[7:10]}")
except:
    print("Error!")
finally:
    driver.quit()
