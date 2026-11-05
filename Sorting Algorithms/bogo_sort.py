#setup
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
def bogoSort(bogoList):
  if len(bogoList) == 0:
    return bogoList, 0
  shuffling = True
  sort_count = 0 
  while shuffling == True:
    list_count = 0
    random.shuffle(bogoList)
    for i in range(len(bogoList)-1):
      
      if bogoList[i] > bogoList[i+1]:
        list_count = 0
      else:
        list_count += 1
    sort_count += 1
    print("current list is ", bogoList)
    if list_count == len(bogoList) - 1:
      shuffling = False
      return bogoList, sort_count

sort_list, sort_counter = bogoSort(sort_list)
print(f"sort complete, total number of trials attempted is {sort_counter}, final list is {sort_list}")
