from logger_config import setup_logger, get_logger


# 在程序启动时配置logger
def init_logging():
    logger = setup_logger(log_file_path='日志管理/logs/app.log', name='app_logger')
    # 记录程序启动信息
    separator = "=" * 80
    logger.info(separator)
    logger.info("程序启动")
    logger.info(separator)
    return logger

def main():
    # 初始化日志
    logger = init_logging()
    
    logger.info("程序开始执行")
    
    try:
        print("============一些数据处理操作")
        process_data()
        logger.info("数据处理完成")
    except Exception as e:
        logger.error(f"程序执行出错: {e}")
    
    logger.info("程序执行结束")

def process_data():
    # 在其他函数中获取logger实例
    logger = get_logger('app_logger')
    logger.info("开始处理数据")
    # 处理数据的代码
    logger.info("数据处理中...")

if __name__ == "__main__":
    main()