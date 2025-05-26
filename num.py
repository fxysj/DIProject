def format_number(num):
    if not isinstance(num, (int, float)):
        return str(num)  # 非数字直接返回原始值或抛出异常

    abs_num = abs(num)  # 保证负数也能正确处理前缀

    if abs_num < 1_000:
        return f"{num:.2f}"
    elif abs_num < 1_000_000:
        return f"{num / 1_000:.2f}K"
    elif abs_num < 1_000_000_000:
        return f"{num / 1_000_000:.2f}M"
    else:
        return f"{num / 1_000_000_000:.2f}B"
print(format_number(999))         # 999.00
print(format_number(1000))        # 1.00K
print(format_number(25300))       # 25.30K
print(format_number(1200000))     # 1.20M
print(format_number(987654321000))  # 9.88B
print(format_number(-4500))       # -4.50K
print(format_number("abc"))       # abc
