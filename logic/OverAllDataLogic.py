"""
工资发放汇总处理，生成发放汇总表和工资汇总单
1.将原始数据中的行政在职的《机关工勤汇总表》《机关在职汇总表》分别筛选出特定单位，
并按照单位合并成一张总表，表字段不变，生成《行政在职人员工资发放汇总表》。
2.将原始数据中的《事业在职汇总表》按单位筛选，表字段不变，生成《事业在职人员工资发放汇总表》。

作者: Gao Cheng
日期: 2026-01-15
"""
import os
from datetime import datetime, date
import logging
import MyPath
import pandas as pd
import util.FileUtil as FileUtil
from util.SalaryDetailUtil import CalculatorFactory, AdminCalculator, InstitutionCalculator

logger = logging.getLogger(__name__)

salary_detail_default_df = pd.DataFrame({
    "精准核销指标": [""],
    "月份":[str(date.today().month).zfill(2)],
    "工资批次ID":[f"103{date.today().year}{str(date.today().month).zfill(2)}002"],
    "工资批次名称":[f"农行代发{date.today().year}年{str(date.today().month).zfill(2)}月工资"],
    "单位编码":[""],
    "单位名称":[""],
    "工资汇总编码":[""],
    "工资汇总名称":[""],
    "工资总额":[""],
    "明细人数":[""],
    "功能科目编码":[""],
    "功能科目名称":[""],
    "收款人名称":["代理财政支付其他批量代发待结算款"],
    "收款人账号":["44248001010046175"],
    "收款人开户行":["农行惠州龙门支行"],
    "支付唯一标识":[""],
    "人员类型":[""],
    "业务处（科）室编码":[""],
    "业务处（科）室名称":[""],
    "指标来源编码":[""],
    "指标来源名称":[""],
    "资金性质编码":[""],
    "资金性质名称":[""],
    "政府经济分类编码":[""],
    "政府经济分类名称":[""],
    "部门经济分类编码":[""],
    "部门经济分类名称":[""],
    "扩展字段1":[""],
    "扩展字段2":[""],
    "扩展字段3":[""],
    "扩展字段4":[""],
    "扩展字段5":[""],
    "付款人全称":["龙门县财政局国库支付局"],
    "付款人账号":["44248001040035552"],
    "付款人开户行":["中国农业银行龙门县支行"],
    "用途":[f"{date.today().month}月统发工资"],
    "支付方式编码":[""],
    "支付方式名称":[""],
})


def generate_salary_summary(file_path, file_path_2=None, output_file_path=None):
    """
    工资发放汇总单生成逻辑
    :param file_path:
    :param file_path_2:
    :param output_file_path:
    :return:
    """
    # 复制file_path的标题行到output目录
    FileUtil.copy_and_get_header_openpyxl(file_path, output_file_path,5)
    # 定义筛选方法
    def find_matching_prefix(value, prefix_list):
        """
        检查value是否以prefix_list中的任一字符串开头。
        如果是，返回匹配到的第一个前缀；否则返回None或其他默认值。
        """
        for prefix in prefix_list:
            if str(value).startswith(prefix):  # 确保转换为字符串进行比较[2](@ref)
                return prefix  # 匹配成功，返回筛选列表中的这个前缀
        return None  # 无匹配项
    # 定义计算合计行方法
    def calculate_total_row(data_frame) -> pd.Series:
        res = data_frame.iloc[:, 2:].sum()
        res[1] = '合计'
        return res
    # 读取单位机构表，获取预算单位列表
    filter_list = pd.read_excel(MyPath.TEMP_DIR + '/单位机构表.xlsx', sheet_name=0)['预算单位'].tolist()
    # 如果file_path_2为空，则只处理事业在职汇总表,否则合并行政在职汇总表和机关工勤汇总表
    if file_path_2:
        # 读取行政在职汇总表和机关工勤汇总表
        df1 = pd.read_excel(file_path, sheet_name=0, header=None, skiprows=5)
        df2 = pd.read_excel(file_path_2, sheet_name=0, header=None, skiprows=5)
        # 筛选出特定单位的数据
        df1 = df1[df1[1].isin(filter_list)]
        # 因为是工勤单位，所以单位名要前缀匹配
        df2[1] = df2[1].apply(lambda x: find_matching_prefix(x, filter_list))
        df2 = df2.dropna(subset=[1])
        df1.set_index(1, inplace=True)
        df2.set_index(1, inplace=True)
        # 以单位名称为键合并两个DataFrame的数据
        merged_df = df1.add(df2, fill_value=0).sort_values(by=0).reset_index().sort_index(axis=1, ascending=True)
        # 计算合计行
        total_row = calculate_total_row(merged_df)
        merged_df = pd.concat([merged_df, pd.DataFrame([total_row])], ignore_index=True)
        # 重新计算序号列0，从1开始
        merged_df[0] = range(1, len(merged_df) + 1)
        print(merged_df)
        FileUtil.append_data_to_excel_openpyxl(output_file_path, merged_df, start_row=5)
        logger.info("行政在职人员工资发放汇总表生成完成，已保存至output目录下。")
        return
    # 读取事业在职汇总表
    df3 = pd.read_excel(file_path, sheet_name=0, header=None, skiprows=5)
    # 筛选出特定单位的数据
    df3[1] = df3[1].apply(lambda x: find_matching_prefix(x, filter_list))
    df3 = df3.dropna(subset=[1])
    df3.iloc[:, 2:] = df3.iloc[:, 2:].apply(pd.to_numeric, errors='coerce').fillna(0)
    # 计算合计行
    total_row = calculate_total_row(df3)
    df3 = pd.concat([df3, pd.DataFrame([total_row])], ignore_index=True)
    # 重新计算序号列0，从1开始
    df3[0] = range(1, len(df3) + 1)
    print(df3)
    FileUtil.append_data_to_excel_openpyxl(output_file_path, df3, start_row=5)
    logger.info("事业在职人员工资发放汇总表生成完成，已保存至output目录下。")
    return

def generate_salary_detail_summary(output_file_path, catalog_flag):
    """
    工资汇总单生成逻辑
    :param output_file_path:
    :param catalog_flag: 目录标识，0.表示使用普通目录，1.表示使用车改住房改补贴目录
    :return:
    """
    # 导入预算单位数财指标目录、行政在职人员工资发放汇总表、事业在职人员工资发放汇总表数据
    if catalog_flag == 1:
        # 使用车改住房改补贴目录
        budget_df = pd.read_excel(MyPath.TEMP_DIR + '/预算单位数财指标目录(车改住房改补贴).xlsx', sheet_name=0)
    else:
        budget_df = pd.read_excel(MyPath.TEMP_DIR + '/预算单位数财指标目录.xlsx', sheet_name=0)
    res = pd.DataFrame()
    # 遍历budget_df
    for index, row in budget_df.iterrows():
        salary_detail_df = salary_detail_default_df.copy()
        # 计算单位编码和单位名称
        unit_info = row['预算单位'].split('-', 1)
        unit_name = unit_info[1].strip() if len(unit_info) > 1 else ""
        salary_detail_df["单位编码"] = unit_info[0].strip()
        salary_detail_df["单位名称"] = unit_name
        # 计算工资总额和明细人数、扩展字段1、扩展字段2
        extend_code = str(row['人员类项目目录（扩展字段1）']).zfill(4)
        salary_detail_df["扩展字段1"] = extend_code.strip()
        salary_detail_df["扩展字段2"] = row['数财对应指标         （扩展字段2）'].strip()
        calculator = CalculatorFactory()
        if extend_code in ['0101', '0201', '0301', '0401', '0601', '0701']:
            calculator = AdminCalculator()
        elif extend_code in ['1301', '1401', '1501', '1901', '1801']:
            calculator = InstitutionCalculator()
        salary_sum = calculator.calculator_factory[extend_code](unit_name)
        if not salary_sum:
            continue
        salary_detail_df["工资总额"] = salary_sum
        salary_detail_df["明细人数"] = calculator.calculate_unit_member_count(unit_name)
        # 功能科目信息
        subject_info = row["支出功能分类"].split('-', 1)
        salary_detail_df["功能科目编码"] = subject_info[0].strip()
        salary_detail_df["功能科目名称"] = subject_info[1].strip()
        # 人员类型
        salary_detail_df["人员类型"] = row["人员类型"].split('-', 1)[0]
        # 业务处室信息
        dept_info = row["资金管理处室"].split('-', 1)
        salary_detail_df["业务处（科）室编码"] = dept_info[0].strip()
        salary_detail_df["业务处（科）室名称"] = dept_info[1].strip()
        res = pd.concat([res, salary_detail_df], ignore_index=True)
    # 导出结果到Excel
    FileUtil.export_dataframe_with_proper_column_width(output_file_path, res)




