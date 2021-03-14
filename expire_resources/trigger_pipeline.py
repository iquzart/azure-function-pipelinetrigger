import os
import json
import requests
import logging

def trigger_pipelines(pipeline_id):
    """
    Trigger Azure pipeline to destroy expired resources
    """
    
    pipeline_url = os.environ.get('PIPELINE_URL')
    personal_access_token = os.environ.get('PAT')
    
    headers = {'Content-Type': 'application/json'}  

    auth = requests.auth.HTTPBasicAuth('', personal_access_token)
    
    payload = {
                "definition": {
                    "id": pipeline_id
                },
                "sourceBranch": "refs/heads/development",
                "sourceVersion": "",
                "reason": 1,
                "demands": [],
                "parameters": "{\"action\":  \"destroy\"}"
            }
    # Triggering Terraform Destroy Stage on pipeline
    response = requests.post(url=pipeline_url, data=json.dumps(payload), auth=auth, headers=headers) 
    return response
