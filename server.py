from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

# --- 1. 初始化应用 ---
app = FastAPI(title="MCP-青佳 请假小能手", version="1.0")

# --- 2. 定义数据结构 ---
class LeaveRequest(BaseModel):
    name: str       # 姓名
    leave_type: str # 类型：病假、事假等
    days: int       # 天数
    reason: str = "无" # 理由，默认为无

# --- 3. 业务逻辑函数 ---
def process_leave_logic(data: LeaveRequest):
    """这里是请假小助手的脑子"""
    if data.days <= 0:
        return {"status": "拒绝", "message": "请假天数必须大于0"}

    # 简单的判断逻辑
    if data.leave_type == "病假":
        if data.days > 5:
            return {"status": "待审核", "message": "病假超过5天，需上传医院证明"}
        else:
            return {"status": "批准", "message": "短期病假，系统自动通过"}
    elif data.leave_type == "事假":
        if data.days > 3:
             return {"status": "待审核", "message": "事假超过3天，需主管审批"}
        else:
            return {"status": "批准", "message": "短期事假，系统自动通过"}
    else:
        return {"status": "拒绝", "message": "不支持的请假类型"}

# --- 4. API 接口 ---
@app.get("/")
def health_check():
    return {"service": "MCP-青佳", "status": "running"}

@app.post("/apply")
def apply_leave(request: LeaveRequest):
    result = process_leave_logic(request)
    return {
        "applicant": request.name,
        "result_status": result["status"],
        "system_message": result["message"]
    }

# --- 5. 启动入口 ---
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
