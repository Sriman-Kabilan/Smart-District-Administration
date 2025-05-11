# Smart District Administration Dashboard - Deployment Guide

This guide provides instructions for deploying the Smart District Administration Dashboard to both AWS and Azure cloud platforms.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [AWS Deployment](#aws-deployment)
   - [Option 1: AWS Elastic Beanstalk](#option-1-aws-elastic-beanstalk)
   - [Option 2: AWS EC2](#option-2-aws-ec2)
   - [Option 3: AWS App Runner](#option-3-aws-app-runner)
3. [Azure Deployment](#azure-deployment)
   - [Option 1: Azure App Service](#option-1-azure-app-service)
   - [Option 2: Azure Container Instances](#option-2-azure-container-instances)
   - [Option 3: Azure Virtual Machines](#option-3-azure-virtual-machines)
4. [Database Setup](#database-setup)
   - [AWS RDS for PostgreSQL](#aws-rds-for-postgresql)
   - [Azure Database for PostgreSQL](#azure-database-for-postgresql)
5. [Environment Variables](#environment-variables)
6. [HTTPS and Domain Setup](#https-and-domain-setup)
7. [Monitoring and Maintenance](#monitoring-and-maintenance)

## Prerequisites

Before deploying, ensure you have:

1. The complete application code from this repository
2. A PostgreSQL database (either hosted on cloud or self-managed)
3. AWS or Azure account with appropriate permissions
4. AWS CLI or Azure CLI installed for command-line deployments
5. Docker installed (for container-based deployments)

## AWS Deployment

### Option 1: AWS Elastic Beanstalk

Elastic Beanstalk provides the easiest way to deploy Python applications on AWS.

1. **Prepare your application**:
   
   Create a `requirements.txt` file if not already present:
   ```bash
   pip freeze > requirements.txt
   ```

   Create a `.ebignore` file to exclude unnecessary files.

2. **Configure Elastic Beanstalk**:

   Create a new file called `.ebextensions/01_streamlit.config`:
   ```yaml
   option_settings:
     aws:elasticbeanstalk:application:environment:
       PYTHONPATH: "/var/app/current"
       DATABASE_URL: "postgresql://username:password@your-rds-endpoint:5432/database"
     aws:elasticbeanstalk:container:python:
       WSGIPath: "app:st.web.bootstrap.server.start"
   ```

   Create a `Procfile` in your project root:
   ```
   web: streamlit run app.py --server.port=5000 --server.address=0.0.0.0
   ```

3. **Deploy to Elastic Beanstalk**:
   
   ```bash
   # Initialize Elastic Beanstalk application
   eb init -p python-3.11 district-admin-dashboard
   
   # Create an environment and deploy
   eb create district-admin-dashboard-prod
   
   # For future deployments
   eb deploy
   ```

4. **Access your application**:
   
   After deployment completes, get the URL:
   ```bash
   eb open
   ```

### Option 2: AWS EC2

For more control over the server environment:

1. **Launch an EC2 instance**:
   - Choose an Amazon Linux 2 or Ubuntu instance
   - Select an appropriate size (t2.micro for testing, larger for production)
   - Configure security groups to allow inbound traffic on ports 22 (SSH) and 5000 (Streamlit)

2. **Set up the server**:
   
   Connect to your instance:
   ```bash
   ssh -i your-key.pem ec2-user@your-instance-ip
   ```
   
   Install dependencies:
   ```bash
   sudo yum update -y  # For Amazon Linux
   # OR
   sudo apt update  # For Ubuntu
   
   # Install Python and pip
   sudo yum install -y python3 python3-pip  # For Amazon Linux
   # OR
   sudo apt install -y python3 python3-pip  # For Ubuntu
   
   # Install git
   sudo yum install -y git  # For Amazon Linux
   # OR
   sudo apt install -y git  # For Ubuntu
   ```

3. **Deploy your application**:
   
   ```bash
   # Clone your repository
   git clone https://your-repo-url.git
   cd your-repo-directory
   
   # Install dependencies
   pip3 install -r requirements.txt
   
   # Set environment variables
   export DATABASE_URL="postgresql://username:password@your-db-endpoint:5432/database"
   
   # Start the application (for testing)
   streamlit run app.py --server.port=5000 --server.address=0.0.0.0
   ```

4. **Set up as a service (for production)**:
   
   Create a service file:
   ```bash
   sudo nano /etc/systemd/system/dashboard.service
   ```
   
   Add the following content:
   ```
   [Unit]
   Description=District Administration Dashboard
   After=network.target
   
   [Service]
   User=ec2-user
   WorkingDirectory=/path/to/your/application
   ExecStart=/usr/local/bin/streamlit run app.py --server.port=5000 --server.address=0.0.0.0
   Restart=always
   Environment=DATABASE_URL=postgresql://username:password@your-db-endpoint:5432/database
   
   [Install]
   WantedBy=multi-user.target
   ```
   
   Enable and start the service:
   ```bash
   sudo systemctl enable dashboard
   sudo systemctl start dashboard
   ```

### Option 3: AWS App Runner

For a fully managed service with automatic deployments:

1. **Create a Dockerfile**:
   ```
   FROM python:3.11-slim
   
   WORKDIR /app
   
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   
   COPY . .
   
   EXPOSE 5000
   
   CMD ["streamlit", "run", "app.py", "--server.port=5000", "--server.address=0.0.0.0"]
   ```

2. **Deploy to AWS App Runner**:
   - Go to AWS App Runner console
   - Create a new service
   - Choose "Source code repository" and connect your GitHub/BitBucket repo
     OR
   - Choose "Container registry" if you've built and pushed your Docker image
   - Configure the build settings (if using source repository)
   - Set environment variables including your DATABASE_URL
   - Deploy the service

3. **App Runner will automatically**:
   - Build your application
   - Deploy it
   - Provide an HTTPS endpoint
   - Scale based on traffic

## Azure Deployment

### Option 1: Azure App Service

Azure App Service provides a fully managed platform for Python applications:

1. **Prepare your application**:
   
   Create a `requirements.txt` file if not already present:
   ```bash
   pip freeze > requirements.txt
   ```

2. **Configure for App Service**:
   
   Create a file called `startup.sh` in your project root:
   ```bash
   #!/bin/bash
   streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```
   
   Create a `web.config` file:
   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <configuration>
     <system.webServer>
       <handlers>
         <add name="httpPlatformHandler" path="*" verb="*" modules="httpPlatformHandler" resourceType="Unspecified" />
       </handlers>
       <httpPlatform processPath="%HOME%\site\wwwroot\startup.sh"
                     arguments=""
                     stdoutLogEnabled="true"
                     stdoutLogFile="%HOME%\LogFiles\stdout.log"
                     startupTimeLimit="60">
         <environmentVariables>
           <environmentVariable name="PORT" value="%HTTP_PLATFORM_PORT%" />
           <environmentVariable name="DATABASE_URL" value="postgresql://username:password@your-db-server:5432/database" />
         </environmentVariables>
       </httpPlatform>
     </system.webServer>
   </configuration>
   ```

3. **Deploy to Azure App Service**:
   
   ```bash
   # Login to Azure CLI
   az login
   
   # Create a resource group if you don't have one
   az group create --name district-dashboard-rg --location eastus
   
   # Create an App Service Plan
   az appservice plan create --name district-dashboard-plan --resource-group district-dashboard-rg --sku B1 --is-linux
   
   # Create a web app
   az webapp create --name district-admin-dashboard --resource-group district-dashboard-rg --plan district-dashboard-plan --runtime "PYTHON|3.11"
   
   # Configure environment variables
   az webapp config appsettings set --name district-admin-dashboard --resource-group district-dashboard-rg --settings DATABASE_URL="postgresql://username:password@your-db-server:5432/database"
   
   # Deploy your code
   az webapp up --name district-admin-dashboard --resource-group district-dashboard-rg --runtime "PYTHON|3.11"
   ```

4. **Access your application**:
   
   Your app will be available at `https://district-admin-dashboard.azurewebsites.net`

### Option 2: Azure Container Instances

For a container-based deployment without managing server infrastructure:

1. **Create a Dockerfile** (same as in AWS App Runner section)

2. **Build and push your Docker image to Azure Container Registry**:
   
   ```bash
   # Create a container registry
   az acr create --name districtdashboardregistry --resource-group district-dashboard-rg --sku Basic
   
   # Log in to the registry
   az acr login --name districtdashboardregistry
   
   # Build and push your Docker image
   docker build -t districtdashboardregistry.azurecr.io/dashboard:latest .
   docker push districtdashboardregistry.azurecr.io/dashboard:latest
   ```

3. **Deploy to Azure Container Instances**:
   
   ```bash
   # Enable admin user for ACR
   az acr update --name districtdashboardregistry --admin-enabled true
   
   # Get credentials
   ACR_PASSWORD=$(az acr credential show --name districtdashboardregistry --query "passwords[0].value" --output tsv)
   
   # Create container instance
   az container create \
     --resource-group district-dashboard-rg \
     --name district-dashboard-container \
     --image districtdashboardregistry.azurecr.io/dashboard:latest \
     --registry-login-server districtdashboardregistry.azurecr.io \
     --registry-username districtdashboardregistry \
     --registry-password $ACR_PASSWORD \
     --dns-name-label district-dashboard \
     --ports 5000 \
     --environment-variables DATABASE_URL="postgresql://username:password@your-db-server:5432/database"
   ```

4. **Access your application**:
   
   Your app will be available at `http://district-dashboard.<region>.azurecontainer.io:5000`

### Option 3: Azure Virtual Machines

For complete control over the environment:

1. **Create an Azure VM**:
   - Go to Azure Portal
   - Create a new VM (Ubuntu recommended)
   - Make sure to open ports 22 (SSH) and 5000 (Streamlit)

2. **Set up the server** (Similar to EC2 setup):
   
   Connect to your VM:
   ```bash
   ssh your-username@your-vm-ip
   ```
   
   Follow the same installation steps as in the EC2 section for installing dependencies and setting up your application.

3. **Set up as a service** (same as in EC2 section)

## Database Setup

### AWS RDS for PostgreSQL

1. **Create a PostgreSQL database**:
   
   ```bash
   aws rds create-db-instance \
     --db-instance-identifier district-dashboard-db \
     --db-instance-class db.t3.micro \
     --engine postgres \
     --master-username adminuser \
     --master-user-password your-secure-password \
     --allocated-storage 20 \
     --db-name districtdb
   ```

2. **Get the endpoint**:
   
   ```bash
   aws rds describe-db-instances --db-instance-identifier district-dashboard-db --query 'DBInstances[0].Endpoint.Address' --output text
   ```

3. **Update your application's DATABASE_URL** with the new endpoint

### Azure Database for PostgreSQL

1. **Create a PostgreSQL database server**:
   
   ```bash
   az postgres server create \
     --name district-dashboard-db \
     --resource-group district-dashboard-rg \
     --location eastus \
     --admin-user adminuser \
     --admin-password your-secure-password \
     --sku-name B_Gen5_1
   ```

2. **Create a database**:
   
   ```bash
   az postgres db create \
     --name districtdb \
     --server-name district-dashboard-db \
     --resource-group district-dashboard-rg
   ```

3. **Configure firewall rules**:
   
   ```bash
   # Allow access from Azure services
   az postgres server firewall-rule create \
     --name AllowAllAzureIPs \
     --server-name district-dashboard-db \
     --resource-group district-dashboard-rg \
     --start-ip-address 0.0.0.0 \
     --end-ip-address 0.0.0.0
   
   # Allow access from your deployment environment
   az postgres server firewall-rule create \
     --name AllowDeploymentServer \
     --server-name district-dashboard-db \
     --resource-group district-dashboard-rg \
     --start-ip-address <your-server-ip> \
     --end-ip-address <your-server-ip>
   ```

4. **Get the connection string**:
   
   ```
   postgresql://adminuser@district-dashboard-db:your-secure-password@district-dashboard-db.postgres.database.azure.com:5432/districtdb
   ```

## Environment Variables

Ensure these environment variables are set in your deployment environment:

- `DATABASE_URL`: PostgreSQL connection string
- `STREAMLIT_SERVER_PORT`: 5000
- `STREAMLIT_SERVER_ADDRESS`: 0.0.0.0

## HTTPS and Domain Setup

### AWS

1. **Using Elastic Beanstalk**:
   - HTTPS is enabled by default on the *.elasticbeanstalk.com domain
   - For custom domains, configure in the Elastic Beanstalk console under "Configuration > Load Balancer"

2. **Using EC2**:
   - Set up an Application Load Balancer (ALB)
   - Configure your domain in Route 53
   - Add an SSL certificate via AWS Certificate Manager

### Azure

1. **Using App Service**:
   - HTTPS is enabled by default on the *.azurewebsites.net domain
   - For custom domains, configure in the App Service console under "Settings > Custom domains"

2. **Using Container Instances or VMs**:
   - Set up Azure Application Gateway
   - Configure your domain and add an SSL certificate

## Monitoring and Maintenance

### AWS

1. **CloudWatch**:
   - Set up CloudWatch Alarms for metrics like CPU usage, memory, and error rates
   - Configure CloudWatch Logs for application logs

2. **Maintenance**:
   - Set up CodePipeline for automated deployments
   - Configure automatic backups for your RDS database

### Azure

1. **Azure Monitor**:
   - Enable Application Insights for monitoring
   - Set up alerts for key metrics

2. **Maintenance**:
   - Use Azure DevOps Pipelines for automated deployments
   - Configure automatic backups for your PostgreSQL database

---

## Additional Deployment Options

### Using Docker Compose

For local testing or simpler deployments, you can use Docker Compose:

1. **Create a `docker-compose.yml` file**:
   ```yaml
   version: '3'
   
   services:
     dashboard:
       build: .
       ports:
         - "5000:5000"
       environment:
         - DATABASE_URL=postgresql://postgres:postgres@db:5432/districtdb
       depends_on:
         - db
     
     db:
       image: postgres:14
       environment:
         - POSTGRES_USER=postgres
         - POSTGRES_PASSWORD=postgres
         - POSTGRES_DB=districtdb
       volumes:
         - postgres_data:/var/lib/postgresql/data
   
   volumes:
     postgres_data:
   ```

2. **Run with Docker Compose**:
   ```bash
   docker-compose up -d
   ```

### Serverless Options

For cost-effective deployments with automatic scaling:

1. **AWS Lambda with API Gateway**:
   - Package your Streamlit app using AWS Lambda layers
   - Create an API Gateway to handle HTTP requests
   - Note: This is more complex and may require modifications to the Streamlit app

2. **Azure Functions**:
   - Similar to AWS Lambda, but with Azure Function Apps
   - Requires specific adaptations for Streamlit

---

For any issues during deployment, please refer to:
- [Streamlit Deployment Documentation](https://docs.streamlit.io/knowledge-base/deploy)
- [AWS Documentation](https://docs.aws.amazon.com/)
- [Azure Documentation](https://docs.microsoft.com/azure/)