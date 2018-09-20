import sys
from AVL import AVLTree

x = AVLTree()
y = AVLTree()

for i in range(1, 101):
    x.insert(i)

x.delete(101)
x.delete(100)
x.delete(98)

x.delete(10)
x.insert(10)

x.delete(12)

x.delete(97)
x.delete(11)
