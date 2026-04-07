import aws_cdk as cdk
from aws_cdk import (
    Stack,
    Duration,
    aws_iam,
    aws_lambda as _lambda,
    aws_apigateway as apigw
)
from constructs import Construct

class StudyBuddyStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # create a lambda function for resuming reviewing
        resume_reviewer_function = _lambda.Function(
            self, "ResumeReviewerFunction",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="index.handler",
            code=_lambda.Code.from_asset("build/lambda/resume_reviewer"),
            timeout=Duration.seconds(45)  # GenAI calls take time
        )

        # Grant Bedrock invoke permissions to this Lambda
        resume_reviewer_function.add_to_role_policy(
            aws_iam.PolicyStatement(
                actions=[
                    "bedrock:InvokeModel",
                    "bedrock:InvokeModelWithResponseStream"
                ],
                resources=["*"] # Broad enough for Nova/Claude models in this region
            )
        )

        # 2. Define the API Gateway
        api = apigw.RestApi(
            self, "StudyBuddyApi",
            rest_api_name="StudyBuddy API",
            description="The core API for StudyBuddy backend."
        )

        # 3. Connect the API to the Lambda
        lambda_integration = apigw.LambdaIntegration(resume_reviewer_function)

        # 4. Create the '/review_resume' endpoint and add a 'POST' request method
        resume_resource = api.root.add_resource("review_resume")
        # Mandate API Key for this specific endpoint
        resume_resource.add_method("POST", lambda_integration, api_key_required=True)

        # 5. Generate a secure API Key
        api_key = api.add_api_key("StudyBuddyApiKey",
            api_key_name="study-buddy-app-key",
            description="The primary API Key used by the Study Buddy client applications."
        )

        # 6. Create a Usage Plan and link the API Key to our deployed stage
        plan = api.add_usage_plan("StudyBuddyUsagePlan",
            name="StandardTier",
            description="Standard usage plan for clients",
            throttle=apigw.ThrottleSettings(
                rate_limit=50, # Requests per second
                burst_limit=10
            )
        )
        plan.add_api_key(api_key)
        plan.add_api_stage(stage=api.deployment_stage)






