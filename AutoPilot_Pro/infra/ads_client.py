import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from core.exceptions import InfraError

class ADSClient:
    def __init__(self, api_url):
        self.api_url = api_url

    def get_user_list(self, page=1, size=50):
        try:
            # 强制按序号排序
            params = {
                "page": page, 
                "page_size": size, 
                "user_sort": '{"serial_number":"asc"}'
            }
            resp = requests.get(
                f"{self.api_url}/api/v1/user/list",
                params=params,
                timeout=10
            )
            data = resp.json()
            if data['code'] == 0:
                return data['data']['list']
            return []
        except Exception as e:
            print(f"获取列表失败: {e}")
            return []

    def start_browser(self, user_id):
        try:
            resp = requests.get(
                f"{self.api_url}/api/v1/browser/start",
                params={"user_id": user_id, "open_tabs": 1},
                timeout=30
            )
            data = resp.json()

            if data.get('code') != 0:
                raise InfraError(f"API启动报错: {data.get('msg')}")

            ws = data["data"]["ws"]["selenium"]
            driver_path = data["data"]["webdriver"]

            opts = Options()
            opts.add_experimental_option("debuggerAddress", ws)
            service = Service(executable_path=driver_path)
            driver = webdriver.Chrome(service=service, options=opts)

            return driver

        except Exception as e:
            raise InfraError(f"启动浏览器异常: {e}")

    def stop_browser(self, user_id):
        try:
            requests.get(f"{self.api_url}/api/v1/browser/stop", params={"user_id": user_id}, timeout=5)
        except:
            pass