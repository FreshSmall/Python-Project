#  图像和办公文档处理
from openpyxl import Workbook
from openpyxl import load_workbook
# 引入模块
import xlrd
import xlwt
from xlutils.copy import copy


def load_excel():
    # 加载存在的excel文件：默认可写
    order_index = "XOUT0"
    wb2 = xlrd.open_workbook("/Users/bjhl/k3出入库单据导入模板.xls")
    newWb = copy(wb2)
    worksheet = wb2.sheet_by_name("销售出库单")
    newWorkSheet = newWb.get_sheet(1)
    nrows = worksheet.nrows
    order_str = worksheet.cell_value(1, 1).__str__()
    order_num = order_str.split(order_index)[1]
    print(order_num)
    firstCode = worksheet.cell_value(1, 2)
    firstNum = int(order_num)
    for i in range(2, nrows):
        code = worksheet.cell_value(i, 2)
        if firstCode != code:
            firstCode = code
            firstNum = firstNum + 1
        newWorkSheet.write(i, 1, order_index + str(firstNum))
    newWb.save("/Users/bjhl/new-k3出入库单据导入模板.xls")


if __name__ == '__main__':
    load_excel()
    # read_excel()
