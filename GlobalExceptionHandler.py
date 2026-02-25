"""
全局异常处理模块
捕获主线程和子线程中的未处理异常，记录到 app.log 并弹窗提醒用户。
"""

import logging
import sys
import threading
import traceback

logger = logging.getLogger(__name__)


class GlobalExceptionHandler:
    """
    全局异常处理类
    覆盖 sys.excepthook（主线程）和 threading.excepthook（子线程），
    确保任何未捕获的异常都不会导致程序静默退出。
    """

    _app_ref = None  # 保存 QApplication 引用，用于弹窗

    @classmethod
    def set_app(cls, app):
        """设置 QApplication 引用，install 之后调用"""
        cls._app_ref = app

    @staticmethod
    def handle_exception(exc_type, exc_value, exc_traceback):
        """
        处理主线程中未捕获的异常
        """
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        tb_lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        tb_text = ''.join(tb_lines)

        logger.error("未处理的异常:\n%s", tb_text)

        GlobalExceptionHandler._show_error_dialog()

    @staticmethod
    def handle_thread_exception(args):
        """
        处理子线程中未捕获的异常（Python 3.8+ threading.excepthook）
        args: threading.ExceptHookArgs(exc_type, exc_value, exc_traceback, thread)
        """
        if issubclass(args.exc_type, KeyboardInterrupt):
            return

        tb_lines = traceback.format_exception(args.exc_type, args.exc_value, args.exc_traceback)
        tb_text = ''.join(tb_lines)
        thread_name = args.thread.name if args.thread else "Unknown"

        logger.error("子线程 [%s] 未处理的异常:\n%s", thread_name, tb_text)

        GlobalExceptionHandler._show_error_dialog()

    @staticmethod
    def _show_error_dialog():
        """
        在主线程中安全地弹出错误提示对话框。
        使用 QMetaObject.invokeMethod 确保跨线程安全调用。
        """
        try:
            from PyQt5.QtWidgets import QMessageBox, QApplication
            from PyQt5.QtCore import QMetaObject, Qt, Q_ARG

            app = QApplication.instance()
            if app is None:
                return

            # 如果当前就在主线程，直接弹窗
            if threading.current_thread() is threading.main_thread():
                QMessageBox.critical(
                    None,
                    "系统异常",
                    "发生异常：请联系开发人员查看系统日志"
                )
            else:
                # 从子线程通过信号机制安全地在主线程弹窗
                # 使用 QTimer.singleShot(0, ...) 将调用投递到主线程事件循环
                from PyQt5.QtCore import QTimer
                QTimer.singleShot(0, lambda: QMessageBox.critical(
                    None,
                    "系统异常",
                    "发生异常：请联系开发人员查看系统日志"
                ))
        except Exception:
            # 弹窗本身失败时不能再抛异常，仅打印到 stderr
            print("发生异常：请联系开发人员查看系统日志", file=sys.stderr)

    @staticmethod
    def install():
        """
        安装全局异常处理器，覆盖主线程和子线程
        """
        sys.excepthook = GlobalExceptionHandler.handle_exception
        threading.excepthook = GlobalExceptionHandler.handle_thread_exception
