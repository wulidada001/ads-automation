import os

# 定义真正的功能代码
code_mapping = {
    # 1. 核心异常定义
    "AutoPilot_Pro/core/exceptions.py": """
class AutoPilotError(Exception):
    pass

class InfraError(AutoPilotError):
    \"\"\"基础设施错误（如ADS启动失败）-> 建议重试\"\"\"
    pass

class BusinessError(AutoPilotError):
    \"\"\"业务逻辑错误（如账号被封）-> 建议跳过\"\"\"
    pass

class NetworkError(AutoPilotError):
    \"\"\"网络波动 -> 建议重试\"\"\"
    pass
""",

    # 2. 核心上下文定义
    "AutoPilot_Pro/core/context.py": """
from dataclasses import dataclass

@dataclass
class TaskContext:
    user_id: str
    serial_number: str
    driver: object
    logger: object
""",

    # 3. 任务基类
    "AutoPilot_Pro/tasks/base.py": """
from abc import ABC, abstractmethod
from core.context import TaskContext

class BaseTask(ABC):
    @abstractmethod
    def run(self, ctx: TaskContext):
        pass
""",

    # 4. [关键修复] 基础设施 - ADS客户端
    "AutoPilot_Pro/infra/ads_client.py": """
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
""",

    # 5. 执行引擎
    "AutoPilot_Pro/engine/runner.py": """
import concurrent.futures
import time
from core.context import TaskContext
from core.exceptions import InfraError, BusinessError, NetworkError

class TaskRunner:
    def __init__(self, ads_client, concurrency=2):
        self.client = ads_client
        self.concurrency = concurrency

    def run_batch(self, user_list, task_instance):
        print(f"🚀 引擎启动: 并发线程数 {self.concurrency}")

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.concurrency) as executor:
            futures = {
                executor.submit(self._worker, user, task_instance): user 
                for user in user_list
            }

            for f in concurrent.futures.as_completed(futures):
                pass 

    def _worker(self, user_info, task):
        user_id = user_info['user_id']
        seq = user_info.get('serial_number', '未知')

        try:
            # 1. 启动
            driver = self.client.start_browser(user_id)

            # 2. 上下文
            ctx = TaskContext(
                user_id=user_id, 
                serial_number=seq, 
                driver=driver, 
                logger=None
            )

            # 3. 执行任务
            task.run(ctx)

        except InfraError as e:
            print(f"❌ [{seq}] 基础设施故障: {e}")
        except BusinessError as e:
            print(f"🚫 [{seq}] 业务逻辑中止: {e}")
        except NetworkError as e:
            print(f"⚠️ [{seq}] 网络异常: {e}")
        except Exception as e:
            print(f"💥 [{seq}] 未知系统错误: {e}")
        finally:
            # 4. 关闭
            self.client.stop_browser(user_id)
"""
}


def repair():
    print("开始修复底层代码...")
    for path, content in code_mapping.items():
        # 写入文件
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content.strip())
            print(f"✅ 已修复: {path}")
        except FileNotFoundError:
            print(f"❌ 找不到路径 (请确保你在项目根目录运行): {path}")


if __name__ == "__main__":
    repair()
    print("\\n🎉 所有底层代码已注入完毕！请重新运行 main.py")