from pydantic import BaseModel


class OrderORM:
    def __init__(self, order_id, amount):
        self.order_id = order_id
        self.amount = amount

class OrderDetail(BaseModel):
    order_id: str
    amount: float

    class Config:
        from_attributes = True  # 👈 开启这个才能从对象属性读取



if __name__ == '__main__':
    order_obj = OrderORM("12345", 99.99)
    order_model = OrderDetail.model_validate(order_obj)
    print(order_model)
