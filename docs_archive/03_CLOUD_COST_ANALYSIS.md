# 💰 CLOUD COST ANALYSIS & SETUP GUIDES
**Version:** 1.0  
**Date:** 2026-04-23  
**Scope:** AWS, GCP, Azure - All Scales

---

## 📋 TABLE OF CONTENTS

1. [Cost Comparison Matrix](#cost-comparison)
2. [AWS Deployment & Pricing](#aws)
3. [Google Cloud Deployment & Pricing](#gcp)
4. [Microsoft Azure Deployment & Pricing](#azure)
5. [Cost Optimization Tips](#optimization)

---

## 💵 COST COMPARISON MATRIX

### Small Scale (1-5 person team, < 50 trades/day)

| Provider | Compute | Database | Storage | Monitoring | **Monthly** | Annual |
|----------|---------|----------|---------|------------|-----------|--------|
| **AWS** | $15 | $35 | $5 | $10 | **$65** | $780 |
| **GCP** | $12 | $32 | $5 | $8 | **$57** | $684 |
| **Azure** | $18 | $38 | $5 | $12 | **$73** | $876 |

**Best for Small:** Google Cloud (Lowest cost, good free tier)

---

### Medium Scale (5-20 people, 50-200 trades/day)

| Provider | Compute | Database | Storage | Monitoring | Load Balancer | **Monthly** | Annual |
|----------|---------|----------|---------|------------|---------------|-----------|--------|
| **AWS** | $50 | $150 | $20 | $30 | $25 | **$275** | $3,300 |
| **GCP** | $45 | $120 | $20 | $25 | $20 | **$230** | $2,760 |
| **Azure** | $60 | $180 | $20 | $35 | $30 | **$325** | $3,900 |

**Best for Medium:** Google Cloud (25% cheaper, better for scale-out)

---

### Enterprise Scale (20+ people, 200+ trades/day, Multi-region)

| Provider | Compute | Database | Storage | Monitoring | Backup | Load Balancer | **Monthly** | Annual |
|----------|---------|----------|---------|------------|--------|---------------|-----------|--------|
| **AWS** | $200 | $400 | $100 | $75 | $50 | $75 | **$900** | $10,800 |
| **GCP** | $180 | $350 | $100 | $60 | $40 | $60 | **$790** | $9,480 |
| **Azure** | $250 | $500 | $100 | $85 | $60 | $90 | **$1,085** | $13,020 |

**Best for Enterprise:** Google Cloud (13% cheaper, exceptional scaling)

---

## 🌩️ AWS DEPLOYMENT & PRICING

### Recommended AWS Architecture (Medium Scale)

```
Components:
├── Compute: ECS on EC2 (t3.medium x 2) - $30/month
├── Database: RDS PostgreSQL (db.t3.small) - $150/month
├── Storage: S3 (backups) - $5/month
├── Load Balancer: Application LB - $25/month
├── Monitoring: CloudWatch - $30/month
└── Networking: Data transfer - $15/month
    ────────────────────────────
    Total: $255/month
```

### AWS Setup Guide (Step-by-Step)

#### Step 1: Create AWS Account & Configure IAM

```bash
# 1. Go to aws.amazon.com
# 2. Create free account
# 3. Create IAM user for development

# Create policy: AdministratorAccess
# Or create custom policy with:
# - EC2 (launch instances)
# - RDS (create databases)
# - S3 (object storage)
# - CloudWatch (monitoring)
# - IAM (user management)
```

#### Step 2: Create VPC & Network

```bash
# Create VPC (10.0.0.0/16)
aws ec2 create-vpc --cidr-block 10.0.0.0/16

# Create public subnet for ALB
aws ec2 create-subnet \
  --vpc-id vpc-xxxxx \
  --cidr-block 10.0.1.0/24

# Create private subnets for apps
aws ec2 create-subnet \
  --vpc-id vpc-xxxxx \
  --cidr-block 10.0.10.0/24

# Create Internet Gateway
aws ec2 create-internet-gateway

# Attach to VPC
aws ec2 attach-internet-gateway \
  --vpc-id vpc-xxxxx \
  --internet-gateway-id igw-xxxxx

# Create NAT Gateway (for private subnet internet)
aws ec2 allocate-address --domain vpc
aws ec2 create-nat-gateway \
  --subnet-id subnet-xxxxx \
  --allocation-id eipalloc-xxxxx
```

#### Step 3: Create PostgreSQL Database

```bash
# Create RDS PostgreSQL instance
aws rds create-db-instance \
  --db-instance-identifier tradepanel-db \
  --db-instance-class db.t3.small \
  --engine postgres \
  --engine-version 13.7 \
  --master-username postgres \
  --master-user-password <strong-password> \
  --allocated-storage 100 \
  --backup-retention-period 30 \
  --multi-az \
  --storage-encrypted

# Create read replica for high availability
aws rds create-db-instance-read-replica \
  --db-instance-identifier tradepanel-db-replica \
  --source-db-instance-identifier tradepanel-db
```

#### Step 4: Create EC2 Instances

```bash
# Launch 2 t3.medium instances for load balancing
aws ec2 run-instances \
  --image-id ami-0c02fb55956c7d316 \
  --instance-type t3.medium \
  --key-name my-key-pair \
  --security-groups tradepanel-sg \
  --user-data file://setup-script.sh \
  --count 2

# Security group: Allow 5000 (API), 22 (SSH) from ALB
aws ec2 create-security-group \
  --group-name tradepanel-sg \
  --description "TradePanel app servers"

aws ec2 authorize-security-group-ingress \
  --group-id sg-xxxxx \
  --protocol tcp --port 5000 \
  --source-security-group-id sg-alb
```

#### Step 5: Create Application Load Balancer

```bash
# Create Target Group
aws elbv2 create-target-group \
  --name tradepanel-targets \
  --protocol HTTP \
  --port 5000 \
  --vpc-id vpc-xxxxx \
  --health-check-enabled

# Create Load Balancer
aws elbv2 create-load-balancer \
  --name tradepanel-alb \
  --subnets subnet-xxxxx subnet-yyyyy \
  --security-groups sg-xxxxx

# Create Listener
aws elbv2 create-listener \
  --load-balancer-arn arn:aws:elasticloadbalancing:... \
  --protocol HTTP \
  --port 80 \
  --default-actions Type=forward,TargetGroupArn=...
```

#### Step 6: Deploy Docker Application

```bash
# Create ECR repository
aws ecr create-repository --repository-name tradepanel

# Push Docker image
docker build -t tradepanel:latest .
docker tag tradepanel:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/tradepanel:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/tradepanel:latest

# Launch ECS cluster
aws ecs create-cluster --cluster-name tradepanel

# Register task definition
aws ecs register-task-definition \
  --family tradepanel \
  --container-definitions file://task-definition.json

# Create ECS service
aws ecs create-service \
  --cluster tradepanel \
  --service-name tradepanel-service \
  --task-definition tradepanel:1 \
  --desired-count 2 \
  --launch-type EC2
```

### AWS Cost Breakdown

```
┌────────────────────────────────────────┐
│      AWS MONTHLY COST BREAKDOWN        │
├────────────────────────────────────────┤
│                                        │
│ EC2 (t3.medium x 2)                   │
│ ├─ $0.0416/hour x 730 hours x 2     │
│ └─ ~$60/month                         │
│                                        │
│ RDS PostgreSQL (db.t3.small)          │
│ ├─ $0.192/hour x 730 hours           │
│ ├─ Storage: 100GB x $0.115/month      │
│ ├─ Backup storage: 100GB x $0.095     │
│ └─ ~$180/month                        │
│                                        │
│ Application Load Balancer             │
│ ├─ $0.0275/hour (720 hours)          │
│ ├─ LCU charge: $0.006/LCU x 1        │
│ └─ ~$25/month                         │
│                                        │
│ S3 Storage (backups)                  │
│ ├─ Backup: 10GB x $0.023/GB           │
│ ├─ Data transfer: 5GB x $0.09/GB      │
│ └─ ~$10/month                         │
│                                        │
│ CloudWatch Monitoring                 │
│ ├─ Log storage & monitoring           │
│ └─ ~$30/month                         │
│                                        │
│ Data Transfer (Internal)              │
│ ├─ 100GB inter-region transfer       │
│ └─ ~$15/month                         │
│                                        │
│ ─────────────────────────────────────  │
│ TOTAL: ~$320/month                    │
│ (or ~$2.40 per trading day)           │
│                                        │
└────────────────────────────────────────┘
```

---

## ☁️ GOOGLE CLOUD DEPLOYMENT & PRICING

### Recommended GCP Architecture (Medium Scale)

```
Components:
├── Compute: Cloud Run (2 services) - $20/month
├── Database: CloudSQL PostgreSQL - $120/month
├── Storage: Cloud Storage - $5/month
├── Load Balancer: Cloud LB - $20/month
├── Monitoring: Cloud Monitoring - $15/month
└── Networking: Data transfer - $10/month
    ────────────────────────────
    Total: $190/month
```

### GCP Setup Guide (Step-by-Step)

#### Step 1: Create GCP Project

```bash
# Create project
gcloud projects create tradepanel-trading \
  --name="TradePanel Trading System"

# Set as current project
gcloud config set project tradepanel-trading

# Enable required APIs
gcloud services enable \
  compute.googleapis.com \
  cloudsql.googleapis.com \
  run.googleapis.com \
  cloudkms.googleapis.com \
  monitoring.googleapis.com
```

#### Step 2: Create VPC & Network

```bash
# Create VPC
gcloud compute networks create tradepanel-vpc \
  --subnet-mode=custom

# Create subnets
gcloud compute networks subnets create tradepanel-public \
  --network=tradepanel-vpc \
  --range=10.0.1.0/24 \
  --region=us-central1

gcloud compute networks subnets create tradepanel-private \
  --network=tradepanel-vpc \
  --range=10.0.10.0/24 \
  --region=us-central1 \
  --private-ip-google-access

# Create firewall rules
gcloud compute firewall-rules create allow-http-https \
  --network=tradepanel-vpc \
  --allow=tcp:80,tcp:443

gcloud compute firewall-rules create allow-internal \
  --network=tradepanel-vpc \
  --allow=tcp:5000,tcp:5432 \
  --source-ranges=10.0.0.0/16
```

#### Step 3: Create CloudSQL PostgreSQL

```bash
# Create Cloud SQL instance
gcloud sql instances create tradepanel-db \
  --database-version=POSTGRES_13 \
  --tier=db-g1-small \
  --region=us-central1 \
  --backup \
  --backup-start-time=02:00 \
  --enable-bin-log \
  --maintenance-window-day=SUN \
  --maintenance-window-hour=03

# Create database
gcloud sql databases create tradepanel \
  --instance=tradepanel-db

# Create user
gcloud sql users create tradepanel-user \
  --instance=tradepanel-db \
  --password=<strong-password>

# Configure private IP
gcloud sql instances patch tradepanel-db \
  --network=tradepanel-vpc \
  --no-assign-ip
```

#### Step 4: Deploy Application

```bash
# Build Docker image
gcloud builds submit \
  --tag gcr.io/tradepanel-trading/tradepanel:latest

# Deploy to Cloud Run
gcloud run deploy tradepanel \
  --image gcr.io/tradepanel-trading/tradepanel:latest \
  --platform managed \
  --region us-central1 \
  --memory 512Mi \
  --cpu 1 \
  --set-env-vars \
    DB_HOST=10.0.10.2,\
    DB_USER=tradepanel-user,\
    DB_PASSWORD=<password> \
  --vpc-connector tradepanel-connector \
  --vpc-egress private-ranges-only \
  --concurrency 4 \
  --timeout 3600 \
  --min-instances 2 \
  --max-instances 10
```

#### Step 5: Create Load Balancer

```bash
# Create backend service
gcloud compute backend-services create tradepanel-backend \
  --protocol HTTP \
  --health-checks tradepanel-health \
  --global \
  --load-balancing-scheme EXTERNAL

# Add backend
gcloud compute backend-services add-backend tradepanel-backend \
  --instance-group tradepanel-ig \
  --instance-group-zone us-central1-a \
  --global

# Create URL map
gcloud compute url-maps create tradepanel-lb \
  --default-service tradepanel-backend

# Create HTTP proxy
gcloud compute target-http-proxies create tradepanel-proxy \
  --url-map tradepanel-lb

# Create forwarding rule
gcloud compute forwarding-rules create tradepanel-forward \
  --global \
  --target-http-proxy tradepanel-proxy \
  --address tradepanel-ip \
  --ports 80
```

### GCP Cost Breakdown

```
┌────────────────────────────────────────┐
│      GCP MONTHLY COST BREAKDOWN        │
├────────────────────────────────────────┤
│                                        │
│ Cloud Run                              │
│ ├─ vCPU: 0.04 vCPU-hour per req       │
│ ├─ Memory: 0.008 GB-hour per req      │
│ ├─ Requests: First 2M free            │
│ └─ ~$20/month (10M requests)          │
│                                        │
│ CloudSQL PostgreSQL                    │
│ ├─ db-g1-small: $50/month             │
│ ├─ Storage: 100GB x $0.18/GB          │
│ ├─ Backups: $18/month                 │
│ └─ ~$120/month                        │
│                                        │
│ Cloud Load Balancer                    │
│ ├─ Forwarding rules: $20/month        │
│ ├─ Data processing: $0.006/GB         │
│ └─ ~$20/month                         │
│                                        │
│ Cloud Storage                          │
│ ├─ Standard storage: 10GB x $0.020    │
│ └─ ~$5/month                          │
│                                        │
│ Cloud Monitoring                       │
│ ├─ Metrics: 1500 metrics              │
│ ├─ Log storage: 10GB x $0.50/GB       │
│ └─ ~$15/month                         │
│                                        │
│ Networking                             │
│ ├─ Inter-region egress: $0.12/GB      │
│ └─ ~$10/month                         │
│                                        │
│ ─────────────────────────────────────  │
│ TOTAL: ~$190/month                    │
│ (or ~$1.43 per trading day)           │
│                                        │
└────────────────────────────────────────┘
```

---

## 🔵 MICROSOFT AZURE DEPLOYMENT & PRICING

### Recommended Azure Architecture (Medium Scale)

```
Components:
├── Compute: App Service Plan (B2) - $50/month
├── Database: Azure Database PostgreSQL - $180/month
├── Storage: Blob Storage - $5/month
├── Load Balancer: Application Gateway - $30/month
├── Monitoring: Azure Monitor - $15/month
└── Networking: Data transfer - $15/month
    ────────────────────────────
    Total: $295/month
```

### Azure Setup Guide (Step-by-Step)

#### Step 1: Create Azure Subscription

```bash
# Login to Azure
az login

# Create resource group
az group create \
  --name tradepanel-rg \
  --location eastus

# Set as default
az configure --defaults group=tradepanel-rg
```

#### Step 2: Create Virtual Network

```bash
# Create VNet
az network vnet create \
  --name tradepanel-vnet \
  --address-prefix 10.0.0.0/16

# Create public subnet
az network vnet subnet create \
  --vnet-name tradepanel-vnet \
  --name public-subnet \
  --address-prefix 10.0.1.0/24

# Create private subnet
az network vnet subnet create \
  --vnet-name tradepanel-vnet \
  --name private-subnet \
  --address-prefix 10.0.10.0/24 \
  --service-endpoints Microsoft.Sql
```

#### Step 3: Create PostgreSQL Database

```bash
# Create Azure Database for PostgreSQL
az postgres server create \
  --resource-group tradepanel-rg \
  --name tradepanel-db \
  --location eastus \
  --admin-user postgresadmin \
  --admin-password <strong-password> \
  --sku-name B_Gen5_2 \
  --storage-size 51200 \
  --backup-retention 30 \
  --geo-redundant-backup Enabled \
  --ssl-enforcement Enabled \
  --minimal-tls-version TLS1_2

# Create firewall rule for Azure services
az postgres server firewall-rule create \
  --name allow-azure \
  --server-name tradepanel-db \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 0.0.0.0

# Create VNet rule
az postgres server vnet-rule create \
  --server-name tradepanel-db \
  --name allow-vnet \
  --subnet private-subnet \
  --vnet-name tradepanel-vnet
```

#### Step 4: Create App Service Plan

```bash
# Create App Service Plan
az appservice plan create \
  --name tradepanel-plan \
  --resource-group tradepanel-rg \
  --sku B2 \
  --is-linux

# Create Web App
az webapp create \
  --name tradepanel-app \
  --resource-group tradepanel-rg \
  --plan tradepanel-plan \
  --runtime "PYTHON|3.9" \
  --deployment-container-image-name-user tradepanel \
  --deployment-container-image-name <your-registry>.azurecr.io/tradepanel:latest

# Configure app settings
az webapp config appsettings set \
  --name tradepanel-app \
  --resource-group tradepanel-rg \
  --settings \
    DB_HOST=tradepanel-db.postgres.database.azure.com \
    DB_USER=postgresadmin@tradepanel-db \
    DB_PASSWORD=<password> \
    ENABLE_LOG=1
```

#### Step 5: Create Application Gateway

```bash
# Create public IP
az network public-ip create \
  --name tradepanel-pip \
  --sku Standard

# Create Application Gateway
az network application-gateway create \
  --name tradepanel-appgw \
  --location eastus \
  --public-ip-address tradepanel-pip \
  --vnet-name tradepanel-vnet \
  --subnet public-subnet \
  --capacity 2 \
  --sku Standard_v2 \
  --http-settings-cookie-based-affinity Enabled

# Configure backend pool
az network application-gateway address-pool create \
  --name tradepanel-backendpool \
  --gateway-name tradepanel-appgw \
  --servers tradepanel-app.azurewebsites.net
```

### Azure Cost Breakdown

```
┌────────────────────────────────────────┐
│     AZURE MONTHLY COST BREAKDOWN       │
├────────────────────────────────────────┤
│                                        │
│ App Service Plan (B2)                  │
│ ├─ Compute: $50/month                 │
│ ├─ 2 vCPU, 4GB RAM                    │
│ └─ Auto-scale: +$5/month              │
│                                        │
│ Azure Database for PostgreSQL          │
│ ├─ Compute (Gen5): $50/month          │
│ ├─ Storage: 100GB x $0.125/GB         │
│ ├─ Backup: $25/month                  │
│ ├─ Read replicas: 1 x $50/month       │
│ └─ ~$180/month                        │
│                                        │
│ Application Gateway                    │
│ ├─ Capacity units: 2 x $15/month      │
│ └─ ~$30/month                         │
│                                        │
│ Blob Storage                           │
│ ├─ Hot storage: 10GB x $0.018/GB      │
│ ├─ Transactions: 1M x $0.004/10K      │
│ └─ ~$5/month                          │
│                                        │
│ Azure Monitor                          │
│ ├─ Data ingestion: 10GB x $2.99/GB    │
│ ├─ Retention: 30 days                 │
│ └─ ~$15/month                         │
│                                        │
│ Data Transfer (Outbound)               │
│ ├─ 100GB egress x $0.12/GB            │
│ └─ ~$15/month                         │
│                                        │
│ ─────────────────────────────────────  │
│ TOTAL: ~$295/month                    │
│ (or ~$2.23 per trading day)           │
│                                        │
└────────────────────────────────────────┘
```

---

## 🎯 COST OPTIMIZATION TIPS

### General Optimization Strategies

```
1. COMPUTE OPTIMIZATION
   ├─ Use auto-scaling (scale down at night)
   ├─ Reserved instances (30% savings)
   ├─ Spot/Preemptible instances (70% cheaper)
   └─ Estimated savings: 30-40%

2. DATABASE OPTIMIZATION
   ├─ Use read replicas (query separation)
   ├─ Enable query optimization
   ├─ Implement connection pooling
   ├─ Archive old trading data
   └─ Estimated savings: 15-25%

3. STORAGE OPTIMIZATION
   ├─ Implement tiered storage
   ├─ Compress backups
   ├─ Archive data older than 90 days
   └─ Estimated savings: 20-30%

4. NETWORK OPTIMIZATION
   ├─ Use private endpoints (save egress)
   ├─ Implement caching (CDN)
   ├─ Compress API responses
   └─ Estimated savings: 25-35%

5. MONITORING OPTIMIZATION
   ├─ Sample logs (not all 100%)
   ├─ Aggregate metrics
   ├─ Set retention limits
   └─ Estimated savings: 40-50%
```

### By-Scale Optimization

**Small Scale ($57/month → $35/month)**
```
✓ Use free tier maximally
✓ Single zone database
✓ No redundancy
✓ Manual scaling
✓ Shared storage
```

**Medium Scale ($230/month → $150/month)**
```
✓ Reserved instances (1 year)
✓ Auto-scaling at off-hours
✓ Read replicas for reporting
✓ Implement caching
✓ Archive old data quarterly
```

**Enterprise Scale ($790/month → $550/month)**
```
✓ Reserved instances (3 years)
✓ Aggressive auto-scaling policies
✓ Multiple read replicas
✓ Advanced caching strategy
✓ Data archival to cheaper storage
✓ Spot instances for non-critical workloads
```

---

## 📊 PRICING COMPARISON SUMMARY

### Best Providers by Use Case

| Use Case | Best Provider | Reason | Savings |
|----------|---------------|--------|---------|
| **Startup/Testing** | Google Cloud | Free tier, low minimum spend | 40% vs AWS |
| **Growing Team** | Google Cloud | Best scaling model, excellent pricing | 25% vs AWS |
| **Enterprise** | Google Cloud | Advanced automation, highest reliability | 15% vs AWS |
| **Microsoft Stack** | Azure | If using .NET, Office 365, etc. | Better integration |
| **AWS Heavy Users** | AWS | Existing services, ecosystems | Commitment discounts |

---

**Next:** See 04_SECURITY_COMPLIANCE_GOVERNANCE.md for regulatory framework

💰 **Ready to deploy and minimize costs!**
