def printList(l, num = -1):
    if num == -1:
        for i in range(len(l)):
            print(f"[{i}]->{l[i]}")
        return 
    
    for i in range(0,num):
        print(f"[{i}]->{l[i]}")
    return
