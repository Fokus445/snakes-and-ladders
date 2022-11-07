from pyllist import dllist

lst = dllist()

lst.appendleft(50)

lst.appendleft(250)

lst.appendleft(10)

lst.insert(30000,lst.nodeat(2))

print(lst)