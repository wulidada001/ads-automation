class AutoPilotError(Exception):
    pass

class InfraError(AutoPilotError):
    """基础设施错误（如ADS启动失败）-> 建议重试"""
    pass

class BusinessError(AutoPilotError):
    """业务逻辑错误（如账号被封）-> 建议跳过"""
    pass

class NetworkError(AutoPilotError):
    """网络波动 -> 建议重试"""
    pass