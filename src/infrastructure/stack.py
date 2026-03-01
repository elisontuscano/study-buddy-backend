from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw
    )
    
from constructs import Construct

class StudyBuddyStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # create a lambda function
        hello_world_function = _lambda.Function(
            self, "HelloWorldFunction",
            runtime=_lambda.Runtime.PYTHON_3_13,
            handler="index.handler",
            code=_lambda.Code.from_asset("src/infrastructure/lambda/hello_world")
        )

        # 2. Define the API Gateway
        api = apigw.RestApi(
            self, "StudyBuddyApi",
            rest_api_name="StudyBuddy API",
            description="The hello world API for StudyBuddy backend."
        )

        # 3. Connect the API to the Lambda
        lambda_integration = apigw.LambdaIntegration(hello_world_function)

        # 4. Create the '/hello_world' endpoint and add a 'GET' request method
        hello_resource = api.root.add_resource("hello_world")
        hello_resource.add_method("GET", lambda_integration)






