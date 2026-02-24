import logging.config

import MyPath
from GlobalExceptionHandler import GlobalExceptionHandler
from logic.PreDataLogic import split_budget_data
from logic.OverAllDataLogic import generate_salary_summary, generate_salary_detail_summary
from logic.PersonalDataLogic import generate_personal_salary_detail

import LogConfig

logging.config.dictConfig(LogConfig.LOGGING_CONFIG)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logger.info("打印日志测试")
    GlobalExceptionHandler.install()
    split_budget_data(MyPath.INPUT_DIR + "/预算单位人员类目录、数财对应指标、功能科目、对口股室归集表（2026）.xlsx")
    generate_salary_summary(MyPath.INPUT_DIR + "/机关在职人员工资发放汇总表.xlsx",
                            MyPath.INPUT_DIR + "/2026-01机关工勤汇总表20251229.xlsx",
                            MyPath.OUTPUT_DIR + "/发放汇总表/行政在职人员工资发放汇总表.xlsx")
    generate_salary_summary(MyPath.INPUT_DIR + "/惠州市龙门县2026年01月事业在职人员工资发放汇总表2051226.xlsx",
                            output_file_path=MyPath.OUTPUT_DIR + "/发放汇总表/事业在职人员工资发放汇总表.xlsx")

    generate_salary_detail_summary(MyPath.OUTPUT_DIR + "/工资汇总单/工资汇总单.xlsx",0)
    generate_salary_detail_summary(MyPath.OUTPUT_DIR + "/工资汇总单/车改、住房改革补贴汇总单.xlsx", 1)
    generate_personal_salary_detail(MyPath.INPUT_DIR + "/明细/惠州市龙门县2026年01月机关单位在职工资发放明细表.xlsx",
                                    MyPath.INPUT_DIR + "/明细/2026-01机关工勤明细表20251229.xlsx",
                                    MyPath.INPUT_DIR + "/明细/惠州市龙门县2026年01月事业单位在职工资发放明细表20251226.xlsx",
                                    0,
                                    MyPath.OUTPUT_DIR + "/工资明细表/个人工资明细表.xlsx")
    generate_personal_salary_detail(MyPath.INPUT_DIR + "/明细/惠州市龙门县2026年01月机关单位在职工资发放明细表.xlsx",
                                    MyPath.INPUT_DIR + "/明细/2026-01机关工勤明细表20251229.xlsx",
                                    MyPath.INPUT_DIR + "/明细/惠州市龙门县2026年01月事业单位在职工资发放明细表20251226.xlsx",
                                    1,
                                    MyPath.OUTPUT_DIR + "/工资明细表/车改住改补贴明细表.xlsx")
