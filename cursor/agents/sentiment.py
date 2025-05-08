def analyze_sentiment(text):
    # 伪代码：简单情感分析
    if any(word in text for word in ["好", "喜欢", "满意"]):
        return "正面"
    elif any(word in text for word in ["差", "不满", "失望"]):
        return "负面"
    else:
        return "中性" 