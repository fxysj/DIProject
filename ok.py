def clean_missing_fields_by_form(data: dict) -> None:
    """
    如果 form 中某字段已有有效值，则从 missFields 中删除该字段。
    """
    form = data.get("form", {})
    miss_fields = data.get("missFields", [])

    def is_empty(val):
        return val in [None, "", [], {}, "0", 0]

    # 生成新的 missFields，保留那些在 form 中为空的字段
    data["missFields"] = [
        field for field in miss_fields
        if is_empty(form.get(field["name"]))
    ]


if __name__ == '__main__':
    response = [
        {
            "success": True,
            "promptedAction": [],
            "data": {
                "description": "您好，我已为您准备好交易页面...",
                "state": "SWAP_TASK_NEED_MORE_INFO",
                "form": {
                    "fromTokenAddress": "native",
                    "fromChain": "60",
                    "fromAddress": "",
                    "toTokenAddress": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
                    "toAddress": "0xc8d243291b9fe15894aba49a4ce819d59740ffa1",
                    "toChain": "60",
                    "amount": 10,
                    "slippage": 0.01,
                    "disableEstimate": False,
                    "signedTx": ""
                },
                "missFields": [
                    {
                        "name": "fromChain",
                        "description": "转账的来源链，例如 ETHEREUM 或 BSC 等"
                    },
                    {
                        "name": "toChain",
                        "description": "目标链，例如 ETHEREUM 或 BSC 等"
                    }
                ],
                "intent": "swap"
            },
            "message": "ok",
            "confidence": 99.9,
            "alternatives": []
        }
    ]

    # 对第一个响应的 data 进行处理
    clean_missing_fields_by_form(response[0]["data"])

    from pprint import pprint
    pprint(response[0]["data"]["missFields"])
