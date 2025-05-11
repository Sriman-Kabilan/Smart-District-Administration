#!/bin/bash

# AWS Deployment Script for Smart District Administration Dashboard
# Make sure to run 'chmod +x deploy_to_aws.sh' before executing

# Variables - change these according to your needs
APP_NAME="district-admin-dashboard"
AWS_REGION="us-east-1"
EB_PLATFORM="Python 3.11"
DB_INSTANCE_CLASS="db.t3.micro"
DB_USERNAME="adminuser"
DB_NAME="districtdb"
ENVIRONMENT_NAME="production"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo -e "${RED}AWS CLI is not installed. Please install it first.${NC}"
    echo "Visit: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html"
    exit 1
fi

# Check if EB CLI is installed
if ! command -v eb &> /dev/null; then
    echo -e "${RED}Elastic Beanstalk CLI is not installed. Please install it first.${NC}"
    echo "Run: pip install awsebcli"
    exit 1
fi

# Check if user is logged in to AWS
echo -e "${YELLOW}Checking AWS credentials...${NC}"
aws sts get-caller-identity &> /dev/null
if [ $? -ne 0 ]; then
    echo -e "${RED}You are not logged in to AWS. Please run 'aws configure' first.${NC}"
    exit 1
fi
echo -e "${GREEN}AWS credentials found.${NC}"

# Ask for DB password
echo -e "${YELLOW}Enter a secure password for your database:${NC}"
read -s DB_PASSWORD
echo

# Create RDS instance
echo -e "${YELLOW}Creating PostgreSQL database...${NC}"
aws rds create-db-instance \
  --db-instance-identifier $APP_NAME-db \
  --db-instance-class $DB_INSTANCE_CLASS \
  --engine postgres \
  --master-username $DB_USERNAME \
  --master-user-password $DB_PASSWORD \
  --allocated-storage 20 \
  --db-name $DB_NAME \
  --region $AWS_REGION

# Wait for DB to be available
echo -e "${YELLOW}Waiting for database to be available (this may take several minutes)...${NC}"
aws rds wait db-instance-available --db-instance-identifier $APP_NAME-db --region $AWS_REGION

# Get DB endpoint
DB_ENDPOINT=$(aws rds describe-db-instances --db-instance-identifier $APP_NAME-db --query 'DBInstances[0].Endpoint.Address' --output text --region $AWS_REGION)
echo -e "${GREEN}Database created successfully at: $DB_ENDPOINT${NC}"

# Create necessary Elastic Beanstalk files
echo -e "${YELLOW}Creating Elastic Beanstalk configuration files...${NC}"

# Create .ebignore
cat > .ebignore << EOF
venv/
__pycache__/
*.pyc
.git/
.github/
.pytest_cache/
.coverage
.vscode/
docker-compose.yml
deploy_to_aws.sh
Dockerfile
EOF

# Create Procfile
cat > Procfile << EOF
web: streamlit run app.py --server.port=5000 --server.address=0.0.0.0
EOF

# Create .ebextensions directory and config file
mkdir -p .ebextensions
cat > .ebextensions/01_streamlit.config << EOF
option_settings:
  aws:elasticbeanstalk:application:environment:
    PYTHONPATH: "/var/app/current"
    DATABASE_URL: "postgresql://$DB_USERNAME:$DB_PASSWORD@$DB_ENDPOINT:5432/$DB_NAME"
  aws:elasticbeanstalk:container:python:
    WSGIPath: "app:st.web.bootstrap.server.start"
EOF

# Deploy to Elastic Beanstalk
echo -e "${YELLOW}Initializing Elastic Beanstalk application...${NC}"
eb init $APP_NAME --region $AWS_REGION --platform "$EB_PLATFORM"

echo -e "${YELLOW}Creating Elastic Beanstalk environment...${NC}"
eb create $ENVIRONMENT_NAME --region $AWS_REGION

echo -e "${GREEN}Deployment completed successfully!${NC}"
echo -e "You can access your application using: eb open"
echo -e "To update your application in the future, run: eb deploy"
echo
echo -e "${YELLOW}IMPORTANT: Save these database credentials in a secure location:${NC}"
echo "Database Endpoint: $DB_ENDPOINT"
echo "Database Name: $DB_NAME"
echo "Database Username: $DB_USERNAME"
echo "Database Password: [The password you entered]"