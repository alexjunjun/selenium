# coding = utf-8
import os
import time
import xlrd
from lib.base_page import BasePage
from lib.init_env import init_env
from lib.log_config import get_logger
from lib.read_config import readConfig
from lib.special_methods import SpecialMethods

'''
    从用例文件中读取用例集、用例
    根据用例集中标识，顺序执行用例sheet中的用例
'''
_mylogger =get_logger(os.path.basename(__file__))

class run_case():
    def __init__(self,):
        browser = readConfig('config.ini', 'browser', 'browser')
        self.driver = init_env().open_browser(browser)
        # self.basePageAction = BasePage(driver)
        # 每步执行结果
        self.stepResult ={}
        # 测试集合执行结果
        self.caseResult ={}

    def run_test(self, caseFile):
        '''
        读取并执行用例
        将用例的分步执行结果保存到stepResult字典中
        每条用例的执行结果保存到caseResult字典中
        :param caseFile:
        :return: stepResult，caseResult
        '''
        # 打开excel case，第一个sheet为用例集，第二个sheet为用例步骤明细
        data = xlrd.open_workbook(caseFile)
        # 获取用例集
        caseGatherSheet = data.sheet_by_index(0)
        # 读取第一个sheet，获取用例集，以及是否需要执行，存放到casegather字典中
        casegather = {}
        for i in range(1,caseGatherSheet.nrows):
            # 用例序号
            caseNo = caseGatherSheet.row_values(i)[0]
            # 用例开关
            caseSwitch = caseGatherSheet.row_values(i)[1]
            try:
                # 用例集中，如果用例序号重复，以最后一条为准
                casegather[caseNo] = caseSwitch
            except Exception as e:
                _mylogger.error('获取用例集发生异常：{}\n请确认测试用例序号是否有重复！！！'.format(e))
                exit()
        # 获取用例具体步骤：
        caseStepSheet = data.sheet_by_index(1)
        # 获取表的行数
        rows = caseStepSheet.nrows
        for i in range(1, rows):
            row = caseStepSheet.row_values(i)
            try:
                caseNo = str(row[0])
                caseStepNo = str(row[1])
                caseStepName = str(row[2])
                caseFunName = str(row[3])
                caseKeyInfo = str(row[4])
                caseKeyValue = str(row[5])
                # 判断用例集是否需要执行
                if caseNo not in casegather.keys() :
                    _mylogger.info('用例集中不存在{}用例，跳过'.format(caseNo))
                    self.stepResult[i] = u'用例集未包含用例，跳过'
                    continue
                if str.lower(casegather[caseNo]) != 'y':
                    _mylogger.info('{}用例已设置为不执行，跳过'.format(caseNo))
                    self.stepResult[i] = u'用例集设置为不执行，跳过'
                    continue

                _mylogger.info(u'开始执行{}用例的{},{}'.format(caseNo,caseStepNo,caseStepName))
                time.sleep(0.5)
                # 使用python的反射机制，判断方法名是否存在
                fuc = getattr(BasePage(self.driver), caseFunName, u'方法不存在')
                if fuc == u'方法不存在':
                    # 判断异常类型为方法未定义，则进入special_methods中执行
                    fuc = getattr(SpecialMethods(self.driver), caseFunName,u'方法不存在')
                try:
                    fuc(caseKeyInfo, caseKeyValue)
                    self.stepResult[i] = u'步骤执行成功'
                    time.sleep(0.5)
                except Exception as e:
                    _mylogger.error(u'执行方法发生异常：{}，异常信息：{}'.format(caseFunName,e))
                    self.stepResult[i] = u'步骤执行失败'
                    # 判断是否为用例的最后一个step，如果是，则返回用例的执行结果
                if (i == rows-1 or caseNo != str(caseStepSheet.row_values(i+1)[0])):
                    if self.stepResult[i] == '步骤执行成功':
                        self.caseResult[caseStepSheet.row_values(i)[0]] = u'执行成功'
                    else:
                        self.caseResult[caseStepSheet.row_values(i)[0]] = u'执行失败'
                else :
                    pass
            except Exception as e:
                _mylogger.error(u'读取用例发生异常：', e)
        time.sleep(3)
        BasePage(self.driver).quit()
        return self.stepResult, self.caseResult
if __name__ == '__main__':
    run = run_case()
    run.run_test()