<template>
  <div class="space-y-8">
    <h2 class="text-2xl font-bold text-gray-900 mb-6">Docker & Deployment</h2>
    
    <!-- Docker Compose -->
    <div class="mb-8">
      <h3 class="text-xl font-semibold text-gray-900 mb-4">Docker Compose Configuration</h3>
      
      <div class="bg-gray-50 rounded p-4 mb-4">
        <p class="text-sm font-semibold mb-2">docker-compose.yml</p>
        <pre class="text-xs overflow-x-auto"><code>version: '3.8'

services:
  # Backend FastAPI
  backend:
    build: ./my-fastapi-app
    container_name: jira-sync-backend
    ports:
      - "8000:8000"
    environment:
      - MYSQL_HOST=mysql
      - MYSQL_USER=root
      - MYSQL_PASSWORD=rootpassword
      - MYSQL_DATABASE=jiradb
    volumes:
      - ./my-fastapi-app/backups:/app/backups
    depends_on:
      - mysql
    networks:
      - jira-sync-network

  # Frontend Vue
  frontend:
    build: ./front
    container_name: jira-sync-frontend
    ports:
      - "5173:5173"
    environment:
      - VITE_API_URL=http://localhost:8000
    depends_on:
      - backend
    networks:
      - jira-sync-network

  # MySQL Database
  mysql:
    image: mysql:8.0
    container_name: jira-sync-mysql
    environment:
      - MYSQL_ROOT_PASSWORD=rootpassword
      - MYSQL_DATABASE=jiradb
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
    networks:
      - jira-sync-network

volumes:
  mysql_data:

networks:
  jira-sync-network:
    driver: bridge</code></pre>
      </div>
    </div>

    <!-- Dockerfile Backend -->
    <div class="mb-8">
      <h3 class="text-xl font-semibold text-gray-900 mb-4">Dockerfile - Backend</h3>
      
      <div class="bg-gray-50 rounded p-4">
        <p class="text-sm font-semibold mb-2">my-fastapi-app/Dockerfile</p>
        <pre class="text-xs overflow-x-auto"><code>FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create backups directory
RUN mkdir -p /app/backups

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]</code></pre>
      </div>
    </div>

    <!-- Dockerfile Frontend -->
    <div class="mb-8">
      <h3 class="text-xl font-semibold text-gray-900 mb-4">Dockerfile - Frontend</h3>
      
      <div class="bg-gray-50 rounded p-4">
        <p class="text-sm font-semibold mb-2">front/Dockerfile</p>
        <pre class="text-xs overflow-x-auto"><code>FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./
RUN npm install

# Copy application
COPY . .

# Expose port
EXPOSE 5173

# Run development server
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]</code></pre>
      </div>
    </div>

    <!-- Deployment Commands -->
    <div class="mb-8">
      <h3 class="text-xl font-semibold text-gray-900 mb-4">Comandos de Deployment</h3>
      
      <div class="space-y-4">
        <div class="bg-gray-50 rounded p-4">
          <p class="text-sm font-semibold mb-2">Iniciar todos los servicios:</p>
          <pre class="text-sm"><code>docker-compose up -d</code></pre>
        </div>
        
        <div class="bg-gray-50 rounded p-4">
          <p class="text-sm font-semibold mb-2">Ver logs:</p>
          <pre class="text-sm"><code>docker-compose logs -f [service_name]</code></pre>
        </div>
        
        <div class="bg-gray-50 rounded p-4">
          <p class="text-sm font-semibold mb-2">Detener servicios:</p>
          <pre class="text-sm"><code>docker-compose down</code></pre>
        </div>
        
        <div class="bg-gray-50 rounded p-4">
          <p class="text-sm font-semibold mb-2">Reconstruir imágenes:</p>
          <pre class="text-sm"><code>docker-compose build --no-cache</code></pre>
        </div>
      </div>
    </div>

    <!-- Production Dockerfile -->
    <div class="mb-8">
      <h3 class="text-xl font-semibold text-gray-900 mb-4">Dockerfile de Producción - Frontend</h3>
      
      <div class="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-4">
        <p class="text-sm text-yellow-700">
          <strong>Tip:</strong> Para producción, usar build multi-stage para optimizar el tamaño de la imagen.
        </p>
      </div>
      
      <div class="bg-gray-50 rounded p-4">
        <p class="text-sm font-semibold mb-2">front/Dockerfile.prod</p>
        <pre class="text-xs overflow-x-auto"><code># Build stage
FROM node:18-alpine as build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Production stage
FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]</code></pre>
      </div>
    </div>

    <!-- Docker Commands Reference -->
    <div class="mb-8">
      <h3 class="text-xl font-semibold text-gray-900 mb-4">Referencia de Comandos Docker</h3>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="border rounded-lg p-4">
          <h4 class="font-semibold text-gray-900 mb-2">Gestión de Contenedores</h4>
          <ul class="text-sm space-y-1">
            <li><code class="bg-gray-100 px-1 rounded">docker ps</code> - Ver contenedores activos</li>
            <li><code class="bg-gray-100 px-1 rounded">docker ps -a</code> - Ver todos los contenedores</li>
            <li><code class="bg-gray-100 px-1 rounded">docker stop [container]</code> - Detener contenedor</li>
            <li><code class="bg-gray-100 px-1 rounded">docker rm [container]</code> - Eliminar contenedor</li>
            <li><code class="bg-gray-100 px-1 rounded">docker exec -it [container] bash</code> - Acceder al contenedor</li>
          </ul>
        </div>
        
        <div class="border rounded-lg p-4">
          <h4 class="font-semibold text-gray-900 mb-2">Gestión de Imágenes</h4>
          <ul class="text-sm space-y-1">
            <li><code class="bg-gray-100 px-1 rounded">docker images</code> - Ver imágenes locales</li>
            <li><code class="bg-gray-100 px-1 rounded">docker rmi [image]</code> - Eliminar imagen</li>
            <li><code class="bg-gray-100 px-1 rounded">docker build -t [tag] .</code> - Construir imagen</li>
            <li><code class="bg-gray-100 px-1 rounded">docker push [image]</code> - Subir imagen a registry</li>
            <li><code class="bg-gray-100 px-1 rounded">docker pull [image]</code> - Descargar imagen</li>
          </ul>
        </div>
      </div>
    </div>

    <!-- Kubernetes Deployment -->
    <div class="mb-8">
      <h3 class="text-xl font-semibold text-gray-900 mb-4">Deployment en Kubernetes (Opcional)</h3>
      
      <div class="bg-blue-50 border-l-4 border-blue-400 p-4 mb-4">
        <p class="text-sm text-blue-700">
          <strong>Info:</strong> Para escalar la aplicación, considera usar Kubernetes con los siguientes manifiestos.
        </p>
      </div>
      
      <div class="bg-gray-50 rounded p-4 mb-4">
        <p class="text-sm font-semibold mb-2">k8s/deployment.yaml</p>
        <pre class="text-xs overflow-x-auto"><code>apiVersion: apps/v1
kind: Deployment
metadata:
  name: jira-sync-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: jira-sync-backend
  template:
    metadata:
      labels:
        app: jira-sync-backend
    spec:
      containers:
      - name: backend
        image: your-registry/jira-sync-backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: MYSQL_HOST
          valueFrom:
            secretKeyRef:
              name: mysql-secret
              key: host
---
apiVersion: v1
kind: Service
metadata:
  name: jira-sync-backend-service
spec:
  selector:
    app: jira-sync-backend
  ports:
    - protocol: TCP
      port: 8000
      targetPort: 8000
  type: LoadBalancer</code></pre>
      </div>
    </div>

    <!-- CI/CD Pipeline -->
    <div>
      <h3 class="text-xl font-semibold text-gray-900 mb-4">CI/CD Pipeline (GitHub Actions)</h3>
      
      <div class="bg-gray-50 rounded p-4">
        <p class="text-sm font-semibold mb-2">.github/workflows/deploy.yml</p>
        <pre class="text-xs overflow-x-auto"><code>name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Build Docker images
      run: |
        docker build -t myapp-backend ./my-fastapi-app
        docker build -t myapp-frontend ./front
    
    - name: Login to Docker Hub
      uses: docker/login-action@v2
      with:
        username: "${DOCKER_USERNAME}"
        password: "${DOCKER_PASSWORD}"
    
    - name: Deploy to server
      uses: appleboy/ssh-action@v0.1.5
      with:
        host: "${HOST}"
        username: "${USERNAME}"
        key: "${SSH_KEY}"
        script: |
          cd /app
          docker-compose pull
          docker-compose up -d</code></pre>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Component logic for Docker Documentation
</script>

<style scoped>
code {
  @apply font-mono text-sm;
}

pre code {
  @apply block;
}
</style> 