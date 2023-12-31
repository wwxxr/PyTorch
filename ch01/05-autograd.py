import torch

print('1.自动梯度计算')
x = torch.arange(4.0, requires_grad=True)  # 1.将梯度附加到想要对其计算偏导数的变量
print('x:', x)
print('x.grad:', x.grad)
y = 2 * torch.dot(x, x)  # 2.记录目标值的计算
print('y:', y)
y.backward()  # 3.执行它的反向传播函数  通过调用反向传播函数来自动计算y关于x每个分量的梯度
print('x.grad:', x.grad)  # 4.访问得到的梯度
print('x.grad == 4*x:', x.grad == 4 * x)

## 计算另一个函数
x.grad.zero_()    # 在默认情况下，pytorch会累积梯度，我们需要清除之前的值
y = x.sum()
print('y:', y)
y.backward()
print('x.grad:', x.grad)

# 非标量变量的反向传播
x.grad.zero_()
print('x:', x)
y = x * x
y.sum().backward()
print('x.grad:', x.grad)

# 将某些计算移动到记录的计算图之外
x.grad.zero_()
y = x * x
u = y.detach()    # 把y当作一个常数，而不是关于x的函数，所有u对系统来讲，就是一个常数，此时y是x的函数，而u不是
z = u * x
z.sum().backward()
x.grad == u

x.grad.zero()
y.sum().backward()
x.grad == 2 * x

# 即使构建函数的计算图需要通过python控制流（例如，条件、循环或任意函数调用），我们仍然可以计算得到的变量的梯度
def f(a):
    b = a * 2
    print(b.norm())
    while b.norm() < 1000:  # 求L2范数：元素平方和的平方根
        b = b * 2
    if b.sum() > 0:
        c = b
    else:
        c = 100 * b
    return c

a = torch.randn(size=(),requires_grad=True)
d = f(a)
d.backward()
a.grad == d / a

print('2.Python控制流的梯度计算')
a = torch.tensor(2.0)  # 初始化变量
a.requires_grad_(True)  # 1.将梯度赋给想要对其求偏导数的变量
print('a:', a)
d = f(a)  # 2.记录目标函数
print('d:', d)
d.backward()  # 3.执行目标函数的反向传播函数
print('a.grad:', a.grad)  # 4.获取梯度
