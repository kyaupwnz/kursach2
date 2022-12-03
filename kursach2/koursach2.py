import csv
from functools import lru_cache
def partition(lst, low, high, sort_columns):
# Выбираем средний элемент в качестве опорного
# Также возможен выбор первого, последнего
# или произвольного элементов в качестве опорного

  pivot = lst[(low + high) // 2][sort_columns[0]] 
  i = low - 1
  j = high + 1
  while True:
    i += 1
    while lst[i][sort_columns[0]] < pivot:
      i += 1

    j -= 1
    while lst[j][sort_columns[0]] > pivot:
      j -= 1

    if i >= j:
      return j
                         
# Если элемент с индексом i (слева от опорного) больше, чем
# элемент с индексом j (справа от опорного), меняем их 
    lst[i], lst[j] = lst[j], lst[i]


def quick_sort(lst, sort_columns):
# Создадим вспомогательную функцию, которая вызывается рекурсивно
  def _quick_sort(lst, low, high, sort_columns):
    if low < high:
# This is the index after the pivot, where our lists are split
      split_index = partition(lst, low, high, sort_columns)
      _quick_sort(lst, low, split_index, sort_columns)
      _quick_sort(lst, split_index + 1, high, sort_columns)

  return _quick_sort(lst, 0, len(lst) - 1, sort_columns)


@lru_cache
def select_sorted(sort_columns=["high"], limit=30, group_by_name=False, order='desc', filename='dump.csv'):
    with open('all_stocks_5yr.csv', 'r', newline='') as csvfile:
           lst = []
           reader = csv.DictReader(csvfile)
           for row in reader:
             if row[sort_columns[0]] != '':
                 lst.append(row)
           #[lst.append(x) for x in csv.DictReader(csvfile)]  
           quick_sort(lst, sort_columns)
           lst_sorted = lst
           '''Дополнительно сортируем по имени'''
           if group_by_name:
             lst = sorted(lst, key=lambda x: x['Name'])
             '''сортируем по возрастанию или по убыванию'''
           if order == 'desc':
             for i in lst[:limit]:
               print(i.values())
           else:
               lst.reverse()
               for i in lst[:limit]:
                   print(i.values())
#Записываем в файл результат сортировки
           if filename:
                with open(filename, 'w', newline='') as csvfile:
                    write = csv.writer(csvfile)
                    for i in lst[:limit]:
                        write.writerow(i.values())
                        



def binary_search_iterativ(lst_sorted, element, name):
  mid = 0
  start = 0
  end = len(lst_sorted)
  step = 0
  
  while (start <= end):
    
    step = step+1
    mid = (start + end) // 2
    if element == lst_sorted[mid]['date'] and name == lst_sorted[mid]['Name']:
      return lst_sorted[mid]
    if element < lst_sorted[mid]['date']:
      end = mid - 1
    else:
      start = mid + 1
  return -1

@lru_cache
def get_by_date(date=None, name=None, filename='dump.csv'):
    with open('all_stocks_5yr.csv', 'r', newline='') as csvfile:
     lst = []
     
     reader = csv.DictReader(csvfile)
     for row in reader:
         lst.append(row)

     lst_sorted = sorted(lst, key=lambda x: x['date'])     

     print(binary_search_iterativ(lst_sorted, date, name))
     #if filename:
          #with open(filename, 'w', newline='') as csvfile:
            #fieldnames = ['date', 'open', 'high', 'low', 'close', 'volume', 'Name']  
            #write = csv.DictWriter(csvfile, fieldnames = fieldnames)
            #write.writeheader()
            
            #write.writerow(binary_search_iterativ(lst, date, name))

    

def main():
    pass




#select_sorted(sort_columns=["date"], order='desc', limit=None, filename='dump.csv' ) 
get_by_date(date="2017-08-08", name="PCLN", filename='dump.csv')
#get_by_date(name="PCLN", filename='dump.csv')
