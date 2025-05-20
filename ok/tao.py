import matplotlib.pyplot as plt

eth_reserve = 90
usdt_reserve = 198_000
k = eth_reserve * usdt_reserve

external_price = 2000
fee_rate = 0.003

eth_prices = []
profits = []
profit_cumsum = []
lp_fees = []
lp_fees_cumsum = []

eth_in_total = 0
profit_total = 0
lp_fee_total = 0

def get_price_from_pool(x, y):
    return y / x

def sell_eth_to_pool(eth_in):
    global eth_reserve, usdt_reserve, k

    eth_in_after_fee = eth_in * (1 - fee_rate)
    new_eth_reserve = eth_reserve + eth_in_after_fee
    new_usdt_reserve = k / new_eth_reserve
    usdt_out = usdt_reserve - new_usdt_reserve

    # 更新池状态
    eth_reserve = new_eth_reserve
    usdt_reserve = new_usdt_reserve
    k = eth_reserve * usdt_reserve

    return usdt_out

threshold = 0.5

while True:
    dex_price = get_price_from_pool(eth_reserve, usdt_reserve)
    if dex_price - external_price < threshold:
        break

    eth_in = 1
    usdt_out = sell_eth_to_pool(eth_in)
    usdt_expected = eth_in * external_price
    profit = usdt_out - usdt_expected

    profit_total += profit
    eth_in_total += eth_in

    # LP 手续费 = 0.3% * eth_in * 当时 ETH 价格（用外部价估算）
    lp_fee = eth_in * fee_rate * external_price
    lp_fee_total += lp_fee

    eth_prices.append(dex_price)
    profits.append(profit)
    profit_cumsum.append(profit_total)
    lp_fees.append(lp_fee)
    lp_fees_cumsum.append(lp_fee_total)

print(f"总套利次数: {len(profits)}")
print(f"总投入 ETH: {eth_in_total}")
print(f"累计套利利润（USDT）: {profit_total:.2f}")
print(f"累计 LP 手续费收益（USDT）: {lp_fee_total:.2f}")
print(f"最终池中 ETH 价格: {get_price_from_pool(eth_reserve, usdt_reserve):.2f}")

# 绘图
fig, ax = plt.subplots(3, 1, figsize=(10, 10), sharex=True)

ax[0].plot(range(len(eth_prices)), eth_prices, label="DEX Price", color="blue")
ax[0].axhline(y=external_price, color="gray", linestyle="--", label="External Price")
ax[0].set_ylabel("ETH Price (USDT)")
ax[0].set_title("📉 DEX Price Converging to External Market Price")
ax[0].legend()
ax[0].grid(True)

ax[1].plot(range(len(profit_cumsum)), profit_cumsum, label="Arbitrage Profit (USDT)", color="green")
ax[1].set_ylabel("Profit (USDT)")
ax[1].set_title("💰 Arbitrage Profit Accumulation")
ax[1].legend()
ax[1].grid(True)

ax[2].plot(range(len(lp_fees_cumsum)), lp_fees_cumsum, label="LP Fee Income (USDT)", color="orange")
ax[2].set_xlabel("Arbitrage Round")
ax[2].set_ylabel("LP Fees (USDT)")
ax[2].set_title("🏦 LP Fee Income Accumulation")
ax[2].legend()
ax[2].grid(True)

plt.tight_layout()
plt.show()
