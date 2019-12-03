from itertools import chain

unsortedList = [['a', '2', ''], ['a', '5', ''], ['b', '4', ''], ['y', '3', ''], ['z', '1', ''], ['z', '6', '']]

sortedList=[]
for (a,b,c) in unsortedList:
    sortedList.append(a)

for (a,b,c) in unsortedList:
    sortedList.append(b)

for (a,b,c) in unsortedList:
    sortedList.append(c)

print(sortedList)

result = [['a', 'a', 'b', 'y', 'z', 'z'], ['2', '5', '4', '3', '1', '6'], ['', '', '', '', '', ''], [], [], []]
print()
print(result)