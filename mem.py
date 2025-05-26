def truncate_link(link):
    """
    截断链接为前8后6字符，中间以'...'连接，链接长度不足15则不处理
    """
    if not isinstance(link, str) or len(link) <= 14:
        return link
    return f"{link[:8]}...{link[-6:]}"


def format_team_links(team_members):
    """
    批量处理团队成员的X链接和LinkedIn链接，进行美化展示
    """
    if not isinstance(team_members, list) or not team_members:
        return []

    for member in team_members:
        if not isinstance(member, dict):
            continue  # 跳过非法格式

        if 'X' in member:
            member['X'] = truncate_link(member['X'])

        if 'linkedin' in member:
            member['linkedin'] = truncate_link(member['linkedin'])

    return team_members


team_members = [
    {
        "name": "Alice",
        "position": "合伙人",
        "X": "https://x.com/alice-investor-profile",
        "linkedin": "https://linkedin.com/in/alice-investor-2025"
    },
    {
        "name": "Bob",
        "position": "分析师",
        "X": "https://x.com/bob",
        "linkedin": ""
    },
    {
        "name": "Charlie",
        "position": "投资经理",
        "linkedin": "https://linkedin.com/in/charlie-the-investor"
        # 没有 X 字段
    },
    {
        "name": "Empty",
        "position": "助理"
        # 没有 X / linkedin 字段
    }
]
formatted_team = format_team_links(team_members)
print(formatted_team)
