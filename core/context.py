from dataclasses import dataclass

@dataclass
class TaskContext:
    """
    任务上下文对象
    用于在 Engine 和 Task 之间传递数据
    """
    user_id: str        # ADS 环境 ID
    serial_number: str  # 环境序号
    driver: object      # Selenium WebDriver 对象
    logger: object      # 日志对象 (预留)