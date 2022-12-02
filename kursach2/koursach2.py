import csv
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



def select_sorted(sort_columns=["high"], limit=30, group_by_name=False, order='desc', filename='dump.csv'):
    with open('all_stocks_5yr.csv', 'r', newline='') as csvfile:
           lst = []
           reader = csv.DictReader(csvfile)
           for row in reader:
             if row[sort_columns[0]] != '':
                 lst.append(row)
           #[lst.append(x) for x in csv.DictReader(csvfile)]  
           quick_sort(lst, sort_columns)
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
        '''Записываем в файл результат сортировки'''
           if filename:
                with open(filename, 'w', newline='') as csvfile:
                    write = csv.writer(csvfile)
                    for i in lst[:limit]:
                        write.writerow(i.values())





select_sorted(sort_columns=["high"], order='desc', group_by_name=True)            
