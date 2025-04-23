import contextlib
import inspect
import time


# 上下文管理器类
class ContextManager:
    def __init__(self):
        pass

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            # 获取函数签名
            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()

            # 打印函数签名和参数
            print(f"Function signature: {sig}")
            print(f"Function arguments: {bound_args.arguments}")

            # 上下文管理开始
            with self._context():
                result = func(*args, **kwargs)
            return result

        return wrapper

    @contextlib.contextmanager
    def _context(self):
        print("Entering context")
        try:
            yield
        finally:
            print("Exiting context")


# 示例业务函数
@ContextManager()
def multiply(a, b):
    time.sleep(2)
    return a * b


if __name__ == "__main__":
    result = multiply(4, 6)
    print("Result:", result)
