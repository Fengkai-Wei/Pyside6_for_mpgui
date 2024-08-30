def dummy_func(*args, **kwargs):
    size = kwargs.get('size', None)
    center = kwargs.get('center', None)
    return f"Size: {size}, Center: {center}, some arg {args}"

# 定义一个字典，包含所需的参数
params = {
    'size': 10,
    'center': [5, 5, 5],
    'color': 'BLue',
}

# 调用函数并传入字典
result = dummy_func(**params)
print(result)  # 输出: "Size: 10, Center: [5, 5, 5]"
