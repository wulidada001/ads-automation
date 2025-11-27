class AutoPilotError(Exception):
    """基础异常类"""
    pass

class InfraError(AutoPilotError):
    """基础设施错误（如ADS启动失败、浏览器崩溃）-> 建议重试"""
    pass

class BusinessError(AutoPilotError):
    """业务逻辑错误（如账号被封、验证码）-> 建议跳过或人工处理"""
    pass

class NetworkError(AutoPilotError):
    """网络问题（如加载超时）-> 建议重试"""
    pass