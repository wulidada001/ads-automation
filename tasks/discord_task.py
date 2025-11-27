import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tasks.base import BaseTask
from core.exceptions import BusinessError, NetworkError


class DiscordTask(BaseTask):
    def run(self, ctx):
        driver = ctx.driver
        print(f"[{ctx.serial_number}] 🔵 正在启动 Discord 任务...")

        try:
            driver.get("https://discord.com/app")

            # 简单等待页面加载
            time.sleep(5)

            page_source = driver.page_source
            current_url = driver.current_url

            if "login" in current_url:
                print(f"[{ctx.serial_number}] 🟡 状态：未登录")
            elif "channels" in current_url:
                print(f"[{ctx.serial_number}] ✅ 状态：已登录")
            else:
                print(f"[{ctx.serial_number}] ℹ️ 页面标题: {driver.title}")

            return True

        except Exception as e:
            raise BusinessError(f"未知错误: {e}")