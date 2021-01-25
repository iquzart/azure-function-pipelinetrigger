import json
import requests
import logging

def trigger_pipelines(expired_resources):
    """
    Trigger Azure pipeline to destroy expired resources
    """
    
    pipeline_ids = set( val for dic in expired_resources for val in dic.get("PipelineID"))
    
    pipeline_url = os.environ.get('PIPELINE_URL')
    personal_access_token = os.environ.get('PAT')
    
    headers = {'Content-Type': 'application/json'}  

    auth = requests.auth.HTTPBasicAuth('', personal_access_token)
    
    for pipeline_id in pipeline_ids:
        payload = {
                    "definition": {
                        "id": pipeline_id
                    },
                    "sourceBranch": "refs/heads/master",
                    "sourceVersion": "",
                    "reason": 1,
                    "demands": [],
                    "parameters": "{\"action\":  \"destroy\"}"
                }
        logging.info("Initiating destroy stage on pipeline id: {}".format(pipeline_id))

        # Triggering Terraform Destroy Stage on pipeline
        response = requests.post(url=pipeline_url, data=json.dumps(payload), auth=auth, headers=headers) 
        return response, pipeline_id