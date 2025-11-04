from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime, timezone
from agents import CrewAgent, StrandAgent

app = FastAPI(title="AgentCore Server", version="1.0.0")


class InvocationRequest(BaseModel):
    input: Dict[str, Any]


class InvocationResponse(BaseModel):
    output: Dict[str, Any]


@app.post("/invocations", response_model=InvocationResponse)
async def invoke_agent(
    request: InvocationRequest,
    x_agent_type: Optional[str] = Header(default="strand", alias="X-Agent-Type")
):
    try:
        user_message = request.input.get("prompt", "")
        if not user_message:
            raise HTTPException(
                status_code=400,
                detail="No prompt found in input. Please provide a 'prompt' key in the input."
            )

        # Switch between agent types based on header
        agent_type = x_agent_type.lower()
        
        if agent_type == "crewai":
            result = CrewAgent(user_message)
            model_name = "crewai-agent"
        elif agent_type == "strand":
            result = StrandAgent(user_message)
            model_name = "strand-agent"
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid agent type: {agent_type}. Supported types: 'crewai', 'strand'"
            )

        response = {
            "message": result.message,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "model": model_name,
        }

        return InvocationResponse(output=response)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent processing failed: {str(e)}")


@app.get("/ping")
async def ping():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)

