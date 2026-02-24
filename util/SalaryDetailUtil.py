"""
工资总额结算工具类
按人员项目目录分类
编号分别为：1301，1401，1501，1901，0101，0201，0301，0401
作者: Gao Cheng
日期: 2026-01-20
"""

from MyPath import OUTPUT_DIR
from pandas import DataFrame, read_excel
import logging

logger = logging.getLogger(__name__)

class CalculatorFactory:
    """
    工资结算计算工厂类
    根据单位类型返回相应的计算类实例
    """
    def __init__(self):
        self.calculator_factory = {}

    def calculate_unit_member_count(self, unit_name):
        pass


class AdminCalculator(CalculatorFactory):
    """
    行政人员工资结算计算类
    """

    def __init__(self):
        super().__init__()
        self.file_path = OUTPUT_DIR + '/发放汇总表/行政在职人员工资发放汇总表.xlsx'
        self.df = read_excel(self.file_path, sheet_name=0, header=None, skiprows=5)
        self.calculator_factory = {
            '0101': self.calculate_salary_detail_0101,
            '0201': self.calculate_salary_detail_0201,
            '0301': self.calculate_salary_detail_0301,
            '0401': self.calculate_salary_detail_0401,
            '0601': self.calculate_salary_detail_0601,
            '0701': self.calculate_salary_detail_0701,
        }

    def calculate_unit_member_count(self, unit_name):
        """
        计算单位明细人数
        """
        row = self.df.loc[self.df.iloc[:,1]==unit_name]
        res = row.iloc[:,2].sum()
        logger.debug(f"单位 {unit_name} 明细人数结算结果: {res}")
        return res


    def calculate_salary_detail_0101(self, unit_name):
        """
        计算人员项目目录为0101 在职公务员（含参公人员）基本工资
        :param unit_name: 预算单位名称
        :return: 工资总额结算结果
        """
        # 计算逻辑，列 3+4+18+19
        res = self.df.loc[self.df.iloc[:,1]==unit_name].iloc[:, [3,4,18,19]].sum().sum()
        logger.debug(f"单位 {unit_name} 人员项目目录0101工资总额结算结果: {res}")
        return res

    def calculate_salary_detail_0201(self, unit_name):
        """
        计算人员项目目录为0201 在职公务员（含参公人员）规范津贴补贴
        :param unit_name: 预算单位名称
        :return: 工资总额结算结果
        """
        # 计算逻辑，列 6+7+21+22-32 返回数字类型
        df_row = self.df.loc[self.df.iloc[:,1]==unit_name]
        res = df_row.iloc[:,6] + df_row.iloc[:,7] + df_row.iloc[:,21] + df_row.iloc[:,22] - df_row.iloc[:,32]
        logger.debug(f"单位 {unit_name} 人员项目目录0201工资总额结算结果: {res.sum()}")
        return res.sum()

    def calculate_salary_detail_0301(self, unit_name):
        """
        计算人员项目目录为0301 在职公务员（含参公人员）岗位津贴
        :param unit_name: 预算单位名称
        :return: 工资总额结算结果
        """
        # 计算逻辑，列 5+20 返回数字类型
        df_row = self.df.loc[self.df.iloc[:,1]==unit_name]
        res = df_row.iloc[:,5] + df_row.iloc[:,20]
        logger.debug(f"单位 {unit_name} 人员项目目录0301工资总额结算结果: {res.sum()}")
        return res.sum()

    def calculate_salary_detail_0401(self, unit_name):
        """
        计算人员项目目录为0401 在职公务员（含参公人员）基础绩效奖
        :param unit_name: 预算单位名称
        :return: 工资总额结算结果
        """
        # 计算逻辑，列 I+X 返回数字类型
        df_row = self.df.loc[self.df.iloc[:,1]==unit_name]
        res = df_row.iloc[:,8] + df_row.iloc[:,23]
        logger.debug(f"单位 {unit_name} 人员项目目录0401工资总额结算结果: {res.sum()}")
        return res.sum()

    def calculate_salary_detail_0601(self, unit_name):
        """
        计算人员项目目录为0601 在职公务员（含参公人员）住房改革补贴
        :param unit_name: 预算单位名称
        :return: 工资总额结算结果
        """
        # 计算逻辑，列 R + Z 返回数字类型
        df_row = self.df.loc[self.df.iloc[:,1]==unit_name]
        res = df_row.iloc[:,17] + df_row.iloc[:,25]
        logger.debug(f"单位 {unit_name} 人员项目目录0601工资总额结算结果: {res.sum()}")
        return res.sum()

    def calculate_salary_detail_0701(self, unit_name):
        """
        计算人员项目目录为0701 在职公务员（含参公人员）公务用车改革补贴
        :param unit_name: 预算单位名称
        :return: 工资总额结算结果
        """
        # 计算逻辑，列 Q + Y 返回数字类型
        df_row = self.df.loc[self.df.iloc[:,1]==unit_name]
        res = df_row.iloc[:,16] + df_row.iloc[:,24]
        logger.debug(f"单位 {unit_name} 人员项目目录0701工资总额结算结果: {res.sum()}")
        return res.sum()


class InstitutionCalculator(CalculatorFactory):
    """
    事业单位工资结算计算类
    """
    def __init__(self):
        super().__init__()
        self.file_path = OUTPUT_DIR + '/发放汇总表/事业在职人员工资发放汇总表.xlsx'
        self.df = read_excel(self.file_path, sheet_name=0, header=None, skiprows=5)
        self.calculator_factory = {
            '1301': self.calculate_salary_detail_1301,
            '1401': self.calculate_salary_detail_1401,
            '1501': self.calculate_salary_detail_1501,
            '1901': self.calculate_salary_detail_1901,
            '1801': self.calculate_salary_detail_1801,
        }

    def calculate_unit_member_count(self, unit_name):
        """
        计算单位明细人数
        """
        row = self.df.loc[self.df.iloc[:,1]==unit_name]
        res = row.iloc[:,2].sum()
        logger.debug(f"单位 {unit_name} 明细人数结算结果: {res}")
        return res

    def calculate_salary_detail_1301(self, unit_name):
        """
        计算人员项目目录为1301 事业单位在职人员基本工资
        :param unit_name: 预算单位名称
        :return: 工资总额结算结果
        """
        # 计算逻辑，列 D+E+R+S
        res = self.df.loc[self.df.iloc[:,1]==unit_name].iloc[:, [3,4,17,18]].sum().sum()
        logger.debug(f"单位 {unit_name} 人员项目目录1301工资总额结算结果: {res}")
        return res

    def calculate_salary_detail_1401(self, unit_name):
        """
        计算人员项目目录为1401 事业单位在职人员基础性绩效工资
        :param unit_name: 预算单位名称
        :return: 工资总额结算结果
        """
        # 计算逻辑，列 G + U - AC，返回数字类型
        df_row = self.df.loc[self.df.iloc[:,1]==unit_name]
        res = df_row.iloc[:,6] + df_row.iloc[:,20] - df_row.iloc[:,28]
        logger.debug(f"单位 {unit_name} 人员项目目录1401工资总额结算结果: {res.sum()}")
        return res.sum()

    def calculate_salary_detail_1501(self, unit_name):
        """
        计算人员项目目录为1501 事业单位在职人员岗位津贴
        :param unit_name: 预算单位名称
        :return: 工资总额结算结果
        """
        # 计算逻辑，列 F + T，返回数字类型
        df_row = self.df.loc[self.df.iloc[:,1]==unit_name]
        res = df_row.iloc[:,5] + df_row.iloc[:,19]
        logger.debug(f"单位 {unit_name} 人员项目目录1501工资总额结算结果: {res.sum()}")
        return res.sum()

    def calculate_salary_detail_1901(self, unit_name):
        """
        计算人员项目目录为1901 事业单位在职人员基础绩效奖
        :param unit_name: 预算单位名称
        :return: 工资总额结算结果
        """
        # 计算逻辑，列 I + W，返回数字类型
        df_row = self.df.loc[self.df.iloc[:,1]==unit_name]
        res = df_row.iloc[:,8] + df_row.iloc[:,22]
        logger.debug(f"单位 {unit_name} 人员项目目录1901工资总额结算结果: {res.sum()}")
        return res.sum()

    def calculate_salary_detail_1801(self, unit_name):
        """
        计算人员项目目录为1801 事业单位在职人员住房改革补贴
        :param unit_name: 预算单位名称
        :return: 工资总额结算结果
        """
        # 计算逻辑，列 Q + X，返回数字类型
        df_row = self.df.loc[self.df.iloc[:,1]==unit_name]
        res = df_row.iloc[:,16] + df_row.iloc[:,23]
        logger.debug(f"单位 {unit_name} 人员项目目录1801工资总额结算结果: {res.sum()}")
        return res.sum()


if __name__ == '__main__':
    calculator = CalculatorFactory()
    calculator = AdminCalculator()
    unit_test_name = "中国共产党龙门县委员会办公室"
    res_unit_member_count = calculator.calculate_unit_member_count(unit_test_name)
    print(f"单位 {unit_test_name} 明细人数结算结果: {res_unit_member_count}")
    res_0101 = calculator.calculator_factory["0101"](unit_test_name)
    res_0201 = calculator.calculator_factory["0201"](unit_test_name)
    res_0301 = calculator.calculator_factory["0301"](unit_test_name)
    res_0401 = calculator.calculator_factory["0401"](unit_test_name)
    print(f"单位 {unit_test_name} 人员项目目录0101工资总额结算结果: {res_0101}")
    print(f"单位 {unit_test_name} 人员项目目录0201工资总额结算结果: {res_0201}")
    print(f"单位 {unit_test_name} 人员项目目录0301工资总额结算结果: {res_0301}")
    print(f"单位 {unit_test_name} 人员项目目录0401工资总额结算结果: {res_0401}")

    calculator = InstitutionCalculator()
    unit_test_name = "中国共产党龙门县委员会办公室"
    res_unit_member_count = calculator.calculate_unit_member_count(unit_test_name)
    print(f"单位 {unit_test_name} 明细人数结算结果: {res_unit_member_count}")
    res_1301 = calculator.calculator_factory["1301"](unit_test_name)
    res_1401 = calculator.calculator_factory["1401"](unit_test_name)
    res_1501 = calculator.calculator_factory["1501"](unit_test_name)
    res_1901 = calculator.calculator_factory["1901"](unit_test_name)
    print(f"单位 {unit_test_name} 人员项目目录1301工资总额结算结果: {res_1301}")
    print(f"单位 {unit_test_name} 人员项目目录1401工资总额结算结果: {res_1401}")
    print(f"单位 {unit_test_name} 人员项目目录1501工资总额结算结果: {res_1501}")
    print(f"单位 {unit_test_name} 人员项目目录1901工资总额结算结果: {res_1901}")