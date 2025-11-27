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