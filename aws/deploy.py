import boto3
import json
from botocore.exceptions import ClientError

# Configuration
RUNTIME_NAME = 'Assistant'
ACCOUNT_ID = '792560738609'
REGION = 'us-east-1'
CONTAINER_URI = f'{ACCOUNT_ID}.dkr.ecr.{REGION}.amazonaws.com/hemz_agents_repo:latest'
ROLE_ARN = f'arn:aws:iam::{ACCOUNT_ID}:role/BedrockAgentRuntimeRole'

client = boto3.client('bedrock-agentcore-control', region_name=REGION)


def get_existing_runtime(runtime_name):
    """Check if a runtime with the given name already exists"""
    try:
        # List all runtimes and find matching name
        response = client.list_agent_runtimes()
        print (response)
        for runtime in response.get('agentRuntimes', []):
            if runtime.get('agentRuntimeName') == runtime_name:
                return {
                    'arn': runtime.get('agentRuntimeArn'),
                    'id': runtime.get('agentRuntimeId')
                }
        return None
    except ClientError as e:
        print(f"Warning: Could not list runtimes: {e}")
        return None


def create_runtime():
    """Create a new agent runtime"""
    try:
        print(f"\n🚀 Creating new Agent Runtime: {RUNTIME_NAME}")
        print(f"   Container: {CONTAINER_URI}")
        
        response = client.create_agent_runtime(
            agentRuntimeName=RUNTIME_NAME,
            agentRuntimeArtifact={
                'containerConfiguration': {
                    'containerUri': CONTAINER_URI
                }
            },
            networkConfiguration={"networkMode": "PUBLIC"},
            roleArn=ROLE_ARN
        )
        
        print(f"✅ Agent Runtime created successfully!")
        print(f"   ARN: {response['agentRuntimeArn']}")
        print(f"   Status: {response['status']}")
        return response['agentRuntimeArn']
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'ConflictException':
            print(f"⚠️  Runtime '{RUNTIME_NAME}' already exists. Try updating instead.")
            # Try to get the existing ARN
            existing_runtime = get_existing_runtime(RUNTIME_NAME)
            if existing_runtime:
                return existing_runtime['arn']
        else:
            print(f"❌ Failed to create runtime: {e}")
        raise


def update_runtime(runtime_info):
    """Update an existing agent runtime with new container image"""
    try:
        print(f"\n🔄 Updating Agent Runtime")
        print(f"   ARN: {runtime_info['arn']}")
        print(f"   ID: {runtime_info['id']}")
        print(f"   New Container: {CONTAINER_URI}")
        
        response = client.update_agent_runtime(
            agentRuntimeId=runtime_info['id'],
            agentRuntimeArtifact={
                'containerConfiguration': {
                    'containerUri': CONTAINER_URI
                }
            },
            roleArn=ROLE_ARN,
            networkConfiguration={"networkMode": "PUBLIC"},
            description='Updated container image to latest version'
        )
        
        print(f"✅ Agent Runtime updated successfully!")
        print(f"   Status: {response['status']}")
        return runtime_info['arn']
        
    except ClientError as e:
        print(f"❌ Failed to update runtime: {e}")
        raise


def deploy():
    """Main deployment logic: create or update runtime"""
    try:
        # Check if runtime already exists
        existing_runtime = get_existing_runtime(RUNTIME_NAME)
        
        if existing_runtime:
            print(f"📦 Found existing runtime: {existing_runtime['arn']}")
            runtime_arn = update_runtime(existing_runtime)
        else:
            print(f"📦 No existing runtime found")
            runtime_arn = create_runtime()
        
        print(f"\n{'='*80}")
        print(f"🎉 Deployment Complete!")
        print(f"{'='*80}")
        print(f"Runtime Name: {RUNTIME_NAME}")
        print(f"Runtime ARN: {runtime_arn}")
        print(f"Container: {CONTAINER_URI}")
        print(f"{'='*80}\n")
        
        return runtime_arn
        
    except Exception as e:
        print(f"\n{'='*80}")
        print(f"💥 Deployment Failed!")
        print(f"{'='*80}")
        print(f"Error: {str(e)}")
        print(f"{'='*80}\n")
        raise


if __name__ == "__main__":
    deploy()

