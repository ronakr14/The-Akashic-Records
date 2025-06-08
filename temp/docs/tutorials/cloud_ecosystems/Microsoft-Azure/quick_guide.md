# Microsoft Azure Tutorial

## Overview

Microsoft Azure is a cloud computing platform and service created by Microsoft. It offers a range of cloud services, including those for computing, analytics, storage, and networking. Users can choose and configure these services to meet their specific needs.

## Introduction to Azure

### What is Microsoft Azure?

Microsoft Azure is a comprehensive cloud platform offering a wide range of services for building, deploying, and managing applications through Microsoft-managed data centers. It supports various programming languages, frameworks, and tools.

### Key Features

- **Scalability:** Scale resources up or down based on demand.
- **Flexibility:** Choose from a wide range of services to fit specific needs.
- **Security:** Built-in security features and compliance certifications.
- **Global Reach:** Data centers around the world for low-latency access.

## Azure Services

### Compute Services

- **Azure Virtual Machines (VMs):** Provides scalable virtual servers in the cloud.
- **Azure App Services:** Platform-as-a-Service (PaaS) for building web apps and APIs.
- **Azure Kubernetes Service (AKS):** Managed Kubernetes cluster for container orchestration.

### Storage Services

- **Azure Blob Storage:** Object storage for unstructured data.
- **Azure Table Storage:** NoSQL store for large amounts of structured data.
- **Azure File Storage:** Managed file shares accessible via the Server Message Block (SMB) protocol.

### Database Services

- **Azure SQL Database:** Managed relational database service.
- **Azure Cosmos DB:** Globally distributed, multi-model database service.

### Networking Services

- **Azure Virtual Network:** Enables secure communication between Azure resources.
- **Azure Load Balancer:** Distributes network traffic across multiple VMs.

## Azure Storage

### Blob Storage

Azure Blob Storage is used for storing large amounts of unstructured data, such as text or binary data.

#### Example: Uploading a File to Blob Storage

```python
from azure.storage.blob import BlobServiceClient

# Connect to Azure Blob Storage
blob_service_client = BlobServiceClient.from_connection_string('your_connection_string')

# Create a container
container_client = blob_service_client.create_container('mycontainer')

# Upload a file
blob_client = container_client.get_blob_client('myfile.txt')
with open('myfile.txt', 'rb') as data:
    blob_client.upload_blob(data)
```

### Table Storage

Azure Table Storage is used for storing large amounts of structured data in a NoSQL store.

#### Example: Inserting an Entity into Table Storage

```python
from azure.data.tables import TableServiceClient, TableClient

# Connect to Azure Table Storage
table_service_client = TableServiceClient.from_connection_string('your_connection_string')

# Create a table
table_client = table_service_client.create_table_if_not_exists('mytable')

# Insert an entity
entity = {
    'PartitionKey': 'partition1',
    'RowKey': 'row1',
    'Name': 'John Doe',
    'Age': 30
}
table_client.upsert_entity(entity)
```

## Azure Virtual Machines

### Creating a Virtual Machine

You can create and manage virtual machines (VMs) through the Azure Portal, Azure CLI, or Azure PowerShell.

#### Example: Creating a VM using Azure CLI

```bash
az vm create \
  --resource-group myResourceGroup \
  --name myVM \
  --image UbuntuLTS \
  --admin-username azureuser \
  --generate-ssh-keys
```

## Azure App Services

Azure App Services allows you to build and host web applications in the programming language of your choice without managing infrastructure.

### Deploying a Web App

#### Example: Deploying an App Using Azure CLI

```bash
az webapp create \
  --resource-group myResourceGroup \
  --plan myAppServicePlan \
  --name my-webapp \
  --runtime "PYTHON|3.8"
```

## Azure SQL Database

Azure SQL Database is a managed relational database service.

### Connecting to Azure SQL Database

#### Example: Connecting Using Python

```python
import pyodbc

# Connect to Azure SQL Database
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=myserver.database.windows.net;DATABASE=mydatabase;UID=myuser;PWD=mypassword')

# Execute a query
cursor = conn.cursor()
cursor.execute("SELECT * FROM mytable")

for row in cursor.fetchall():
    print(row)
```

## Azure Functions

Azure Functions allows you to run small pieces of code without managing servers.

### Creating a Function

#### Example: Creating an HTTP-triggered Function

```python
import logging
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}!")
    else:
        return func.HttpResponse(
             "Please pass a name on the query string or in the request body",
             status_code=400
        )
```

## Azure DevOps

Azure DevOps provides tools for DevOps and CI/CD pipelines.

### Creating a Pipeline

#### Example: YAML Pipeline Configuration

```yaml
trigger:
- main

pool:
  vmImage: 'ubuntu-latest'

steps:
- task: UsePythonVersion@0
  inputs:
    versionSpec: '3.x'
  name: InstallPython

- script: |
    python -m pip install --upgrade pip
    pip install -r requirements.txt
  displayName: 'Install dependencies'

- script: |
    python -m unittest discover
  displayName: 'Run tests'
```

## Azure Networking

### Virtual Network

Azure Virtual Network enables you to create isolated network environments in the cloud.

#### Example: Creating a Virtual Network

```bash
az network vnet create \
  --resource-group myResourceGroup \
  --name myVNet \
  --address-prefix 10.0.0.0/16
```

## Azure CLI

The Azure CLI is a command-line tool for managing Azure resources.

### Basic Commands

#### Example: Listing Resource Groups

```bash
az group list --output table
```

#### Example: Deleting a Resource Group

```bash
az group delete --name myResourceGroup --yes --no-wait
```

## Summary

This document provides an overview of Microsoft Azure, covering key services such as Azure Storage, Virtual Machines, App Services, SQL Database, Functions, DevOps, and Networking. It includes examples for common tasks and commands to help you get started with Azure.