import json

from strands import Agent
from strands.models.bedrock import BedrockModel

def handler(event, context):
    try:
        raw_body = event.get("body", "{}")
        if not raw_body:
            raw_body = "{}"
            
        body = json.loads(raw_body)
        
        job_title = body.get("title", "Software Developer") # Default config if missing
        resume_content = body.get("resume_content", "")
        
        if not resume_content:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing 'resume_content' string in request payload."})
            }

        # Setup Strands Agent with Bedrock
        model = BedrockModel(
            model_id="amazon.nova-micro-v1:0",
            region_name="us-east-1"
        )
        
        agent = Agent(model=model)
        
        prompt = f"""
        You are an expert technical recruiter and resume reviewer. 
        The candidate is applying for the job title: {job_title}
        
        Here is their extracted resume content:
        ---
        {resume_content}
        ---
        
        Please act as the reviewer and provide your response addressing the candidate. Include:
        1. A score out of 10 for how well their resume matches this specific job title.
        2. A brief analysis of their strengths.
        3. Actionable feedback on their weaknesses, missing skills, or formatting.
        """
        
        # Invoke the Agent
        response = agent(prompt)
        
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "job_title_evaluated": job_title,
                "review": str(response)
            })
        }
        
    except Exception as e:
        import traceback
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(e),
                "trace": traceback.format_exc()
            })
        }
