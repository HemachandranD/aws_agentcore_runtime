import boto3
import json

agent_core_client = boto3.client('bedrock-agentcore', region_name='us-east-1')
payload = json.dumps({
    "input": {"prompt": "What is the weather in Tokyo?"}
})

response = agent_core_client.invoke_agent_runtime(
    agentRuntimeArn='arn:aws:bedrock-agentcore:us-east-1:792560738609:runtime/strands_agent_pilot-mqzi7bD7T8',
    runtimeSessionId='dfmeoagmreaklgmrkleafremoigrmtesogytrskhmtkrlshmt',  # Must be 33+ chars
    payload=payload,
    qualifier="DEFAULT"
)

response_body = response['response'].read()
response_data = json.loads(response_body)
print("Agent Response:", response_data)