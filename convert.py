from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import sys

char_mapping = {
    "A": "1", "B": "2", "C": "3", "D": "4", "E": "5", "F": "6", "G": "7", "H": "8", "I": "9",
    "J": "1", "K": "2", "L": "3", "M": "4", "N": "5", "O": "6", "P": "7", "Q": "8", "R": "9",
    "S": "1", "T": "2", "U": "3", "V": "4", "W": "5", "X": "6", "Y": "7", "Z": "8",
    "a": "0", "b": "1", "c": "2", "d": "3", "e": "4", "f": "5", "g": "6", "h": "7", "i": "8", "j": "9",
    "k": "1", "l": "2", "m": "3", "n": "4", "o": "5", "p": "6", "q": "7", "r": "8", "s": "9",
    "t": "1", "u": "2", "v": "3", "w": "4", "x": "5", "y": "6", "z": "7"
}

# check arguments
if len(sys.argv) < 2:
    print("Usage: python convert.py <gc code(s)>")
    sys.exit(1)
# get gc code
gc_codes = sys.argv[1:]
# create browser
driver_options = webdriver.EdgeOptions()
driver_options.add_argument("headless")
driver_options.add_argument("disable-gpu")
driver_options.add_argument("log-level=3")
driver = webdriver.Edge(driver_options)
print("\nStarting...")

try:
    for gc in gc_codes:
        # get geocache site
        try:
            driver.get("https://www.geocaching.com/geocache/" + gc)
        except:
            raise Exception("Unable to create browser. (Offline?)")
        # get geocache title
        try:
            cache_title = driver.find_element(By.XPATH, '//*[@id="ctl00_ContentBody_CacheName"]').text
        except:
            raise Exception("Trouble retrieving cache title! (Invalid GC code?)")
        # check cache title
        if cache_title[:4] == "NAN ":
            print(f"\nSolving: {cache_title}")
            cache_title = cache_title[4:]
        else:
            raise Exception("Error: Not a NAN cache!")
        # convert title to code
        if len(cache_title) > 12:
            cache_title = cache_title[:12]
        print(f"Title to Convert: {cache_title}")
        converted_title = []
        for c in cache_title:
            converted_title.append(char_mapping[c])
        print(f"Converted Title: {converted_title}")
        # get secret from gc
        secret = []
        for element in driver.find_element(By.XPATH, '//*[@id="ctl00_ContentBody_LongDescription"]').find_elements(By.TAG_NAME, "img"):
            secret.append(element.get_attribute("src")[28:30])
        print(f"GC Page Secret: {secret}")
        # get table from witzabout using code to create translation values
        driver.get("https://witzabout.com/NAN/")
        driver.find_element(By.XPATH, "/html/body/form/input").send_keys(''.join(converted_title) + Keys.RETURN)
        table_rows = driver.find_element(By.XPATH, "/html/body/table/tbody").find_elements(By.TAG_NAME, "tr")
        header_values = [None]
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
        # use translation values to convert secret to numbers
        translation = []
        for c in secret:
            v = translation_values[c]
            if v < 0 or v > 9:
                raise Exception("Each coordinate number should return between 0 and 9 (inclusive). (THIS MIGHT BE A CODING ERROR!)")
            translation.append(v)
        print(f"Translation: {translation}")
        # print output
        # TODO get beginning coordinates from GC then replace with translated ends to print completed coordinates
        print(f"Coordinate Ends: {translation[0:2]}.{translation[2:5]} & {translation[5:7]}.{translation[7:10]}")
    print("\nDone!")
except Exception as e:
    print(f"\n UNEXPECTED ERROR: {e}")
finally:
    driver.quit()
