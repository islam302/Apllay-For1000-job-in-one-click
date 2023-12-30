import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from os import path
class WebDriver:
    def __init__(self):
        ...

    def start_driver(self):
        js_code = """(
        ()=>{
            const elementDescriptor = Object.getOwnPropertyDescriptor(HTMLElement.prototype, 'offsetHeight');
            Object.defineProperty(HTMLDivElement.prototype, 'offsetHeight', {
            ...elementDescriptor,
            get: function() {
                    if (this.id === 'modernizr') {
                            return 1;
                    }
                    return elementDescriptor.get.apply(this);
                    },
            });
        }
        )()"""

        CODE_PATH = path.abspath('.')
        core_path = path.join(CODE_PATH,"Core","App", "Chrome-bin", "chrome.exe")
        machine_path = path.join(CODE_PATH,"Core","chromedriver.exe")
        if not path.exists(core_path) or not path.exists(machine_path):
            return
        chrome_options = Options()
        chrome_options.binary_location = core_path
        # chrome_options.page_load_strategy = "eager"

        chrome_options.add_argument('--incognito')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--disable-devtools')
        chrome_options.add_argument('--disable-notifications')
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--disable-logging-redirect")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-automation")
        chrome_options.add_argument('--disable-animations')
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument('--disable-images')
        chrome_options.add_argument('--fast-start')
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        chrome_options.add_experimental_option("prefs", {
            #"profile.managed_default_content_settings.images": 2,
            "profile.default_content_setting_values.geolocation": 2,
            "profile.default_content_setting_values.notifications": 2,
            "profile": {"exit_type": "Normal"}, 
            "translate" : {"enabled": False},
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "intl.accept_languages": "en, en_US"
        })

        # chrome_options.headless = True
        # chrome_options.add_argument("--disable-gpu")


        try:
            serv = Service(machine_path)
            driver = webdriver.Chrome(service=serv, options=chrome_options)
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source":js_code})
            driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                        "source":"const newProto = navigator._proto_;"
                            "delete newProto.webdriver;"
                            "navigator._proto_ = newProto;"})
            driver.execute_cdp_cmd('Network.setUserAgentOverride',
                                        {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                                            'AppleWebKit/537.36 (KHTML, like Gecko) '
                                                            'Chrome/85.0.4183.102 Safari/537.36'})
            driver.set_window_size(1920,1080)
            driver.delete_all_cookies()
            return driver
        except:
            driver.quit()
            print("Err occured")
            return
