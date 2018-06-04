from tkinter import *
import tkinter.messagebox as messagebox


class Cal:
    # 获取表达式的优先级
    def getPriority(self, s):
        if s == "(":
            return 0
        elif s == "+" or s == "-":
            return 1
        elif s == "x" or s == "/":
            return 2
        else:
            return 3
   
    # 将输入的字符串转换为表达式
    def getExpression(self, input):
        expression = []
        str = ""
        for c in input:
            if c in "+-x/()":
                if str:
                    expression.append(str)
                    str = ""
                expression.append(c)
            else:
                str += c
        if str:
            expression.append(str)
        return expression
    
    # 得到逆波兰表达式
    def postExpression(self, expression):
        post = []
        stack = []
        for c in expression:
            if c == "(":
                stack.append(c)
            elif c == ")":
                while stack[-1] != "(":
                    post.append(stack.pop())
                stack.pop()
            else:
                if c not in "+-x/":
                    stack.append(c)
                else:
                    while stack and self.getPriority(stack[-1]) >= self.getPriority(c):
                        post.append(stack.pop())
                    stack.append(c)
        while stack:
            post.append(stack.pop())
        return post
    
    # 逆波兰表达式求值
    def evaluateExpression(self, input):
        expression = self.getExpression(input)
        post = self.postExpression(expression)
        stack = []
        for c in post:
            if c in "+-x/":
                num = 0
                x = int(stack.pop())
                y = int(stack.pop())
                if c == "+":
                    num = y + x
                elif c == "-":
                    num = y - x
                elif c == "x":
                    num = y*x
                else:
                    if x == 0:
                        return 0
                    else:
                        num = y//x
                stack.append(str(num))
            else:
                stack.append(c)
        if stack:
            return stack.pop()
        else:
            return 0


'''   
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

if __name__ == '__main__':
    input = input('Input:')
    tokens = tokenize(input)
    node = parse(tokens)
    print(evaluate(node))
'''


class Application(Frame, Cal):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
    
    # 页面布局
    def createWidgets(self):
        # 文本框
        self.stringInput = Entry(self, width=25)
        self.stringInput.grid(row=0, column=0, columnspan=4)
        # Button
        self.alertButton = Button(self, text='CE', width=5, height=2, command=self.clearInput)
        self.alertButton.grid(row=1, column=0)

        self.alertButton = Button(self, text='C', width=5, height=2, command=self.clearInput)
        self.alertButton.grid(row=1, column=1)

        self.alertButton = Button(self, text='<-', width=5, height=2, command=self.backupInput)
        self.alertButton.grid(row=1, column=2)

        self.alertButton = Button(self, text='/', width=5, height=2, command=lambda: self.handlerOpe(str='/'))
        self.alertButton.grid(row=1, column=3)

        self.alertButton = Button(self, text='7', width=5, height=2, command=lambda: self.handlerNum(str='7'))
        self.alertButton.grid(row=2, column=0)
        
        self.alertButton1 = Button(self, text='8', width=5, height=2, command=lambda: self.handlerNum(str='8'))
        self.alertButton1.grid(row=2, column=1)
        
        self.alertButton2 = Button(self, text='9', width=5, height=2, command=lambda: self.handlerNum(str='9'))
        self.alertButton2.grid(row=2, column=2)
        
        self.alertButton3 = Button(self, text='x', width=5, height=2,  command=lambda: self.handlerOpe(str='x'))
        self.alertButton3.grid(row=2, column=3)
        
        self.alertButton4 = Button(self, text='4', width=5, height=2, command=lambda: self.handlerNum(str='4'))
        self.alertButton4.grid(row=3, column=0)
        
        self.alertButton5 = Button(self, text='5', width=5, height=2, command=lambda: self.handlerNum(str='5'))
        self.alertButton5.grid(row=3, column=1)
        
        self.alertButton6 = Button(self, text='6', width=5, height=2, command=lambda: self.handlerNum(str='6'))
        self.alertButton6.grid(row=3, column=2)
        
        self.alertButton7 = Button(self, text='-', width=5, height=2, command=lambda: self.handlerOpe(str='-'))
        self.alertButton7.grid(row=3, column=3)
        
        self.alertButton8 = Button(self, text='1', width=5, height=2, command=lambda: self.handlerNum(str='1'))
        self.alertButton8.grid(row=4, column=0)
        
        self.alertButton9 = Button(self, text='2', width=5, height=2, command=lambda: self.handlerNum(str='2'))
        self.alertButton9.grid(row=4, column=1)

        self.alertButton10 = Button(self, text='3', width=5, height=2, command=lambda: self.handlerNum(str='3'))
        self.alertButton10.grid(row=4, column=2)
        
        self.alertButton11 = Button(self, text='+', width=5, height=2, command=lambda: self.handlerOpe(str='+'))
        self.alertButton11.grid(row=4, column=3)
        
        self.alertButton12 = Button(self, text='0', width=5, height=2, command=lambda: self.handlerNum(str='0'))
        self.alertButton12.grid(row=5, column=0)
        
        self.alertButton13 = Button(self, text='(', width=5, height=2, command=lambda: self.handler(str='('))
        self.alertButton13.grid(row=5, column=1)

        self.alertButton14 = Button(self, text=')', width=5, height=2, command=lambda: self.handler(str=')'))
        self.alertButton14.grid(row=5, column=2)
        
        self.alertButton15 = Button(self, text='=', width=5, height=2, command=self.getResult)
        self.alertButton15.grid(row=5, column=3)
    # 相应函数

    # 获取文本框的字符串,计算表达式的值，清空文本框，显示结果，并修改flag的值
    def getResult(self):
        x = Cal()
        if self.flag == 0:
            result = self.stringInput.get()
            self.stringInput.delete(0, END)
            message = x.evaluateExpression(result)
            self.flag = 1
            self.stringInput.insert('insert', message)
    
    # EC和C键清空文本框
    def clearInput(self):
        self.stringInput.delete(0, END)
    
    # 回退一位
    def backupInput(self):
        if self.stringInput.get():
            size = len(self.stringInput.get())
            self.stringInput.delete(size-1, END)
    
    # 不同数字和括号按键在文本框输出
    def handlerNum(self, str):
        if self.flag == 1:
            self.stringInput.delete(0, END)
            self.flag = 0
        self.stringInput.insert('insert', str)
    
    # 不同的运算符按键在文本框输出
    def handlerOpe(self, str):
        self.flag = 0
        self.stringInput.insert('insert', str)

    # 是否已经显示出结果
    flag = 0


app = Application()
# 设置窗口标题:
app.master.title('Calculator')
app.master.geometry('400x300')
# 主消息循环:
app.mainloop()