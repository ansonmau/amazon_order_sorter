from PyPDF2 import PdfFileReader, PdfFileWriter
import secret

amazonIndices = {
    'order id': 0,
    'sku': 10,
    'item name': 11,
}


def getGroupedPageOrder(lines):
    # one list for the item number (to keep track of where each one went) and one for the item name.
    item_numbers = []
    items = []
    i = 0
    # the first line is titles so i'm ignoring that
    for line in lines:
        data = line.split('\t')
        sku = data[amazonIndices['sku']]

        # if the item exists already, insert it in the first position it's found. All of them should
        # be together anyways, so this is kind of adding it to the 'front' of that list.
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


if __name__ == "__main__":
    main()


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

    return
