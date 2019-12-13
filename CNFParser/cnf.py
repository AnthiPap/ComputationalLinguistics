from sys import stdin, stderr
from json import loads, dumps

def cnf(tree):
    #implement the method below to all trees
    tree = to_cnf(tree)
    return tree

def to_cnf(tree):
    n = len(tree)
    #cases like 'S', no modification
    if type(tree) is str:
        return tree
    #two elements, no modification
    if n == 2 and type(tree[1]) is str:
        return tree
    #unary rules
    while n == 2 and type(tree[1]) is list:
        #create new node
        new_name =  tree[0] + '+' + tree[1][0]
        tree  = [new_name] + tree[1][1:]
        n = len(tree)
    #trees with length more than 3
    if n > 3:
        tree1 = tree[2:]
        tree2 = tree[:2]
        #create new node
        new_name =  tree[0] + '|' + tree[1][0]
        tree = tree2 + [[new_name] + tree1]
        
    #implement recursion to take all trees into consideration          
    tree = [to_cnf(each) for each in tree]
    return tree   
     

def is_cnf(tree):
    n = len(tree)
    if n == 2:
        return isinstance(tree[1], str)
    elif n == 3:
        return is_cnf(tree[1]) and is_cnf(tree[2])
    else:
        return False

def words(tree):
    if isinstance(tree, str):
        return [tree]
    else:
        ws = []
        for t in tree[1:]:
            ws = ws + words(t)
        return ws

if __name__ == "__main__":
    count = 0
    for line in stdin:
        tree = loads(line)
        sentence = words(tree)
        input = str(dumps(tree))
        tree = cnf(tree) 
        if is_cnf(tree) and words(tree) == sentence:
            print(dumps(tree))
        else:
            print("Something went wrong!", file=stderr)
            print("Sentence: " + " ".join(sentence), file=stderr)
            print("Input: " + input, file=stderr)
            print("Output: " + str(dumps(tree)), file=stderr)
            exit()



