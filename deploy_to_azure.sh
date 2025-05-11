#!/bin/bash

# Azure Deployment Script for Smart District Administration Dashboard
# Make sure to run 'chmod +x deploy_to_azure.sh' before executing

# Variables - change these according to your needs
APP_NAME="district-admin-dashboard"
RESOURCE_GROUP="$APP_NAME-rg"
LOCATION="eastus"
APP_SERVICE_PLAN="$APP_NAME-plan"
DB_SERVER_NAME="$APP_NAME-db"
DB_NAME="districtdb"
DB_USERNAME="adminuser"
SKU="B1"
ENVIRONMENT_NAME="production"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo -e "${RED}Azure CLI is not installed. Please install it first.${NC}"
    echo "Visit: https://docs.microsoft.com/cli/azure/install-azure-cli"
    exit 1
fi

# Check if user is logged in to Azure
echo -e "${YELLOW}Checking Azure login status...${NC}"
az account show &> /dev/null
if [ $? -ne 0 ]; then
    echo -e "${RED}You are not logged in to Azure. Please run 'az login' first.${NC}"
    exit 1
fi
echo -e "${GREEN}Azure credentials found.${NC}"

# Ask for DB password
echo -e "${YELLOW}Enter a secure password for your database:${NC}"
read -s DB_PASSWORD
echo

# Create resource group
echo -e "${YELLOW}Creating resource group...${NC}"
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create App Service Plan
echo -e "${YELLOW}Creating App Service Plan...${NC}"
az appservice plan create --name $APP_SERVICE_PLAN --resource-group $RESOURCE_GROUP --sku $SKU --is-linux

# Create PostgreSQL database
echo -e "${YELLOW}Creating PostgreSQL database...${NC}"
az postgres server create \
  --name $DB_SERVER_NAME \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION \
  --admin-user $DB_USERNAME \
  --admin-password $DB_PASSWORD \
  --sku-name B_Gen5_1 \
  --version 12

# Create the database
echo -e "${YELLOW}Creating database...${NC}"
az postgres db create \
  --name $DB_NAME \
  --server-name $DB_SERVER_NAME \
  --resource-group $RESOURCE_GROUP

# Allow Azure services to access the database
echo -e "${YELLOW}Configuring database firewall...${NC}"
az postgres server firewall-rule create \
  --name AllowAllAzureIPs \
  --server-name $DB_SERVER_NAME \
  --resource-group $RESOURCE_GROUP \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 0.0.0.0

# Create startup script
echo -e "${YELLOW}Creating startup script...${NC}"
cat > startup.sh << EOF
#!/bin/bash
streamlit run app.py --server.port=\$PORT --server.address=0.0.0.0
EOF
chmod +x startup.sh

# Create web.config
echo -e "${YELLOW}Creating web.config...${NC}"
cat > web.config << EOF
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
        <environmentVariable name="DATABASE_URL" value="postgresql://$DB_USERNAME@$DB_SERVER_NAME:$DB_PASSWORD@$DB_SERVER_NAME.postgres.database.azure.com:5432/$DB_NAME" />
      </environmentVariables>
    </httpPlatform>
  </system.webServer>
</configuration>
EOF

# Create web app
echo -e "${YELLOW}Creating web app...${NC}"
az webapp create \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --plan $APP_SERVICE_PLAN \
  --runtime "PYTHON|3.11"

# Configure environment variables
echo -e "${YELLOW}Configuring environment variables...${NC}"
az webapp config appsettings set \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --settings DATABASE_URL="postgresql://$DB_USERNAME@$DB_SERVER_NAME:$DB_PASSWORD@$DB_SERVER_NAME.postgres.database.azure.com:5432/$DB_NAME"

# Deploy the app
echo -e "${YELLOW}Deploying application...${NC}"
az webapp up \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --runtime "PYTHON|3.11"

# Get the URL of the deployed application
APP_URL=$(az webapp show --name $APP_NAME --resource-group $RESOURCE_GROUP --query defaultHostName -o tsv)

echo -e "${GREEN}Deployment completed successfully!${NC}"
echo -e "You can access your application at: https://$APP_URL"
echo
echo -e "${YELLOW}IMPORTANT: Save these database credentials in a secure location:${NC}"
echo "Database Server: $DB_SERVER_NAME.postgres.database.azure.com"
echo "Database Name: $DB_NAME"
echo "Database Username: $DB_USERNAME@$DB_SERVER_NAME"
echo "Database Password: [The password you entered]"