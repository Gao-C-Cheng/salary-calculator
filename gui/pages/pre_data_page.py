"""
前置数据处理页面
支持拖拽上传和选择路径上传 Excel 文件，
提供「选择输出路径」和「开始转换」按钮。
"""
import os
import sys
import logging
import traceback

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFileDialog, QMessageBox, QFrame,
    QProgressBar, QSizePolicy, QApplication
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QMimeData
from PyQt5.QtGui import QFont, QDragEnterEvent, QDropEvent

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

logger = logging.getLogger(__name__)


class ProcessWorker(QThread):
    """后台线程执行数据处理，避免阻塞 UI"""
    finished = pyqtSignal(bool, str)          # (success, message)
    progress = pyqtSignal(str)                # status text

    def __init__(self, input_file: str, output_dir: str):
        super().__init__()
        self.input_file = input_file
        self.output_dir = output_dir

    def run(self):
        try:
            self.progress.emit("正在读取 Excel 文件…")

            # 修改 MyPath.TEMP_DIR 为用户选择的输出路径
            import MyPath
            MyPath.TEMP_DIR = self.output_dir

            from logic.PreDataLogic import split_budget_data

            self.progress.emit("正在拆分数据…")
            split_budget_data(self.input_file)

            # 统计生成的文件
            generated = [f for f in os.listdir(self.output_dir) if f.endswith('.xlsx')]
            msg = "数据拆分完成！共生成 {} 个文件：\n".format(len(generated))
            msg += "\n".join("  \u2022 {}".format(f) for f in generated)
            self.finished.emit(True, msg)

        except BaseException as e:
            # 记录完整异常堆栈到 app.log
            tb_text = traceback.format_exc()
            logger.error("前置数据处理异常:\n%s", tb_text)
            # 通过信号通知主线程显示错误状态和弹窗
            self.finished.emit(False, "发生异常：请联系开发人员查看系统日志")


class DropArea(QFrame):
    """可拖拽的文件上传区域"""
    file_dropped = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setObjectName("dropArea")
        self.setMinimumHeight(200)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(12)

        icon_label = QLabel("\U0001F4C2")
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("font-size: 48px; background: transparent; border: none;")
        layout.addWidget(icon_label)

        hint_label = QLabel("拖拽 Excel 文件到此处\n或点击下方按钮选择文件")
        hint_label.setAlignment(Qt.AlignCenter)
        hint_label.setObjectName("dropHint")
        layout.addWidget(hint_label)

        sub_hint = QLabel("支持 .xlsx 和 .xls 格式")
        sub_hint.setAlignment(Qt.AlignCenter)
        sub_hint.setObjectName("dropSubHint")
        layout.addWidget(sub_hint)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                path = url.toLocalFile()
                if path.lower().endswith(('.xlsx', '.xls')):
                    event.acceptProposedAction()
                    self.setProperty("dragOver", True)
                    self.style().unpolish(self)
                    self.style().polish(self)
                    return
        event.ignore()

    def dragLeaveEvent(self, event):
        self.setProperty("dragOver", False)
        self.style().unpolish(self)
        self.style().polish(self)

    def dropEvent(self, event: QDropEvent):
        self.setProperty("dragOver", False)
        self.style().unpolish(self)
        self.style().polish(self)
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if path.lower().endswith(('.xlsx', '.xls')):
                self.file_dropped.emit(path)
                return


class PreDataPage(QWidget):
    """前置数据处理 - 完整页面"""

    def __init__(self):
        super().__init__()
        self.selected_file: str = ""
        self.output_dir: str = os.getcwd()
        self.worker: ProcessWorker | None = None
        self._setup_ui()
        self._apply_styles()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(20)

        # ---- 页面标题 ----
        title = QLabel("前置数据处理")
        title.setObjectName("pageTitle")
        layout.addWidget(title)

        desc = QLabel(
            "上传《预算单位人员类目录、数财对应指标、功能科目、对口股室归集表》Excel 文件，\n"
            "系统将自动拆分为《单位机构表》和《数财对应指标表》等数据文件。"
        )
        desc.setObjectName("pageDesc")
        desc.setWordWrap(True)
        layout.addWidget(desc)

        # ---- 拖拽上传区 ----
        self.drop_area = DropArea()
        self.drop_area.file_dropped.connect(self._on_file_dropped)
        layout.addWidget(self.drop_area)

        # ---- 选择文件按钮 ----
        browse_btn = QPushButton("\U0001F4C1  选择文件")
        browse_btn.setObjectName("browseBtn")
        browse_btn.clicked.connect(self._browse_file)
        layout.addWidget(browse_btn, alignment=Qt.AlignCenter)

        # ---- 已选文件显示 ----
        self.file_label = QLabel("尚未选择文件")
        self.file_label.setObjectName("fileLabel")
        self.file_label.setWordWrap(True)
        layout.addWidget(self.file_label)

        # ---- 输出路径 + 开始转换 按钮行 ----
        btn_row = QHBoxLayout()
        btn_row.setSpacing(16)

        self.output_btn = QPushButton("选择输出路径")
        self.output_btn.setObjectName("outputBtn")
        self.output_btn.setMinimumHeight(44)
        self.output_btn.clicked.connect(self._choose_output_dir)
        btn_row.addWidget(self.output_btn)

        self.start_btn = QPushButton("开始转换")
        self.start_btn.setObjectName("startBtn")
        self.start_btn.setMinimumHeight(44)
        self.start_btn.setEnabled(False)
        self.start_btn.clicked.connect(self._start_processing)
        btn_row.addWidget(self.start_btn)

        layout.addLayout(btn_row)

        # ---- 输出路径显示 ----
        self.output_label = QLabel("输出路径：{}".format(self.output_dir))
        self.output_label.setObjectName("outputLabel")
        self.output_label.setWordWrap(True)
        layout.addWidget(self.output_label)

        # ---- 进度条 ----
        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("progressBar")
        self.progress_bar.setRange(0, 0)  # indeterminate
        self.progress_bar.setVisible(False)
        self.progress_bar.setFixedHeight(6)
        layout.addWidget(self.progress_bar)

        # ---- 状态信息 ----
        self.status_label = QLabel("")
        self.status_label.setObjectName("statusLabel")
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)

        layout.addStretch()

    # -------------------------------------------------------- 事件处理
    def _on_file_dropped(self, path: str):
        self._set_file(path)

    def _browse_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "选择 Excel 文件", "",
            "Excel 文件 (*.xlsx *.xls);;所有文件 (*)"
        )
        if path:
            self._set_file(path)

    def _set_file(self, path: str):
        self.selected_file = path
        filename = os.path.basename(path)
        self.file_label.setText("已选择文件：{}".format(filename))
        self.file_label.setToolTip(path)
        self.start_btn.setEnabled(True)
        self.status_label.setText("")

    def _choose_output_dir(self):
        dir_path = QFileDialog.getExistingDirectory(
            self, "选择输出路径", self.output_dir
        )
        if dir_path:
            self.output_dir = dir_path
            self.output_label.setText("输出路径：{}".format(self.output_dir))

    def _start_processing(self):
        if not self.selected_file:
            QMessageBox.warning(self, "提示", "请先选择要处理的 Excel 文件。")
            return

        if not os.path.exists(self.selected_file):
            QMessageBox.warning(self, "提示", "文件不存在：{}".format(self.selected_file))
            return

        # 禁用按钮，显示进度
        self.start_btn.setEnabled(False)
        self.output_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.status_label.setText("正在处理中，请稍候…")
        self.status_label.setStyleSheet("color: #3b82f6; font-size: 13px;")

        # 启动后台线程
        self.worker = ProcessWorker(self.selected_file, self.output_dir)
        self.worker.progress.connect(self._on_progress)
        self.worker.finished.connect(self._on_finished)
        self.worker.start()

    def _on_progress(self, text: str):
        self.status_label.setText(text)

    def _on_finished(self, success: bool, message: str):
        self.progress_bar.setVisible(False)
        self.start_btn.setEnabled(True)
        self.output_btn.setEnabled(True)

        if success:
            self.status_label.setStyleSheet("color: #16a34a; font-size: 13px;")
            self.status_label.setText("\u2705 {}".format(message))
        else:
            self.status_label.setStyleSheet("color: #dc2626; font-size: 13px;")
            self.status_label.setText("\u274c {}".format(message))
            # 弹窗提醒用户查看日志
            QMessageBox.critical(
                self,
                "系统异常",
                "发生异常：请联系开发人员查看系统日志"
            )

        self.worker = None

    # -------------------------------------------------------- 样式
    def _apply_styles(self):
        self.setStyleSheet("""
            #pageTitle {
                font-size: 22px;
                font-weight: bold;
                color: #1e293b;
            }
            #pageDesc {
                font-size: 13px;
                color: #64748b;
                line-height: 1.6;
            }

            /* 拖拽区域 */
            #dropArea {
                border: 2px dashed #cbd5e1;
                border-radius: 12px;
                background-color: #f8fafc;
            }
            #dropArea[dragOver="true"] {
                border-color: #3b82f6;
                background-color: #eff6ff;
            }
            #dropHint {
                font-size: 14px;
                color: #64748b;
                background: transparent;
                border: none;
            }
            #dropSubHint {
                font-size: 12px;
                color: #94a3b8;
                background: transparent;
                border: none;
            }

            /* 选择文件按钮 */
            #browseBtn {
                background-color: #e2e8f0;
                color: #334155;
                border: none;
                border-radius: 8px;
                padding: 10px 28px;
                font-size: 13px;
                font-weight: 500;
            }
            #browseBtn:hover {
                background-color: #cbd5e1;
            }

            #fileLabel {
                font-size: 13px;
                color: #475569;
                padding: 4px 0;
            }

            /* 输出路径按钮 */
            #outputBtn {
                background-color: #f1f5f9;
                color: #334155;
                border: 1px solid #cbd5e1;
                border-radius: 8px;
                padding: 8px 20px;
                font-size: 14px;
                font-weight: 500;
            }
            #outputBtn:hover {
                background-color: #e2e8f0;
                border-color: #94a3b8;
            }
            #outputBtn:disabled {
                background-color: #f1f5f9;
                color: #94a3b8;
            }

            /* 开始转换按钮 */
            #startBtn {
                background-color: #3b82f6;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 32px;
                font-size: 14px;
                font-weight: bold;
            }
            #startBtn:hover {
                background-color: #2563eb;
            }
            #startBtn:disabled {
                background-color: #93c5fd;
            }

            #outputLabel {
                font-size: 12px;
                color: #64748b;
                padding: 2px 0;
            }

            /* 进度条 */
            #progressBar {
                border: none;
                border-radius: 3px;
                background-color: #e2e8f0;
            }
            #progressBar::chunk {
                background-color: #3b82f6;
                border-radius: 3px;
            }

            #statusLabel {
                font-size: 13px;
                padding: 4px 0;
            }
        """)
