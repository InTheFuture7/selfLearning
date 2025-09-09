# logger_config.py
import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
"""
handler 决定日志消息的输出目标（文件/控制台/网络），处理方式（每个handler都有独立的日志级别）
"""

def setup_logger(log_file_path='scenery/logs/scenery_process.log', name='scenery_processor', file_mode='w'):
    """
    配置日志系统，输出到文件和控制台
    
    参数:
        log_file_path (str): 日志文件的完整路径（含文件名）
        name (str): logger 的名称，用于标识和区分不同的logger实例
        file_mode (str): 文件写入模式，'a'表示追加，'w'表示覆盖
    
    返回:
        logging.Logger: 配置好的 logger 实例
    """

    # 生成时间戳
    timestamp = datetime.now().strftime("_%Y%m%d%H%M")

    # 在文件名的.log前添加时间戳
    if log_file_path.endswith('.log'):
        log_file_path = log_file_path[:-4] + timestamp + '.log'
    else:
        # 如果文件路径没有.log扩展名，直接在末尾添加时间戳
        log_file_path = log_file_path + timestamp


    # 从文件路径中提取目录部分
    log_dir = os.path.dirname(log_file_path)
    
    # 如果目录不存在，则创建
    if not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    # 获取或创建 logger
    logger = logging.getLogger(name)

    # 如果 logger 已经配置过，直接返回
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    # handler 决定日志写入到文件还是控制台
    # 创建文件 handler，根据file_mode参数选择写入模式
    if file_mode == 'w':
        # 覆盖模式：使用普通的FileHandler
        file_handler = logging.FileHandler(
            log_file_path,
            mode='w',
            encoding='utf-8'
        )
    else:
        # 追加模式：使用RotatingFileHandler支持日志轮转
        file_handler = RotatingFileHandler(
            log_file_path,
            maxBytes=2048 * 1024,  # 每个文件最大 2 MB
            backupCount=5,          # 最多保留 5 个备份。如果文件大小达到1M，那么另创建一个日志文件 .1、.2
            encoding='utf-8'
        )
    file_handler.setLevel(logging.INFO)   # 写入到文件的日志，最小级别为 INFO

    # 创建控制台 handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)   # 写入到控制台的日志，最小级别为 INFOR

    # 定义日志格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # 添加 handler 到 logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

def get_logger(name='app_logger'):
    """
    获取已配置的logger实例，如果不存在则使用默认配置创建

    适用场景：多个py文件中向同一个log文件写入日志
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        # 如果logger还没有配置，使用默认配置
        return setup_logger(name=name)
    return logger