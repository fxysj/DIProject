def count_risks_filtered(security_list, *, risk_level="Risk"):
    """
    过滤掉非 dict 的无效项，并统计指定 riskLevel 中 risked 为 True 的项数量。
    同时根据条件添加 color_type 字段：
        - riskLevel == "Risk" 且 risked=True -> color_type = 1（红色）
        - riskLevel == "Attention" 且 risked=True -> color_type = 2（黄色）
        - 其他情况 -> color_type = 3（默认）

    :param security_list: 合约安全项列表
    :param risk_level: 指定要统计的风险等级，默认为 "Risk"
    :return: (filtered_list, risk_count)
    """
    filtered_list = []
    risk_count = 0

    for item in security_list:
        if isinstance(item, dict):
            # 判断 color_type
            if item.get("risked") is True and item.get("riskLevel") == "Risk":
                item["color_type"] = 1  # 红色
            elif item.get("risked") is True and item.get("riskLevel") == "Attention":
                item["color_type"] = 2  # 黄色
            else:
                item["color_type"] = 3  # 默认

            filtered_list.append(item)

            # 统计指定 risk_level 中 risked 为 True 的数量
            if item.get("risked") is True and item.get("riskLevel") == risk_level:
                risk_count += 1

    return filtered_list, risk_count
data = [
    {"risked": True, "riskLevel": "Risk"},
    {"risked": True, "riskLevel": "Attention"},
    {"risked": False, "riskLevel": "Risk"},
    {"risked": True, "riskLevel": "Info"},
    "invalid_entry",
]

filtered, count = count_risks_filtered(data)
print(filtered)
print("Risk count:", count)
