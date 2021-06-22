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
    file = open("./amazon.txt", "r")
    lines = file.readlines()[1:]

    for i in range(len(lines)):
        lines[i] = lines[i].split('\t')

    print("BEFORE---------------------")
    for line in range(len(lines)):
        print("[{}]->{}".format(line, lines[line][amazonIndices['order id']]))
    print()

    line_index = 0
    len_lines = len(lines)
    while line_index < (len_lines - 1):
        order_id_1 = lines[line_index][amazonIndices['order id']]
        order_id_2 = lines[line_index + 1][amazonIndices['order id']]
        while order_id_1 == order_id_2: # since they will be together, I can just look 1 after.
            print(f"Found duplicate for {order_id_1}")
            del lines[line_index + 1]
            len_lines = len(lines)
            if (line_index + 1 == len_lines):
                break
            else:
                order_id_2 = lines[line_index + 1][amazonIndices['order id']]
        line_index += 1

    print("AFTER---------------------")
    for line in range(len(lines)):
        print("[{}]->{}".format(line, lines[line][amazonIndices['order id']]))
    print()
    

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
    

def testPDFText():
    file = open("./amazon.pdf", "rb")
    pdf = PdfFileReader(file)
    for i in range(0, pdf.getNumPages()):
        print(pdf.getDocumentInfo())
        break
    file.close()
    return


def testMergePDFS():
    new_pdf_file = open("./amazon_all.pdf", "wb")
    new_pdf = PdfFileWriter()

    pdf_count = 0

    while True:
        try:
            file = open(f"./amazon{pdf_count + 1}.pdf", "rb")
        except:
            print(f"There are {pdf_count} pdfs!")
            break 

        print(f"Merging amazon{pdf_count + 1}.pdf")
        pdf = PdfFileReader(file)
        for page_num in range(pdf.getNumPages()):
            new_pdf.addPage(pdf.getPage(page_num))
        new_pdf.write(new_pdf_file)
        pdf_count += 1
        file.close()

    new_pdf_file.close()
    return new_pdf

def testReturnMerge():
    new_pdf = testMergePDFS()
    print(new_pdf.getNumPages())

testReturnMerge()