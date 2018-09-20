import sys

class AVLTree:
    def __init__(self):
        self._root = None;

    def insert(self, key):
        print("Insert: " + str(key))
        if self._root is None:
            self._root = Node(key)
        else:
            self._root = self._root.insert(key)
        print(self)
        print("\n")

    def delete(self, key):
        print("Delete: " + str(key))
        if self._root is not None:
            self._root = self._root.delete(key)
        print(self)
        print("\n")

    def __str__(self):
        if self._root is not None:
            return str(self._root)
        else:
            return "empty";

def treeAsString(list):
    currentHeight = 0
    val = ''
    prevPosition = 0
    for node in list:
        if node._height > currentHeight:
            currentHeight = node._height
            prevPosition = 0
            val += "\n"
        if node._left is not None:
            list.append(node._left)
            leftChildStart = node._left._stringPosition
        if node._right is not None:
            list.append(node._right)
            rightChildStart = node._right._stringPosition

        if node._left is not None:
            for i in range(prevPosition, leftChildStart):
                val += " "
            val += "┌"
            for i in range(leftChildStart+1, node._stringPosition):
                val += "─"
        else:
            for i in range(prevPosition, node._stringPosition):
                val += " "
        stringValue = str(node._key)
        val += stringValue

        if node._right is not None:
            for i in range(node._stringPosition + len(stringValue), rightChildStart):
                val += "─"
            val += "┐"
            prevPosition = rightChildStart + 1
        else:
            prevPosition = node._stringPosition + len(stringValue)

    return val

class Node:
    def __init__(self, key):
        self._key = key;
        self._balance = 0;
        self._left = None;
        self._right = None;

    def __str__(self):
        self._calcStringPosition(0, 0)
        list = [self]
        return treeAsString(list)

    def _calcStringPosition(self, startPos, height):
        self._height = height
        if self._left is None:
            endPos = startPos
        else:
            endPos = self._left._calcStringPosition(startPos, height + 1)

        self._stringPosition = endPos
        endPos += len(str(self._key))

        if self._right is not None:
            endPos = self._right._calcStringPosition(endPos, height + 1)

        return endPos

    def insert(self, key):
        if key < self._key:
            if self._left is None:
                self._left = Node(key)
                self._balance += 1
            else:
                old = self._left._balance
                self._left = self._left.insert(key)
                new = self._left._balance
                if old == 0 and new != 0:
                    self._balance += 1
        else:
            if self._right is None:
                self._right = Node(key)
                self._balance -= 1
            else:
                old = self._right._balance
                self._right = self._right.insert(key)
                new = self._right._balance
                if old == 0 and new != 0:
                    self._balance -= 1
        return self._balanceNode()

    def delete(self, key):
        if key < self._key:
            if self._left is None:
                return self
            else:
                old = self._left._balance
                self._left = self._left.delete(key)
                if self._left is None:
                    self._balance -= 1
                else:
                    new = self._left._balance
                    if old != 0 and new == 0:
                        self._balance -= 1
                return self._balanceNode()
        elif key > self._key:
            if self._right is None:
                return self
            else:
                old = self._right._balance
                self._right = self._right.delete(key)
                if self._right is None:
                    self._balance += 1
                else:
                    new = self._right._balance
                    if old != 0 and new == 0:
                        self._balance += 1
                return self._balanceNode()
        else:
            left = self._left
            right = self._right
            if left is None and right is None:
                return None
            elif left is None and right is not None:
                return right
            elif left is not None and right is None:
                return left
            else:
                greatestLesserChild = left
                while greatestLesserChild._right is not None:
                    greatestLesserChild = greatestLesserChild._right
                self._key = greatestLesserChild._key
                old = self._left._balance
                self._left = self._left.delete(greatestLesserChild._key)
                if self._left is None:
                    self._balance -= 1
                else:
                    new = self._left._balance
                    if old != 0 and new == 0:
                        self._balance -= 1
                return self._balanceNode()


    def _balanceNode(self):
        if self._balance != 2 and self._balance != -2:
            return self

        if self._balance == 2:
            if self._left._balance == 1:
                self._balance = 0
                self._left._balance = 0;
                return self._rotateRight()
            elif self._left._balance == 0:
                self._balance = 1
                self._left._balance = -1
                return self._rotateRight()
            elif self._left._balance == -1:
                leftRightBalance = self._left._right._balance
                if leftRightBalance == 0:
                    self._balance = 0
                    self._left._balance = 0
                elif leftRightBalance == 1:
                    self._balance = -1
                    self._left._balance = 0
                elif leftRightBalance == -1:
                    self._balance = 0
                    self._left._balance = 1
                self._left._right._balance = 0
                self._left = self._left._rotateLeft()
                return self._rotateRight()

        elif self._balance == -2:
            if self._right._balance == -1:
                self._balance = 0
                self._right._balance = 0;
                return self._rotateLeft()
            elif self._right._balance == 0:
                self._balance = -1
                self._right._balance = 1
                return self._rotateLeft()
            elif self._right._balance == 1:
                rightLeftBalance = self._right._left._balance
                if rightLeftBalance == 0:
                    self._balance = 0
                    self._right._balance = 0
                elif rightLeftBalance == -1:
                    self._balance = 1
                    self._right._balance = 0
                elif rightLeftBalance == 1:
                    self._balance = 0
                    self._right._balance = -1
                self._right._left._balance = 0
                self._right = self._right._rotateRight()
                return self._rotateLeft()

    def _rotateLeft(self):
        right = self._right
        if right is None:
            return self #maybe throw an exception instead

        oldRightLeftChild = right._left
        right._left = self
        right._left._right = oldRightLeftChild
        return right

    def _rotateRight(self):
        left = self._left
        if left is None:
            return self #maybe throw an exception instead

        oldLeftRightChild = left._right
        left._right = self
        left._right._left = oldLeftRightChild
        return left
