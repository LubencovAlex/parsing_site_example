import xlsxwriter
from main_pars import pars_card

def writer_cards(parametr):
    file = xlsxwriter.Workbook("cards_data.xlsx")
    page = file.add_worksheet("товар")

    row = 0
    column = 0

    page.set_column("A:A", 24)
    page.set_column("B:B", 8)
    page.set_column("C:C", 124)
    page.set_column("D:D", 45)

    for item in parametr():
        page.write(row, column, item[0])
        page.write(row, column, item[1])
        page.write(row, column, item[2])
        page.write(row, column, item[3])
        row += 1

    file.close()

writer_cards(pars_card)