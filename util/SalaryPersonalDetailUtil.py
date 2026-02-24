"""
个人工资明细计算工具类
在行政在职，行政工勤，事业在职三张表中分别计算
“统发工资”、“车改住房改补贴”、“应发工资”、“实发工资”、“代扣合计”等项目
作者: Gao Cheng
日期: 2026-01-29
"""

import logging

logger = logging.getLogger(__name__)


class AdminPersonalSalaryUtil:
    """
    行政人员个人工资明细计算类
    """

    @staticmethod
    def calculate_general_salary(admin_df, citizen_id):
        """
        计算统发工资
        :param admin_df: 行政人员明细DataFrame
        :param citizen_id: 证件号码
        :return: 统发工资金额
        """
        temp_row = admin_df.loc[admin_df[4] == citizen_id]
        if temp_row.empty:
            return None
        # 计算：列 AN - W - X
        general_salary = temp_row.iloc[:, 39].sum() - temp_row.iloc[:, 22].sum() - temp_row.iloc[:, 23].sum()
        logger.debug(f"证件号码 {citizen_id} 统发工资计算结果: {general_salary}")
        return general_salary

    @staticmethod
    def calculate_car_housing_subsidy(admin_df, citizen_id):
        """
        计算车改住房改补贴
        :param admin_df: 行政人员明细DataFrame
        :param citizen_id: 证件号码
        :return: 车改住房改补贴金额
        """
        temp_row = admin_df.loc[admin_df[4] == citizen_id]
        if temp_row.empty:
            return None
        # 计算：列 W + X
        subsidy = temp_row.iloc[:, 22].sum() + temp_row.iloc[:, 23].sum()
        logger.debug(f"证件号码 {citizen_id} 车改住房改补贴计算结果: {subsidy}")
        return subsidy

    @staticmethod
    def calculate_gross_salary(admin_df, citizen_id):
        """
        计算应发工资
        :param admin_df: 行政人员明细DataFrame
        :param citizen_id: 证件号码
        :return:
        """
        temp_row = admin_df.loc[admin_df[4] == citizen_id]
        if temp_row.empty:
            return None
        # 计算工资总额 = 列 P + W + X
        gross_salary = temp_row.iloc[:, 15].sum() + temp_row.iloc[:, 22].sum() + temp_row.iloc[:, 23].sum()
        logger.debug(f"证件号码 {citizen_id} 应发工资计算结果: {gross_salary}")
        return gross_salary

    @staticmethod
    def calculate_net_salary(admin_df, citizen_id):
        """
        计算实发工资
        :param admin_df: 行政人员明细DataFrame
        :param citizen_id: 证件号码
        :return:
        """
        temp_row = admin_df.loc[admin_df[4] == citizen_id]
        if temp_row.empty:
            return None
        # 计算实发工资 = 列 AN
        net_salary = temp_row.iloc[:, 39].sum()
        logger.debug(f"证件号码 {citizen_id} 实发工资计算结果: {net_salary}")
        return net_salary

    @staticmethod
    def calculate_deductions(admin_df, citizen_id):
        """
        计算代扣合计
        :param admin_df: 行政人员明细DataFrame
        :param citizen_id: 证件号码
        :return:
        """
        temp_row = admin_df.loc[admin_df[4] == citizen_id]
        if temp_row.empty:
            return None
        # 计算扣款合计 = 列 Q + R + S + T + U + V
        deductions = (temp_row.iloc[:,16].sum() + temp_row.iloc[:,17].sum() + temp_row.iloc[:,18].sum()
                      + temp_row.iloc[:,19].sum() + temp_row.iloc[:,20].sum() + temp_row.iloc[:,21].sum() )
        logger.debug(f"证件号码 {citizen_id} 代扣合计计算结果: {deductions}")
        return deductions


class AdminGongqinPersonalSalaryUtil:
    """
    行政工勤人员个人工资明细计算类
    """

    @staticmethod
    def calculate_general_salary(admin_gongqin_df, citizen_id):
        """
        计算统发工资
        :param admin_gongqin_df: 行政工勤人员明细DataFrame
        :param citizen_id: 证件号码
        :return: 统发工资金额
        """
        temp_row = admin_gongqin_df.loc[admin_gongqin_df[4] == citizen_id]
        if temp_row.empty:
            return None
        # 计算：列 P - W - X
        general_salary = temp_row.iloc[:, 39].sum() - temp_row.iloc[:, 22].sum() - temp_row.iloc[:, 23].sum()
        logger.debug(f"证件号码 {citizen_id} 统发工资计算结果: {general_salary}")
        return general_salary

    @staticmethod
    def calculate_car_housing_subsidy(admin_gongqin_df, citizen_id):
        """
        计算车改住房改补贴
        :param admin_gongqin_df: 行政工勤人员明细DataFrame
        :param citizen_id: 证件号码
        :return: 车改住房改补贴金额
        """
        temp_row = admin_gongqin_df.loc[admin_gongqin_df[4] == citizen_id]
        if temp_row.empty:
            return None
        # 计算：列 W + X
        subsidy = temp_row.iloc[:, 22].sum() + temp_row.iloc[:, 23].sum()
        logger.debug(f"证件号码 {citizen_id} 车改住房改补贴计算结果: {subsidy}")
        return subsidy

    @staticmethod
    def calculate_gross_salary(admin_gongqin_df, citizen_id):
        """
        计算应发工资
        :param admin_gongqin_df: 行政工勤人员明细DataFrame
        :param citizen_id: 证件号码
        :return:
        """
        temp_row = admin_gongqin_df.loc[admin_gongqin_df[4] == citizen_id]
        if temp_row.empty:
            return None
        # 计算工资总额 = 列 P + W + X
        gross_salary = temp_row.iloc[:, 15].sum() + temp_row.iloc[:, 22].sum() + temp_row.iloc[:, 23].sum()
        logger.debug(f"证件号码 {citizen_id} 应发工资计算结果: {gross_salary}")
        return gross_salary

    @staticmethod
    def calculate_net_salary(admin_gongqin_df, citizen_id):
        """
        计算实发工资
        :param admin_gongqin_df: 行政工勤人员明细DataFrame
        :param citizen_id: 证件号码
        :return:
        """
        temp_row = admin_gongqin_df.loc[admin_gongqin_df[4] == citizen_id]
        if temp_row.empty:
            return None
        # 计算实发工资 = 列 AN
        net_salary = temp_row.iloc[:, 39].sum()
        logger.debug(f"证件号码 {citizen_id} 实发工资计算结果: {net_salary}")
        return net_salary

    @staticmethod
    def calculate_deductions(admin_gongqin_df, citizen_id):
        """
        计算代扣合计
        :param admin_gongqin_df: 行政工勤人员明细DataFrame
        :param citizen_id: 证件号码
        :return:
        """
        temp_row = admin_gongqin_df.loc[admin_gongqin_df[4] == citizen_id]
        if temp_row.empty:
            return None
        # 计算扣款合计 = 列 Q + R + S + T + U + V
        deductions = (temp_row.iloc[:,16].sum() + temp_row.iloc[:,17].sum() + temp_row.iloc[:,18].sum()
                      + temp_row.iloc[:,19].sum() + temp_row.iloc[:,20].sum() + temp_row.iloc[:,21].sum() )
        logger.debug(f"证件号码 {citizen_id} 代扣合计计算结果: {deductions}")
        return deductions


class InstitutionPersonalSalaryUtil:
    """
    事业人员个人工资明细计算类
    """

    @staticmethod
    def calculate_general_salary(institution_df, citizen_id):
        """
        计算统发工资
        :param institution_df: 事业人员明细DataFrame
        :param citizen_id: 证件号码
        :return: 统发工资金额
        """
        temp_row = institution_df.loc[institution_df[4] == citizen_id]
        if temp_row.empty:
            return None
        # 计算：列 AH - U
        general_salary = temp_row.iloc[:, 33].sum() - temp_row.iloc[:, 20].sum()
        logger.debug(f"证件号码 {citizen_id} 统发工资计算结果: {general_salary}")
        return general_salary

    @staticmethod
    def calculate_car_housing_subsidy(institution_df, citizen_id):
        """
        计算车改住房改补贴
        :param institution_df: 事业人员明细DataFrame
        :param citizen_id: 证件号码
        :return: 车改住房改补贴金额
        """
        temp_row = institution_df.loc[institution_df[4] == citizen_id]
        if temp_row.empty:
            return None
        # 计算：列 U
        subsidy = temp_row.iloc[:, 20].sum()
        logger.debug(f"证件号码 {citizen_id} 车改住房改补贴计算结果: {subsidy}")
        return subsidy

    @staticmethod
    def calculate_gross_salary(institution_df, citizen_id):
        """
        计算应发工资
        :param institution_df: 事业人员明细DataFrame
        :param citizen_id: 证件号码
        :return:
        """
        temp_row = institution_df.loc[institution_df[4] == citizen_id]
        if temp_row.empty:
            return None
        # 计算工资总额 = 列 N + U
        gross_salary = temp_row.iloc[:, 13].sum() + temp_row.iloc[:, 20].sum()
        logger.debug(f"证件号码 {citizen_id} 应发工资计算结果: {gross_salary}")
        return gross_salary

    @staticmethod
    def calculate_net_salary(institution_df, citizen_id):
        """
        计算实发工资
        :param institution_df: 事业人员明细DataFrame
        :param citizen_id: 证件号码
        :return:
        """
        temp_row = institution_df.loc[institution_df[4] == citizen_id]
        if temp_row.empty:
            return None
        # 计算实发工资 = 列 AH
        net_salary = temp_row.iloc[:, 33].sum()
        logger.debug(f"证件号码 {citizen_id} 实发工资计算结果: {net_salary}")
        return net_salary

    @staticmethod
    def calculate_deductions(institution_df, citizen_id):
        """
        计算代扣合计
        :param institution_df: 事业人员明细DataFrame
        :param citizen_id: 证件号码
        :return:
        """
        temp_row = institution_df.loc[institution_df[4] == citizen_id]
        if temp_row.empty:
            return None
        # 计算代扣合计 = 列 O + P + Q + R + S + T
        deductions = (temp_row.iloc[:, 14].sum() + temp_row.iloc[:, 15].sum() + temp_row.iloc[:, 16].sum()
                      + temp_row.iloc[:, 17].sum() + temp_row.iloc[:, 18].sum() + temp_row.iloc[:, 19].sum())
        logger.debug(f"证件号码 {citizen_id} 代扣合计计算结果: {deductions}")
        return deductions
