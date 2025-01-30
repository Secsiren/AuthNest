# AuthNest
simple web app

# Task 1: Flask Web Application
Objective
Develop a Flask web application with user registration and login functionality, using SQLite for data storage.

Steps
Create the Flask Application:

Write app.py with routes for the home page, registration, and login.

Use render_template_string to render HTML templates directly in the code.

Initialize SQLite Database:

Create a users table with columns for id, username, and password.

Implement Password Hashing:

Use sha256 to hash passwords before storing them in the database.

Fix SQL Injection Vulnerability:

Replace vulnerable SQL queries with parameterized queries.

Set Debug Mode to False:

Ensure the Flask app runs in production mode (debug=False).

# Run the Flask application
python3 app.py
Task 2: Containerization with Docker
Objective
Containerize the Flask web application using Docker and Docker Compose.

Steps
Create a Dockerfile:

Use python:3.9-slim as the base image.

Install dependencies from requirements.txt.

Expose port 5000 for the Flask application.

Create a docker-compose.yml File:

Define services for the Flask app and SQLite database (later removed since SQLite is file-based).

Build and Run the Docker Container:

Build the Docker image and run the container.

# Build the Docker image
docker build -t flask-app .

# Run the Docker container
docker run -p 5000:5000 flask-app
Task 3: Infrastructure as Code (IaC)
Objective
Use Terraform to define and deploy cloud resources (VPC, subnet, EC2 instance, security group, and Elastic IP) on AWS.

Steps
Write Terraform Configuration:

Define resources for VPC, subnet, security group, EC2 instance, and Elastic IP.

Initialize and Apply Terraform:

Initialize Terraform and apply the configuration to create the resources.

Verify Deployment:

Check the outputs for the public IP address of the EC2 instance.

# Initialize Terraform
terraform init

# Apply the Terraform configuration
terraform apply
Task 4: CI/CD Pipeline with Cloud Integration
Objective
Create a CI/CD pipeline using GitHub Actions to build, push, and deploy the Flask application.

Steps
Create a GitHub Actions Workflow:

Define stages for building, pushing, and deploying the Docker image.

Configure Secrets:

Add Docker Hub credentials, EC2 host IP, and SSH key as secrets in GitHub.

Run the Pipeline:

Push changes to the main branch to trigger the pipeline.

# GitHub Actions workflow file (.github/workflows/cicd.yml)
name: CI/CD Pipeline

on:
  push:
    branches:
      - main

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Log in to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_HUB_USERNAME }}
          password: ${{ secrets.DOCKER_HUB_TOKEN }}

      - name: Build and tag Docker image
        run: |
          docker build -t your-dockerhub-username/authnest:latest -t your-dockerhub-username/authnest:$GITHUB_SHA .
          docker images

      - name: Push Docker image
        run: |
          docker push your-dockerhub-username/authnest:latest
          docker push your-dockerhub-username/authnest:$GITHUB_SHA

  deploy:
    runs-on: ubuntu-latest
    needs: build-and-push
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Deploy to EC2
        uses: appleboy/ssh-action@v0.1.10
        with:
          host: ${{ secrets.EC2_HOST }}
          username: ec2-user
          key: ${{ secrets.EC2_SSH_KEY }}
          script: |
            docker pull your-dockerhub-username/authnest:latest
            docker stop authnest || true
            docker rm authnest || true
            docker run -d --name authnest -p 5000:5000 your-dockerhub-username/authnest:latest
Task 5: Site Reliability Engineering (SRE)
Objective
Implement basic SRE principles by monitoring and ensuring the reliability of the deployed web application.

Steps
Set Up Prometheus:

Install and configure Prometheus to collect metrics from the Flask app and EC2 instance.

Set Up Grafana:

Install Grafana and connect it to Prometheus for visualization.

Configure Alerts:

Define alert rules for high CPU usage, high memory usage, and application downtime.

Implement Incident Response:

Create a runbook for resolving common issues.

# Install Prometheus
wget https://github.com/prometheus/prometheus/releases/download/v2.47.0/prometheus-2.47.0.linux-amd64.tar.gz
tar -xvf prometheus-2.47.0.linux-amd64.tar.gz
cd prometheus-2.47.0.linux-amd64
./prometheus --config.file=prometheus.yml

# Install Grafana
sudo apt-get install -y adduser libfontconfig1
wget https://dl.grafana.com/oss/release/grafana_10.1.5_amd64.deb
sudo dpkg -i grafana_10.1.5_amd64.deb
sudo systemctl start grafana-server
sudo systemctl enable grafana-server
Bonus Task: Ansible Configuration Management
Objective
Write an Ansible playbook to configure the EC2 instance with PostgreSQL, Nginx, and file permissions.

Steps
Create an Inventory File:

Define the EC2 instance as the target.

Write the Playbook:

Copy a file to /opt with specific permissions.

Install and configure PostgreSQL.

Install and configure Nginx.

Run the Playbook:

Execute the playbook to configure the EC2 instance.

# Inventory file (inventory)
[webserver]
34.233.102.110 ansible_user=ec2-user ansible_ssh_private_key_file=/path/to/your-key.pem

# Playbook (playbook.yml)
---
- name: Configure EC2 instance
  hosts: webserver
  become: yes
  tasks:
    - name: Ensure devops group exists
      group:
        name: devops
        state: present

    - name: Add ec2-user to devops group
      user:
        name: ec2-user
        groups: devops
        append: yes

    - name: Copy config.txt to /opt
      copy:
        src: config.txt
        dest: /opt/config.txt
        owner: ec2-user
        group: devops
        mode: '0660'

    - name: Install PostgreSQL
      yum:
        name: postgresql-server
        state: latest

    - name: Initialize PostgreSQL database
      command: postgresql-setup --initdb

    - name: Ensure PostgreSQL service is enabled and running
      service:
        name: postgresql
        state: started
        enabled: yes

    - name: Install Nginx
      yum:
        name: nginx
        state: latest

    - name: Ensure Nginx service is enabled and running
      service:
        name: nginx
        state: started
        enabled: yes

    - name: Allow HTTP traffic in firewall
      firewalld:
        service: http
        state: enabled
        permanent: yes
        immediate: yes

# Run the playbook
ansible-playbook -i inventory playbook.yml
Conclusion
This report covers the implementation of all tasks, including the Flask web application, Docker containerization, Terraform infrastructure, CI/CD pipeline, SRE monitoring, and Ansible configuration management. Each task is documented with the correct steps, commands, and brief descriptions.
