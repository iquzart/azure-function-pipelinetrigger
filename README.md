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

## How it works
The function will list all the resources with tag "ExpiryDate" from given Azure Resource groups. Compare the expiry date with current time. Then the function will queue the Azure IaC pipeline destroy stage with below parameters.

```
{
    "definition": {
        "id": pipeline_id
        },
    "sourceBranch": "refs/heads/master",
    "sourceVersion": "",
    "reason": 1,
    "demands": [],
    "parameters": "{\"action\":  \"destroy\"}" -------------> (The pipline destroy stage should have a condition to run only when the action variable value is destroy)
    }
```
## Azure DevOps Pipeline sample

You may find a sample pipline [here](https://github.com/iquzart/azure-iac/tree/master/go-app)

## License
MIT

## Author Information
Muhammed Iqbal <iquzart@hotmail.com>