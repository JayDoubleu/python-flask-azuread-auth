# python-flask-azuread-auth
Sample python code to authenticate against azureAD


Creating a Service Principal in the Azure Portal
There are four tasks necessary to create a Service Principal using the Azure Portal:

* Create an Application in Azure Active Directory (which acts as a Service Principal)
* Generate a Client Secret for the Azure Active Directory Application (store secret in config.py)
* Configure Redirect URIs to "http://localhost:5000/authorize" (replace with production url)
* In API permissions select Graph openid. (https://docs.microsoft.com/en-gb/graph/permissions-reference#openid-permissions)
