import aws_cdk as cdk
from stack import StudyBuddyStack

# 1. Initialize the CDK App
app = cdk.App()

# 2. Instantiate our Stack
StudyBuddyStack(app, "StudyBuddyStack")

app.synth()

