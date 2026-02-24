"""
全局异常处理模块
该模块定义了一个全局异常处理类，用于捕获和处理应用程序中的未处理异常。
"""

import logging
import sys
import traceback

logger = logging.getLogger(__name__)

class GlobalExceptionHandler:
    """
    全局异常处理类
    """

    @staticmethod
    def handle_exception(exc_type, exc_value, exc_traceback):
        """
        处理未捕获的异常
        :param exc_type: 异常类型
        :param exc_value: 异常值
        :param exc_traceback: 异常追踪信息
        """
        if issubclass(exc_type, KeyboardInterrupt):
            # 允许键盘中断异常正常退出
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        # 格式化异常信息
        tb_lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        tb_text = ''.join(tb_lines)

        # 记录异常日志
        logger.error("未处理的异常:\n%s", tb_text)

    @staticmethod
    def install():
        """
        安装全局异常处理器
        """
        sys.excepthook = GlobalExceptionHandler.handle_exception