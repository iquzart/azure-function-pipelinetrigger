import os
import asyncio
import logging
import datetime
import azure.functions as func
from azure.identity import DefaultAzureCredential
from azure.common.credentials import (ServicePrincipalCredentials, get_azure_cli_credentials)
from azure.mgmt.resource import ResourceManagementClient


from .resource_ops import (resource_extractor, check_managed_resource_status, check_rg_availability)
from .util import tabulate_report
from .trigger_pipeline import trigger_pipelines

async def main(mytimer: func.TimerRequest) -> None:
    """
    The main entry point to the function.
    """

    if "MSI_ENDPOINT" in os.environ:
        credential = DefaultAzureCredential()
    else:
        credential, *_ = get_azure_cli_credentials()
   
    subscription_id = os.environ.get(
        'AZURE_SUBSCRIPTION_ID', '11111111-1111-1111-1111-111111111111')
    
    # Obtain the management object for resources.
    resource_client = ResourceManagementClient(credential, subscription_id)

    
    # managed resource groups provided on env
    managed_resource_groups = os.environ["RESOURCE_GROUPS"].split(",")
    
    managed_resource_groups = check_rg_availability(resource_client, managed_resource_groups)

    managed_resources = []
    for managed_resource_group in managed_resource_groups:
        resources = resource_client.resources.list_by_resource_group(managed_resource_group)

        for resource in resources:
            if (resource.tags != None) and ('ExpiryDate' in resource.tags):   
                try:
                    managed_resources.append(resource_extractor(resource, 
                                                                type="get_resource"))
                except Exception as e:
                    logging.error("encountered: {0}".format(str(e)))  

    # get Expired and Valid resources
    expired_resources, valid_resources = check_managed_resource_status(managed_resources)
    
    if len(valid_resources) != 0:
        logging.info("Valid Resources:")
        logging.info(tabulate_report(valid_resources))         
    else:
        logging.info("No Valid Resources found")

    if len(expired_resources) != 0:
        logging.info("Expired Resources:")
        logging.info(tabulate_report(expired_resources))
        
        pipeline_ids = set( val for dic in expired_resources for val in dic.get("PipelineID"))
        # trigger pipeline to destroy the expired resources
        for pipeline_id in pipeline_ids:
            logging.info("Initiating destroy stage on pipeline id: {}".format(pipeline_id))
            response = trigger_pipelines(pipeline_id)
            if response.status_code == 200:
                logging.info("Successfully Triggerd pipeline")
            else:
                logging.error("Failed while initiating destroy on pipeline - {}".format(pipeline_id))
    else:
        logging.info("No Expired Resources found")