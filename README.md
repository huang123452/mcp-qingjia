from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from datetime import datetime

# 初始化 FastAPI 应用
app = FastAPI(title="MCP-青佳 请假小能手", version="1.0")

# --- 定义数据结构 (用于接收前端/AI传来的数据) ---
class LeaveRequest(BaseModel):
    name: str           # 申请人姓名
    leave_type: str     # 请假类型：事假/病假/年假
    days: int           # 请假天数
    reason: str = "无"  # 请假理由（可选）

# --- 核心业务逻辑函数 ---
def process_leave_logic(data: LeaveRequest):
    """
    这里是'请假小能手'的大脑，负责判断请假是否合规
    """
    # 1. 基础校验
    if data.days <= 0:
        return {"status": "拒绝", "message": "请假天数必须大于0"}

    # 2. 根据假期类型和天数进行智能判断
    if data.leave_type == "病假":
        # 病假比较宽松，但超过5天需要证明
        if data.days > 5:
            return {
                "status": "待审核",
                "message": f"{data.name} 申请病假 {data.days} 天，请上传医院诊断证明后由人工审批。"
            }
        else:
            return {"status": "批准", "message": f"系统已自动批准 {data.name} 的 {data.days} 天病假。祝早日康复！"}

    elif data.leave_type == "年假":
        # 年假看余额（这里模拟逻辑），通常不超过15天
        if data.days > 15:
             return {"status": "拒绝", "message": "年假余额不足或单次申请过长，请联系HR。"}
        else:
            return {"status": "批准", "message": f"年假申请通过，扣除 {data.days} 天额度。好好休息！"}

    elif data.leave_type == "事假":
        # 事假最严格
        if data.days > 3:
            return {"status": "待审核", "message": f"事假超过3天，需部门经理人工审批。理由：{data.reason}"}
        else:
            return {"status": "批准", "message": f"短期事假已备案，请注意交接工作。"}

    else:
        return {"status": "错误", "message": f"不支持的请假类型：{data.leave_type}"}

# --- API 接口定义 ---

# 1. 首页/健康检查（百炼平台通常会先访问这个）
@app.get("/")
def root():
    return {
        "service": "MCP-青佳 请假小能手",
        "status": "running",
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

# 2. 处理请假的主接口
@app.post("/apply")
def apply_leave(request: LeaveRequest):
    """
    接收请假申请并返回结果
    """
    result = process_leave_logic(request)

    # 构造最终返回给大模型的数据结构
    response = {
        "applicant": request.name,
        "type": request.leave_type,
        "days": request.days,
        "result_status": result["status"],
        "system_message": result["message"]
    }
    return response

# --- 启动入口 ---
if __name__ == "__main__":
    # 在本地运行时使用，部署到云端时通常由云平台接管
    print("正在启动请假小能手服务...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
