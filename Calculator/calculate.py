from tkinter import *
import tkinter.messagebox as messagebox

class Buffer(object):
    def __init__(self, data):
        self.data = data
        self.offset = 0

    def peek(self):
        if self.offset >= len(self.data):
            return None
        return self.data[self.offset]

    def advance(self):
        self.offset += 1


class Token(object):
    def consume(self, buffer):
        pass


class TokenInt(Token):
    def consume(self, buffer):
        accum = ""
        while True:
            ch = buffer.peek()
            if ch is None or ch not in "0123456789":
                break
            else:
                accum += ch
                buffer.advance()

        if accum != "":
            return ("int", int(accum))
        else:
            return None


class TokenOperator(Token):
    def consume(self, buffer):
        ch = buffer.peek()
        if ch is not None and ch in "+-":
            buffer.advance()
            return ("ope", ch)
        return None


class Node(object):
    pass


class NodeInt(Node):
    def __init__(self, value):
        self.value = value


class NodeBinaryOp(Node):
    def __init__(self, kind):
        self.kind = kind
        self.left = None
        self.right = None


def operator(string):
    tokens = tokenize(string)
    node = parse(tokens)
    return evaluate(node)


def evaluate(node):
    if isinstance(node, NodeInt):
        return node.value
    else:
        return calculate(node)


def tokenize(string):
    buffer = Buffer(string)
    tk_int = TokenInt()
    tk_op = TokenOperator()
    tokens = []    
    while buffer.peek():
        token = None
        for tk in (tk_int, tk_op):      
            token = tk.consume(buffer)
            if token:
                print(token)
                tokens.append(token)
                break

        if not token:
            raise ValueError("Error in syntax")    
    return tokens


def parse(tokens):
    if tokens[0][0] != "int":
        raise ValueError("Must start with an int")

    node = NodeInt(tokens[0][1])
    nbo = None
    last = tokens[0][0]

    for token in tokens[1:]:
        if token[0] == last:
            raise ValueError("Error in syntax")
        last = token[0]
        if token[0] == 'ope':
            nbo = NodeBinaryOp(token[1])
            nbo.left = node

        if token[0] == 'int':
            nbo.right = NodeInt(token[1])
            node = nbo
    return node


def calculate(nbo):
    
    if isinstance(nbo.left, NodeBinaryOp):
        leftval = calculate(nbo.left)
    else:
        leftval = nbo.left.value
    
    leftval = nbo.left.value

    if nbo.kind == '-':
        return leftval - nbo.right.value
    elif nbo.kind == '+':
        return leftval + nbo.right.value
    else:
        raise ValueError("Wrong operator")


def operate(string):
    tokens = tokenize(string)
    node = parse(tokens)
    return evaluate(node)

'''
if __name__ == '__main__':
    input = input('Input:')
    tokens = tokenize(input)
    node = parse(tokens)
    print(evaluate(node))
'''


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.stringInput = Entry(self)
        self.stringInput.grid(row=0,column=1)
        self.alertButton = Button(self, text='Compute', command=self.hello)
        self.alertButton.grid(row=1,column=0)
        self.alertButton1 = Button(self, text='Compute1', command=self.hello)
        self.alertButton1.grid(row=1,column=1)
        self.alertButton2 = Button(self, text='Compute2', command=self.hello)
        self.alertButton2.grid(row=1,column=2)
        self.alertButton3 = Button(self, text='Compute3', command=self.hello)
        self.alertButton3.grid(row=2,column=0)
        self.alertButton4 = Button(self, text='Compute4', command=self.hello)
        self.alertButton4.grid(row=2,column=1)

    def hello(self):
        result = self.stringInput.get() 
        messagebox.showinfo('Message', operate(result))

app = Application()
# 设置窗口标题:
app.master.title('Hello World')
app.master.geometry('250x150')
# 主消息循环:
app.mainloop()