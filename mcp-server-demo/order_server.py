from datetime import datetime
import json
import uuid

import httpx
from PIL.Image import Image
from mcp.server.fastmcp import FastMCP,Context
from mcp.types import TextContent
from pydantic import BaseModel, Field
from typing import Optional
from mcp.server.fastmcp.prompts import base
from PIL import Image as PILImage
mcp = FastMCP("订单服务")


@mcp.resource("config://app")
def get_config() -> str:
    """Static configuration data"""
    return "App configuration here"


class SqlConfig(BaseModel):
    HOST:str=Field(...,description="host")


@mcp.resource("config://sql",mime_type="application/json")
def getSqlConfig()->SqlConfig:
    return  SqlConfig(HOST="127.0.0.1")
    


@mcp.resource("users://{user_id}/profile")
def get_user_profile(user_id: str) -> str:
    """Dynamic user data"""
    data = {}
    data["user_id": user_id]
    return json.dumps(data)



class OrderDetail(BaseModel):
    order_id: str = Field(..., description="订单唯一标识")
    user_id: str = Field(..., description="用户ID")
    product_name: str = Field(..., description="产品名称")
    quantity: int = Field(..., description="购买数量")
    price: float = Field(..., description="单价")
    total_amount: float = Field(..., description="总金额（价格 x 数量）")
    order_status: str = Field(..., description="订单状态，例如：待付款、已付款、已发货、已完成")
    created_at: datetime = Field(..., description="下单时间")
    updated_at: Optional[datetime] = Field(None, description="最后更新时间")

    class Config:
        from_attributes = True

#订单信息
class Order(BaseModel):
     OrderId:str=Field(default=uuid.uuid4(),description="订单Id")
     OrderUserId:str=Field(description="订单的用户Id",default="10010")
     Version:str=Field(default="1.0",description="版本号")
     OrderDetailInfo:Optional[OrderDetail]=Field(None,description="订单详情信息")
     class Config:
         from_attributes = True  # 👈 开启这个才能从对象属性读取


#获取用户订单信息
@mcp.resource("orders://{user_id}/profile")
def get_orders_info(user_id: str) -> Order:
    """Dynamic user data"""
    orderDetail = OrderDetail(
        order_id="ORD123456",
        user_id="USR789",
        product_name="Bitcoin T-Shirt",
        quantity=2,
        price=29.99,
        total_amount=59.98,
        order_status="已付款",
        created_at=datetime.now()
    )
    order = Order(OrderId=uuid.uuid4().__str__(),OrderUserId=user_id,Version="v1.0.2",OrderDetailInfo=orderDetail)
    return order

@mcp.resource("orders://{order_id}/detail")
def get_order_detailInfo(order_id:str)->OrderDetail:
    order = OrderDetail(
        order_id="ORD123456",
        user_id="USR789",
        product_name="Bitcoin T-Shirt",
        quantity=2,
        price=29.99,
        total_amount=59.98,
        order_status="已付款",
        created_at=datetime.now()
    )
    return  order

@mcp.tool()
def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """Calculate BMI given weight in kg and height in meters"""
    return weight_kg / (height_m**2)


@mcp.tool()
async def fetch_weather(city: str) -> str:
    """Fetch current weather for a city"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.weather.com/{city}")
        return response.text

@mcp.prompt()
def review_code(code: str) -> str:
    return f"Please review this code:\n\n{code}"

@mcp.prompt()
def debug_error(error: str) -> list[base.Message]:
    return [
        base.UserMessage("I'm seeing this error:"),
        base.UserMessage(error),
        base.AssistantMessage("I'll help debug that. What have you tried so far?"),
    ]

@mcp.tool()
def create_thumbnail(image_path: str) -> Image:
    """Create a thumbnail from an image"""
    img = PILImage.open(image_path)
    img.thumbnail((100, 100))
    return Image(data=img.tobytes(), format="png")


@mcp.tool()
async def long_task(files: list[str], ctx: Context) -> str:
    for i, file in enumerate(files):
        ctx.info(f"Processing {file}")
        await ctx.report_progress(i + 1, len(files))
        data, mime_type = await ctx.read_resource(f"file://{file}")

        # Saving file to a local directory
        try:
            with open(f"/tmp/output_{i}.bin", "wb") as f:
                f.write(data)
            ctx.info(f"File {file} saved successfully.")
        except Exception as e:
            ctx.error(f"Failed to save {file}: {str(e)}")
            return f"Error processing {file}: {str(e)}"

    return "处理完成 ✅"

if __name__ == "__main__":
    print("服务器启动！！！")
    mcp.run()