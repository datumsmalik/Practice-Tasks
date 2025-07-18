'''
# Original list
lis = [[11, 22, 33, 44], [55, 66, 77], [88, 99, 100]]

# iterate through the sublist using List comprehension
flatList = [element for innerList in lis for element in innerList]

# printing original list
print('List', lis)
# printing flat list
print('Flat List', flatList)
'''
# i have chnages this example simple nesting yani list or sublist is method k zarye ho jati he ab masla ye he k hamara problem me nesting ziada he to is logic k mutabiq nested iterable consider nahi hon gi error ae ga


# ab recursive code likh rha hun mene geeks for geeks se recursion samagh k kia he 
Data = [1,[2,[3,4],5],6,[[7]]]

output = []

def remove_kr_nesting(Data):
    for i in Data:
        if type(i) == list:
            remove_kr_nesting(i)
        else:
            output.append(i)

remove_kr_nesting(Data)
print(output)