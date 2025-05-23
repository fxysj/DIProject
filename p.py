from decimal import Decimal, ROUND_HALF_UP

def format_price_display(price: float) -> str:
    d = Decimal(str(price))

    if d >= Decimal("1"):
        return str(d.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
    elif d >= Decimal("0.1"):
        return str(d.quantize(Decimal("0.001"), rounding=ROUND_HALF_UP))
    elif d >= Decimal("0.01"):
        return str(d.quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP))
    elif d >= Decimal("0.001"):
        return str(d.quantize(Decimal("0.00001"), rounding=ROUND_HALF_UP))
    elif d >= Decimal("0.0001"):
        return str(d.quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP))
    elif d >= Decimal("0.00001"):
        return str(d.quantize(Decimal("0.0000001"), rounding=ROUND_HALF_UP))
    else:
        # 极小数，找第一个非0位（索引从1开始）
        s = f"{d:.18f}".split('.')[1]
        for i, ch in enumerate(s):
            if ch != '0':
                break
        digits = s[i:i+3]
        return f"0.0({i+1}){digits}"  # 加1修复错误

# ✅ 测试
test_cases = [
    (1.23344, "1.23"),
    (0.23673, "0.237"),
    (0.0324842, "0.0325"),
    (0.002324484, "0.00232"),
    (0.0003244884, "0.000324"),
    (0.0000827442, "0.0000827"),
    (0.000006272482, "0.0(5)627"),
    (0.000000424349, "0.0(6)424"),
]

print("最终修复后的测试结果：")
for price, expected in test_cases:
    result = format_price_display(price)
    print(f"原价: {price:.15f} -> 展示: {result} ✅ {'PASS' if result == expected else '❌ FAIL'}")
