from cmath import inf

import numpy as np
import skimage
from setuptools.build_meta import no_install_setup_requires

Numbers = [(3, 6,34 ), (17, 15, 3), (13, 15, 23), (6, 12,99 ), (9, 1, 6), (2, 7, 45), (10, 19, 47)]

Numbers = np.random.random((7,3))



class Node:
    def __init__(self,key):
        self.left = None
        self.right = None
        self.val = key

    def __repr__(self):
        # https://stackoverflow.com/questions/62406562/how-to-print-a-binary-search-tree-in-python
        lines = []
        if self.right:
            found = False
            for line in repr(self.right).split("\n"):
                if line[0] != " ":
                    found = True
                    line = " ┌─" + line
                elif found:
                    line = " | " + line
                else:
                    line = "   " + line
                lines.append(line)
        lines.append(str(self.val))

        if self.left:
            found = False
            for line in repr(self.left).split("\n"):
                if line[0] != " ":
                    found = True
                    line = " └─" + line
                elif found:
                    line = "   " + line
                else:
                    line = " | " + line
                lines.append(line)
        return "\n".join(lines)

class KDColorTreeLab:
    def __init__(self, colorLabs):
        self.colorLabs = colorLabs
        self.smallesDist = np.inf
        self.bestNode = None
        self.rootNode = None
        self.dimasion = 3

        for val in colorLabs:
            if self.rootNode is not None:
                self.insert(1,self.rootNode,val)
            else:
                self.rootNode = Node(val)

    def insert(self,depth,node, val):
        if val[depth%self.dimasion] < node.val[depth%self.dimasion]:
            if node.left is None:
                # print("left", depth)
                node.left = Node(val)
                return True
            self.insert(depth+1,node.left,val)
        else:
            if node.right is None:
                # print("right", depth)
                node.right = Node(val)
                return True
            self.insert(depth+1,node.right,val)


    def search(self, depth, node, target, bestNode=None):
        if node is None:
            return bestNode

        currentDimsion = depth % self.dimasion

        next_best = None
        next_branch = None
        other_branch = None

        distValue = self.dist(node, target)
        if bestNode is None or distValue < self.smallesDist:
            # print("fgdsjhf")
            next_best = node
            self.smallesDist = distValue
        else:
            next_best = bestNode

        if target[currentDimsion] < node.val[currentDimsion]:
            next_branch = node.left
            other_branch = node.right
        else:
            next_branch = node.right
            other_branch = node.left

        bestNode = self.search(depth + 1, next_branch, target, next_best)
        if self.smallesDist > abs(target[currentDimsion] - node.val[currentDimsion]):
            bestNode = self.search(depth + 1, other_branch, target, bestNode)
        # print(bestNode)
        return bestNode

        # if target[currentDimsion] < node.val[currentDimsion]:
        #     if node.left is None:
        #         distValue = self.dist(node, target)
        #         if self.smallesDist > distValue:
        #             self.smallesDist = self.dist(node, target)
        #             return node
        #
        #         if node.right is not None:
        #             if self.smallesDist > abs(node.val[currentDimsion]-target[currentDimsion]):
        #                 self.bestNode = self.search(depth + 1, node.right, target)
        #         return self.bestNode
        #     self.bestNode = self.search(depth + 1, node.left, target)
        # else:
        #     if node.right is None:
        #         distValue = self.dist(node, target)
        #         if self.smallesDist > distValue:
        #             self.smallesDist = self.dist(node, target)
        #             return node
        #
        #         if node.left is not None:
        #             if self.smallesDist > abs(node.val[currentDimsion]-target[currentDimsion]):
        #                 self.bestNode = self.search(depth + 1, node.left, target)
        #         return self.bestNode
        #     self.bestNode = self.search(depth + 1, node.right, target)


        return self.bestNode

    def dist(self, node, target):
        return ((target[0] - node.val[0]) ** 2 + (target[1] - node.val[1]) ** 2 + (target[2] - node.val[2]) ** 2) ** 0.5

test = KDColorTreeLab(Numbers)

def printLeftSide(node):
    print(node.val)
    if node.left:
        # print(node.left)
        printLeftSide(node.left)

def printRightSide(node):
    print(node.val)
    if node.right:
        # print(node.left)
        printRightSide(node.right)

print(test.rootNode.left)


print("-----------------------------")
print(str(test.rootNode))
print("-----------------------------")


print(test.search(0,test.rootNode, (42,69,22)).val, test.dist(test.search(0,test.rootNode, (42,69,22)), (42,69,22)))

best = inf
bestNodexs = None
for value in Numbers:
    print(value,test.dist(Node(value), (42,69,22)))
    if ((value[0]-42)**2 + (value[1]-69)**2 + (value[2]-22)**2)**0.5 < best:
        best = ((value[0]-42)**2 + (value[1]-69)**2 + (value[2]-22)**2)**0.5
        bestNodexs = value

bestNodexs = Node(bestNodexs)
print(bestNodexs, test.dist(bestNodexs,(42,69,22)))

antall_feil= 0
for i in range(100000):
    Numbers = np.random.random((7, 3))
    test = KDColorTreeLab(Numbers)
    nodeDK = test.search(0,test.rootNode, (42,69,22))

    best = inf
    bestNodexs = None
    for value in Numbers:
        # print(value, test.dist(Node(value), (42, 69, 22)))
        if ((value[0] - 42) ** 2 + (value[1] - 69) ** 2 + (value[2] - 22) ** 2) ** 0.5 < best:
            best = ((value[0] - 42) ** 2 + (value[1] - 69) ** 2 + (value[2] - 22) ** 2) ** 0.5
            bestNodexs = value

    bestNodexs = Node(bestNodexs)
    for y in range(3):
        if bestNodexs.val[y] != nodeDK.val[y]:
            print("feil",bestNodexs.val,nodeDK.val)
            antall_feil +=1
            break
print(antall_feil)