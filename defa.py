def apply_default_form_values(data: dict, isSwpRes: str) -> None:
    """
    如果用户没有主动修改过 form 字段，则根据 isSwpRes 设置默认值。
    - Swap: Ethereum → Ethereum 上的 USDT
    - Bridge: Ethereum → BSC 上的 USDT
    """

    # 定义默认值
    default_forms = {
        "Swap": {
            "fromChain": "60",
            "fromTokenAddress": "native",
            "toTokenAddress": "0xdAC17F958D2ee523a2206206994597C13D831ec7",  # USDT on Ethereum
            "toChain": "60"
        },
        "Bridge": {
            "fromChain": "60",
            "fromTokenAddress": "native",
            "toTokenAddress": "0x55d398326f99059ff775485246999027b3197955",  # USDT on BSC
            "toChain": "56"
        }
    }

    form = data.setdefault("form", {})
    defaults = default_forms.get(isSwpRes)

    if not defaults:
        return  # 无效的 isSwpRes，不处理

    def is_unmodified_or_empty(value, default):
        """判断字段是否为空/未设置/未主动修改"""
        return value in [None, "", 0, "0"] or str(value) == str(default)

    is_default = all(
        is_unmodified_or_empty(form.get(k), v)
        for k, v in defaults.items()
    )

    if is_default:
        form.update(defaults)


if __name__ == '__main__':
    data = {
        "form": {
            "fromChain": 0,
            "fromTokenAddress": "",
            "toTokenAddress": "",
            "toChain": 0
        }
    }

    isSwpRes = "Bridge"
    apply_default_form_values(data, isSwpRes)

    print(data["form"])


{
    "id": "HxFZ2BIL2hwW2E6z111342",
    "messages": [
        {
            "role": "user",
            "content": "将DOT换成DOGE跨链",
            "data": {
                 "intent": "swap"
            }
        }
    ],
    "session_id": "0x22223xx23232xwe"
}