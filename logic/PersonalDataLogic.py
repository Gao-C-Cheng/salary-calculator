"""
个人工资明细表处理，
1.将《惠州市龙门县2026年01月机关单位在职工资发放明细表》、《2026-01机关工勤明细表20251229》
和《惠州市龙门县2026年01月事业单位在职工资发放明细表20251226》的数据以《1.财供人员个人信息（截至2023年11月8日）》表
为基准筛选，新增实发工资一列，生成《个人工资明细表》和《车改住改补贴明细表》
"""

import logging
from datetime import date

import MyPath
import pandas as pd
from util.FileUtil import export_dataframe_with_proper_column_width
from util.SalaryPersonalDetailUtil import AdminPersonalSalaryUtil, AdminGongqinPersonalSalaryUtil, \
    InstitutionPersonalSalaryUtil

logger = logging.getLogger(__name__)


def generate_personal_salary_detail(admin_detail_file, admin_gongqin_file, institution_detail_file,
                                    catalog_flag, output_file_path):
    """
    生成工资明细表
    :param admin_detail_file: 行政人员明细文件
    :param admin_gongqin_file: 机关工勤明细文件
    :param institution_detail_file: 事业人员明细文件
    :param catalog_flag: 目录表示 0-普通目录 1-车改住改补贴目录
    :param output_file_path: 输出文件路径
    :return: None
    """
    admin_df = pd.read_excel(admin_detail_file, sheet_name=0, header=None, skiprows=3)
    admin_gongqin_df = pd.read_excel(admin_gongqin_file, sheet_name=0, header=None, skiprows=3)
    institution_df = pd.read_excel(institution_detail_file, sheet_name=0, header=None, skiprows=3)
    personal_info_df = pd.read_excel(MyPath.INPUT_DIR + '/1.财供人员个人信息（截至2023年11月8日）.xlsx', sheet_name=0,
                                     header=3)
    header = personal_info_df.columns.values.tolist() + ['实发工资']
    res = pd.DataFrame(columns=header)
    logger.info(f"输出dataframe表头: {res}")
    for index, row in personal_info_df.iterrows():
        new_row = row.copy()
        citizen_id = row["证件号码"]
        # 计算工资明细表的统发工资
        if catalog_flag == 0:
            salary = AdminPersonalSalaryUtil.calculate_general_salary(admin_df, citizen_id)
            salary = AdminGongqinPersonalSalaryUtil.calculate_general_salary(admin_gongqin_df,citizen_id) \
                if salary is None else salary
            salary = InstitutionPersonalSalaryUtil.calculate_general_salary(institution_df,citizen_id) \
                if salary is None else salary
        else:
            salary = AdminPersonalSalaryUtil.calculate_car_housing_subsidy(admin_df, citizen_id)
            salary = AdminGongqinPersonalSalaryUtil.calculate_car_housing_subsidy(admin_gongqin_df,citizen_id) \
                if salary is None else salary
            salary = InstitutionPersonalSalaryUtil.calculate_car_housing_subsidy(institution_df,citizen_id) \
                if salary is None else salary
        if not salary:
            continue
        new_row['实发工资'] = salary
        res = pd.concat([res, pd.DataFrame([new_row])], ignore_index=True)
        logger.debug(f"行政人员 {citizen_id} 实发工资: {salary}")
    export_dataframe_with_proper_column_width(output_file_path, res)
    # 同时生成最终发放数据，没有列名，只保留姓名，个人账号，实发工资三列，并生成序号
    final_res = generate_final_salary_detail(res)
    print(final_res)
    output_filename = output_file_path.split('/')[-1]
    final_output_file_path = MyPath.OUTPUT_DIR + '/加密数据/' + output_filename.replace(".xlsx", "加密数据.xlsx")
    export_dataframe_with_proper_column_width(final_output_file_path, final_res, header=False)

    logger.info(f"个人工资明细表生成完成，已保存至{output_file_path}。")
    return


def generate_final_salary_detail(data: pd.DataFrame):
    """
    生成最终发放数据，没有列名，只保留职员姓名，个人账号，实发工资三列，并生成序号
    :param data: 个人工资明细表数据
    :return: 最终发放数据DataFrame
    """
    final_res = pd.DataFrame(columns=['序号', '职员姓名', '个人账号', '实发工资'])
    for index, row in data.iterrows():
        final_row = {
            '序号': index + 1,
            '职员姓名': row['职员姓名'],
            '个人账号': row['个人账号'],
            '实发工资': row['实发工资']
        }
        final_res = pd.concat([final_res, pd.DataFrame([final_row])], ignore_index=True)
    return final_res

def handle_salary_detail_for_import(row: pd.DataFrame, admin_df, admin_gongqing_df, institution_df):
    res = pd.DataFrame({'区划编号': ["441324000"],
                        '区划名称':["龙门县"],
                        '姓名':[row['职员姓名']],
                        '身份证号':[row['证件号码']],
                        '预算单位名称':[""],
                        '发放月份':[f"{date.today().month}月"],
                        '应发工资':[""],
                        '代扣项合计':[],
                        '补发工资':[],
                        '扣发工资':[],
                        '实发工资':[]})
    citizen_id = row['证件号码']
    net_salary = None
    if admin_df.loc[admin_df[4]==citizen_id].empty is False:
        pass
    elif admin_gongqing_df.loc[admin_gongqing_df[4]==citizen_id].empty is False:
        pass
    elif institution_df.loc[institution_df[4]==citizen_id].empty is False:
        pass
    return res if net_salary is not None else None