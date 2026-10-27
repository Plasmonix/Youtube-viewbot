import os
import random
import time
import json
import itertools
from selenium import webdriver
import undetected_chromedriver as uc
from fake_useragent import UserAgent
from colorama import Fore, Style, init

init(autoreset=True)

class ViewbotCLI:
    def __init__(self):
        self.load_data()
        self.ua = UserAgent()
        self.proxies = itertools.cycle(self.raw_proxies) if self.raw_proxies else None

    def load_data(self):
        """Safely load configuration and proxies with fallback checks."""
        try:
            with open('./data/config.json', 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            print(f"{Fore.RED}[ERROR] ./data/config.json not found! Please create it.{Style.RESET_ALL}")
            exit(1)

        try:
            with open('./data/proxies.txt', 'r', encoding='utf-8') as f:
                self.raw_proxies = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            self.raw_proxies = []

    def ui(self):
        """Render a clean, modern CLI header."""
        os.system('cls' if os.name == "nt" else 'clear')
        print(f"""{Fore.RED}
         __ __     _     _      _____ _             _     _      
        |  |  |___ _ _| |_ _ _| |_ ___   |  |  |_|___ _ _ _| |_ ___| |_   
        |     | . | | |  _| | | . | -_|  |  |  | | -_| | | | . | . |  _|  
         _| |___|___|_| |___|___|___|   \___/|_|___|_____|___|___|_|    
        {Fore.RESET}{Fore.DIM}github.com/Plasmonix | CLI Enhanced Version{Style.RESET_ALL}
        """)
        print(f"{Fore.CYAN}[CONFIG]{Fore.RESET} Target URL : {self.config.get('url', 'N/A')}")
        print(f"{Fore.CYAN}[CONFIG]{Fore.RESET} Total Views: {self.config.get('views', 0)}")
        print(f"{Fore.CYAN}[CONFIG]{Fore.RESET} Proxies    : {len(self.raw_proxies)} loaded\n" + "-"*60)

    def open_url(self, current_view, total_views):
        proxy = next(self.proxies) if self.proxies else None
        sleep_time = random.randint(self.config["min_watch"], self.config["max_watch"])
        user_agent = self.ua.random

        print(f"{Fore.YELLOW}[{current_view}/{total_views}] {Style.RESET_ALL}Launching browser instance...")
        if proxy:
            print(f" └── {Fore.DIM}Proxy:{Style.RESET_ALL} {proxy}")

        options = webdriver.ChromeOptions()
        options.add_argument("--incognito")
        options.add_argument('--start-maximized')
        options.add_argument(f'user-agent={user_agent}')
        options.add_argument("--headless=new")
        
        if proxy:
            options.add_argument(f"--proxy-server={proxy}")

        browser = None
        try:
            browser = uc.Chrome(options=options)
            browser.get(self.config["url"])
            print(f" {Fore.GREEN}✔{Style.RESET_ALL} Page loaded. Watching for {sleep_time} seconds...")
            time.sleep(sleep_time)
        except Exception as e:
            print(f" {Fore.RED}✖ Error during view execution:{Style.RESET_ALL} {e}")
        finally:
            if browser:
                try:
                    browser.quit()
                except:
                    pass
            print(f" {Fore.BLUE}ℹ{Style.RESET_ALL} Session closed.\n" + "-"*60)

    def main(self):
        self.ui()
        total_views = self.config.get("views", 1)
        
        for i in range(1, total_views + 1):
            self.open_url(i, total_views)
            
        print(f"\n{Fore.GREEN}[SUCCESS] All target views have been completed!{Style.RESET_ALL}")

if __name__ == "__main__":
    bot = ViewbotCLI()
    bot.main()
