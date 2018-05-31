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
    res = "1+2"
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()


    def createWidgets(self):
        self.stringInput = Entry(self)
        self.stringInput.grid(row=0, column=0, columnspan=4)

        self.alertButton = Button(self, text=' 7 ', command=self.putStringSeven)
        self.alertButton.grid(row=1, column=0)
        
        self.alertButton1 = Button(self, text=' 8 ', command=self.putStringEight)
        self.alertButton1.grid(row=1, column=1)
        
        self.alertButton2 = Button(self, text=' 9 ', command=self.putStringNine)
        self.alertButton2.grid(row=1, column=2)
        
        self.alertButton3 = Button(self, text=' x ', command=self.putStringMUL)
        self.alertButton3.grid(row=1, column=3)
        
        self.alertButton4 = Button(self, text=' 4 ', command=self.putStringFour)
        self.alertButton4.grid(row=2, column=0)
        
        self.alertButton5 = Button(self, text=' 5 ', command=self.putStringFive)
        self.alertButton5.grid(row=2, column=1)
        
        self.alertButton6 = Button(self, text=' 6 ', command=self.putStringSix)
        self.alertButton6.grid(row=2, column=2)
        
        self.alertButton7 = Button(self, text=' - ', command=self.putStringSUB)
        self.alertButton7.grid(row=2, column=3)
        
        self.alertButton8 = Button(self, text=' 1 ', command=self.putStringOne)
        self.alertButton8.grid(row=3, column=0)
        
        self.alertButton9 = Button(self, text=' 2 ', command=self.putStringTwo)
        self.alertButton9.grid(row=3, column=1)

        self.alertButton10 = Button(self, text=' 3 ', command=self.putStringThree)
        self.alertButton10.grid(row=3, column=2)
        
        self.alertButton11 = Button(self, text=' + ', command=self.putStringADD)
        self.alertButton11.grid(row=3, column=3)
        
        self.alertButton12 = Button(self, text=' 0 ', command=self.putStringZero)
        self.alertButton12.grid(row=4, column=0)
        
        self.alertButton13 = Button(self, text=' ( ', command=self.putStringLeft)
        self.alertButton13.grid(row=4, column=1)

        self.alertButton14 = Button(self, text=' ) ', command=self.putStringRight)
        self.alertButton14.grid(row=4, column=2)
        
        self.alertButton15 = Button(self, text=' = ', command=self.getResult)
        self.alertButton15.grid(row=4, column=3)

    def getResult(self):
        result = self.stringInput.get()
        messagebox.showinfo('Results', operate(result))

    def putStringSeven(self):
        self.stringInput.insert('insert', '7')

    def putStringEight(self):
        self.stringInput.insert('insert', '8')

    def putStringNine(self):
        self.stringInput.insert('insert', '9')

    def putStringMUL(self):
        self.stringInput.insert('insert', 'x')
    
    def putStringFour(self):
        self.stringInput.insert('insert', '4')

    def putStringFive(self):
        self.stringInput.insert('insert', '5')

    def putStringSix(self):
        self.stringInput.insert('insert', '6')

    def putStringSUB(self):
        self.stringInput.insert('insert', '-')
    
    def putStringOne(self):
        self.stringInput.insert('insert', '1')

    def putStringTwo(self):
        self.stringInput.insert('insert', '2')

    def putStringThree(self):
        self.stringInput.insert('insert', '3')

    def putStringADD(self):
        self.stringInput.insert('insert', '+')

    def putStringZero(self):
        self.stringInput.insert('insert', '0')

    def putStringLeft(self):
        self.stringInput.insert('insert', '(')

    def putStringRight(self):
        self.stringInput.insert('insert', ')')


app = Application()
# 设置窗口标题:
app.master.title('Calculator')
app.master.geometry('300x200')
# 主消息循环:
app.mainloop()