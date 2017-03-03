from bs4 import BeautifulSoup, NavigableString, Tag

import time
while True:
    if time.strftime('%H',time.localtime()) =='16':
        print(123)
    else:
        print(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime()))
    time.sleep(3)
