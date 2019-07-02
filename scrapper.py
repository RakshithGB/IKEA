from selenium import webdriver
#from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
#from urllib.request import urlopen, Request
import os
import requests
import sys
import shutil
import re
import pyexcel as pe
from sys import platform

path = os.getcwd()
chrome_driver = None
slash = "/"
if platform == "darwin":
    chrome_driver = path+"/Driver/Mac/chromedriver"
elif platform == "win32":
    chrome_driver = path+"\\Driver\\Windows\\chromedriver.exe"
    slash = "\\"

keys=["chair","wardrobe","lamp", "bed"]
ignore=["cover", "pad", "legs", "base", "support", "beam", "box", "under", "canopy", "tent", "curtain", "frame", "pocket", "tray", "leg", "skirt", "sheet", "sleeper", "pillow", "headboard", "set","hinge","hanger","mirror","rail","glass","drawer","box","storage","driver","handle","piece","crib","canopy", "spread"]

url = "https://www.ikea.com"
query_url = "https://www.ikea.com/us/en/search/?query="
folder_name = "Downloads"

if(os.path.isdir(path+slash+folder_name)):
    print("directory exists: "+folder_name)
else:
    os.mkdir(path+slash+folder_name)
    print("created: "+folder_name)

products = []
names = []
MAX_ALLOWED_IMAGES = 200
image_count = 0
previous_name = ""

def Cloning(li1): 
    li_copy = list(li1) 
    return li_copy 

def requesthandle( link, name, key, description ):
    global image_count, previous_name, names
    if name == previous_name or name=="":
        return
    try:
        r = requests.get( link, stream=True )
        if r.status_code == 200:
            r.raw.decode_content = True
            #f = open(folder_name+slash+key+slash+ name, "wb" )
            f = open(path+slash+folder_name+slash+key+slash+str(image_count)+".jpg", "wb" )
            shutil.copyfileobj(r.raw, f)
            f.close()
            image_count+=1
            previous_name = name
            names.append(description)
            print("[*] Downloaded Image: %s" % name)
    except:
        print("[~] Error Occured with %s" % name)

def scrapePage(soup, key):
    global keys, names, ignore
    for a in soup.findAll('div', attrs={'class':'productContainer'}):
        name=a.find('img')
        desc = a.find('span', attrs={'class':'prodDesc'})
        li2 = Cloning(keys)+ignore
        li2.remove(key)
        if(name is not None):
            description = re.sub('[^A-Za-z]+', ' ', desc.text)
            for k in li2:
                if k in description.lower():
                    break
                if key in description.lower():
                    image_link = url+name['src']
                    #products.append(image_link)
                    try:
                        image_src = re.findall('/PIAimages/([^"]+)', image_link)
                        str1 = ''.join(image_src)
                        requesthandle(image_link,str1, key, description.lower() )
                        #names.append(desc.text.lower())
                    except Exception as e:
                        print(e)

options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(executable_path=chrome_driver, chrome_options=options)

for key in keys:
    names = []
    previous_name = ""
    image_count = 0
    if(os.path.isdir(path+slash+folder_name+slash+key)):
        print("directory exists: "+folder_name+slash+key)
    else:
        os.mkdir(path+slash+folder_name+slash+key)
        print("created: "+folder_name+slash+key)

    test = query_url+key
    driver.get(test)

    content = driver.page_source
    soup = BeautifulSoup(content)

    page = []

    if soup is not None:
        p = soup.find('div', attrs={'class':'pagination'})
        for pages in p.findAll('a', href=True):
                page.append(pages.text)

        #Compute max number of pages for the given key
        max_pages = int(page[len(page)-1])

        scrapePage(soup, key)

        i = 2
        while(i<=max_pages):
            #check = folder_name+slash+key
            if(image_count>=MAX_ALLOWED_IMAGES):
                break
            driver.get(test+"&pageNumber="+str(i))
            content = driver.page_source
            soup = BeautifulSoup(content)
            scrapePage(soup, key)
            i+=1
        products.append(names)

sheet = pe.Sheet(products)
sheet.save_as(path+slash+"products.csv")
driver.close()

