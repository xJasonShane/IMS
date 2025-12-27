import logging
import sys
from logging.handlers import RotatingFileHandler
from app.core.config import settings

# 创建日志记录器
logger = logging.getLogger("ims")
logger.setLevel(logging.DEBUG if settings.app_debug else logging.INFO)

# 创建日志格式
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
)

# 控制台日志处理器
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG if settings.app_debug else logging.INFO)
console_handler.setFormatter(formatter)

# 文件日志处理器（仅在生产环境使用）
if not settings.app_debug:
    file_handler = RotatingFileHandler(
        "logs/ims.log",
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,  # 保留5个备份文件
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

# 添加控制台日志处理器
logger.addHandler(console_handler)
