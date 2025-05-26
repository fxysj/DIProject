from datetime import datetime

def sort_events(events):
    if not isinstance(events, list) or len(events) == 0:
        return []

    def parse_time(item):
        try:
            return datetime.fromisoformat(item.get("hap_date", ""))
        except Exception:
            return datetime.min  # 无法解析的时间排到最后

    # 按时间降序排序
    sorted_events = sorted(events, key=parse_time, reverse=True)

    # 保留指定字段
    result = [
        {
            "hap_date": item.get("hap_date", ""),
            "event": item.get("event", "")
        }
        for item in sorted_events
    ]

    return result
events = [
    {"hap_date": "2025-05-26T09:00:00", "event": "发布新产品"},
    {"hap_date": "2025-05-27T14:30:00", "event": "达成合作协议"},
    {"hap_date": "2025-05-25T18:00:00", "event": "季度财报公布"}
]

print(sort_events(events))
