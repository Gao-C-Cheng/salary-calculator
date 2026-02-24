"""
前置数据处理逻辑，包括数据清洗、转换和加载等功能。
主要用于拆分《预算单位人员类目录、数财对应指标、功能科目、对口股室归集表（2026）》中的数据。
将其拆分为《单位机构表》和《数财对应指标表两部分》。并存在resources目录下，方便后续调用。
作者: Gao Cheng
日期: 2026-01-09
"""
import logging
import MyPath
from pandas import read_excel, DataFrame
from util.FileUtil import export_dataframe_with_proper_column_width

logger = logging.getLogger(__name__)

def split_budget_data(file_path):
    # 读取Excel文件,如果文件不存在抛出异常
    df = read_excel(file_path, sheet_name=0, header=2)
    df.loc[:,"人员类项目目录（扩展字段1）"] = df.loc[:,"人员类项目目录（扩展字段1）"].astype(str).str.zfill(4)
    print(df)
    print(df.dtypes)
    logger.debug(df.keys())

    # 提取单位机构表,去重后保存
    unit_org_df = df['预算单位'].drop_duplicates()
    # 去除预算单位列前的编号，只保留名称部分，如（207001-）
    unit_org_df_list = (unit_org_df.str.split('-', n=1, expand=True)[1]
                        .str.strip()
                        .fillna(unit_org_df)
                        .tolist())
    unit_org_df = DataFrame(unit_org_df_list, columns=['预算单位'])
    export_dataframe_with_proper_column_width(MyPath.TEMP_DIR + '/单位机构表.xlsx', unit_org_df)
    # 提取数财对应指标表,去重后保存
    financial_index_df = df[['人员类项目目录（扩展字段1）', '数财对应指标         （扩展字段2）']].drop_duplicates(
        subset=['人员类项目目录（扩展字段1）'])
    export_dataframe_with_proper_column_width(MyPath.TEMP_DIR + '/数财对应指标表.xlsx', financial_index_df)

    # 人员目录扩展字段号(排除车改住房改补贴)
    extended_field_numbers = ["0101","0201","0301","0401","1301","1401","1501","1901"]
    extended_field_numbers_car_housing = ["0601","0701","1801"]
    # 提取单位机构与数财对应指标的映射关系表，筛选掉扩展字段1为“2706、2705、2702、2701”
    middle_df = df.loc[df['人员类项目目录（扩展字段1）'].isin(extended_field_numbers)]
    middle_df_car_housing = df.loc[df['人员类项目目录（扩展字段1）'].isin(extended_field_numbers_car_housing)]
    export_dataframe_with_proper_column_width(MyPath.TEMP_DIR + '/预算单位数财指标目录.xlsx', middle_df)
    export_dataframe_with_proper_column_width(MyPath.TEMP_DIR + '/预算单位数财指标目录(车改住房改补贴).xlsx', middle_df_car_housing)

    logger.info("数据拆分完成，已保存至resources目录下。")

