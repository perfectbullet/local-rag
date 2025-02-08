import torch

# 创建一个需要计算梯度的张量
x = torch.tensor([2.0], requires_grad=True)

# 检查x的requires_grad属性
# print("x.requires_grad:", x.requires_grad)  # 输出: x.requires_grad: True

# 对x进行一个操作
y = x * x
y.backward()
print('y', y)
print('x.grad', x.grad)
# x.detach_()
# y.detach_()
#
z = x * 3
z.backward()
print('z', z)
print('x.grad', x.grad)
#
# # 检查y的requires_grad属性
# print("y.requires_grad:", y.requires_grad)  # 输出: y.requires_grad: True
#
# # 使用detach()从计算图中分离y
# y_detached = y.detach()
#
# # 检查y_detached的requires_grad属性
# print("y_detached.requires_grad:", y_detached.requires_grad)  # 输出: y_detached.requires_grad: False
#
# # 但是，检查原始张量y的requires_grad属性，它并没有改变
# print("y.requires_grad:", y.requires_grad)  # 输出: y.requires_grad: True
#
# # 这也说明了detach()返回了一个新的张量，而不是修改了原始张量
# print("y is y_detached:", y is y_detached)  # 输出: y is y_detached: False
