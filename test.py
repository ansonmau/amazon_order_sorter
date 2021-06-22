import mundane as m
from PyPDF2 import PdfFileReader, PdfFileWriter
def testswap():
    l = [0, 3, 2, 9, 1, 3, 72, 12]

    for i in range(len(l) - 1):
        swapped = False
        for j in range((len(l) - i) - 1):
            if l[j] > l[j+1]:
                l[j], l[j+1] = l[j+1], l[j]
                swapped = True
        if not swapped:
            break

    m.printList(l)


def testRemoveDup():
    amazonIndices = {
    'order id': 0,
    'payment date': 2,
    'sku': 10,
    'item name': 11,
    }   
    file = open("./amazon_test.txt", "r")
    lines = file.readlines()[1:]

    for i in range(len(lines)):
        lines[i] = lines[i].split('\t')

    print("BEFORE---------------------")
    for line in lines:
        print(line[amazonIndices['order id']])
    print()

    line_index = 0
    len_lines = len(lines)
    while line_index < (len_lines - 1):
        order_id_1 = lines[line_index][amazonIndices['order id']]
        order_id_2 = lines[line_index + 1][amazonIndices['order id']]
        while order_id_1 == order_id_2: # since they will be together, I can just look 1 after.
            del lines[line_index + 1]
            len_lines = len(lines)
            if (line_index + 1 == len_lines):
                break
            else:
                order_id_2 = lines[line_index + 1][amazonIndices['order id']]
        line_index += 1

    print("AFTER---------------------")
    for line in lines:
        print(line[amazonIndices['order id']])
    

    file.close()

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

testRemoveDup()