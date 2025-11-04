import boto3
import json

agent_core_client = boto3.client('bedrock-agentcore', region_name='us-east-1')

# Payload matching the /invocations endpoint format
payload = json.dumps({
    "input": {
        "prompt": "what is AI?"
    }
})

# Additional context for agent type (maps to X-Agent-Type header in the container)
# Options: "crewai" or "strand"
agent_type = "crewai"

response = agent_core_client.invoke_agent_runtime(
    agentRuntimeArn='arn:aws:bedrock-agentcore:us-east-1:792560738609:runtime/strands_agent_pilot-v0R8bzFtCC',
    runtimeSessionId='dfmeoagmreaklgmruleafremoigrmtesogytrskhmtkrlshmt',  # Must be 33+ chars
    payload=payload,
    qualifier="DEFAULT",
    # Pass agent type as additional context
    additionalContext={
        'agentType': agent_type
    }
)

response_body = response['response'].read()
response_data = json.loads(response_body)

print("="*80)
print("Agent Response:")
print("="*80)
print(json.dumps(response_data, indent=2))
print("="*80)

