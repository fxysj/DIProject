import re
def build_sensitive_pattern(sensitive_words: str) -> re.Pattern:
    words = re.findall(r'\S+', sensitive_words)
    pattern = r'|'.join(map(re.escape, set(words)))
    return re.compile(pattern, re.IGNORECASE)

def contains_sensitive(text: str, pattern: re.Pattern) -> bool:
    return bool(pattern.search(text))

# 初始化
pattern = build_sensitive_pattern(SENSITIVE_WORDS)

# 示例文本
text = "这个人涉嫌暴力犯罪，持刀伤人"

# 检查是否包含敏感词
if contains_sensitive(text, pattern):
    print("检测到敏感内容！")
else:
    print("内容安全。")