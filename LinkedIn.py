import openpyxl
wb = openpyxl.load_workbook('company.xlsx')
print("files loaded successfully" )
print(wb.get_sheet_names())