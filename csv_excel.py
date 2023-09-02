import openpyxl
import csv
def writeHeaderInfoToCsv( header, location):

    with open(location, 'w', newline='')as f:
        f_csv = csv.DictWriter(f, header)
        f_csv.writeheader()
        f.flush()

def writeRowsInfoToCsv(rows, header, location):
    with open(location, 'a', newline='')as f:
        f_csv = csv.DictWriter(f, header)
        f_csv.writerows(rows)
        f.flush()


# writeInfoToCsv(rows,headers,'','test.csv')
