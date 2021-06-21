from PyPDF2 import PdfFileReader, PdfFileWriter
from datetime import datetime
import secret
import mundane as m

amazonIndices = {
    'order id': 0,
    'payment date': 2,
    'sku': 10,
    'item name': 11,
}

# the purpose of this func is to remove any duplicates with the same ID. Orders with multiple
# items are stored as different orders in the file, so this is to remove the lines and the pdf
# pages line up.
def groupIDs(lines):
    # -1 in for loop below because i will be looking at the next order, so on the last one I will
    # get index out of bounds if I don't stop 1 before.
    for line_index in range(len(lines) - 1):
        order_id_1 = lines[line_index][amazonIndices['order id']]
        order_id_2 = lines[line_index + 1][amazonIndices['order id']]
        while order_id_1 == order_id_2: # since they will be together, I can just look 1 after.
            del lines[line_index + 1][amazonIndices['order id']]
            try:
                order_id_2 = lines[line_index + 1][amazonIndices['order id']]
            except:
                break
    return


# The purpose of this func is to sort the lines read in the file by date (ascending order)
def sortAscendingPurchaseDate(lines):
    # the formatting of the date in the file is always char 0 to char 18 on that column.
    last_date_char = 19

    # one list to keep track of order dates and one to keep track of which page is which order date
    order_dates = []
    order_pages = []

    # grabbing the order date of each item along with it's page num
    page_num = 0
    for line in lines:
        payment_date = (line.split('\t'))[
            amazonIndices['payment date']][0:last_date_char]
        date_obj = datetime.strptime(payment_date, "%Y-%m-%dT%H:%M:%S")
        order_dates.append(date_obj)
        order_pages.append(page_num)
        page_num += 1

    # ascending bubble sort with custom feature :D
    # custom feature: sorts the page numbers with it lol
    for i in range(len(order_dates) - 1):
        swapped = False
        for j in range((len(order_dates) - i) - 1):
            if order_dates[j] > order_dates[j+1]:
                order_dates[j], order_dates[j +1] = order_dates[j+1], order_dates[j]
                order_pages[j], order_pages[j + 1] = order_pages[j+1], order_pages[j] # amazing strat xd!
                swapped = True
        if not swapped:
            break

    return order_pages


def getGroupedPageOrder(lines):
    # one list for the item number (to keep track of where each one went) and one for the item name.
    item_numbers = []
    items = []
    i = 0

    # sort the lines in ascending date order. The PDF is sorted in this way, so now the lines
    # list and the pdf are synced.
    page_order = sortAscendingPurchaseDate(lines)
    m.printList(lines)

    # go through the text lines in ascending purchase date order.
    for page in page_order:
        data = lines[page].split('\t')
        sku = data[amazonIndices['sku']]

        # if the item exists already, insert it in the first position it's found. All of them should
        # be together anyways, so this is kind of adding it to the 'front' of that group.
        if sku in items:
            index = items.index(sku)
            items.insert(index, sku)
            item_numbers.insert(index, i)  # items and item_numbers are in sync
        else:
            items.append(sku)
            item_numbers.append(i)
        i += 1

    return item_numbers


def createSortedPdf(originalPDF, page_order):
    output_file = open('Grouped.pdf', 'wb')
    output_pdf = PdfFileWriter()
    for i in page_order:
        if i < originalPDF.getNumPages():
            output_pdf.addPage(originalPDF.getPage(i))
        else:
            print("Could not add page {}".format(i + 1))
    output_pdf.write(output_file)
    output_file.close()
    return


def main():
    file = open('./amazon.txt', 'r')

    # ignore first line in readlines() cus it's the titles
    page_order = getGroupedPageOrder(file.readlines()[1:])
    file.close()
    pdf_file = open('./amazon.pdf', 'rb')
    pdf_obj = PdfFileReader(pdf_file)
    createSortedPdf(pdf_obj, page_order)
    pdf_file.close()

    return 0


def pdfTest():
    file = open('./amazon.pdf', 'rb')
    pdf = PdfFileReader(file)
    output_pdf = PdfFileWriter()
    out_file = open('out.pdf', 'wb')
    output_pdf.addPage(pdf.getPage(0))
    output_pdf.write(out_file)
    print(pdf.getNumPages())
    file.close()
    out_file.close()
    return


def pdfTextTest():
    file = open("./amazon.pdf", "rb")
    pdf = PdfFileReader(file)
    for i in range(0, pdf.getNumPages()):
        print(pdf.getDocumentInfo())
        break
    file.close()
    return


if __name__ == "__main__":
    main()
