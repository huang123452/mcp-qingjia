from mcp.server.fastmcp import FastMCP

# 初始化 MCP 服务实例
mcp = FastMCP("请假小能手")

@mcp.tool()
def process_leave_logic(name: str, leave_type: str, days: int, reason: str = "无") -> dict:
    """
    处理学生的请假申请逻辑。
    :param name: 申请人姓名
    :param leave_type: 请假类型 (事假/病假/年假)
    :param days: 请假天数
    :param reason: 请假理由 (可选)
    """
    # --- 这里保留你原来的业务逻辑 ---

    # 1. 基础校验
    if days <= 0:
        return {"status": "拒绝", "message": "请假天数必须大于0"}

    # 2. 智能判断逻辑
    if leave_type == "病假":
        if days > 3:
            return {
                "status": "待审核",
                "message": f"{name} 申请病假 {days} 天，超过3天需要医生证明"
            }
    elif leave_type == "事假":
        if days > 5:
             return {
                "status": "拒绝",
                "message": f"{name} 申请事假 {days} 天，超过5天系统自动拒绝"
            }

    # 3. 默认通过
    return {
        "status": "批准",
        "message": f"{name} 的 {leave_type} 申请已通过，共 {days} 天。"
    }

# 启动入口
if __name__ == "__main__":
    # 使用 SSE 传输协议，这是百炼目前推荐的方式
    mcp.run(transport="sse")
