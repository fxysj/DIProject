from datetime import datetime

def process_reports(reports):
    if not isinstance(reports, list) or len(reports) == 0:
        return []

    def parse_time(report):
        try:
            return datetime.fromisoformat(report.get("time_east", ""))
        except Exception:
            return datetime.min  # 解析失败放最末尾

    # 排序（时间倒序）
    sorted_reports = sorted(reports, key=parse_time, reverse=True)

    # 提取指定字段
    result = [
        {
            "title": report.get("title", ""),
            "url": report.get("url", ""),
            "time_east": report.get("time_east", "")
        }
        for report in sorted_reports
    ]

    return result

reports = [
    {
        "title": "新闻一",
        "url": "https://example.com/1",
        "site": "新华社",
        "time_east": "2025-05-26T12:30:00"
    },
    {
        "title": "新闻二",
        "url": "https://example.com/2",
        "site": "人民日报",
        "time_east": "2025-05-26T14:00:00"
    }
]

print(process_reports(reports))

