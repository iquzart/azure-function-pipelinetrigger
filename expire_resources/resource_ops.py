

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
        