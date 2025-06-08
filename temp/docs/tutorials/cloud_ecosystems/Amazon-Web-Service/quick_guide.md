# Amazon Web Services (AWS) Tutorial

## Overview

Amazon Web Services (AWS) is a comprehensive cloud computing platform provided by Amazon. It offers a broad range of cloud services including computing power, storage options, and networking capabilities. AWS is widely used for scalable applications, data processing, and enterprise solutions.

## Table of Contents

1. [Introduction to AWS](#introduction-to-aws)
2. [AWS Services](#aws-services)
3. [Amazon EC2](#amazon-ec2)
4. [Amazon S3](#amazon-s3)
5. [Amazon RDS](#amazon-rds)
6. [AWS Lambda](#aws-lambda)
7. [Amazon ECS](#amazon-ecs)
8. [Amazon CloudWatch](#amazon-cloudwatch)
9. [AWS CLI](#aws-cli)

---

## Introduction to AWS

### What is Amazon Web Services?

Amazon Web Services is a cloud platform offering a variety of services including computing power, storage, and databases. It enables users to build, deploy, and manage applications through Amazon's global network of data centers.

### Key Features

- **Scalability:** Easily scale resources up or down based on demand.
- **Global Reach:** Data centers around the world ensure low-latency access.
- **Security:** Advanced security features and compliance certifications.
- **Flexibility:** Support for various programming languages, frameworks, and tools.

## AWS Services

### Compute Services

- **Amazon EC2:** Scalable virtual servers in the cloud.
- **AWS Lambda:** Serverless computing service for running code without provisioning servers.
- **Amazon ECS:** Managed container service for running Docker containers.

### Storage Services

- **Amazon S3:** Object storage for scalable storage of unstructured data.
- **Amazon EBS:** Block storage for Amazon EC2 instances.
- **Amazon Glacier:** Low-cost archival storage for long-term data backup.

### Database Services

- **Amazon RDS:** Managed relational database service for SQL databases.
- **Amazon DynamoDB:** Managed NoSQL database service.
- **Amazon Aurora:** High-performance relational database compatible with MySQL and PostgreSQL.

### Monitoring and Management

- **Amazon CloudWatch:** Monitoring service for AWS resources and applications.
- **AWS CloudTrail:** Service that enables governance, compliance, and operational auditing.

## Amazon EC2

### Launching an EC2 Instance

Amazon EC2 allows you to create and manage virtual servers in the cloud.

#### Example: Launching a New EC2 Instance using AWS CLI

```bash
aws ec2 run-instances \
  --image-id ami-0abcdef1234567890 \
  --count 1 \
  --instance-type t2.micro \
  --key-name my-key-pair \
  --security-group-ids sg-0123456789abcdef0 \
  --subnet-id subnet-0123456789abcdef0
```

## Amazon S3

### Storing and Retrieving Data

Amazon S3 provides scalable object storage for unstructured data.

#### Example: Uploading a File to S3

```bash
aws s3 cp local-file.txt s3://my-bucket/
```

#### Example: Downloading a File from S3

```bash
aws s3 cp s3://my-bucket/remote-file.txt local-directory/
```

## Amazon RDS

### Managing Relational Databases

Amazon RDS is a managed relational database service for various SQL databases.

#### Example: Creating an RDS Instance

```bash
aws rds create-db-instance \
  --db-instance-identifier mydbinstance \
  --db-instance-class db.t2.micro \
  --engine mysql \
  --master-username admin \
  --master-user-password password \
  --allocated-storage 20
```

#### Example: Connecting to an RDS Database

```bash
mysql -h mydbinstance.c9akciq32.rds.amazonaws.com -u admin -p
```

## AWS Lambda

### Creating Serverless Functions

AWS Lambda allows you to run code in response to events without managing servers.

#### Example: Creating a Lambda Function

```bash
aws lambda create-function \
  --function-name my-function \
  --runtime python3.8 \
  --role arn:aws:iam::123456789012:role/service-role/my-role \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://function.zip
```

#### Example: Lambda Function Code (Python)

```python
def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': 'Hello, world!'
    }
```

## Amazon ECS

### Managing Docker Containers

Amazon ECS is a managed container service for running Docker containers.

#### Example: Creating an ECS Cluster

```bash
aws ecs create-cluster --cluster-name my-cluster
```

#### Example: Running a Task

```bash
aws ecs run-task \
  --cluster my-cluster \
  --task-definition my-task-definition
```

## Amazon CloudWatch

### Monitoring AWS Resources

Amazon CloudWatch provides monitoring and logging for AWS resources and applications.

#### Example: Creating a CloudWatch Alarm

```bash
aws cloudwatch put-metric-alarm \
  --alarm-name my-alarm \
  --metric-name CPUUtilization \
  --namespace AWS/EC2 \
  --statistic Average \
  --period 300 \
  --threshold 80 \
  --comparison-operator GreaterThanOrEqualToThreshold \
  --evaluation-periods 1 \
  --alarm-actions arn:aws:sns:us-east-1:123456789012:my-topic
```

## AWS CLI

### Using the AWS Command Line Interface

The AWS CLI is a tool to manage AWS services from the command line.

#### Example: Installing AWS CLI

```bash
curl "https://d1uj6qtbmh3dt5.cloudfront.net/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

#### Example: Configuring AWS CLI

```bash
aws configure
```

#### Example: Listing EC2 Instances

```bash
aws ec2 describe-instances
```

## Summary

This document provides an overview of Amazon Web Services (AWS), including key services such as Amazon EC2, S3, RDS, Lambda, ECS, and CloudWatch. It includes examples for common tasks and commands to help you get started with AWS.