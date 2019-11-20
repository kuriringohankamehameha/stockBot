#!/usr/bin/env python3

import discord
import sys
import time
import os
import re

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

from PIL import Image
import datetime

from imgurpython import ImgurClient

import socket

try:
    filename = sys.argv[1]
    if filename == "slow":
        filename = "token.txt"
except:
    filename = "token.txt"

token = open(filename, "r").readline().strip()
if token == '':
    print('Error: Need a valid Discord Bot token inside token.txt. Get it from developer options and try again')
    exit(0)
client = discord.Client()

client_id = ''
client_secret = ''

with open('imgur_creds.txt', 'r') as f:
    for i, line in enumerate(f):
        if i == 0:
            client_id = line.strip()
        else:
            client_secret = line.strip()

if client_id == '' or client_secret == '':
    print('Error: Imgur tokens must be valid. Set them before running the bot.')
    exit(0)

WAIT_TIME = 17

SLOW_INTERNET = 0

try:
    if sys.argv[1] == "slow":
        SLOW_INTERNET = 12
except IndexError:
    SLOW_INTERNET = 0


##print("SLOW_INTERNET = " + str(SLOW_INTERNET))

# Change this to whatever your bot name is
BOT_NAME = "!stock"

BOT_IS_IDLE = True

GECKO_PATH = os.path.join(os.path.join(os.getcwd(), "geckodriver"), "geckodriver")

# Download Latest version of Chrome Driver and replace this with the necessary
# path
CHROME_DRIVER_PATH = GECKO_PATH

if not os.path.exists(os.path.join(os.getcwd(), 'screenshots')):
    os.mkdir('screenshots')


def upload_image(filename):
    # Account settings for imgur. Get these from the Imgur API
    client = ImgurClient(client_id, client_secret)
    image = client.upload_from_path(filename, anon=True)
    url = image['link']
    return url

class SGXScraper(object):
        def __init__(self, browser, company, time, message):
                self.browser = browser
                self.company = None
                self.message = message
                self.company_name= None
                code = None
                self.graph_time = time
                if self.graph_time not in ["1D","1W","1M","1Y","5Y"]:
                    self.graph_time = "1Y"
                self.SG_Q=[]
                self.headless = False
                self.embed_stats = None
                self.matches = {}

                if company == "":
                    print("Company Name not found. Please try again")

                elif company == "selectall":
                    self.company = ""
                    company =  ""
                    with open(os.path.join(os.getcwd(), "Listings", "sgx.csv"), "r") as file:
                        for line in file:
                            if self.company.lower() in line.split(",")[0].lower():
                                code = line.split(",")[0]
                                self.company_name = line.split(",")[1].strip()
                                self.matches[code] = self.company_name

                elif ((len(company) <= 5) and (company.isupper() or (re.match('^.*[0-9]+', company)))):
                    self.company = company
                    with open(os.path.join(os.getcwd(), "Listings", "sgx.csv"), "r") as file:
                        for line in file:
                            if self.company.lower() == line.split(",")[0].lower():
                                self.company_name = line.split(",")[1].strip()
                                self.matches[self.company] = self.company_name
                else:
                    with open(os.path.join(os.getcwd(), "Listings", "sgx.csv"), "r") as file:
                        for line in file:
                            if company.lower() in line.split(",")[1].lower():
                                code = line.split(",")[0]
                                self.company_name = line.split(",")[1].strip()
                                self.matches[code] = self.company_name

                    self.company = code
                    if self.company is None:
                        print("Company Name not found. Please try again")

        @client.event
        async def setupDrivers(self):
                if self.browser == "Firefox":
                        options = webdriver.FirefoxOptions()
                        options.headless = True
                        self.headless = options.headless
                        options.set_preference("dom.push.enabled", False)
                        self.driver = webdriver.Firefox(executable_path=GECKO_PATH, options=options)
                        self.driver.set_window_size(1080,966) # Set a headless window with MIN_RESOLUTION = (1000x900) for taking screenshots
                elif self.browser == "Chrome":
                        chrome_options = webdriver.ChromeOptions()
                        chrome_options.add_argument("--disable-infobars")
                        #chrome_options.add_argument("--window-size=1000,966")
                        self.driver = webdriver.Chrome(executable_path = CHROME_DRIVER_PATH,chrome_options=chrome_options)

        def take_screenshot(self, filename):
            current_dir = os.getcwd()
            os.chdir(current_dir + "/screenshots")

            timeline = {
                "1D":"/html/body/div[1]/main/div[1]/article/template-base/div/div/section[1]/div/sgx-widgets-wrapper/widget-securities-prices-and-chart/div[2]/div[2]/sgx-state-tabs/div/div/span[1]",
                "1W":"/html/body/div[1]/main/div[1]/article/template-base/div/div/section[1]/div/sgx-widgets-wrapper/widget-securities-prices-and-chart/div[2]/div[2]/sgx-state-tabs/div/div/span[2]",
                "1M":"/html/body/div[1]/main/div[1]/article/template-base/div/div/section[1]/div/sgx-widgets-wrapper/widget-securities-prices-and-chart/div[2]/div[2]/sgx-state-tabs/div/div/span[3]",
                "1Y":"/html/body/div[1]/main/div[1]/article/template-base/div/div/section[1]/div/sgx-widgets-wrapper/widget-securities-prices-and-chart/div[2]/div[2]/sgx-state-tabs/div/div/span[4]",
                "5Y":"/html/body/div[1]/main/div[1]/article/template-base/div/div/section[1]/div/sgx-widgets-wrapper/widget-securities-prices-and-chart/div[2]/div[2]/sgx-state-tabs/div/div/span[5]",
            }

            end_path = "]"

            if self.graph_time != "1Y":
                button = self.driver.find_element_by_xpath(timeline[self.graph_time])

                ActionChains(self.driver).move_to_element(button).click().perform()

                time.sleep(5)

            self.driver.save_screenshot(filename)

            element = self.driver.find_elements_by_class_name("highcharts-background")[0]
            #highcharts-26qoi1y-0 > svg > rect.highcharts-background
            location = element.location
            size = element.size

            im = Image.open(filename)


            left = location['x']
            top = location['y']
            right = location['x'] + size['width']
            bottom = location['y'] + size['height']

            if self.browser == "Chrome":
                #browser_navigation_panel_height = self.driver.execute_script('return window.outerHeight - window.innerHeight;')

                pixel_ratio = self.driver.execute_script("return window.devicePixelRatio")
                right = location['x'] + size['width']*pixel_ratio
                bottom = location['y'] + size['height']*pixel_ratio

            im = im.crop((left,top,right,bottom))
            im.save(filename)

            os.chdir(current_dir)

            self.SG_Q.append(filename)

        @client.event
        async def scrape_site(self):
                stock_market_limit = 1
                curr = 0

                url = "https://www2.sgx.com/securities/equities/" + self.company
                self.driver.get(url)
                time.sleep(WAIT_TIME + SLOW_INTERNET)

                cookies = "#gdpr-banner > div > button"
                try:
                    cookies = self.driver.find_elements_by_css_selector(cookies)[0]
                    ActionChains(self.driver).move_to_element(cookies).click().perform()
                except NoSuchElementException:
                    pass

                except IndexError:
                    pass

                #current_graph = self.driver.find_element_by_xpath("/html/body/div[1]/main/div[1]/article/template-base/div/div/section[1]/div/sgx-widgets-wrapper/widget-securities-prices-and-chart/div[2]/div[2]/sgx-state-tabs/div/div/span[4]")

                screenshot_name = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S") + ".png"

                overview = "/html/body/div[1]/main/div[1]/article/template-base/div/div/section[1]/div/sgx-widgets-wrapper/widget-stocks-company-data/div[1]/sgx-content-table/div/table/tbody"

                try:
                    overview = self.driver.find_element_by_xpath(overview)
                except NoSuchElementException:
                    time.sleep(SLOW_INTERNET)
                    try:
                        overview = self.driver.find_element_by_xpath(overview)
                    except NoSuchElementException:
                        try:
                            self.embed_stats = discord.Embed(title="Stock Market Analysis for " + self.company_name, color=0x00008b)

                            price = self.driver.find_elements_by_class_name("sgx-price-value")[0].text
                            change = self.driver.find_elements_by_class_name("sgx-price-change")[0].text

                            self.embed_stats.add_field(name="URL", value=url)

                            self.embed_stats.add_field(name="Price", value=price)
                            self.embed_stats.add_field(name="Price Change", value=change)

                            base = "/html/body/div[1]/main/div[1]/article/template-base/div/div/section[1]/div/sgx-widgets-wrapper/widget-securities-prices-and-chart/div[2]/div[1]/table/tbody/tr["
                            for i in range(1,9):
                                #print("i = " + str(i))
                                self.embed_stats.add_field(name=self.driver.find_element_by_xpath(base + str(i) + "]/th").text,value=self.driver.find_element_by_xpath(base + str(i) + "]/td").text)
                            self.graph_time = "1Y"
                            self.take_screenshot(screenshot_name)
                            return
                        except:
                            #print("Exception")
                            self.driver.quit()
                            return



                #overview_list = overview.find_elements_by_xpath(".//*")

                overview_path = "/html/body/div[1]/main/div[1]/article/template-base/div/div/section[1]/div/sgx-widgets-wrapper/widget-stocks-company-data/div[1]/sgx-content-table/div/table/tbody/tr["

                self.embed_stats = discord.Embed(title="Stock Market Analysis for " + self.company_name, color=0x00008b)

                self.embed_stats.add_field(name="URL", value=url)

                price = self.driver.find_elements_by_class_name("sgx-price-value")[0].text
                change = self.driver.find_elements_by_class_name("sgx-price-change")[0].text

                self.embed_stats.add_field(name="Price", value=price)
                self.embed_stats.add_field(name="Price Change", value=change)


                for i in range(1,8):
                        overview_element = overview_path + str(i) + "]/"
                        data_one = self.driver.find_element_by_xpath(overview_element + "td[1]").text
                        data_two = self.driver.find_element_by_xpath(overview_element + "td[2]").text
                        heading_one = self.driver.find_element_by_xpath(overview_element + "th[1]").text
                        heading_two = self.driver.find_element_by_xpath(overview_element + "th[2]").text
                        self.embed_stats.add_field(name= heading_one,value= data_one)
                        self.embed_stats.add_field(name= heading_two,value= data_two)

                if self.graph_time == "1Y":
                    self.take_screenshot(screenshot_name)

                #self.driver.get(url)
                #time.sleep(WAIT_TIME)

                quarters_path = "/html/body/div[1]/main/div[1]/article/template-base/div/div/section[1]/div/sgx-widgets-wrapper/widget-securities-prices-and-chart/div[2]/div[2]/div[1]/sgx-chart/div/svg/g[7]/g[6]"

                latest_quarter = "/html/body/div[1]/main/div[1]/article/template-base/div/div/section[1]/div/sgx-widgets-wrapper/widget-securities-prices-and-chart/div[2]/div[2]/div[1]/sgx-chart/div/svg/g[7]/g[6]"

                latest_quarter = []

                quarter_list = []

                curr_quarter = 1
                limit_reached = False

                while curr_quarter <= 4:
                    try:
                        latest_quarter = self.driver.find_elements_by_class_name("highcharts-label highcharts-point ");
                        latest_quarter = self.driver.find_elements_by_css_selector("g.highcharts-point:nth-child(" + str(curr_quarter) + ")")
                        latest_quarter_element = latest_quarter[0]
                        child = latest_quarter_element.find_elements_by_xpath(".//*")[1]

                    except IndexError:
                        if curr_quarter > 1:
                            limit_reached = True
                            #print("Limit reached at quarter = " + str(curr_quarter))
                        else:
                            #print("IndexError at " + str(curr_quarter))
                            break

                    except NoSuchElementException:
                        if curr + 1 < stock_market_limit:
                            curr += 1
                            continue
                        else:
                            #print("No element. Trying again..")
                            time.sleep(5)
                            try:
                                latest_quarter = self.driver.find_elements_by_class_name("highcharts-label highcharts-point ");
                                latest_quarter = self.driver.find_elements_by_css_selector("g.highcharts-point:nth-child(" + str(curr_quarter) + ")")
                                latest_quarter_element = latest_quarter[0]
                                child = latest_quarter_element.find_elements_by_xpath(".//*")[1]
                            except NoSuchElementException:
                                break

                    if not limit_reached:
                        quarter_list.append(child.text)

                        #print('curr_quarter = ' + str(curr_quarter))
                        #print("No of windows before click = " + str(len(self.driver.window_handles)))

                        ActionChains(self.driver).move_to_element(latest_quarter_element).click().perform()

                        self.driver.switch_to.window(self.driver.window_handles[0])
                        curr_quarter += 1
                        #print("No of windows = " + str(len(self.driver.window_handles)))

                    if limit_reached:
                        break

                curr_quarter -= 1

                header_list = []
                attachment_list = []

                curr = curr_quarter

                self.driver.switch_to.window(self.driver.window_handles[0])

                if self.graph_time != "1Y":
                    self.take_screenshot(screenshot_name)

                while curr > 0:
                    # Now, go to the PDF of the reports
                    #print("Curr = " + str(curr))
                    #print("Length is " + str(len(self.driver.window_handles)))
                    try:
                        self.driver.switch_to.window(self.driver.window_handles[curr])
                    except IndexError:
                        #print("Index Out of Bounds")
                        self.driver.quit()

                    time.sleep(1)

                    if SLOW_INTERNET > 0 and curr == curr_quarter:
                        time.sleep(SLOW_INTERNET)

                    header = "/html/body/form/div[2]/div/div[2]/h1"
                    header = self.driver.find_element_by_xpath(header).text

                    link_to_attachment = self.driver.find_element_by_xpath("/html/body/form/div[2]/div/div[2]/div[5]/dl/dd[1]/a").get_attribute("href")
                    header_list.append(header)
                    attachment_list.append(link_to_attachment)

                    curr -= 1

                self.driver.quit()

                index = 0

                for header, link_to_attachment in zip(header_list, attachment_list):
                    if index == 0:
                        self.embed_stats.add_field(name="Latest Quarter Results", value= "Quarter " + quarter_list[index])
                    else:
                        self.embed_stats.add_field(name="Previous Quarter Results", value= "Quarter " + quarter_list[index])

                    self.embed_stats.add_field(name="Report", value=link_to_attachment)

                    index += 1

        @client.event
        async def send_sg_photo(self):
            current_dir = os.getcwd()
            os.chdir(current_dir + "/screenshots")

            self.embed_stats.add_field(name=self.company_name + " Graph", value="Visualization over a period of " + self.graph_time)
            try:
                self.embed_stats.set_image(url=upload_image(os.getcwd() + "/" + self.SG_Q[0]))
            except:
                self.embed_stats.add_field(name="Image Not Uploaded",value="Server OverLoaded. Please try again later")
                os.chdir(current_dir)
                self.SG_Q = []
                return await self.message.channel.send(embed=self.embed_stats)

            await self.message.channel.send(embed=self.embed_stats)

            self.embed_stats = None
            #Delete the screenshot after upload
            try:
                os.remove(os.path.join(os.getcwd(), self.US_Q[0]))
            except:
                pass
            os.chdir(current_dir)
            self.SG_Q = []


class NYSEScraper(object):
        def __init__(self, browser, company, time, message):
                self.browser = browser
                self.company = None
                self.graph_time = time
                self.message = message
                self.company_name = None

                self.US_Q = []
                self.embed_stats = None
                self.gray_market = None

                # List the exceptions (Companies with <= 5 letters, like AT&T)
                self.exceptions = ["AT&T"]
                self.stock_market = None
                self.stock_code = None
                self.file_dict = {
                    os.path.join(os.getcwd(), "Listings", "nyse.csv") :"xnys",
                    os.path.join(os.getcwd(), "Listings", "NASDAQ.csv") :"xnas",
                    os.path.join(os.getcwd(), "Listings", "amex.csv"): "xase",
                    os.path.join(os.getcwd(), "Listings", "otcbb.csv"): "pinx"
                }

                self.matches = {}
                self.exchange = []

                if company == "":
                    print("Company Name not found. Please try again")

                elif company == "selectall":
                    self.company = ""
                    company =  ""
                    self.check_files_name(self.file_dict, company)

                elif ((len(company) <= 5) and (company.isupper() or (re.match('^.*[0-9]+', company)))):
                    self.company = company
                    self.check_files_code(self.file_dict, company)
                else:
                    self.company = company
                    self.check_files_name(self.file_dict, company)

                    # Exceptions
                    if company in self.exceptions:
                        self.company = "T"

                    if self.company_name is None:
                        print("Company Name not found. Please try again")

        def check_files_code(self, file_list, company):
            for filename in file_list:
                #print("Filename = " + filename)
                with open(filename, "r") as file:
                    for line in file:
                        if self.company.lower() == line.split(",")[0].lower():
                            self.company_name = line.split(",")[1].strip()
                            self.stock_code = file_list[filename]
                            self.matches[self.company] = self.company_name
                            self.exchange.append(filename.split(".")[0])

        def check_files_name(self, file_list, company):
            for filename in file_list:
                with open(filename, "r") as file:
                    for line in file:
                        if company.lower() in line.split(",")[1].lower():
                            self.company = line.split(",")[0]
                            self.company_name = line.split(",")[1].strip()
                            self.stock_code = file_list[filename]
                            self.matches[self.company] = self.company_name
                            self.exchange.append(filename.split(".")[0])

        @client.event
        async def setupDrivers(self):
                if self.browser == "Firefox":
                        options = webdriver.FirefoxOptions()
                        options.headless = True
                        options.set_preference("dom.push.enabled", False)
                        self.driver = webdriver.Firefox(executable_path=GECKO_PATH, options=options)
                elif self.browser == "Chrome":
                        chrome_options = webdriver.ChromeOptions()
                        chrome_options.add_argument("--disable-infobars")
                        chrome_options.add_argument("--window-size=1000,966")
                        self.driver = webdriver.Chrome(executable_path = CHROME_DRIVER_PATH,chrome_options=chrome_options)

        def take_screenshot(self, company_name, option, filename):
            current_dir = os.getcwd()
            os.chdir(current_dir + "/screenshots")

            base_path = "/html/body/div/div[1]/div/div[2]/div[3]/section[1]/div/button["
            timeline = {
                "1D":"1",
                "5D":"2",
                "15D":"3",
                "1M":"4",
                "3M":"5",
                "6M":"6",
                "1Y":"8",
                "3Y":"9",
                "5Y":"10",
            }
            end_path = "]"

            #open_chart = "/html/body/div[3]/main/div/div/div/div[2]/div/div[1]/section[1]/div/div[2]/div/div/div/div[1]/div/div[1]/div[2]/div[1]/div[1]/a/span"
            open_chart = self.driver.find_elements_by_class_name("chart-iframe-full-chart-label")[0]

            ActionChains(self.driver).move_to_element(open_chart).click().perform()

            time.sleep(4)
            time.sleep(7)

            full_chart = self.driver.find_element_by_xpath("//*[@id='sal-iframe-full-chart-modal']")
            full_chart = full_chart.find_elements_by_xpath(".//*")[1]
            chart_url = full_chart.get_attribute("src")

            self.driver.get(chart_url)
            time.sleep(7)

            button = self.driver.find_element_by_xpath(base_path + timeline[option] + end_path)
            button.click()

            time.sleep(2)

            self.driver.save_screenshot(filename)

            element = self.driver.find_element_by_xpath("/html/body/div/div[1]/div/div[3]/div[1]")
            location = element.location
            size = element.size

            im = Image.open(filename)

            left = location['x']
            top = location['y']
            right = location['x'] + size['width']
            bottom = location['y'] + size['height']

            if self.browser == "Chrome":
                #browser_navigation_panel_height = self.driver.execute_script('return window.outerHeight - window.innerHeight;')

                pixel_ratio = self.driver.execute_script("return window.devicePixelRatio")
                right = location['x'] + size['width']*pixel_ratio
                bottom = location['y'] + size['height']*pixel_ratio

            im = im.crop((left,top,right,bottom))
            im.save(filename)
            os.chdir(current_dir)
            self.US_Q.append(filename)

        @client.event
        async def scrape_site(self):
                stock_market_limit = 4
                curr = 0
                absolute_list = []
                percent_list = []
                self.gray_market = False

                self.embed_stats = discord.Embed(description="Stock Market Analysis for " + self.graph_time, color=0x00008b)

                while(True):
                    #print("Looping")
                    url = "https://www.morningstar.com/stocks/" + self.stock_code + "/" + self.company.lower() + "/quote.html"
                    self.driver.get(url)
                    time.sleep(5)

                    self.embed_stats.add_field(name="URL", value=url)

                    price_path = "//*[@id='message-box-price']"

                    try:
                        price = self.driver.find_element_by_xpath(price_path).text
                        self.gray_market = True
                    except NoSuchElementException:
                        if not self.gray_market:
                            self.stock_code = "grey"
                            self.gray_market = True
                            continue
                        else:
                            self.driver.quit()
                            self.gray_market = False
                            await self.message.channel.send("Not available in the current market. Company may be down")
                            break
                    if self.gray_market == True:
                        break

                self.gray_market = False


                if self.stock_code == "grey":
                    self.embed_stats.add_field(name="Warning", value="The data below is from a Grey Market")

                change_path = "//*[@id='message-box-percentage']"
                try:
                    change = self.driver.find_element_by_xpath(change_path).text
                except socket.error:
                    #print("Wrong URL Pal")
                    return

                percent_list.append(change.split(" | ")[1])
                absolute_list.append(change.split(" | ")[0])

                self.embed_stats.add_field(name="Company", value=self.company_name, inline=False)
                self.embed_stats.add_field(name="Price", value=price, inline=False)
                self.embed_stats.add_field(name="Absolute Change", value=absolute_list[0], inline=False)
                self.embed_stats.add_field(name="Percentage Change", value=percent_list[0], inline=False)

                base_path = "/html/body/div[1]/div/div/div[3]/main/div[2]/div/div/div[1]/sal-components/section/div/div/div[1]/div/div[2]/div/div/div/div[2]/ul/li["
                for i in range(1,13):
                    list_path = base_path + str(i) + "]/div/div["
                    heading = self.driver.find_element_by_xpath(list_path + "1]").text
                    data = self.driver.find_element_by_xpath(list_path + "2]").text
                    #heading = base_path[i-1].find_element_by_xpath(".//div[1]").get_attribute("innerHTML").strip()
                    #data = base_path[i-1].find_element_by_xpath(".//div[2]").get_attribute("innerHTML").strip()
                    ##print("Length = " + str(len(listing)))
                    #heading = listing[0].text
                    #data = listing[1].text
                    ##print(heading,data)
                    self.embed_stats.add_field(name=heading, value=data)

                screenshot_name = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S") + ".png"

                time.sleep(2)

                self.take_screenshot(self.company, self.graph_time, screenshot_name)

                self.driver.quit()

        @client.event
        async def send_us_photo(self):
            current_dir = os.getcwd()
            os.chdir(os.path.join(current_dir,  "screenshots"))

            self.embed_stats.add_field(name=self.company_name + " Graph", value="Visualization over a period of " + self.graph_time)
            self.embed_stats.set_image(url=upload_image(os.getcwd() + "/" + self.US_Q[0]))
            await self.message.channel.send(embed=self.embed_stats)
            self.embed_stats = None
            #Delete the screenshot after upload
            try:
                os.remove(os.path.join(os.getcwd(), self.US_Q[0]))
            except:
                pass
            os.chdir(current_dir)
            self.US_Q = []

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    global BOT_IS_IDLE
    print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")

    if (BOT_NAME + " help" in message.content):
        embed1 = discord.Embed(title="StockBot Help", description="", color=0x0000bb)
        embed1.add_field(name="Search USA Stocks", value=BOT_NAME + " US {company}")
        embed1.add_field(name="Search USA Stocks across a Time Period", value=BOT_NAME + " US {company} {time}\n")
        embed1.add_field(name="Time Period Options for USA: ", value="1D, 15D, 1M, 3M, 6M, 1Y, 3Y, 5Y")
        embed1.add_field(name="Example : ", value="'" + BOT_NAME + " US Apple Inc 1M'")
        embed1.add_field(name="View All USA Companies", value="'" + BOT_NAME + " US all'")
        embed2 = discord.Embed(title="StockBot Help", description="", color=0x0000eb)
        embed2.add_field(name="Search Singapore Stocks", value=BOT_NAME + " SG {company}")
        embed2.add_field(name="Search Singapore Stocks across a Time Period", value=BOT_NAME + " SG {company} {time}")
        embed2.add_field(name="Time Period Options for Singapore: ", value="1D, 1W, 1M, 1Y, 5Y")
        embed2.add_field(name="Example : ", value="'" + BOT_NAME + " SG Katrina Inc 1M'")
        embed2.add_field(name="View All Singapore Companies", value="'" + BOT_NAME + " SG all'")
        await message.channel.send(embed=embed1)
        await message.channel.send(embed=embed2)

    def check(msg):
        return msg.author == message.author

    if (BOT_NAME + " SG " in message.content and BOT_IS_IDLE == True):
        arg_list = message.content.split(BOT_NAME + " SG ")

        if(arg_list[1] == "" or message.content == BOT_NAME + " SG "):
            await message.channel.send("Bad Request")

        if arg_list[0] == "":
            time_limit = arg_list[1].split(" ")[-1]
            if time_limit == "":
                time_limit = "1Y"

            company_code = arg_list[1].split(" ")

            if isinstance(company_code, list):
                company_str = ""

                for i in range(len(company_code)-1):
                    if i == 0:
                        company_str += company_code[i]

                    if i > 0:
                        company_str = company_str + " " + company_code[i]
                company_code = company_str

            #print("Company = " + "'" + company_code + "'")

            if (company_code == ""):
                company_code = time_limit
                time_limit = "1Y"
                if company_code == "all":
                    company_code = "selectall"

            SG_TIME = ["1D", "1W", "1M", "1Y", "5Y"]

            if time_limit not in SG_TIME and re.search('[a-zA-Z]', time_limit):
                company_code += " " + time_limit
                time_limit = "1Y"
            else:
                time_limit = time_limit.upper()

            if time_limit not in SG_TIME:
                await message.channel.send("Please send the correct Time Period (Options = {1D, 1W, 1M, 1Y, 5Y})")

            stocksbot = SGXScraper("Firefox", company_code, time_limit ,message)
            await make_choice(stocksbot, message, check, time_limit, 'SG')

    elif (BOT_NAME + " US " in message.content and BOT_IS_IDLE == True):
        arg_list = message.content.split(BOT_NAME + " US ")

        if(arg_list[1] == ""or message.content == BOT_NAME + " US "):
            await message.channel.send("Bad Request")

        if arg_list[0] == "":
            time_limit = arg_list[1].split(" ")[-1]
            company_code = arg_list[1].split(" ")

            if isinstance(company_code, list):
                company_str = ""
                for i in range(len(company_code)-1):
                    if i == 0:
                        company_str += company_code[i]
                    if i > 0:
                        company_str = company_str + " " + company_code[i]
                company_code = company_str

            if (company_code == ""):
                company_code = time_limit
                time_limit = "1Y"
                if company_code == "all":
                    company_code = "selectall"

            US_TIME = ["1D", "15D", "1M", "3M", "6M", "1Y", "3Y", "5Y"]
            #time_limit = time_limit.upper()

            if time_limit not in US_TIME and re.search('[a-zA-Z]', time_limit):
                company_code += " " + time_limit
                time_limit = "1Y"
            else:
                time_limit = time_limit.upper()

            if time_limit not in US_TIME:
                await message.channel.send("Please send the correct Time Period (Options = {1D, 15D, 1M, 3M, 6M, 1Y, 3Y, 5Y})")
                return
            #print("Company = " + company_code + " and time = " + time_limit)
            stocksbot = NYSEScraper("Firefox", company_code, time_limit, message)
            await make_choice(stocksbot, message, check, time_limit, 'US')

async def make_choice(stocksbot, message, check, time_limit, region='US'):
    if len(stocksbot.matches) == 0:
        await message.channel.send("Company Name not found.")

    elif len(stocksbot.matches) > 1:
        embed = discord.Embed(title="", description="Please select the Stock Number : (" + BOT_NAME + " {number})", color=0x00003b)
        curr = 1
        for company_code in stocksbot.matches:
            embed.add_field(name=str(curr) + ". " + stocksbot.matches[company_code].strip('"'), value="Symbol: " + company_code.strip('"') + "\n" + "Exchange: " + stocksbot.exchange[curr-1].replace("Listings/","").upper())
            if curr % 25 == 0:
                await message.channel.send(embed=embed)
                embed = discord.Embed(title="", description="Please select the Stock Number : (" + BOT_NAME + "{number})", color=0x00003b)
            curr += 1

        if curr-1 % 25 != 0:
            await message.channel.send(embed=embed)

        # Now get the response
        msg = await client.wait_for('message', check=check)

        if BOT_NAME + " " in msg.content:
            arg_list = msg.content.split(BOT_NAME + " ")

            if arg_list[0] == "":
                input_num = int(arg_list[1])
                try:
                    code = list(stocksbot.matches.keys())[input_num-1]
                except IndexError:
                    return
                #print("Code = " + code, )
                stocksbot = NYSEScraper("Firefox", code.upper(), time_limit, message)
                await stocksbot.setupDrivers()
                await stocksbot.scrape_site()
                if region == 'US':
                    await stocksbot.send_us_photo()
                else:
                    await stocksbot.send_sg_photo()
    else:
        await stocksbot.setupDrivers()
        await stocksbot.scrape_site()
        if region == 'US':
            await stocksbot.send_us_photo()
        else:
            await stocksbot.send_sg_photo()

def main():
    client.run(token)

if __name__ == '__main__':
    main()
