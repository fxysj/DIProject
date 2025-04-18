下面是基于 **Lark（飞书）富文本格式** 的【本周工作总结】+【下周工作计划】，已经适配为飞书文档/飞书群聊支持的 **Markdown 风格语法**，可以直接粘贴使用，无需额外调整：

---

## 🗓️ 本周工作总结（2024-04-14 至 2024-04-18）

---

### ✅ 4月14日（周一）

- 完成大模型异常捕获机制，增强 FastAPI 服务稳定性与健壮性  
- 新增 6 个异常拦截器，覆盖大模型 LLM 调用中常见的异常场景  
- **代码产出：** [feature/deep_search_0520 分支](https://github.com/fxysj/ai-wallet/tree/feature/deep_search_0520)  
- **需求来源：** 产品团队、项目组  

---

### ✅ 4月15日（周二）

- 完成深度搜索功能整合，支持关键词解析 → 类型映射 → 数据路由  
- 支持多个数据源的大模型调用整合，包括补全、分片、优化提示词  
- 实现 API 整合、交互逻辑串联、测试用例设计等完整流程  
- AI钱包算法工程师招聘  
- **对接 API：**  
  - [GO-Plus](https://docs.gopluslabs.io/reference/tokensecurityusingget_1)  
  - [RowData](https://www.rootdata.com/zh/Api/Doc)  
  - [CoinMarketCap](https://coinmarketcap.com/api/documentation/v1/#operation/getV2CryptocurrencyQuotesLatest)  
- **需求文档：** [Axure 原型](https://87wigh.axshare.com/?g=4)  

---

### ✅ 4月16日（周三）

- 初步完成其他类型数据源 API 工具调用逻辑封装  
- 预留未来 API 扩展接口和异步结构：
  ```
  def api_extra_asnyc(attached_data, type_value):
      pass 
  ```
- 完成 GOPLUS 和 Symbol 数据合并  
- 完成 OverDetail.data 数据合并  
- 深度搜索功能开发完成  
- 编写深度搜索测试代码  
- 添加字段校验与字段返回说明信息  
- `typeList` 返回过滤非 1、2、4、3 的信息  
- 添加 SystemMessage、HumanMessage、AIMessage 返回案例  
- 使用 XML 进行深度搜索测试  
- 增强 `send_request_post` 和 `send_request_get`  
- 更新 `requirements` 文件  

---

### ✅ 4月17日（周四）

- 编写深度搜索提示词测试脚本：
  - `deepSearchTask_prompt_test.py`  
  - `llm.py`
  ```
  def test_case_2_modify_input():
      run_deep_search_test("深度搜索")
  ```

---

### ✅ 4月18日（周五）

- 分支合并至 main，进行深度搜索功能测试  
- 修复跨链转账智能体功能 Bug  
- 拆分测试各函数逻辑单元  
- **UnClearTemplate 模板：**  
  - 新增两个用于处理“不清晰输入”和“敏感词”的案例  
  - 保证输出符合 JSON 格式  
- 生成标题规则：  
  - `Analysis report of the + token name`  
  - `Background information of the + Project name`  
- 暂不纳入“钱包地址分析 Agent”  
- 上线测试地址：  
  [深度分析模型 Agent 原型](https://97d3iw.axshare.com/?g=14&id=drayln&p=%E6%B7%B1%E5%BA%A6%E5%88%86%E6%9E%90%E6%A8%A1%E5%9E%8Bagent___&sc=3)

---

### 🧩 总结

本周聚焦于 **深度搜索能力闭环开发**，完成了从异常处理 → 多源数据聚合 → 提示词适配 → 功能测试 的全链路联调与上线。实现了复杂数据源下的稳定调用，并为下阶段 **Memetoken 报告生成与展示逻辑** 打下良好基础。

---

## 📌 下周工作计划（2024-04-21 至 2024-04-26）

---

### 🎯 Memetoken 报告字段渲染开发

- 精度控制：价格、FDV、MCap 等字段单位（K/M/B）自动格式化  
- 空值字段统一展示为 “- -”，地址字段缩略与一键复制  
- Contract Security 与 Honeypot 风险提示展示逻辑完善  
- 渲染图片字段与图表组件联调  
- 渲染字段自动化测试覆盖  

---

### 🎯 主流币与项目字段联调

- Brief、Ecosystem、Social Media、Team 等字段联调展示逻辑  
- 折叠逻辑 + 外链跳转 + 多行限制展示处理  
- Description、Events、Reports 字段动态处理逻辑测试  

---

### 🎯 深度搜索智能体细节优化

- 模型提示词策略微调  
- 模糊问答、空值处理、格式不规范问题的容错能力增强  
- JSON 返回格式的健壮性与兼容性优化  

---

### 🎯 接口联调 & UI 联测

- 前后端字段联调测试  
- 自动化测试脚本补充：空值、异常、精度、链路错误断点  
- 协同产品验证最终交互体验与细节展示  

---

如需我帮你生成飞书文档链接、结构图或同步成日报模板，也可以说一声，我可以继续帮你格式化 😊