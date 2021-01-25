import pytz
import logging
from datetime import datetime


def resource_extractor(resource, type):
    """
    Return dict based on arg type value
    """
    if type == "get_resource":
        return {
            "name": resource.name,
            "ExpiryDate": resource.tags['ExpiryDate'],
            "PipelineID": resource.tags['PipelineID']
        }  
    elif type == "check_resource_status":
        return {
            "Name": resource['name'],
            "ExpiryDate": resource['ExpiryDate'],
            "PipelineID": resource['PipelineID']
            }  
    else:
        logging.error("resource_extractory - type did not match any")      
        
        
def check_managed_resource_status(managed_resources):
    
    tz = pytz.timezone('Asia/Dubai') 
    now = datetime.now(tz).strftime("%d/%m/%Y %H:%M:%S")
    
    expired_resources = []
    valid_resources = []
    for managed_resource in managed_resources:
        expiry_time = managed_resource['ExpiryDate']

        if now > expiry_time:
            expired_resources.append(resource_extractor(managed_resource, 
                                                        type="check_resource_status"))
        else:
            valid_resources.append(resource_extractor(managed_resource, 
                                   type="check_resource_status"))
    
    return expired_resources, valid_resources
         