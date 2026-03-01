from invoke import task

@task
def synth(c):
    """Synthesizes the CDK stack to generate CloudFormation templates."""
    print("Synthesizing CDK stack...")
    c.run("cdk synth")

@task
def diff(c):
    """Shows the difference between local CDK stack and deployed AWS infrastructure."""
    print("Running CDK diff...")
    c.run("cdk diff")

@task
def deploy(c):
    """Deploys the CDK stack to AWS."""
    print("Deploying CDK stack...")
    c.run("cdk deploy --require-approval never")

@task
def bootstrap(c):
    """Bootstraps the AWS environment for CDK."""
    print("Bootstrapping CDK environment...")
    c.run("cdk bootstrap")

