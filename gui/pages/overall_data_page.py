"""
汇总数据处理页面
提供三个文件上传窗口（机关在职、机关工勤、事业在职），
以及「生成发放汇总表」和「生成工资汇总单」两个功能按钮。
"""
import os
import sys
import logging
import traceback

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFileDialog, QMessageBox, QFrame,
    QProgressBar, QSizePolicy, QScrollArea
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QDragEnterEvent, QDropEvent

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import MyPath

logger = logging.getLogger(__name__)


# ============================================================
# 小型文件上传卡片组件
# ============================================================
class FileUploadCard(QFrame):
    """带标题的文件上传卡片，支持拖拽和点击选择"""
    file_changed = pyqtSignal(str)

    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self.title_text = title
        self.file_path = ""
        self.setAcceptDrops(True)
        self.setObjectName("uploadCard")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setMinimumHeight(140)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(8)

        # 标题行
        title_label = QLabel(self.title_text)
        title_label.setObjectName("cardTitle")
        layout.addWidget(title_label)

        # 拖拽提示区
        self.hint_frame = QFrame()
        self.hint_frame.setObjectName("cardDropZone")
        hint_layout = QVBoxLayout(self.hint_frame)
        hint_layout.setContentsMargins(12, 10, 12, 10)
        hint_layout.setSpacing(4)

        self.icon_label = QLabel("\U0001F4C4")
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.icon_label.setStyleSheet("font-size: 24px; background: transparent; border: none;")
        hint_layout.addWidget(self.icon_label)

        self.hint_label = QLabel("拖拽文件到此处或点击选择")
        self.hint_label.setAlignment(Qt.AlignCenter)
        self.hint_label.setObjectName("cardHint")
        hint_layout.addWidget(self.hint_label)

        layout.addWidget(self.hint_frame)

        # 按钮行
        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)

        self.browse_btn = QPushButton("选择文件")
        self.browse_btn.setObjectName("cardBrowseBtn")
        self.browse_btn.clicked.connect(self._browse_file)
        btn_row.addWidget(self.browse_btn)

        self.clear_btn = QPushButton("清除")
        self.clear_btn.setObjectName("cardClearBtn")
        self.clear_btn.setVisible(False)
        self.clear_btn.clicked.connect(self._clear_file)
        btn_row.addWidget(self.clear_btn)

        btn_row.addStretch()
        layout.addLayout(btn_row)

        # 文件名显示
        self.file_label = QLabel("")
        self.file_label.setObjectName("cardFileLabel")
        self.file_label.setWordWrap(True)
        self.file_label.setVisible(False)
        layout.addWidget(self.file_label)

    def _browse_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "选择 Excel 文件 - {}".format(self.title_text), "",
            "Excel 文件 (*.xlsx *.xls);;所有文件 (*)"
        )
        if path:
            self._set_file(path)

    def _clear_file(self):
        self.file_path = ""
        self.file_label.setVisible(False)
        self.clear_btn.setVisible(False)
        self.hint_label.setText("拖拽文件到此处或点击选择")
        self.icon_label.setText("\U0001F4C4")
        self.setProperty("hasFile", False)
        self.style().unpolish(self)
        self.style().polish(self)
        self.file_changed.emit("")

    def _set_file(self, path: str):
        self.file_path = path
        filename = os.path.basename(path)
        self.file_label.setText("\u2705 {}".format(filename))
        self.file_label.setToolTip(path)
        self.file_label.setVisible(True)
        self.clear_btn.setVisible(True)
        self.hint_label.setText("已选择文件")
        self.icon_label.setText("\u2705")
        self.setProperty("hasFile", True)
        self.style().unpolish(self)
        self.style().polish(self)
        self.file_changed.emit(path)

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
                self._set_file(path)
                return

    def has_file(self) -> bool:
        return bool(self.file_path) and os.path.exists(self.file_path)


# ============================================================
# 后台处理线程
# ============================================================
class SummaryWorker(QThread):
    """后台线程执行汇总数据处理"""
    finished = pyqtSignal(bool, str)
    progress = pyqtSignal(str)

    def __init__(self, task_type: str, admin_file: str = "", worker_file: str = "", inst_file: str = ""):
        super().__init__()
        self.task_type = task_type
        self.admin_file = admin_file
        self.worker_file = worker_file
        self.inst_file = inst_file

    def run(self):
        try:
            from logic.OverAllDataLogic import generate_salary_summary, generate_salary_detail_summary

            output_base = MyPath.OUTPUT_DIR
            os.makedirs(output_base, exist_ok=True)

            if self.task_type == "summary":
                # ---- 生成发放汇总表 ----
                summary_dir = os.path.join(output_base, "发放汇总表")
                os.makedirs(summary_dir, exist_ok=True)

                # 第一次：机关在职 + 机关工勤 -> 行政在职人员工资发放汇总表
                self.progress.emit("正在生成《行政在职人员工资发放汇总表》…")
                admin_output = os.path.join(summary_dir, "行政在职人员工资发放汇总表.xlsx")
                generate_salary_summary(self.admin_file, self.worker_file, admin_output)

                # 第二次：事业在职 -> 事业在职人员工资发放汇总表
                self.progress.emit("正在生成《事业在职人员工资发放汇总表》…")
                inst_output = os.path.join(summary_dir, "事业在职人员工资发放汇总表.xlsx")
                generate_salary_summary(self.inst_file, output_file_path=inst_output)

                msg = "发放汇总表生成完成！\n"
                msg += "  \u2022 行政在职人员工资发放汇总表.xlsx\n"
                msg += "  \u2022 事业在职人员工资发放汇总表.xlsx\n"
                msg += "输出目录：{}".format(summary_dir)
                self.finished.emit(True, msg)

            elif self.task_type == "detail":
                # ---- 生成工资汇总单 ----
                detail_dir = os.path.join(output_base, "工资汇总单")
                os.makedirs(detail_dir, exist_ok=True)

                # catalog_flag=0 -> 工资汇总单
                self.progress.emit("正在生成《工资汇总单》…")
                detail_output_0 = os.path.join(detail_dir, "工资汇总单.xlsx")
                generate_salary_detail_summary(detail_output_0, 0)

                # catalog_flag=1 -> 车改、住房改革补贴汇总单
                self.progress.emit("正在生成《车改、住房改革补贴汇总单》…")
                detail_output_1 = os.path.join(detail_dir, "车改、住房改革补贴汇总单.xlsx")
                generate_salary_detail_summary(detail_output_1, 1)

                msg = "工资汇总单生成完成！\n"
                msg += "  \u2022 工资汇总单.xlsx\n"
                msg += "  \u2022 车改、住房改革补贴汇总单.xlsx\n"
                msg += "输出目录：{}".format(detail_dir)
                self.finished.emit(True, msg)

        except BaseException as e:
            tb_text = traceback.format_exc()
            logger.error("汇总数据处理异常:\n%s", tb_text)
            self.finished.emit(False, "发生异常：请联系开发人员查看系统日志")


# ============================================================
# 汇总数据处理页面
# ============================================================
class OverallDataPage(QWidget):
    """汇总数据处理 - 完整页面"""

    def __init__(self):
        super().__init__()
        self.worker = None
        self._setup_ui()
        self._apply_styles()

    def _setup_ui(self):
        # 使用 QScrollArea 以防内容溢出
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setObjectName("scrollArea")

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(20)

        # ---- 页面标题 ----
        title = QLabel("汇总数据处理")
        title.setObjectName("pageTitle")
        layout.addWidget(title)

        desc = QLabel(
            "上传机关在职、机关工勤、事业在职三类数据文件，\n"
            "系统将生成《发放汇总表》和《工资汇总单》。"
        )
        desc.setObjectName("pageDesc")
        desc.setWordWrap(True)
        layout.addWidget(desc)

        # ---- 三个文件上传卡片（横向排列） ----
        cards_row = QHBoxLayout()
        cards_row.setSpacing(16)

        self.admin_card = FileUploadCard("机关在职数据上传")
        self.admin_card.file_changed.connect(self._on_file_changed)
        cards_row.addWidget(self.admin_card)

        self.worker_card = FileUploadCard("机关工勤数据上传")
        self.worker_card.file_changed.connect(self._on_file_changed)
        cards_row.addWidget(self.worker_card)

        self.inst_card = FileUploadCard("事业在职数据上传")
        self.inst_card.file_changed.connect(self._on_file_changed)
        cards_row.addWidget(self.inst_card)

        layout.addLayout(cards_row)

        # ---- 按钮区（上下布局） ----
        btn_layout = QVBoxLayout()
        btn_layout.setSpacing(12)

        self.summary_btn = QPushButton("生成发放汇总表")
        self.summary_btn.setObjectName("summaryBtn")
        self.summary_btn.setMinimumHeight(48)
        self.summary_btn.setEnabled(False)
        self.summary_btn.clicked.connect(self._start_summary)
        btn_layout.addWidget(self.summary_btn)

        self.detail_btn = QPushButton("生成工资汇总单")
        self.detail_btn.setObjectName("detailBtn")
        self.detail_btn.setMinimumHeight(48)
        self.detail_btn.setEnabled(False)
        self.detail_btn.clicked.connect(self._start_detail)
        btn_layout.addWidget(self.detail_btn)

        layout.addLayout(btn_layout)

        # ---- 输出路径显示 ----
        self.output_label = QLabel("输出根目录：{}".format(MyPath.OUTPUT_DIR))
        self.output_label.setObjectName("outputLabel")
        self.output_label.setWordWrap(True)
        layout.addWidget(self.output_label)

        # ---- 进度条 ----
        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("progressBar")
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setVisible(False)
        self.progress_bar.setFixedHeight(6)
        layout.addWidget(self.progress_bar)

        # ---- 状态信息 ----
        self.status_label = QLabel("")
        self.status_label.setObjectName("statusLabel")
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)

        layout.addStretch()

        scroll.setWidget(container)

        # 外层布局
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)

    # -------------------------------------------------------- 状态检查
    def _on_file_changed(self, _path: str):
        """文件变更时更新按钮状态"""
        all_uploaded = (
            self.admin_card.has_file()
            and self.worker_card.has_file()
            and self.inst_card.has_file()
        )
        self.summary_btn.setEnabled(all_uploaded and self.worker is None)
        # 检查发放汇总表文件是否存在
        self._check_detail_btn_enabled()

    def _check_detail_btn_enabled(self):
        """检查生成工资汇总单按钮是否可用"""
        summary_dir = os.path.join(MyPath.OUTPUT_DIR, "发放汇总表")
        admin_summary = os.path.join(summary_dir, "行政在职人员工资发放汇总表.xlsx")
        inst_summary = os.path.join(summary_dir, "事业在职人员工资发放汇总表.xlsx")
        enabled = os.path.exists(admin_summary) and os.path.exists(inst_summary) and self.worker is None
        self.detail_btn.setEnabled(enabled)

    # -------------------------------------------------------- 事件处理
    def _start_summary(self):
        """启动生成发放汇总表"""
        if not (self.admin_card.has_file() and self.worker_card.has_file() and self.inst_card.has_file()):
            QMessageBox.warning(self, "提示", "请先上传全部三个数据文件。")
            return

        self._set_processing(True)
        self.status_label.setText("正在处理中，请稍候…")
        self.status_label.setStyleSheet("color: #3b82f6; font-size: 13px;")

        self.worker = SummaryWorker(
            task_type="summary",
            admin_file=self.admin_card.file_path,
            worker_file=self.worker_card.file_path,
            inst_file=self.inst_card.file_path
        )
        self.worker.progress.connect(self._on_progress)
        self.worker.finished.connect(self._on_finished)
        self.worker.start()

    def _start_detail(self):
        """启动生成工资汇总单"""
        summary_dir = os.path.join(MyPath.OUTPUT_DIR, "发放汇总表")
        admin_summary = os.path.join(summary_dir, "行政在职人员工资发放汇总表.xlsx")
        inst_summary = os.path.join(summary_dir, "事业在职人员工资发放汇总表.xlsx")

        if not (os.path.exists(admin_summary) and os.path.exists(inst_summary)):
            QMessageBox.warning(self, "提示", "请先生成发放汇总表后再执行此操作。")
            return

        self._set_processing(True)
        self.status_label.setText("正在处理中，请稍候…")
        self.status_label.setStyleSheet("color: #3b82f6; font-size: 13px;")

        self.worker = SummaryWorker(task_type="detail")
        self.worker.progress.connect(self._on_progress)
        self.worker.finished.connect(self._on_finished)
        self.worker.start()

    def _set_processing(self, processing: bool):
        """设置处理中状态"""
        self.summary_btn.setEnabled(not processing and self.admin_card.has_file()
                                     and self.worker_card.has_file() and self.inst_card.has_file())
        self.detail_btn.setEnabled(not processing)
        self.progress_bar.setVisible(processing)

    def _on_progress(self, text: str):
        self.status_label.setText(text)

    def _on_finished(self, success: bool, message: str):
        self.progress_bar.setVisible(False)
        self.worker = None

        if success:
            self.status_label.setStyleSheet("color: #16a34a; font-size: 13px;")
            self.status_label.setText("\u2705 {}".format(message))
        else:
            self.status_label.setStyleSheet("color: #dc2626; font-size: 13px;")
            self.status_label.setText("\u274c {}".format(message))
            QMessageBox.critical(
                self,
                "系统异常",
                "发生异常：请联系开发人员查看系统日志"
            )

        # 更新按钮状态
        self._on_file_changed("")
        self._check_detail_btn_enabled()

    # -------------------------------------------------------- 样式
    def _apply_styles(self):
        self.setStyleSheet("""
            #scrollArea {
                background-color: transparent;
                border: none;
            }

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

            /* 上传卡片 */
            #uploadCard {
                background-color: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
            }
            #uploadCard[dragOver="true"] {
                border: 2px solid #3b82f6;
                background-color: #eff6ff;
            }
            #uploadCard[hasFile="true"] {
                border-color: #86efac;
                background-color: #f0fdf4;
            }

            #cardTitle {
                font-size: 14px;
                font-weight: bold;
                color: #1e293b;
            }

            #cardDropZone {
                border: 1px dashed #cbd5e1;
                border-radius: 8px;
                background-color: #f8fafc;
                min-height: 50px;
            }

            #cardHint {
                font-size: 12px;
                color: #94a3b8;
                background: transparent;
                border: none;
            }

            #cardBrowseBtn {
                background-color: #e2e8f0;
                color: #334155;
                border: none;
                border-radius: 6px;
                padding: 6px 16px;
                font-size: 12px;
            }
            #cardBrowseBtn:hover {
                background-color: #cbd5e1;
            }

            #cardClearBtn {
                background-color: transparent;
                color: #ef4444;
                border: 1px solid #fca5a5;
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 12px;
            }
            #cardClearBtn:hover {
                background-color: #fef2f2;
            }

            #cardFileLabel {
                font-size: 12px;
                color: #16a34a;
                padding: 2px 0;
            }

            /* 生成发放汇总表按钮 */
            #summaryBtn {
                background-color: #3b82f6;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 32px;
                font-size: 15px;
                font-weight: bold;
            }
            #summaryBtn:hover {
                background-color: #2563eb;
            }
            #summaryBtn:disabled {
                background-color: #93c5fd;
            }

            /* 生成工资汇总单按钮 */
            #detailBtn {
                background-color: #8b5cf6;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 32px;
                font-size: 15px;
                font-weight: bold;
            }
            #detailBtn:hover {
                background-color: #7c3aed;
            }
            #detailBtn:disabled {
                background-color: #c4b5fd;
            }

            #outputLabel {
                font-size: 12px;
                color: #64748b;
                padding: 2px 0;
            }

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
