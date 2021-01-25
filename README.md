# Pipeline Trigger

Azure Function to queue Azure Pipleine based on Azure Resource expiry.

Environment Vars
----------------

| Variable Name | Description | Sample |
|---|---|---|
| AZURE_SUBSCRIPTION_ID  | Azure subscription ID  | 00000000-0000-0000-0000-000000000000  |
| RESOURCE_GROUPS  | Azure Resource Groups where you have IaC managed resources (comma separated values)  |  RG_MyApp_Dev,RG_exmaple_app_dev |
| PIPELINE_URL  | Azure DevOps Build Pipeline URL  | https://dev.azure.com/MY-ORG/MY-PROJECT/_apis/build/builds?api-version=6.0  |
| PAT  | Azure DevOps PAT  | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx  |
