def transform_investors(investors):
    type_mapping = {
        1: "Project",
        2: "VC",
        3: "People"
    }
    for investor in investors:
        if investor.get("type") in type_mapping:
            investor["type"] = type_mapping[investor["type"]]
    return investors


investors = [
    {"type": 1, "invest_id": 101, "name": "A投资", "logo": "logo1.png", "lead_investor": 1},
    {"type": 2, "invest_id": 102, "name": "B投资", "logo": "logo2.png", "lead_investor": 0},
    {"type": 3, "invest_id": 103, "name": "C投资", "logo": "logo3.png", "lead_investor": 1},
    {"type": 4, "invest_id": 104, "name": "D投资", "logo": "logo4.png", "lead_investor": 0}
]

transformed = transform_investors(investors)
print(transformed)
