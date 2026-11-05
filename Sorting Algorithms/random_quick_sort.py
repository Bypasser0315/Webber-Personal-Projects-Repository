import time 
sort = True
sort_list = []

while sort == True:
  item = input("input a number here, or finish by inputting 'end': ")
  if item != 'end':
    try:
      sort_list.append(float(item))
      print(sort_list)
    except:
      print("item could not be inserted into list. Try something else.")
  else:
    sort = False

#Sort Function
import random
def RquickSort(qList):
    #logic for a triple (or more) item list
    if len(qList) >= 3:
      #seperate left, middle, right
      left = []
      right = []
      pivot = random.randint(0, len(qList)-1)
      middle = qList[pivot]
      qList.pop(pivot)
      #the quick sort moving
      for i in qList:
        left.append(i) if i < middle else right.append(i)
      #this continutes the sort as left and right may not be sorted yet
      return RquickSort(left), middle, RquickSort(right)
    #apply a standard bubble sort for a 2 item list
    elif len(qList) == 2:
      if qList[0] < qList[1]:
        return qList[0], qList[1] 
      return qList[1], qList[0]
    #list is only one item, so this doesnt need to be sorted
    else:
      return qList

def flatten(items):
    flat = []
    for item in items:
        if isinstance(item, (list, tuple)):
            flat.extend(flatten(item))
        else:
            flat.append(item)
    return flat

sort_list = flatten(RquickSort(sort_list))
print("Sort completed, final list is: ", sort_list)

