from dataclasses import dataclass

@dataclass
class TaskContext:
    user_id: str
    serial_number: str
    driver: object
    logger: object