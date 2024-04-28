# CI/CD Pipeline Setup for Containerized Java Applications in ECS using Jenkins

## Prerequisites:
- launched Ubuntu server for Jenkins.

![Screenshot from 2024-04-28 15-16-32](https://github.com/jyotiSharma099/scipio-erp/assets/86827121/b5544f19-10d9-45fa-b5f0-fc6e6c067a98)

- Jenkins and Docker installed and configured using script `Docker_jenkins_install.sh`

```bash
#!/bin/bash

#Docker Installation
sudo apt update 
sudo apt  install docker.io -y

#Jenkins Installation 
# For Jenkins firstly you need Java so 
sudo apt update
sudo apt install fontconfig openjdk-17-jre

#Jenkins
sudo wget -O /usr/share/keyrings/jenkins-keyring.asc \
  https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key
echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc]" \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null
sudo apt-get update
sudo apt-get install jenkins -y

#for start jenkins
sudo systemctl start jenkins
sudo systemctl enable jenkins

```

![Screenshot from 2024-04-28 15-32-59](https://github.com/jyotiSharma099/scipio-erp/assets/86827121/5eda5820-3f8d-45bc-8a8a-a8f879b8ee9d)


- AWS CLI installed on Jenkins server.

## Pipeline Overview:
1. **Source**: The pipeline will be triggered by changes in the source code repository.
2. **Build**: Jenkins will build the Java application and create a Docker image.
3. **Test**: The built Docker image will be tested to ensure application integrity.
4. **Deploy**: The Docker image will be deployed to ECS.

## Step 1: Jenkins Configuration:

![Screenshot from 2024-04-28 15-35-36](https://github.com/jyotiSharma099/scipio-erp/assets/86827121/c20ef191-3c08-491e-b14d-68e6972a569f)


## a) **Install the necessary plugins**:

  - Docker Plugin
  - Git Plugin
  - Amazon ECR Plugin
  - Amazon Elastic Container Service (ECS) / Fargate Plugin
  - AWS plugin
  - AWS SAM Plugin


![Screenshot from 2024-04-28 17-25-24](https://github.com/jyotiSharma099/scipio-erp/assets/86827121/1fd58eb5-27d8-4113-ab1e-880729f17375)


     


## b) **Configure Jenkins to communicate with your AWS account**:
  - Go to Jenkins dashboard > Manage Jenkins > Configure System.
  - Add AWS credentials with the necessary permissions.

      ![Screenshot from 2024-04-28 16-31-21](https://github.com/jyotiSharma099/scipio-erp/assets/86827121/09427c13-0fd9-45b6-b9e5-a7663a25a564)



## c) **Dockerized Source code on GitHub**

### WebHook Integrated

![Screenshot from 2024-04-28 16-39-44](https://github.com/jyotiSharma099/scipio-erp/assets/86827121/736acb1e-6c29-4d53-893f-d80c7ef9a688)



## Step 2: Jenkinsfile Setup:

```groovy
pipeline {
    agent any
    stages {
        stage('Clone repository') {
            steps {
                git([url: 'https://github.com/jyotiSharma099/java-Dockerized.git', branch: 'main'])
            }
        }
        stage('Build') {
            steps {
                sh 'sudo docker build --platform linux/x86_64/v3 -t miguno/java-docker-build-tutorial:latest .'
            }
        }
        stage('Docker test') {
            steps {
                sh 'sudo docker run -itd -p 8123:8123 miguno/java-docker-build-tutorial:latest'
            }
        }
        stage('AWS Configure') {
            steps {
                script {
                    withCredentials([
                        [
                            $class: 'AmazonWebServicesCredentialsBinding',
                            credentialsId: 'aws',
                            accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                            secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
                        ]
                    ]) {
                        sh 'aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 767397830848.dkr.ecr.us-east-1.amazonaws.com'
                        sh 'sudo docker tag miguno/java-docker-build-tutorial:latest 767397830848.dkr.ecr.us-east-1.amazonaws.com/java:latest'
                        sh 'sudo docker push 767397830848.dkr.ecr.us-east-1.amazonaws.com/java:latest'
                    }
                }
            }
        }

        stage('Deploy with SAM') {
            steps {
                script {
                    sh 'sam --version'
                    sh 'sam deploy --template-file ECS.yml --stack-name my-ecs-stack --capabilities CAPABILITY_IAM --region us-east-1'
               }
            }
        }
    }
}

```

![Screenshot from 2024-04-28 19-11-20](https://github.com/jyotiSharma099/scipio-erp/assets/86827121/a39cecd2-5fc5-47e7-bb45-8700d2d3f991)



![Screenshot from 2024-04-28 19-12-48](https://github.com/jyotiSharma099/scipio-erp/assets/86827121/18211c08-596e-47ff-935d-e5cd3049e89a)

