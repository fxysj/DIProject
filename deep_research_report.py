P="""
### 1. 报告整体摘要生成

```
请基于以下数据，帮我生成一份关于加密货币【{{tokenSymbol}}】的分析报告摘要。
包括项目背景、代币价格、流通量、市值、持币地址数、以及合约安全相关风险评估。
数据详情：
- 代币名称: {{selectedType.title}}
- 代币简介: {{selectedType.detail}}
- 当前价格: {{overview.tokenPrice}}
- 市值: {{overview['m.cap']}}
- 流通量: {{overview.circulation}}
- 持币地址数量: {{overview.tokerHolders}}
- 前十大持有者占比: {{overview.top10HoldersRatio}}%
- 合约地址: {{overview.contractAddress[0]}}
请特别指出合约是否已验证、是否存在铸币函数、代理合约风险、是否存在黑名单和白名单功能等安全要素。
```

---

### 2. 合约安全风险检查提示词

```
请帮我分析这份合约的安全风险，重点关注以下指标：
- 合约源码是否已验证？({{details.contractSourceCodeVerified.value}})
- 是否有代理合约？({{details.noProxy.value}})
- 是否有铸币(mint)函数？({{details.noMintFunction.value}})
- 是否存在隐藏所有权？({{details.noHiddenOwner.value}})
- 是否能自毁？({{details.thisTokenCanNotSelfDestruct.value}})
- 是否有黑名单功能？({{details.noBlacklist.value}})
- 是否有白名单功能？({{details.noWhitelist.value}})
- 是否有交易冷却时间或交易暂停功能？({{details.noTradingCooldownFunction.value}}, {{details.noCodesFoundToSuspendTrading.value}})
结合以上信息，请给出这份合约的安全评级及潜在风险说明。
```

---

### 3. 代币经济模型与持币分布分析

```
请分析代币【{{tokenSymbol}}】的经济模型和持币分布情况。
- 最大供应量：{{overview.maxSupply}}
- 总供应量：{{overview.tokenSupply}}
- 流通量：{{overview.circulation}}
- 前十大持有者占比：{{overview.top10HoldersRatio}}%
- 持币地址数量：{{overview.tokerHolders}}
请判断是否存在中心化风险，例如大户持币比例过高，以及代币是否有自动分红或销毁机制，影响代币稀缺性。
```

---

### 4. 交易和税费机制提示词

```
请描述代币【{{tokenSymbol}}】的交易相关机制，尤其关注买卖税费和防护机制。
- 买入税率：{{details.buyTax}}
- 卖出税率：{{details.sellTax}}
- 是否存在反鲸鱼交易限制？({{details.noAntiWhaleUnlimitedNumberOfTransactions.value}})
- 反鲸鱼限制是否可修改？({{details.antiWhaleCannotBeModified.value}})
- 是否存在交易黑名单或白名单？({{details.noBlacklist.value}}, {{details.noWhitelist.value}})
请结合上述指标，分析代币的交易安全性和潜在风险。
```

---

### 5. 去中心化交易对和流动性分析

```
请根据以下去中心化交易平台（DEX）流动性信息，分析【{{tokenSymbol}}】的流动性分布和风险。
列出主要流动性池名称、类型和流动性数值。
例如：
{{#each details.dexAndLiquidity}}- 平台名称：{{this.name}}, 类型：{{this.liquidity_type}}, 流动性：{{this.liquidity}}  {{/each}}
结合流动性池的分布情况，评估该代币在不同DEX的交易活跃度和风险集中度。
```

---

### 6. 动态行动建议提示词

```
基于当前代币【{{tokenSymbol}}】的价格、合约安全、流动性和交易机制，请给出以下建议：
- 是否适合持有或买入？
- 是否存在潜在的智能合约风险需要警惕？
- 是否建议关注代币持仓集中度带来的市场波动风险？
- 对普通投资者的风险提示。
请结合实际数据给出详尽的建议说明。
```
[目标]

---
"""