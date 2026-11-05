#setup
import time 
sort = True
sort_list = []
print("Hello World")


while sort == True:
  item = input("input a number here, or finish by inputting 'end': ")
  if item != 'end':
    try:
      sort_list.append(float(item))
      print("item successfully appended")
      print(sort_list)
    except:
      print("item could not be inserted into list. Try something else.")
  else:
    sort = False

def bubbleSort(sorting_list):
  bubbleSort_counter = 0 
  while bubbleSort_counter != len(sorting_list):
    bubbleSort_counter = 0
    for i in range(len(sorting_list)):
      if i < len(sorting_list) - 1 and sorting_list[i] > sorting_list[i+1]:
        temp_var = sorting_list[i+1]
        sorting_list.insert(i, temp_var)
        sorting_list.pop(i+2)
        bubbleSort_counter = 0
      else:
        bubbleSort_counter += 1
    print("pass complete, the list after the pass is: ", sorting_list, "length of list is", len(sorting_list))
    time.sleep(1)
  return sorting_list

bubbleSort(sort_list)
print("sort completed, final list is ", sort_list)