from PyPDF2 import PdfFileReader, PdfFileWriter
from datetime import datetime
import mundane as m

file_indices = {
    'order id': 0,
    'payment date': 2,
    'sku': 10,
    'item name': 11,
}

def isInSync(lines, pdf):
    return len(lines) == pdf.getNumPages()

# the purpose of this func is to remove any duplicates with the same ID. Orders with multiple
# items are stored as different orders in the file, so this is to remove the lines so the pdf
# pages and the text line up.
def RemoveDupIDs(lines):

    lineData = []

    # splitting lines here for less typing and less headache for the while loop (yay!)
    for line_index in range(len(lines)):
        lineData.append(lines[line_index].split('\t'))
    
    # Must keep track of current line index and the current length of the lines list
    line_index = 0
    len_lines = len(lines)

    # using while instead of for loop since len_lines will be updating throughout the loop.
    # -1 because I will be looking at index + 1 and dont want to go out of bounds.
    while line_index < (len_lines - 1):
        # keep track of order id of current index and the next. Duplicates will be next to each other.
        orderID_1 = lineData[line_index][file_indices['order id']]
        orderID_2 = lineData[line_index + 1][file_indices['order id']]
        
        # since they are next to each other, I'll just keep looping the one infront of them until it hits one that
        # isn't the same.
        while orderID_1 == orderID_2:
            del lineData[line_index + 1]
            del lines[line_index + 1]
            len_lines = len(lines) # update this right after del so I can make sure not to go out of bounds
            if (line_index + 1 == len_lines): # guard for index out of bound
                break 
            else:
                orderID_2 = lineData[line_index + 1][file_indices['order id']]
        line_index += 1
    
    # no return value since lines is a list (PBR) and that's what I want to change.
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
            file_indices['payment date']][0:last_date_char]
        date_obj = datetime.strptime(payment_date, "%Y-%m-%dT%H:%M:%S")
        order_dates.append(date_obj)
        order_pages.append(page_num)
        page_num += 1

    # ascending bubble sort with custom feature :D
    # bubble sort not ideal but it is good practice
    # custom feature: sorts the page numbers with it lol
    for i in range(len(order_dates) - 1):
        swapped = False
        for j in range((len(order_dates) - i) - 1):
            if order_dates[j] > order_dates[j+1]:
                order_dates[j], order_dates[j + 1] = order_dates[j + 1], order_dates[j]
                order_pages[j], order_pages[j + 1] = order_pages[j + 1], order_pages[j] # amazing strat xd!
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

    # go through the text lines in ascending purchase date order.
    for page in page_order:
        data = lines[page].split('\t')
        sku = data[file_indices['sku']]

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
    output_file = open('SORTED.pdf', 'wb')
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
    try:
        file = open('./amazon.txt', 'r')
    except:
        input("Missing amazon.txt. Press enter to exit.")
        return
    try:
        pdf_file = open('./amazon1.pdf', 'rb')
    except:
        input("Missing amazon pdf file. Press enter to exit.")
        return

    pdf_obj = PdfFileReader(pdf_file)

    lines = file.readlines()[1:]
    
    # multiple items in the same order are counted as different orders in the file. I do not want this.
    RemoveDupIDs(lines)

    if not isInSync(lines, pdf_obj):
        print("There are a different number of orders in the text file than there are in the pdf(s).")
        file.close()
        pdf_file.close()
        input("Press enter to exit.")
        return
            

    page_order = getGroupedPageOrder(lines) # ignore first line in readlines() cus it's the titles
    file.close() # don't need the file anymore after getting proper order
    
    createSortedPdf(pdf_obj, page_order)
    
    pdf_file.close()

    return


if __name__ == "__main__":
    main()
