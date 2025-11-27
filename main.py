import config
from infra.ads_client import ADSClient
from engine.runner import TaskRunner
from tasks.discord_task import DiscordTask


def main():
    print("=== AutoPilot Pro 自动化系统启动 ===")

    # 1. 初始化基础设施 (连接 ADS)
    print(f"[*] 正在连接 ADS API: {config.ADS_API_URL}")
    client = ADSClient(config.ADS_API_URL)

    # 2. 获取任务目标
    # 这里演示：获取前 3 个环境
    # 如果你想获取指定分组，可以改写 get_user_list 的参数
    print("[*] 正在获取环境列表...")
    all_users = client.get_user_list(page=1, size=3)

    if not all_users:
        print("❌ 未获取到环境，请检查：\n1. ADS软件是否打开？\n2. 账号列表是否为空？")
        return

    print(f"[*] 获取到 {len(all_users)} 个环境，准备执行任务。")

    # 3. 实例化具体的任务插件
    # 核心优势：这里决定了今天要干什么。
    # 如果明天想做 Twitter，就改成 current_task = TwitterTask()
    current_task = DiscordTask()

    # 4. 启动引擎 (并发执行)
    # config.THREADS 在 config.py 里定义，默认是 2
    runner = TaskRunner(client, concurrency=config.THREADS)

    # 开始批量跑！
    runner.run_batch(all_users, current_task)

    print("=== 所有任务执行完毕 ===")


if __name__ == "__main__":
    main()