## Dockerizing and Testing a Java Application and Pushing to Amazon ECR then going to deploy on ECS fargate using Cloudformation

This guide will walk you through the process of dockerizing a Java application, testing it, and then pushing the Docker image to Amazon ECR.

## Prerequisites

Make sure you have the following installed:

- Docker
- Java Development Kit (JDK)

Also, ensure you have an AWS account and the AWS CLI configured with necessary permissions.

## Step 1: Dockerizing the Java Application

1. **Dockerfile**: Create a Dockerfile in the root of your Java project.

    ```Dockerfile
    # Use OpenJDK 8 as the base image
    FROM adoptopenjdk/openjdk8:latest

    # Set the working directory
    WORKDIR /app

    # Copy the entire repository to the working directory
    COPY . /app

    # Install Maven for building the project
    RUN apt-get update && apt-get install -y maven

    # Clean up apt-get cache
    RUN apt-get clean && rm -rf /var/lib/apt/lists/*

    # Compile the project using Maven
    RUN mvn clean install

    # Set environment variables
    ENV LANG=C.UTF-8
    ENV JAVA_HOME=/usr/lib/jvm/java-1.8-openjdk
    ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/lib/jvm/java-1.8-openjdk/jre/bin:/usr/lib/jvm/java-1.8-openjdk/bin
    ENV JAVA_VERSION=8u111
    ENV JAVA_ALPINE_VERSION=8.111.14-r0
    ENV SCIPIO_VERSION=1.14.4
    ENV SCIPIO_TGZ_URL=https://github.com/ilscipio/scipio-erp/archive/v1.14.4.tar.gz
    ENV SCIPIO_HOME=/opt/scipio
    ENV PATH=/opt/scipio/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/lib/jvm/java-1.8-openjdk/jre/bin:/usr/lib/jvm/java-1.8-openjdk/bin

    # Create the Scipio ERP directory
    RUN mkdir -p "$SCIPIO_HOME"

    # Switch to the Scipio ERP directory
    WORKDIR /opt/scipio

    # Download and extract Scipio ERP
    RUN set -x && \
        curl -L "$SCIPIO_TGZ_URL" | tar xz --strip-components=1

    # Expose the Tomcat server ports
    EXPOSE 8080 8443 8983

    # Set the default command to start Scipio ERP
    CMD ["sh", "./start.sh"]
    ```

    

2. **Building the Docker Image**: Build the Docker image using the following command:

    ```bash
    docker build -t ilscipio/scipio-erp:demo .
    ```

    Replace `ilscipio/scipio-erp` with the desired name for your Docker image.

## Step 2: Testing the Dockerized Application

1. **Running Tests**: Run tests against your Dockerized application:

    ```bash
    docker run -itd -p 8443:8443 ilscipio/scipio-erp:demo
    ```

   a) To access the application visit the SCIPIO ERP Dashboard: https://localhost:8443/admin
    
   b) To access the SCIPIO ERP applications from the Dashboard use: Username: admin Password: scipio

     ![Screenshot from 2024-04-27 15-14-56](https://github.com/jyotiSharma099/scipio-erp/assets/86827121/1bdff09b-4f8c-4b0a-876e-334a47d53dbd)


## Step 3: Pushing the Docker Image to Amazon ECR

1. **Login to Amazon ECR**: Log in to Amazon ECR using the AWS CLI:

    ```bash
    aws ecr get-login-password --region your-region | docker login --username AWS --password-stdin your-account-id.dkr.ecr.your-region.amazonaws.com
    ```

    Replace `your-region` with your AWS region and `your-account-id` with your AWS account ID.

2. **Tag the Image**: Tag your Docker image with the ECR repository URI:

    ```bash
    docker tag your-image-name:latest your-account-id.dkr.ecr.your-region.amazonaws.com/your-repository-name:latest
    ```

    Replace `your-account-id`, `your-region`, and `your-repository-name` accordingly.

3. **Push the Image**: Push the Docker image to Amazon ECR:

    ```bash
    docker push your-account-id.dkr.ecr.your-reg

# Infrastructure Deployment for Java-Based Microservices on AWS

let's create a basic infrastructure using AWS CloudFormation to deploy a collection of Java-based microservices that communicate through named aliases and DNS namespaces.

## Prerequisites

We'll create the following components:

- Virtual Private Cloud (VPC)
- Subnets
- ECS and LB Security Groups
- ECS (Fargate) Cluster
- ECS Service
- ALB (Application Load Balancer) to route traffic to microservices

## Amazon ECS Application Architecture:

![amazon_ecs_arch](https://github.com/jyotiSharma099/scipio-erp/assets/86827121/4bb348f7-465a-4a68-a8d5-3e8e16e389f8)

## Let's create VPC using AWS Cloudformation

- **Virtual Private Cloud (VPC)**
   
![Screenshot from 2024-04-27 15-55-51](https://github.com/jyotiSharma099/scipio-erp/assets/86827121/a3535377-a7fa-4f73-be76-1e8bcda1962d)

## Now, Moving with ECS fargate

AWS Fargate is a technology for Amazon ECS that allows you to run containers without having to manage servers or clusters. With AWS Fargate, you no longer have to provision, configure, and scale clusters of virtual machines to run containers. This removes the need to choose server types, decide when to scale your clusters, or optimize cluster packing. AWS Fargate removes the need for you to interact with or think about servers or clusters. Fargate lets you focus on designing and building your applications instead of managing the infrastructure that runs them.

![Screenshot from 2024-04-27 16-23-12](https://github.com/jyotiSharma099/scipio-erp/assets/86827121/feba1ddf-9ff2-44b7-9810-02a4c5c0e304)
      
**Note:** Rest of the Code you can check in ECS.yml file.

![Screenshot from 2024-04-27 18-09-13](https://github.com/jyotiSharma099/scipio-erp/assets/86827121/8470985a-b36c-473f-9ccf-de8cd63eebfc)
