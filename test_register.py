"""
============================
Project: py42API
Author:柠檬班-海励
Time:9/8/2021 下午 8:04
E-mail:2227092769@qq.com
Company:湖南零檬信息技术有限公司
Site: http://www.lemonban.com
Forum: http://testingpai.com 
============================
"""
"""
注册接口
unittest + ddt 
1、写测试用例数据--excel保存

"""
import unittest
import requests
from ddt import ddt,data
import ast

from tools.handle_path import case_data_dir
from conf.settings import excel_sheet
from tools.handle_excel import HandleExcel
from tools.handle_db import mysql
from tools.handle_replace import HandleReplace
from tools.handle_check_db import HandleCheckDb
from conf.settings import replace_data

case_list = HandleExcel(file_name=case_data_dir,sheet_name=excel_sheet["register"]).get_test_case()

@ddt
class TestRegister(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.headers = {"X-Lemonban-Media-Type": "lemonban.v2", "Content-Type": "application/json"}
        cls.replace = HandleReplace()
        cls.handle_check_db = HandleCheckDb()

    @classmethod
    def tearDownClass(cls) -> None:
        mysql.close()

    @data(*case_list)
    def test_register(self,case):
        try:
            #1、参数替换
            # 造数据：fake ，正则表达式：re   数据提取：jsonpath
            new_data = self.replace.replace_data(data=case["data"],sql=case["replace_sql"])

            #2、发送requests请求，post,get，patch
            res = requests.post(url=case["url"], json=new_data, headers=self.headers)
            print(res.json())

            #3、接口断言
            actual_data = {"code":res.json()["code"],"msg":res.json()["msg"]}
            expect_data = case["expected_data"] # 从excel读出来的 都是 str类型
            self.assertEqual(ast.literal_eval(expect_data),actual_data)

            #4、数据库断言
            # {"expect_data":1,"actual_data":1}
            self.handle_check_db.check_db(check_db=case["check_db"],replace_data=replace_data)
        except:
            raise AssertionError
