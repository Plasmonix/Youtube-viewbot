import os, random, time
from urllib.request import Request, urlopen
from selenium import webdriver
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from colorama import Fore

class Viewbot:
    def __init__(self):
        self.proxies = []
        self.ua = UserAgent()

    def ui(self):
        os.system('cls && title Youtube Viewbot v2 ^| github.com/Plasmonix' if os.name == "nt" else 'clear') 
        print(f"""{Fore.RED}                                                           
         __ __         _       _          _____ _           _       _     
        |  |  |___ _ _| |_ _ _| |_ ___   |  |  |_|___ _ _ _| |_ ___| |_   
        |_   _| . | | |  _| | | . | -_|  |  |  | | -_| | | | . | . |  _|  
          |_| |___|___|_| |___|___|___|   \___/|_|___|_____|___|___|_|    
        {Fore.RESET}""")

    def load_proxies(self):
        try:
            proxy_file = open(self.proxy_path, "r+", encoding="utf8").readlines()
            for i in proxy_file:
                ip, port = i.split(":", 2)
                self.proxies.append({'ip': ip,'port': port})
        except FileNotFoundError:
            print(f'{Fore.RED}File not found{Fore.RESET}')
            os.system('pause >nul')
            quit()

    def scrape_proxies(self):
        try:
            proxies_req = Request('https://www.sslproxies.org/')
            proxies_req.add_header('User-Agent', self.ua.random)
            proxies_doc = urlopen(proxies_req).read().decode('utf8')
            soup = BeautifulSoup(proxies_doc, 'html.parser')
            proxies_table = soup.find('table', attrs={'class': 'table table-striped table-bordered'})
            for row in proxies_table.tbody.find_all('tr'):
                self.proxies.append({'ip': row.find_all('td')[0].string, 'port': row.find_all('td')[1].string})
        except:
            print(f'{Fore.RED}Failed to scrape proxies{Fore.RESET}')
            os.system('pause >nul')
            quit()
        
    def open_url(self, ua, sleep_time, proxy):
        options = webdriver.ChromeOptions()
        options.add_argument('--proxy-server=%s' % (proxy['ip'] + ':' + proxy['port']))
        options.add_argument('user-agent=%s' % ua.random)
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        #Uncomment below if you don't have chromedriver.exe in root folder
        #browser_driver = path/to/webdriver
        #driver = webdriver.Chrome(executable_path=browser_driver, options=options)
        
        driver = webdriver.Chrome(options=options)
        driver.get(self.url)
        time.sleep(sleep_time)
        driver.quit()

    def main(self):
        self.ui()
        try:
            self.url = input(f'{Fore.CYAN}>{Fore.RESET} Video url: ')
            self.views = int(input(f'{Fore.CYAN}>{Fore.RESET} Views: '))
            self.minwatch = int(input(f'{Fore.CYAN}>{Fore.RESET} Min watchtime (in seconds): '))
            self.maxwatch = int(input(f'{Fore.CYAN}>{Fore.RESET} Max watchtime (in seconds); '))
            customproxies = input(f'{Fore.CYAN}?{Fore.RESET} Use custom proxies ? Y/n: ').lower()
            if customproxies == 'y':
                self.proxy_path = input(f'{Fore.CYAN}>{Fore.RESET} Path to proxyfile: ')
                self.load_proxies()
            elif customproxies == 'n':
                self.scrape_proxies()
            else:
                print(f'{Fore.RED}Please enter a valid choice such as Y or n!{Fore.RESET}')
                os.system('pause >nul')
                quit()
        
        except ValueError: 
            print(f'{Fore.RED}Value must be an integer{Fore.RESET}')
            os.system('pause >nul')
            quit()
        
        self.ui()
        for _ in range(self.views):
            self.sleeptime = random.randint(self.minwatch, self.maxwatch)
            proxy = random.choice(self.proxies)
            self.open_url(self.ua, self.sleeptime, proxy)

if __name__ == "__main__":
    n = Viewbot()
    n.main()
