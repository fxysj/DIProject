from decimal import Decimal, ROUND_HALF_UP


def format_price(price: float) -> str:
    """
    格式化价格显示，根据有效数字起始位置决定保留的小数位数。
    """
    price_decimal = Decimal(str(price))

    # 如果价格为0，直接返回"0"
    if price_decimal == 0:
        return "0"

    # 获取有效数字起始的位置
    str_price = f"{price:.18f}".lstrip('0')
    if '.' in str_price:
        decimals = str_price.split('.')[1]
    else:
        decimals = ''

    # 找到第一个非零数字所在的小数位
    for idx, ch in enumerate(decimals):
        if ch != '0':
            break
    else:
        idx = len(decimals)  # 全是0

    # 计算应保留的小数位数（从有效位开始 + 2）
    precision = min(idx + 2, 6)

    # 使用 Decimal 进行四舍五入
    quantize_str = '0.' + '0' * (precision - 1) + '1'
    rounded = price_decimal.quantize(Decimal(quantize_str), rounding=ROUND_HALF_UP)

    return str(rounded)


# ✅ 测试案例
test_prices = [
    1.23344,  # -> 1.23
    0.23673,  # -> 0.237
    0.0324842,  # -> 0.0325
    0.002324484,  # -> 0.00232
    0.0003244884,  # -> 0.000324
    0.0000827442,  # -> 0.0000827
    0.000006272482,  # -> 0.00000627
    0.00000424349,  # -> 0.00000424
    0.0  # -> 0
]

for p in test_prices:
    print(f"原价: {p} -> 展示价: {format_price(p)}")
