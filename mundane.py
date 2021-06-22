def printList(l, num = -1, order = []):
    if num == -1:
        if order:
            myRange = order
        else:
            myRange = range(len(l))
    else:
        if order:
            myRange = order[:num]
        else:
            myRange = range(0, num)

    for i in myRange:
        print(f"[{i}]->{l[i]}")
    return

def printListOrdered(l, order):
    x = 0
    for i in order:
        print(f"[{x}]->{l[i]}")
        x+=1