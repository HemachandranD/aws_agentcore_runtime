import boto3
import json

agent_core_client = boto3.client('bedrock-agentcore', region_name='us-east-1')

# Payload matching the /invocations endpoint format
payload = json.dumps({
    "input": {
        "prompt": "what is AI?",
        "x_agent_framework": "crewai"
    }
})

response = agent_core_client.invoke_agent_runtime(
    agentRuntimeArn='arn:aws:bedrock-agentcore:us-east-1:792560738609:runtime/Assistant-4c7zx08wQi',
    runtimeSessionId='dfmeoagmreaklgmrkleafremoigrytesogmtrskhmtkrlshmk',  # Must be 33+ chars
    payload=payload,
    qualifier="DEFAULT",
)

response_body = response['response'].read()
response_data = json.loads(response_body)

print("="*80)
print("Agent Response:")
print("="*80)
print(json.dumps(response_data, indent=2))
print("="*80)

