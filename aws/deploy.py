import boto3

client = boto3.client('bedrock-agentcore-control')

response = client.create_agent_runtime(
    agentRuntimeName='flash_agent_runtime',
    agentRuntimeArtifact={
        'containerConfiguration': {
            'containerUri': '792560738609.dkr.ecr.us-east-1.amazonaws.com/hemz_agents_repo:latest'
        }
    },
    networkConfiguration={"networkMode": "PUBLIC"},
    roleArn='arn:aws:iam::792560738609:role/BedrockAgentRuntimeRole'
)

print(f"Agent Runtime created successfully!")
print(f"Agent Runtime ARN: {response['agentRuntimeArn']}")
print(f"Status: {response['status']}")

