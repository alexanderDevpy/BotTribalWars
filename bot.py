from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
import time
import xml.etree.ElementTree as ET
import random
import requests
from bs4 import BeautifulSoup
import re


def timpComenzi():
    '''

    :return random time between commands

    '''
    timp_intre_comenzi = random.randint(5, 25)
    return timp_intre_comenzi


class BotTriburile:

    def __init__(self, username, password, word):
        self.username = username
        self.password = password
        

        try:
            self.bot = webdriver.Firefox(executable_path=r'geckodriver.exe')
        except Exception as e:
            print(e)
        self.word = word
        print('Is working')
        self.urls = ['overview', 'place', 'barracks', 'train','main','smith','storage','market','farm','wall','hide']
        self.comands = {'overview': 'overview', 'place': 'place', 'barracks': 'barracks', 'train': 'train'}

    def login(self):
        '''
        Log to the game

        '''
        global work_url
        try:
            bot = self.bot
            bot.get('https://www.triburile.ro/')
        except WebDriverException as e:
            print('check the internet')
        time.sleep(timpComenzi())
        user = bot.find_element_by_name('username')
        password = bot.find_element_by_id('password')
        user.clear()
        password.clear()
        user.send_keys(self.username)
        password.send_keys(self.password)
        password.send_keys(Keys.ENTER)
        time.sleep(timpComenzi())
        bot.get('https://www.triburile.ro/page/play/' + self.word)
        time.sleep(2)
        general = bot.find_element_by_class_name('overview')
        time.sleep(1)
        general.click()
        try:
            bot.find_element_by_class_name('quickedit-label').click()
        except Exception as e:
            print(e)



        time.sleep(3)



        time.sleep(3)
        work_url = bot.current_url
        print(work_url)

    def atac(self):
        """
        get coordinates from whitelist.txt

        """
        time.sleep(3)
        bot = self.bot
        yes = [work_url.replace(s, self.comands["place"]) for s in self.urls if s in work_url]
        print(yes[0])
        bot.get(yes[0])
        time.sleep(timpComenzi())
        tinta = open('whitelist.txt', 'r')

        # Create a list with coordinates from whitelist
        l = []
        for line in tinta:
            li = line.strip()
            if li.startswith('#'):
                continue
            else:
                l.append(line.strip())
        tinta.close()

        self.send_atack(l)


    def barbari(self, distanta):
        """
         get coordinates from barbarii.txt
         and the distance from barbarian villages

         """

        bot = self.bot

        yes = [work_url.replace(s, self.comands["place"]) for s in self.urls if s in work_url]
        print(yes[0])
        bot.get(yes[0])
        self.scanbarbari()
        time.sleep(timpComenzi())
        tinta = open('barbarii.txt', 'r')

        l = []
        print(distanta)
        for x in tinta:
            atacuri = x.split()
            # Ver distance
            if float(atacuri[0]) <= int(distanta):
                l.append(atacuri[1])


        tinta.close()
        self.send_atack(l)

    def scanbarbari(self):
        '''
        Scan for barbarian villages on twstats.com and create a file barbarii.txt with all coordinates and distance

        '''


        url = 'https://ro.twstats.com/' + self.word + '/index.php?page=village_locator&stage=4&source=player&village_coords=500|500&searchstring=' + self.username + '&tribe_id=0&filter=abandoned'
        res = requests.get(url)
        html_page = res.content
        soup = BeautifulSoup(html_page, 'html.parser')
        satele = []

        table = soup.find_all('tr', {'class': ['r1', 'r2']})

        r = re.compile(r"\d\d\d[|]\d\d\d")

        f = open('barbarii.txt', 'w')
        for x in table:
            distanta = x.findChildren('td')[1:2]
            barbarii = x.findChildren('td')[5:6]
            for y in distanta:

                for z in barbarii:
                    temp = []
                    temp.append(y.text.replace(',', '.'))
                    temp.append(str(r.findall(z.text)).replace('[', '').replace(']', '').replace("'", ''))
                    satele.append(temp)
                    f.write(y.text.replace(',', '.'))
                    f.write(' ')
                    f.write(str(r.findall(z.text)).replace('[', '').replace(']', '').replace("'", ''))
                    f.write('\n')

        f.close()

    def baraca(self):
        '''
        Go to barrack and make troops from train.xml

        '''

        bot = self.bot
        yes = [work_url.replace(s, self.comands["train"]) for s in self.urls if s in work_url]
        print(yes[0])
        bot.get(yes[0])
        tree = ET.parse('train.xml')
        root = tree.getroot()
        resurse = self.rss()
        print(resurse)
        buff = self.buffer()
        print(buff)
        # Check to see if rss are more that buffer
        if buff['wood'] < int(resurse['wood']) and buff['stone'] < int(resurse['stone']) and buff['iron'] < int(
                resurse['iron']):
            for unitati in root.iter('units'):
                for trupe in unitati:
                    time.sleep(timpComenzi())
                    try:

                        trop = bot.find_element_by_name(trupe.tag)
                        trop.clear()
                        trop.send_keys(Keys.PAGE_DOWN)
                        trop.send_keys(trupe.text)
                    except Exception as e:
                        print(e)


                try:
                    press = bot.find_element_by_class_name("btn-recruit")
                    print(timpComenzi())
                    time.sleep(timpComenzi())
                    print(timpComenzi())
                    press.click()
                except Exception as e:
                    print(e)

    def rss(self):
        #find the filed where rss are stored
        bot = self.bot
        resurse = {'wood': bot.find_element_by_id('wood').text, 'stone': bot.find_element_by_id('stone').text,
                   'iron': bot.find_element_by_id('iron').text}
        return resurse

    def buffer(self):
        # get the buffer rss from train.xml
        tree = ET.parse('train.xml')
        root = tree.getroot()
        drec = {}
        for ele in root.iter('buffer'):

            for x in ele:
                drec[x.tag] = int(x.text)
        return drec

    def send_atack(self, coord):
        '''
        sent atack at coord from  barbarian or whitelist

        '''


        bot = self.bot

        e = ET.parse('farm.xml')
        root = e.getroot()

        for atacuri in coord:


            coordonate = bot.find_element_by_name('input')
            time.sleep(2)
            # imitate the human typing sending char one by one
            for cara in atacuri:
                coordonate.send_keys(str(cara))
                time.sleep(0.3)

            time.sleep(0.3)
            for elemente in root:

                numaratoare = 0


                # exit from loop
                running = False
                time.sleep(0.3)

                for subelement in elemente:
                    unit = bot.find_element_by_name(subelement.tag)
                    nr_unit = bot.find_element_by_id('units_entry_all_'+str(subelement.tag)).text
                    if int(nr_unit.replace("(", "").replace(")", "")) >= int(subelement.text):
                        unit.clear()
                        time.sleep(2)
                        unit.send_keys(subelement.text)
                        numaratoare +=1

                    else:

                        continue
                    print(len(elemente))
                    print(numaratoare)
                    if numaratoare == len(elemente):  # send attack if the troops are the same with farm.xml
                        running = True
                        try:
                            atac = bot.find_element_by_name('attack')
                            atac.click()
                            time.sleep(3)
                            trimite = bot.find_element_by_name('submit')
                            trimite.click()
                        except Exception as e:
                            print(e)
                        time.sleep(3)
                        bot.refresh()
                        time.sleep(3)
                try:
                    unit.clear()
                except Exception as e:
                    print(e)
                if running:  # exit from loop if the troops are not enough
                    break