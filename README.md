# PyLoggerX

[![PyPI version](https://badge.fury.io/py/pyloggerx.svg)](https://badge.fury.io/py/pyloggerx)
[![Python](https://img.shields.io/pypi/pyversions/pyloggerx.svg)](https://pypi.org/project/pyloggerx/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Bibliothèque de logging moderne, colorée et riche en fonctionnalités pour Python avec logging structuré, tracking de performance et logging distant.**

PyLoggerX est un wrapper puissant qui étend le module logging standard de Python avec une sortie console élégante, du logging JSON structuré, une rotation automatique des logs, et du logging distant vers des services populaires comme Elasticsearch, Grafana Loki, Sentry, Datadog, et plus encore. Conçu pour les workflows DevOps modernes et les applications cloud-native.

---

## Table des Matières

- [Fonctionnalités](#fonctionnalités)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Intégration DevOps](#intégration-devops)
  - [Docker & Kubernetes](#docker--kubernetes)
  - [Pipelines CI/CD](#pipelines-cicd)
  - [Stack d'Observabilité](#stack-dobservabilité)
  - [Infrastructure as Code](#infrastructure-as-code)
- [Guide d'Utilisation Complet](#guide-dutilisation-complet)
- [Logging Distant](#logging-distant-v30)
- [Fonctionnalités Avancées](#fonctionnalités-avancées)
- [Référence de Configuration](#référence-de-configuration)
- [Configuration Avancée](#configuration-avancée)
  - [Chargement depuis Fichiers](#chargement-depuis-fichiers)
  - [Configuration par Variables d'Environnement](#configuration-par-variables-denvironnement)
  - [Configuration Multi-Sources](#configuration-multi-sources)
  - [Validation de Configuration](#validation-de-configuration)
  - [Configurations Prédéfinies](#configurations-prédéfinies)
- [Monitoring et Métriques](#monitoring-et-métriques)
  - [Collecteur de Métriques](#collecteur-de-métriques)
  - [Gestionnaire d'Alertes](#gestionnaire-dalertes)
  - [Monitoring de Santé](#monitoring-de-santé)
  - [Dashboard Console](#dashboard-console)
- [Intégrations Monitoring](#intégrations-monitoring)
  - [Prometheus](#intégration-prometheus)
  - [Grafana](#intégration-grafana)
  - [Custom Metrics](#métriques-personnalisées)
- [Exemples Complets](#exemples-complets)
- [Référence Config](#référence-config)
- [Exemples Réels](#exemples-réels)
- [Meilleures Pratiques](#meilleures-pratiques)
- [Référence API](#référence-api)
- [Tests](#tests)
- [Dépannage](#dépannage)
- [Contribution](#contribution)
- [Licence](#licence)

---

## Fonctionnalités

### Fonctionnalités Core
- **Sortie Console Colorée** - Logs console élégants avec indicateurs emoji
- **Logging JSON Structuré** - Export de logs en format JSON structuré
- **Rotation Automatique** - Rotation basée sur la taille et le temps
- **Tracking de Performance** - Chronométrage et monitoring intégrés
- **Zéro Configuration** - Fonctionne immédiatement avec des valeurs par défaut sensées
- **Hautement Configurable** - Options de personnalisation étendues
- **Enrichissement de Contexte** - Injection de métadonnées automatique
- **Formats de Sortie Multiples** - Console, JSON, texte

### Fonctionnalités DevOps & Cloud-Native
- **Compatible Conteneurs** - Logging structuré adapté aux conteneurs
- **Compatible Kubernetes** - Sortie JSON pour les log collectors
- **Intégration CI/CD** - Support pour GitHub Actions, GitLab CI, Jenkins
- **Support Correlation ID** - Pour le tracing distribué
- **Logging Health Check** - Monitoring de santé des services
- **Format Prêt pour les Métriques** - Sortie compatible avec Prometheus
- **Configuration par Environnement** - Adaptation automatique selon l'environnement
- **Conforme 12-Factor App** - Suit les meilleures pratiques

### Fonctionnalités Avancées
- **Logging Distant** - Export vers Elasticsearch, Loki, Sentry, Datadog
- **Échantillonnage de Logs** - Gestion efficace des scénarios à haut volume
- **Limitation de Débit** - Prévention de l'inondation de logs
- **Filtrage Avancé** - Filtres par niveau, pattern ou logique personnalisée
- **Traitement par Batch** - Batching efficace pour les exports distants
- **Support Webhook** - Envoi de logs vers des endpoints personnalisés
- **Intégration Slack** - Alertes critiques dans Slack
- **Processing Asynchrone** - Non-bloquant pour les performances

---

## Installation

### Installation Basique

```bash
pip install pyloggerx
```

### Dans requirements.txt

```text
pyloggerx>=1.0.0
```

### Dans pyproject.toml (Poetry)

```toml
[tool.poetry.dependencies]
pyloggerx = "^1.0.0"
```

### Avec Support de Logging Distant

```bash
# Pour Elasticsearch
pip install pyloggerx[elasticsearch]

# Pour Sentry
pip install pyloggerx[sentry]

# Pour tous les services distants
pip install pyloggerx[all]
```

### Installation Développement

```bash
git clone https://github.com/yourusername/pyloggerx.git
cd pyloggerx
pip install -e ".[dev]"
```

---

## Quick Start

### Usage Basique

```python
from pyloggerx import log

# Logging simple
log.info("Application démarrée")
log.warning("Ceci est un avertissement")
log.error("Une erreur s'est produite")
log.debug("Informations de debug")

# Avec contexte
log.info("Utilisateur connecté", user_id=123, ip="192.168.1.1")
```

### Instance de Logger Personnalisée

```python
from pyloggerx import PyLoggerX

logger = PyLoggerX(
    name="myapp",
    level="INFO",
    console=True,
    colors=True,
    json_file="logs/app.json",
    text_file="logs/app.log"
)

logger.info("Logger personnalisé initialisé")
```

### Logger avec Export Distant

```python
logger = PyLoggerX(
    name="production-app",
    console=True,
    json_file="logs/app.json",
    
    # Export vers Elasticsearch
    elasticsearch_url="http://localhost:9200",
    elasticsearch_index="myapp-logs",
    
    # Alertes Sentry pour les erreurs
    sentry_dsn="https://xxx@sentry.io/xxx",
    
    # Notifications Slack pour les critiques
    slack_webhook="https://hooks.slack.com/services/xxx"
)

logger.info("Application démarrée")
logger.error("Erreur critique")  # Envoyé à tous les services
```

---

## Intégration DevOps

### Docker & Kubernetes

#### Application Conteneurisée

```python
# app.py
import os
from pyloggerx import PyLoggerX

# Configuration pour environnement conteneur
logger = PyLoggerX(
    name=os.getenv("APP_NAME", "myapp"),
    level=os.getenv("LOG_LEVEL", "INFO"),
    console=True,  # Logs vers stdout pour les collecteurs
    colors=False,  # Désactiver les couleurs dans les conteneurs
    json_file=None,  # Utiliser stdout uniquement
    include_caller=True,
    enrichment_data={
        "environment": os.getenv("ENVIRONMENT", "production"),
        "pod_name": os.getenv("POD_NAME", "unknown"),
        "namespace": os.getenv("NAMESPACE", "default"),
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "region": os.getenv("AWS_REGION", "us-east-1")
    }
)

logger.info("Application démarrée", port=8080)
```

#### Dockerfile Optimisé

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Installation des dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Variables d'environnement pour logging
ENV LOG_LEVEL=INFO \
    APP_NAME=myapp \
    ENVIRONMENT=production \
    PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8080/health')"

# Exécution
CMD ["python", "app.py"]
```

#### Déploiement Kubernetes avec Logging

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  namespace: production
  labels:
    app: myapp
    version: v1
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
        version: v1
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8080"
    spec:
      containers:
      - name: myapp
        image: myapp:1.0.0
        env:
        - name: LOG_LEVEL
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: log-level
        - name: APP_NAME
          value: "myapp"
        - name: ENVIRONMENT
          value: "production"
        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace
        - name: APP_VERSION
          value: "1.0.0"
        - name: NODE_NAME
          valueFrom:
            fieldRef:
              fieldPath: spec.nodeName
        ports:
        - containerPort: 8080
          name: http
        # Probes avec logging
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: production
data:
  log-level: "INFO"
```

#### Sortie JSON pour Kubernetes (Fluentd/Filebeat)

```python
# Pour les collecteurs de logs Kubernetes
logger = PyLoggerX(
    name="k8s-app",
    console=True,
    colors=False,  # IMPORTANT: désactiver pour les collecteurs
    format_string='{"timestamp":"%(asctime)s","level":"%(levelname)s","logger":"%(name)s","message":"%(message)s"}',
    enrichment_data={
        "cluster": os.getenv("CLUSTER_NAME", "prod-cluster"),
        "pod_ip": os.getenv("POD_IP", "unknown")
    }
)

logger.info("Requête traitée", 
           duration_ms=123, 
           status_code=200,
           endpoint="/api/users")
```

### Pipelines CI/CD

#### GitHub Actions

```yaml
# .github/workflows/test-and-deploy.yml
name: Test, Build & Deploy

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  LOG_LEVEL: DEBUG
  APP_NAME: myapp

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11']
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Cache dependencies
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
      
      - name: Install dependencies
        run: |
          pip install -e .
          pip install pytest pytest-cov pytest-xdist
      
      - name: Run tests with logging
        run: |
          python -c "
          from pyloggerx import PyLoggerX
          import os
          
          logger = PyLoggerX(
              name='ci-tests',
              level='DEBUG',
              console=True,
              json_file='test-results/logs.json',
              enrichment_data={
                  'pipeline': 'github-actions',
                  'commit': '${{ github.sha }}',
                  'branch': '${{ github.ref_name }}',
                  'actor': '${{ github.actor }}',
                  'run_id': '${{ github.run_id }}',
                  'python_version': '${{ matrix.python-version }}'
              }
          )
          logger.info('Démarrage des tests CI')
          "
          pytest -n auto --cov=pyloggerx --cov-report=xml --cov-report=html
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml
      
      - name: Upload test logs
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: test-logs-${{ matrix.python-version }}
          path: test-results/
          retention-days: 30
  
  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2
      
      - name: Login to DockerHub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
      
      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: |
            myapp:latest
            myapp:${{ github.sha }}
          cache-from: type=registry,ref=myapp:buildcache
          cache-to: type=registry,ref=myapp:buildcache,mode=max
  
  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to Kubernetes
        run: |
          echo "${{ secrets.KUBECONFIG }}" > kubeconfig
          export KUBECONFIG=kubeconfig
          kubectl set image deployment/myapp myapp=myapp:${{ github.sha }} -n production
          kubectl rollout status deployment/myapp -n production
```

#### GitLab CI

```yaml
# .gitlab-ci.yml
variables:
  LOG_LEVEL: "DEBUG"
  APP_NAME: "myapp"
  DOCKER_DRIVER: overlay2
  DOCKER_TLS_CERTDIR: "/certs"

stages:
  - test
  - build
  - deploy
  - monitor

# Template pour logging
.logging_template: &logging_setup
  before_script:
    - |
      python -c "
      from pyloggerx import PyLoggerX
      import os
      
      logger = PyLoggerX(
          name='gitlab-ci',
          level=os.getenv('LOG_LEVEL', 'INFO'),
          console=True,
          json_file='logs/ci.json',
          enrichment_data={
              'pipeline_id': os.getenv('CI_PIPELINE_ID'),
              'job_id': os.getenv('CI_JOB_ID'),
              'commit_sha': os.getenv('CI_COMMIT_SHA'),
              'branch': os.getenv('CI_COMMIT_REF_NAME'),
              'runner': os.getenv('CI_RUNNER_DESCRIPTION'),
              'project': os.getenv('CI_PROJECT_NAME')
          }
      )
      logger.info('Job GitLab CI démarré')
      "

test:unit:
  stage: test
  image: python:3.11
  <<: *logging_setup
  script:
    - pip install -e .[dev]
    - pytest --cov=pyloggerx --cov-report=xml --cov-report=term
  coverage: '/TOTAL.*\s+(\d+%)$/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml
    paths:
      - logs/
      - htmlcov/
    expire_in: 1 week
  only:
    - merge_requests
    - main
    - develop

test:integration:
  stage: test
  image: python:3.11
  services:
    - postgres:14
    - redis:7
  variables:
    POSTGRES_DB: testdb
    POSTGRES_USER: testuser
    POSTGRES_PASSWORD: testpass
    REDIS_URL: redis://redis:6379
  script:
    - pip install -e .[dev]
    - pytest tests/integration/ -v
  only:
    - main
    - develop

build:docker:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker tag $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA $CI_REGISTRY_IMAGE:latest
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
    - docker push $CI_REGISTRY_IMAGE:latest
  only:
    - main

deploy:production:
  stage: deploy
  image: bitnami/kubectl:latest
  script:
    - kubectl config use-context production
    - kubectl set image deployment/myapp myapp=$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA -n production
    - kubectl rollout status deployment/myapp -n production
  environment:
    name: production
    url: https://myapp.example.com
  when: manual
  only:
    - main

monitor:health:
  stage: monitor
  image: curlimages/curl:latest
  script:
    - |
      for i in {1..5}; do
        STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://myapp.example.com/health)
        if [ "$STATUS" == "200" ]; then
          echo "Health check passed"
          exit 0
        fi
        echo "Attempt $i failed, retrying..."
        sleep 10
      done
      exit 1
  only:
    - main
```

#### Jenkins Pipeline

```groovy
// Jenkinsfile
pipeline {
    agent any
    
    environment {
        LOG_LEVEL = 'DEBUG'
        APP_NAME = 'myapp'
        ENVIRONMENT = 'staging'
        DOCKER_REGISTRY = 'registry.example.com'
        KUBE_NAMESPACE = 'production'
    }
    
    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timeout(time: 1, unit: 'HOURS')
        timestamps()
    }
    
    stages {
        stage('Setup') {
            steps {
                script {
                    sh '''
                        python3 -m venv venv
                        . venv/bin/activate
                        pip install -e .[dev]
                    '''
                }
            }
        }
        
        stage('Test') {
            parallel {
                stage('Unit Tests') {
                    steps {
                        script {
                            sh '''
                                . venv/bin/activate
                                python -c "
from pyloggerx import PyLoggerX
logger = PyLoggerX(
    name='jenkins-tests',
    json_file='logs/unit-tests.json',
    enrichment_data={
        'build_number': '${BUILD_NUMBER}',
        'job_name': '${JOB_NAME}',
        'node_name': '${NODE_NAME}'
    }
)
logger.info('Tests unitaires démarrés')
                                "
                                pytest tests/unit/ -v --junitxml=results/unit.xml
                            '''
                        }
                    }
                }
                
                stage('Integration Tests') {
                    steps {
                        script {
                            sh '''
                                . venv/bin/activate
                                pytest tests/integration/ -v --junitxml=results/integration.xml
                            '''
                        }
                    }
                }
            }
            post {
                always {
                    junit 'results/*.xml'
                }
            }
        }
        
        stage('Build') {
            steps {
                script {
                    docker.build("${DOCKER_REGISTRY}/${APP_NAME}:${BUILD_NUMBER}")
                }
            }
        }
        
        stage('Push') {
            steps {
                script {
                    docker.withRegistry("https://${DOCKER_REGISTRY}", 'docker-credentials') {
                        docker.image("${DOCKER_REGISTRY}/${APP_NAME}:${BUILD_NUMBER}").push()
                        docker.image("${DOCKER_REGISTRY}/${APP_NAME}:${BUILD_NUMBER}").push('latest')
                    }
                }
            }
        }
        
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                script {
                    withKubeConfig([credentialsId: 'kube-config']) {
                        sh """
                            kubectl set image deployment/${APP_NAME} \
                                ${APP_NAME}=${DOCKER_REGISTRY}/${APP_NAME}:${BUILD_NUMBER} \
                                -n ${KUBE_NAMESPACE}
                            kubectl rollout status deployment/${APP_NAME} -n ${KUBE_NAMESPACE}
                        """
                    }
                }
            }
        }
        
        stage('Smoke Tests') {
            when {
                branch 'main'
            }
            steps {
                script {
                    sh '''
                        for i in {1..5}; do
                            if curl -f https://myapp.example.com/health; then
                                echo "Smoke test passed"
                                exit 0
                            fi
                            sleep 10
                        done
                        exit 1
                    '''
                }
            }
        }
    }
    
    post {
        always {
            archiveArtifacts artifacts: 'logs/*.json', allowEmptyArchive: true
            cleanWs()
        }
        success {
            slackSend(
                color: 'good',
                message: "Build #${BUILD_NUMBER} succeeded for ${JOB_NAME}"
            )
        }
        failure {
            slackSend(
                color: 'danger',
                message: "Build #${BUILD_NUMBER} failed for ${JOB_NAME}"
            )
        }
    }
}
```

### Stack d'Observabilité

#### ELK Stack (Elasticsearch, Logstash, Kibana)

```python
# Configuration pour ELK
from pyloggerx import PyLoggerX
import socket
import os

logger = PyLoggerX(
    name="elk-app",
    console=True,
    json_file="/var/log/myapp/app.json",  # Filebeat surveille ce fichier
    colors=False,
    
    # Export direct vers Elasticsearch
    elasticsearch_url="http://elasticsearch:9200",
    elasticsearch_index="myapp-logs",
    elasticsearch_username=os.getenv("ES_USERNAME"),
    elasticsearch_password=os.getenv("ES_PASSWORD"),
    
    enrichment_data={
        "service": "payment-api",
        "environment": os.getenv("ENVIRONMENT", "production"),
        "hostname": socket.gethostname(),
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "datacenter": os.getenv("DATACENTER", "us-east-1")
    }
)

# Les logs sont envoyés à Elasticsearch et écrits dans un fichier
logger.info("Paiement traité", 
           transaction_id="txn_123",
           amount=99.99,
           currency="USD",
           customer_id="cust_456",
           payment_method="card")
```

**Configuration Filebeat** (`filebeat.yml`):

```yaml
filebeat.inputs:
- type: log
  enabled: true
  paths:
    - /var/log/myapp/*.json
  json.keys_under_root: true
  json.add_error_key: true
  json.message_key: message
  fields:
    service: myapp
    environment: production
  fields_under_root: true

processors:
  - add_host_metadata:
      when.not.contains.tags: forwarded
  - add_cloud_metadata: ~
  - add_docker_metadata: ~
  - add_kubernetes_metadata: ~

output.elasticsearch:
  hosts: ["elasticsearch:9200"]
  index: "myapp-logs-%{+yyyy.MM.dd}"
  username: "${ES_USERNAME}"
  password: "${ES_PASSWORD}"
  ssl.verification_mode: none

setup.kibana:
  host: "kibana:5601"

setup.ilm.enabled: true
setup.ilm.rollover_alias: "myapp-logs"
setup.ilm.pattern: "{now/d}-000001"

logging.level: info
logging.to_files: true
logging.files:
  path: /var/log/filebeat
  name: filebeat
  keepfiles: 7
  permissions: 0644
```

#### Prometheus & Grafana

```python
from pyloggerx import PyLoggerX
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time
import functools

# Métriques Prometheus
request_counter = Counter(
    'http_requests_total', 
    'Total HTTP requests', 
    ['method', 'endpoint', 'status']
)
request_duration = Histogram(
    'http_request_duration_seconds', 
    'HTTP request duration',
    ['method', 'endpoint']
)
active_requests = Gauge(
    'http_requests_active',
    'Active HTTP requests'
)
error_counter = Counter(
    'application_errors_total',
    'Total application errors',
    ['error_type']
)

logger = PyLoggerX(
    name="metrics-app",
    json_file="logs/metrics.json",
    performance_tracking=True,
    
    # Export vers services de monitoring
    datadog_api_key=os.getenv("DATADOG_API_KEY"),
    
    enrichment_data={
        "service": "api-gateway",
        "version": "2.0.0"
    }
)

def monitor_request(func):
    """Décorateur pour monitorer les requêtes"""
    @functools.wraps(func)
    def wrapper(method, endpoint, *args, **kwargs):
        active_requests.inc()
        start_time = time.time()
        
        logger.info("Requête reçue", 
                   method=method, 
                   endpoint=endpoint)
        
        try:
            result = func(method, endpoint, *args, **kwargs)
            duration = time.time() - start_time
            
            # Mettre à jour les métriques
            request_counter.labels(
                method=method,
                endpoint=endpoint,
                status=200
            ).inc()
            request_duration.labels(
                method=method,
                endpoint=endpoint
            ).observe(duration)
            
            logger.info("Requête complétée",
                       method=method,
                       endpoint=endpoint,
                       status=200,
                       duration_ms=duration*1000)
            
            return result
            
        except Exception as e:
            duration = time.time() - start_time
            error_type = type(e).__name__
            
            request_counter.labels(
                method=method,
                endpoint=endpoint,
                status=500
            ).inc()
            error_counter.labels(error_type=error_type).inc()
            
            logger.error("Requête échouée",
                        method=method,
                        endpoint=endpoint,
                        status=500,
                        duration_ms=duration*1000,
                        error=str(e),
                        error_type=error_type)
            raise
        finally:
            active_requests.dec()
    
    return wrapper

@monitor_request
def handle_request(method, endpoint, data=None):
    # Logique de traitement
    time.sleep(0.1)  # Simulation
    return {"status": "success"}

# Démarrer le serveur de métriques Prometheus
start_http_server(8000)
logger.info("Serveur de métriques démarré", port=8000)

# Endpoint de métriques custom
def get_performance_metrics():
    stats = logger.get_performance_stats()
    return {
        "logging": {
            "total_logs": stats.get("total_operations", 0),
            "avg_duration": stats.get("avg_duration", 0),
            "max_duration": stats.get("max_duration", 0)
        },
        "requests": {
            "total": request_counter._value.sum(),
            "active": active_requests._value.get()
        }
    }
```

#### OpenTelemetry Integration

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from pyloggerx import PyLoggerX
import os

# Setup OpenTelemetry
resource = Resource.create({
    "service.name": "myapp",
    "service.version": "1.0.0",
    "deployment.environment": os.getenv("ENVIRONMENT", "production")
})

trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)

# Export vers OTLP collector
otlp_exporter = OTLPSpanExporter(
    endpoint="http://otel-collector:4317",
    insecure=True
)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

logger = PyLoggerX(
    name="otel-app",
    json_file="logs/traces.json",
    enrichment_data={
        "service": "order-service"
    }
)

def process_order(order_id):
    """Traiter une commande avec tracing distribué"""
    with tracer.start_as_current_span("process_order") as span:
        span.set_attribute("order.id", order_id)
        
        # Récupérer le contexte de trace
        ctx = span.get_span_context()
        trace_id = format(ctx.trace_id, '032x')
        span_id = format(ctx.span_id, '016x')
        
        logger.info("Traitement de la commande",
                   order_id=order_id,
                   trace_id=trace_id,
                   span_id=span_id)
        
        # Étapes de traitement avec spans
        validate_order(order_id, trace_id, span_id)
        charge_payment(order_id, trace_id, span_id)
        ship_order(order_id, trace_id, span_id)
        
        logger.info("Commande complétée",
                   order_id=order_id,
                   trace_id=trace_id,
                   span_id=span_id)

def validate_order(order_id, trace_id, span_id):
    with tracer.start_as_current_span("validate_order"):
        logger.debug("Validation de la commande",
                    order_id=order_id,
                    trace_id=trace_id,
                    span_id=span_id)
        # Logique de validation
        time.sleep(0.1)

def charge_payment(order_id, trace_id, span_id):
    with tracer.start_as_current_span("charge_payment"):
        logger.info("Traitement du paiement",
                   order_id=order_id,
                   trace_id=trace_id,
                   span_id=span_id)
        # Logique de paiement
        time.sleep(0.2)

def ship_order(order_id, trace_id, span_id):
    with tracer.start_as_current_span("ship_order"):
        logger.info("Expédition de la commande",
                   order_id=order_id,
                   trace_id=trace_id,
                   span_id=span_id)
        # Logique d'expédition
        time.sleep(0.15)
```

#### Grafana Loki Integration

```python
from pyloggerx import PyLoggerX
import os

logger = PyLoggerX(
    name="loki-app",
    console=True,
    
    # Export direct vers Loki
    loki_url="http://loki:3100",
    loki_labels={
        "app": "payment-service",
        "environment": os.getenv("ENVIRONMENT", "production"),
        "region": os.getenv("AWS_REGION", "us-east-1"),
        "version": os.getenv("APP_VERSION", "1.0.0")
    },
    
    enrichment_data={
        "service": "payment-api",
        "instance": os.getenv("HOSTNAME", "unknown")
    }
)

# Les logs sont automatiquement envoyés à Loki
logger.info("Paiement initié", 
           transaction_id="txn_789",
           amount=150.00,
           currency="EUR")

logger.info("Paiement complété",
           transaction_id="txn_789",
           status="success",
           processing_time_ms=234)
```

**Configuration Promtail** (`promtail-config.yml`):

```yaml
server:
  http_listen_port: 9080
  grpc_listen_port: 0

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://loki:3100/loki/api/v1/push

scrape_configs:
  - job_name: system
    static_configs:
      - targets:
          - localhost
        labels:
          job: varlogs
          __path__: /var/log/*log

  - job_name: containers
    docker_sd_configs:
      - host: unix:///var/run/docker.sock
        refresh_interval: 5s
    relabel_configs:
      - source_labels: ['__meta_docker_container_name']
        regex: '/(.*)'
        target_label: 'container'
      - source_labels: ['__meta_docker_container_log_stream']
        target_label: 'logstream'
      - source_labels: ['__meta_docker_container_label_logging_jobname']
        target_label: 'job'
```

### Infrastructure as Code

#### Terraform avec Logging

```python
# terraform_deploy.py
from pyloggerx import PyLoggerX
import subprocess
import json
import sys

logger = PyLoggerX(
    name="terraform",
    console=True,
    json_file="logs/terraform.json",
    performance_tracking=True,
    
    # Notifications Slack pour les déploiements
    slack_webhook=os.getenv("SLACK_WEBHOOK"),
    
    enrichment_data={
        "tool": "terraform",
        "workspace": os.getenv("TF_WORKSPACE", "default")
    }
)

def run_terraform_command(command, **kwargs):
    """Exécuter une commande Terraform avec logging"""
    logger.info(f"Exécution: terraform {command}", **kwargs)
    
    result = subprocess.run(
        ["terraform"] + command.split(),
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        logger.info(f"Commande réussie: terraform {command}")
    else:
        logger.error(f"Commande échouée: terraform {command}",
                    stderr=result.stderr,
                    returncode=result.returncode)
    
    return result

def terraform_deploy(workspace="production", auto_approve=False):
    """Déploiement Terraform complet avec logging détaillé"""
    logger.info("Déploiement Terraform démarré", 
               workspace=workspace,
               auto_approve=auto_approve)
    
    try:
        # Init
        with logger.timer("Terraform Init"):
            result = run_terraform_command("init -upgrade")
            if result.returncode != 0:
                raise Exception("Terraform init failed")
        
        # Workspace
        if workspace != "default":
            with logger.timer("Terraform Workspace"):
                run_terraform_command(f"workspace select {workspace}")
        
        # Plan
        with logger.timer("Terraform Plan"):
            result = run_terraform_command("plan -out=tfplan -json")
            
            # Parser la sortie JSON
            changes = {"add": 0, "change": 0, "destroy": 0}
            for line in result.stdout.split('\n'):
                if line.strip():
                    try:
                        data = json.loads(line)
                        if data.get("type") == "change_summary":
                            changes = data.get("changes", changes)
                    except:
                        pass
            
            logger.info("Plan Terraform terminé",
                       resources_to_add=changes["add"],
                       resources_to_change=changes["change"],
                       resources_to_destroy=changes["destroy"])
            
            # Alerte si destruction de ressources
            if changes["destroy"] > 0:
                logger.warning("Destruction de ressources détectée",
                             count=changes["destroy"])
        
        # Apply
        apply_cmd = "apply tfplan"
        if auto_approve:
            apply_cmd += " -auto-approve"
        
        with logger.timer("Terraform Apply"):
            result = run_terraform_command(apply_cmd)
            
            if result.returncode == 0:
                logger.info("Déploiement Terraform réussi")
            else:
                logger.error("Déploiement Terraform échoué",
                           returncode=result.returncode)
                sys.exit(1)
        
        # Statistiques finales
        stats = logger.get_performance_stats()
        logger.info("Déploiement complété",
                   total_duration=stats["total_duration"],
                   avg_duration=stats["avg_duration"])
        
    except Exception as e:
        logger.exception("Erreur lors du déploiement Terraform",
                        error=str(e))
        sys.exit(1)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", default="production")
    parser.add_argument("--auto-approve", action="store_true")
    args = parser.parse_args()
    
    terraform_deploy(args.workspace, args.auto_approve)
```

#### Ansible avec Logging

```python
# ansible_playbook.py
from pyloggerx import PyLoggerX
import subprocess
import json
from datetime import datetime
import os

logger = PyLoggerX(
    name="ansible",
    json_file="logs/ansible.json",
    
    # Export vers Elasticsearch pour analyse
    elasticsearch_url=os.getenv("ES_URL"),
    elasticsearch_index="ansible-logs",
    
    enrichment_data={
        "automation": "ansible",
        "run_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "user": os.getenv("USER")
    }
)

def run_playbook(playbook_path, inventory="hosts.ini", extra_vars=None, tags=None):
    """Exécuter un playbook Ansible avec logging détaillé"""
    logger.info("Playbook Ansible démarré",
               playbook=playbook_path,
               inventory=inventory,
               extra_vars=extra_vars,
               tags=tags)
    
    cmd = [
        "ansible-playbook",
        playbook_path,
        "-i", inventory,
        "-v"  # Verbosité
    ]
    
    if extra_vars:
        cmd.extend(["--extra-vars", json.dumps(extra_vars)])
    
    if tags:
        cmd.extend(["--tags", tags])
    
    # Exécution avec capture de sortie
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )
    
    # Parser la sortie Ansible
    stats = parse_ansible_output(result.stdout)
    
    # Logger les résultats
    if stats:
        logger.info("Playbook Ansible terminé",
                   hosts_processed=len(stats),
                   total_ok=sum(s.get("ok", 0) for s in stats.values()),
                   total_changed=sum(s.get("changed", 0) for s in stats.values()),
                   total_failed=sum(s.get("failures", 0) for s in stats.values()),
                   total_unreachable=sum(s.get("unreachable", 0) for s in stats.values()))
        
        # Logger par hôte
        for host, host_stats in stats.items():
            logger.debug("Statistiques par hôte",
                        host=host,
                        ok=host_stats.get("ok", 0),
                        changed=host_stats.get("changed", 0),
                        failed=host_stats.get("failures", 0))
    
    if result.returncode != 0:
        logger.error("Playbook Ansible échoué",
                    returncode=result.returncode,
                    stderr=result.stderr)
        return False
    
    return True

def parse_ansible_output(output):
    """Parser la sortie Ansible"""
    stats = {}
    in_recap = False
    
    for line in output.split('\n'):
        if "PLAY RECAP" in line:
            in_recap = True
            continue
        
        if in_recap and ":" in line:
            parts = line.split(":")
            if len(parts) >= 2:
                host = parts[0].strip()
                stats_str = parts[1].strip()
                
                # Parser les statistiques
                host_stats = {}
                for stat in stats_str.split():
                    if "=" in stat:
                        key, value = stat.split("=")
                        try:
                            host_stats[key] = int(value)
                        except:
                            pass
                
                stats[host] = host_stats
    
    return stats

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("playbook", help="Chemin du playbook")
    parser.add_argument("-i", "--inventory", default="hosts.ini")
    parser.add_argument("-e", "--extra-vars", help="Variables supplémentaires (JSON)")
    parser.add_argument("-t", "--tags", help="Tags à exécuter")
    args = parser.parse_args()
    
    extra_vars = json.loads(args.extra_vars) if args.extra_vars else None
    
    success = run_playbook(
        args.playbook,
        inventory=args.inventory,
        extra_vars=extra_vars,
        tags=args.tags
    )
    
    sys.exit(0 if success else 1)
```

#### AWS CDK avec Logging

```python
# cdk_app.py
from aws_cdk import (
    App, Stack, Duration,
    aws_lambda as lambda_,
    aws_apigateway as apigw,
    aws_dynamodb as dynamodb,
    aws_logs as logs
)
from pyloggerx import PyLoggerX
import os

logger = PyLoggerX(
    name="cdk-deploy",
    json_file="logs/cdk.json",
    
    enrichment_data={
        "tool": "aws-cdk",
        "account": os.getenv("CDK_DEFAULT_ACCOUNT"),
        "region": os.getenv("CDK_DEFAULT_REGION", "us-east-1")
    }
)

class MyApplicationStack(Stack):
    def __init__(self, scope, id, **kwargs):
        super().__init__(scope, id, **kwargs)
        
        logger.info("Création du stack CDK", stack_name=id)
        
        # DynamoDB Table
        logger.info("Création de la table DynamoDB")
        table = dynamodb.Table(
            self, "DataTable",
            partition_key=dynamodb.Attribute(
                name="id",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY
        )
        logger.info("Table DynamoDB créée", table_name=table.table_name)
        
        # Lambda Function
        logger.info("Création de la fonction Lambda")
        lambda_fn = lambda_.Function(
            self, "ApiHandler",
            runtime=lambda_.Runtime.PYTHON_3_11,
            handler="index.handler",
            code=lambda_.Code.from_asset("lambda"),
            environment={
                "TABLE_NAME": table.table_name,
                "LOG_LEVEL": "INFO"
            },
            timeout=Duration.seconds(30),
            memory_size=256,
            log_retention=logs.RetentionDays.ONE_WEEK
        )
        
        # Permissions
        table.grant_read_write_data(lambda_fn)
        
        logger.info("Fonction Lambda créée",
                   function_name=lambda_fn.function_name)
        
        # API Gateway
        logger.info("Création de l'API Gateway")
        api = apigw.LambdaRestApi(
            self, "ApiGateway",
            handler=lambda_fn,
            proxy=False,
            deploy_options=apigw.StageOptions(
                logging_level=apigw.MethodLoggingLevel.INFO,
                data_trace_enabled=True,
                metrics_enabled=True
            )
        )
        
        # Endpoints
        items = api.root.add_resource("items")
        items.add_method("GET")
        items.add_method("POST")
        
        item = items.add_resource("{id}")
        item.add_method("GET")
        item.add_method("PUT")
        item.add_method("DELETE")
        
        logger.info("API Gateway créée",
                   api_id=api.rest_api_id,
                   api_url=api.url)

def main():
    app = App()
    
    logger.info("Synthèse CDK démarrée")
    
    # Créer les stacks
    MyApplicationStack(
        app, "MyApp-Dev",
        env={
            "account": os.getenv("CDK_DEFAULT_ACCOUNT"),
            "region": "us-east-1"
        }
    )
    
    MyApplicationStack(
        app, "MyApp-Prod",
        env={
            "account": os.getenv("CDK_DEFAULT_ACCOUNT"),
            "region": "us-west-2"
        }
    )
    
    logger.info("Synthèse CDK complétée")
    
    # Synthétiser l'application
    app.synth()

if __name__ == "__main__":
    main()
```

---

## Guide d'Utilisation Complet

### 1. Console Logging

```python
from pyloggerx import PyLoggerX

logger = PyLoggerX(
    name="console_app",
    console=True,
    colors=True
)

logger.debug("Message de debug")      
logger.info("Message d'info")         
logger.warning("Message d'avertissement")  
logger.error("Message d'erreur")      
logger.critical("Message critique")  
```

### 2. Logging vers Fichiers

#### JSON Structuré

```python
logger = PyLoggerX(
    name="json_logger",
    json_file="logs/app.json",
    max_bytes=10 * 1024 * 1024,  # 10MB
    backup_count=5
)

logger.info("Action utilisateur",
    user_id=123,
    action="login",
    ip="192.168.1.1",
    user_agent="Mozilla/5.0"
)
```

**Sortie** (`logs/app.json`):
```json
{
  "timestamp": "2025-01-15T10:30:45.123456",
  "level": "INFO",
  "logger": "json_logger",
  "message": "Action utilisateur",
  "module": "main",
  "function": "login_handler",
  "user_id": 123,
  "action": "login",
  "ip": "192.168.1.1",
  "user_agent": "Mozilla/5.0"
}
```

#### Fichier Texte

```python
logger = PyLoggerX(
    name="text_logger",
    text_file="logs/app.log",
    format_string="%(asctime)s - %(levelname)s - %(message)s"
)
```

#### Rotation Basée sur le Temps

```python
logger = PyLoggerX(
    name="timed_logger",
    text_file="logs/app.log",
    rotation_when="midnight",  # Rotation à minuit
    rotation_interval=1,  # Chaque jour
    backup_count=7  # Garder 7 jours
)

# Options pour rotation_when:
# "S": Secondes
# "M": Minutes
# "H": Heures
# "D": Jours
# "midnight": À minuit
# "W0"-"W6": Jour de la semaine (0=Lundi)
```

### 3. Tracking de Performance

```python
logger = PyLoggerX(
    name="perf_logger",
    performance_tracking=True
)

# Utilisation du context manager
with logger.timer("Requête Base de Données"):
    result = db.query("SELECT * FROM users WHERE active = true")

# Chronométrage manuel
import time
start = time.time()
process_large_dataset(data)
duration = time.time() - start

logger.info("Traitement complété",
           duration_seconds=duration,
           records_processed=len(data))

# Récupérer les statistiques
stats = logger.get_performance_stats()
print(f"Moyenne: {stats['avg_duration']:.3f}s")
print(f"Maximum: {stats['max_duration']:.3f}s")
print(f"Total opérations: {stats['total_operations']}")
```

---

## Logging Distant

### Elasticsearch

```python
logger = PyLoggerX(
    name="es_logger",
    elasticsearch_url="http://elasticsearch:9200",
    elasticsearch_index="myapp-logs",
    elasticsearch_username="elastic",
    elasticsearch_password="changeme",
    batch_size=100,  # Taille du batch
    batch_timeout=5  # Timeout en secondes
)

logger.info("Log envoyé vers Elasticsearch",
           service="api",
           environment="production",
           request_id="req_123")
```

### Grafana Loki

```python
logger = PyLoggerX(
    name="loki_logger",
    loki_url="http://loki:3100",
    loki_labels={
        "app": "myapp",
        "environment": "production",
        "region": "us-east-1",
        "tier": "backend"
    }
)

logger.info("Log envoyé vers Loki",
           endpoint="/api/users",
           method="GET",
           status_code=200)
```

### Sentry (Error Tracking)

```python
logger = PyLoggerX(
    name="sentry_logger",
    sentry_dsn="https://examplePublicKey@o0.ingest.sentry.io/0",
    sentry_environment="production",
    sentry_release="myapp@1.0.0"
)

# Seuls les erreurs et critiques sont envoyés à Sentry
logger.error("Échec du traitement du paiement",
            user_id=123,
            amount=99.99,
            error_code="PAYMENT_DECLINED",
            card_type="visa")
```

### Datadog

```python
logger = PyLoggerX(
    name="datadog_logger",
    datadog_api_key="your_datadog_api_key",
    datadog_site="datadoghq.com",  # ou datadoghq.eu
    datadog_service="web-api",
    datadog_tags=["env:prod", "version:1.0.0"]
)

logger.info("Log Datadog",
           service="web-api",
           env="prod",
           metric="request.duration",
           value=234)
```

### Slack Notifications

```python
logger = PyLoggerX(
    name="slack_logger",
    slack_webhook="https://hooks.slack.com/services/YOUR/WEBHOOK/URL",
    slack_channel="#alerts",
    slack_username="PyLoggerX Bot"
)

# Seuls les warnings et au-dessus sont envoyés à Slack
logger.warning("Utilisation mémoire élevée",
              memory_percent=95,
              hostname="server-01")

logger.error("Service indisponible",
            service="payment-api",
            error="Connection timeout")
```

### Webhook Personnalisé

```python
logger = PyLoggerX(
    name="webhook_logger",
    webhook_url="https://your-api.com/logs",
    webhook_method="POST",
    webhook_headers={
        "Authorization": "Bearer YOUR_TOKEN",
        "Content-Type": "application/json"
    }
)

logger.info("Log webhook personnalisé",
           custom_field="value")
```

### Configuration Multi-Services

```python
logger = PyLoggerX(
    name="multi_logger",
    
    # Console et fichiers locaux
    console=True,
    json_file="logs/app.json",
    
    # Elasticsearch pour tous les logs
    elasticsearch_url="http://elasticsearch:9200",
    elasticsearch_index="myapp-logs",
    
    # Loki pour le streaming
    loki_url="http://loki:3100",
    loki_labels={"app": "myapp", "env": "prod"},
    
    # Sentry pour les erreurs
    sentry_dsn="https://xxx@sentry.io/xxx",
    
    # Slack pour les alertes critiques
    slack_webhook="https://hooks.slack.com/services/xxx",
    
    # Datadog pour les métriques
    datadog_api_key="your_api_key",
    
    # Configuration des batchs
    batch_size=100,
    batch_timeout=5
)

# Ce log ira partout sauf Slack (niveau trop bas)
logger.info("Application démarrée")

# Ce log ira partout y compris Slack
logger.error("Erreur critique détectée", 
            component="database",
            error="Connection pool exhausted")
```

---

## Fonctionnalités Avancées

### 1. Filtrage Avancé

#### Filtrage par Niveau

```python
from pyloggerx import PyLoggerX
from pyloggerx.filters import LevelFilter

logger = PyLoggerX(name="filtered_logger")

# Garder seulement WARNING et ERROR
level_filter = LevelFilter(min_level="WARNING", max_level="ERROR")
logger.add_filter(level_filter)

logger.debug("Ceci ne sera pas loggé")
logger.warning("Ceci sera loggé")
logger.error("Ceci sera loggé")
logger.critical("Ceci ne sera pas loggé (au-dessus de ERROR)")
```

#### Filtrage par Pattern

```python
from pyloggerx.filters import MessageFilter

# Inclure seulement les messages correspondant au pattern
include_filter = MessageFilter(pattern="user_.*", exclude=False)
logger.add_filter(include_filter)

# Exclure les messages correspondant au pattern
exclude_filter = MessageFilter(pattern="debug_.*", exclude=True)
logger.add_filter(exclude_filter)
```

#### Limitation de Débit (Rate Limiting)

```python
from pyloggerx.filters import RateLimitFilter

# Maximum 100 logs par minute
rate_limiter = RateLimitFilter(max_logs=100, period=60)
logger.add_filter(rate_limiter)

# Utile pour les boucles à haut volume
for i in range(10000):
    logger.debug(f"Traitement de l'item {i}")
    # Seuls ~100 logs seront émis
```

#### Filtre Personnalisé

```python
import logging

class CustomFilter(logging.Filter):
    def filter(self, record):
        # Logique personnalisée
        # Retourne True pour garder le log, False pour l'ignorer
        
        # Exemple: garder seulement les logs d'un module spécifique
        if record.module != "payment_processor":
            return False
        
        # Exemple: ignorer les logs contenant des données sensibles
        if hasattr(record, 'password') or hasattr(record, 'ssn'):
            return False
        
        return True

logger.add_filter(CustomFilter())
```

### 2. Échantillonnage de Logs (Log Sampling)

Pour les applications à haut volume, l'échantillonnage réduit le volume de logs:

```python
logger = PyLoggerX(
    name="sampled_logger",
    enable_sampling=True,
    sampling_rate=0.1  # Garder seulement 10% des logs
)

# Utile pour les logs de debug en production
for i in range(10000):
    logger.debug(f"Traitement de l'item {i}")
    # Environ 1000 seront loggés

# Les logs ERROR et CRITICAL ne sont jamais échantillonnés
logger.error("Erreur importante")  # Toujours loggé
```

#### Échantillonnage Adaptatif

```python
from pyloggerx.sampling import AdaptiveSampler

logger = PyLoggerX(
    name="adaptive_logger",
    enable_sampling=True,
    sampler=AdaptiveSampler(
        base_rate=0.1,  # Taux de base 10%
        error_rate=1.0,  # 100% pour les erreurs
        spike_threshold=1000,  # Détection de pic
        spike_rate=0.01  # 1% pendant les pics
    )
)
```

### 3. Enrichissement de Contexte

```python
logger = PyLoggerX(name="enriched_logger")

# Ajouter un contexte global
logger.add_enrichment(
    app_version="2.0.0",
    environment="production",
    hostname=socket.gethostname(),
    region="us-east-1",
    datacenter="dc1"
)

# Tous les logs suivants incluront ces données
logger.info("Utilisateur connecté", user_id=123)
# Output: {..., "app_version": "2.0.0", "environment": "production", ..., "user_id": 123}

# Enrichissement dynamique par requête
with logger.context(request_id="req_789", user_id=456):
    logger.info("Traitement de la requête")
    # Ce log inclut request_id et user_id
    
    process_request()
    
    logger.info("Requête complétée")
    # Ce log inclut aussi request_id et user_id

# Hors du contexte
logger.info("Log suivant")
# Ce log n'inclut plus request_id et user_id
```

### 4. Gestion des Exceptions

```python
try:
    result = risky_operation()
except ValueError as e:
    logger.exception("Opération risquée échouée",
                    operation="data_validation",
                    input_value=user_input,
                    error_type=type(e).__name__)
    # Inclut automatiquement la stack trace complète

except Exception as e:
    logger.error("Erreur inattendue",
                operation="data_validation",
                error=str(e),
                exc_info=True)  # Inclut la traceback sans exception()
```

### 5. Niveaux de Log Dynamiques

```python
logger = PyLoggerX(name="dynamic_logger", level="INFO")

# Basé sur l'environnement
import os
if os.getenv("DEBUG_MODE") == "true":
    logger.set_level("DEBUG")

# Basé sur une condition
if user.is_admin():
    logger.set_level("DEBUG")
else:
    logger.set_level("WARNING")

# Changement temporaire
original_level = logger.level
logger.set_level("DEBUG")
debug_sensitive_operation()
logger.set_level(original_level)
```

### 6. Loggers Multiples

```python
# Séparer les logs par composant
api_logger = PyLoggerX(
    name="api",
    json_file="logs/api.json",
    elasticsearch_index="api-logs"
)

database_logger = PyLoggerX(
    name="database",
    json_file="logs/database.json",
    elasticsearch_index="db-logs",
    performance_tracking=True
)

worker_logger = PyLoggerX(
    name="worker",
    json_file="logs/worker.json",
    elasticsearch_index="worker-logs"
)

# Utilisation
api_logger.info("Requête API reçue", endpoint="/api/users")
database_logger.info("Requête exécutée", query="SELECT * FROM users")
worker_logger.info("Job traité", job_id="job_123")
```

---

## Référence de Configuration

### Paramètres PyLoggerX

| Paramètre | Type | Défaut | Description |
|-----------|------|--------|-------------|
| `name` | str | "PyLoggerX" | Nom du logger |
| `level` | str | "INFO" | Niveau de log (DEBUG, INFO, WARNING, ERROR, CRITICAL) |
| `console` | bool | True | Activer la sortie console |
| `colors` | bool | True | Activer les couleurs console |
| `json_file` | str | None | Chemin vers fichier JSON |
| `text_file` | str | None | Chemin vers fichier texte |
| `max_bytes` | int | 10MB | Taille max avant rotation |
| `backup_count` | int | 5 | Nombre de fichiers de sauvegarde |
| `rotation_when` | str | "midnight" | Quand faire la rotation temporelle |
| `rotation_interval` | int | 1 | Intervalle de rotation |
| `format_string` | str | None | Format personnalisé |
| `include_caller` | bool | False | Inclure fichier/ligne dans les logs |
| `performance_tracking` | bool | False | Activer le tracking de performance |
| `enrichment_data` | dict | {} | Données ajoutées à tous les logs |

### Paramètres de Logging Distant

#### Elasticsearch
| Paramètre | Type | Défaut | Description |
|-----------|------|--------|-------------|
| `elasticsearch_url` | str | None | URL du serveur Elasticsearch |
| `elasticsearch_index` | str | "pyloggerx" | Nom de l'index |
| `elasticsearch_username` | str | None | Nom d'utilisateur (optionnel) |
| `elasticsearch_password` | str | None | Mot de passe (optionnel) |
| `elasticsearch_ca_certs` | str | None | Certificats CA pour SSL |
| `elasticsearch_verify_certs` | bool | True | Vérifier les certificats SSL |

#### Grafana Loki
| Paramètre | Type | Défaut | Description |
|-----------|------|--------|-------------|
| `loki_url` | str | None | URL du serveur Loki |
| `loki_labels` | dict | {} | Labels par défaut |
| `loki_batch_size` | int | 100 | Taille du batch |
| `loki_batch_timeout` | int | 5 | Timeout du batch (secondes) |

#### Sentry
| Paramètre | Type | Défaut | Description |
|-----------|------|--------|-------------|
| `sentry_dsn` | str | None | DSN Sentry |
| `sentry_environment` | str | "production" | Nom de l'environnement |
| `sentry_release` | str | None | Version de release |
| `sentry_traces_sample_rate` | float | 0.0 | Taux d'échantillonnage des traces |

#### Datadog
| Paramètre | Type | Défaut | Description |
|-----------|------|--------|-------------|
| `datadog_api_key` | str | None | Clé API Datadog |
| `datadog_site` | str | "datadoghq.com" | Site Datadog |
| `datadog_service` | str | None | Nom du service |
| `datadog_tags` | list | [] | Tags par défaut |

#### Slack
| Paramètre | Type | Défaut | Description |
|-----------|------|--------|-------------|
| `slack_webhook` | str | None | URL webhook Slack |
| `slack_channel` | str | None | Canal (optionnel) |
| `slack_username` | str | "PyLoggerX" | Nom d'utilisateur du bot |
| `slack_min_level` | str | "WARNING" | Niveau minimum à envoyer |

#### Webhook
| Paramètre | Type | Défaut | Description |
|-----------|------|--------|-------------|
| `webhook_url` | str | None | URL du webhook |
| `webhook_method` | str | "POST" | Méthode HTTP |
| `webhook_headers` | dict | {} | En-têtes HTTP |
| `webhook_timeout` | int | 5 | Timeout (secondes) |

### Paramètres Avancés
| Paramètre | Type | Défaut | Description |
|-----------|------|--------|-------------|
| `enable_sampling` | bool | False | Activer l'échantillonnage |
| `sampling_rate` | float | 1.0 | Taux d'échantillonnage (0.0-1.0) |
| `enable_rate_limit` | bool | False | Activer la limitation de débit |
| `rate_limit_messages` | int | 100 | Max messages par période |
| `rate_limit_period` | int | 60 | Période en secondes |
| `batch_size` | int | 100 | Taille du batch pour export distant |
| `batch_timeout` | int | 5 | Timeout du batch (secondes) |
| `async_export` | bool | True | Export asynchrone (non-bloquant) |
| `queue_size` | int | 1000 | Taille de la queue d'export |
| `filters` | list | [] | Liste de filtres |

---

```markdown
# Configuration Avancée et Monitoring - PyLoggerX

## Configuration Avancée

PyLoggerX offre plusieurs méthodes flexibles pour configurer votre logger, permettant de s'adapter à différents environnements et workflows.

### Chargement depuis Fichiers

#### Configuration JSON

La méthode la plus simple et portable pour configurer PyLoggerX.

```python
from pyloggerx import PyLoggerX
from pyloggerx.config import load_config

# Charger la configuration depuis un fichier JSON
config = load_config(config_file="pyloggerx.json")
logger = PyLoggerX(**config)

logger.info("Logger configuré depuis JSON")
```

**Exemple de fichier `pyloggerx.json`:**

```json
{
  "name": "myapp",
  "level": "INFO",
  "console": true,
  "colors": true,
  "json_file": "logs/app.json",
  "text_file": "logs/app.log",
  "max_bytes": 10485760,
  "backup_count": 5,
  "include_caller": true,
  "performance_tracking": true,
  
  "elasticsearch_url": "http://elasticsearch:9200",
  "elasticsearch_index": "myapp-logs",
  "elasticsearch_username": "elastic",
  "elasticsearch_password": "changeme",
  
  "loki_url": "http://loki:3100",
  "loki_labels": {
    "app": "myapp",
    "environment": "production",
    "region": "us-east-1"
  },
  
  "sentry_dsn": "https://xxx@sentry.io/xxx",
  "sentry_environment": "production",
  "sentry_release": "1.0.0",
  
  "slack_webhook": "https://hooks.slack.com/services/xxx",
  "slack_channel": "#alerts",
  "slack_username": "PyLoggerX Bot",
  
  "enable_rate_limit": true,
  "rate_limit_messages": 100,
  "rate_limit_period": 60,
  
  "enable_sampling": false,
  "sampling_rate": 1.0,
  
  "batch_size": 100,
  "batch_timeout": 5,
  "async_export": true,
  
  "enrichment_data": {
    "service": "web-api",
    "version": "2.0.0",
    "datacenter": "dc1"
  }
}
```

#### Configuration YAML

Pour ceux qui préfèrent YAML (plus lisible pour les humains).

```python
from pyloggerx.config import load_config

# Installation requise: pip install pyyaml
config = load_config(config_file="pyloggerx.yaml")
logger = PyLoggerX(**config)
```

**Exemple de fichier `pyloggerx.yaml`:**

```yaml
# Configuration générale
name: myapp
level: INFO
console: true
colors: true

# Fichiers de logs
json_file: logs/app.json
text_file: logs/app.log
max_bytes: 10485760  # 10MB
backup_count: 5

# Options
include_caller: true
performance_tracking: true

# Elasticsearch
elasticsearch_url: http://elasticsearch:9200
elasticsearch_index: myapp-logs
elasticsearch_username: elastic
elasticsearch_password: changeme

# Grafana Loki
loki_url: http://loki:3100
loki_labels:
  app: myapp
  environment: production
  region: us-east-1

# Sentry
sentry_dsn: https://xxx@sentry.io/xxx
sentry_environment: production
sentry_release: "1.0.0"

# Slack
slack_webhook: https://hooks.slack.com/services/xxx
slack_channel: "#alerts"
slack_username: PyLoggerX Bot

# Rate limiting
enable_rate_limit: true
rate_limit_messages: 100
rate_limit_period: 60

# Sampling
enable_sampling: false
sampling_rate: 1.0

# Export batch
batch_size: 100
batch_timeout: 5
async_export: true

# Enrichissement
enrichment_data:
  service: web-api
  version: "2.0.0"
  datacenter: dc1
```

#### Détection Automatique du Format

```python
from pyloggerx.config import ConfigLoader

# Détecte automatiquement JSON ou YAML selon l'extension
config = ConfigLoader.from_file("config.json")   # JSON
config = ConfigLoader.from_file("config.yaml")   # YAML
config = ConfigLoader.from_file("config.yml")    # YAML

logger = PyLoggerX(**config)
```

### Configuration par Variables d'Environnement

Idéal pour les applications conteneurisées et les déploiements cloud-native suivant les principes 12-factor.

#### Variables Supportées

```bash
# Configuration de base
export PYLOGGERX_NAME=myapp
export PYLOGGERX_LEVEL=INFO
export PYLOGGERX_CONSOLE=true
export PYLOGGERX_COLORS=false  # Désactiver dans les conteneurs

# Fichiers de logs
export PYLOGGERX_JSON_FILE=/var/log/myapp/app.json
export PYLOGGERX_TEXT_FILE=/var/log/myapp/app.log

# Rate limiting
export PYLOGGERX_RATE_LIMIT_ENABLED=true
export PYLOGGERX_RATE_LIMIT_MESSAGES=100
export PYLOGGERX_RATE_LIMIT_PERIOD=60

# Services distants
export PYLOGGERX_ELASTICSEARCH_URL=http://elasticsearch:9200
export PYLOGGERX_LOKI_URL=http://loki:3100
export PYLOGGERX_SENTRY_DSN=https://xxx@sentry.io/xxx
export PYLOGGERX_DATADOG_API_KEY=your_api_key
export PYLOGGERX_SLACK_WEBHOOK=https://hooks.slack.com/services/xxx
```

#### Utilisation des Variables d'Environnement

```python
from pyloggerx.config import load_config

# Charger uniquement depuis les variables d'environnement
config = load_config(from_env=True)
logger = PyLoggerX(**config)

# Ou utiliser directement ConfigLoader
from pyloggerx.config import ConfigLoader

env_config = ConfigLoader.from_env(prefix="PYLOGGERX_")
logger = PyLoggerX(**env_config)
```

#### Exemple Docker Compose

```yaml
version: '3.8'

services:
  myapp:
    build: .
    environment:
      PYLOGGERX_LEVEL: INFO
      PYLOGGERX_CONSOLE: "true"
      PYLOGGERX_COLORS: "false"
      PYLOGGERX_JSON_FILE: /var/log/app.json
      PYLOGGERX_ELASTICSEARCH_URL: http://elasticsearch:9200
      PYLOGGERX_RATE_LIMIT_ENABLED: "true"
      PYLOGGERX_RATE_LIMIT_MESSAGES: 100
    volumes:
      - ./logs:/var/log
    depends_on:
      - elasticsearch
  
  elasticsearch:
    image: elasticsearch:8.11.0
    environment:
      - discovery.type=single-node
    ports:
      - "9200:9200"
```

#### Exemple Kubernetes ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: pyloggerx-config
  namespace: production
data:
  PYLOGGERX_LEVEL: "INFO"
  PYLOGGERX_CONSOLE: "true"
  PYLOGGERX_COLORS: "false"
  PYLOGGERX_ELASTICSEARCH_URL: "http://elasticsearch.logging.svc.cluster.local:9200"
  PYLOGGERX_RATE_LIMIT_ENABLED: "true"
  PYLOGGERX_RATE_LIMIT_MESSAGES: "100"

---
apiVersion: v1
kind: Secret
metadata:
  name: pyloggerx-secrets
  namespace: production
type: Opaque
stringData:
  PYLOGGERX_SENTRY_DSN: "https://xxx@sentry.io/xxx"
  PYLOGGERX_DATADOG_API_KEY: "your_api_key"
  PYLOGGERX_SLACK_WEBHOOK: "https://hooks.slack.com/services/xxx"

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  template:
    spec:
      containers:
      - name: myapp
        image: myapp:1.0.0
        envFrom:
        - configMapRef:
            name: pyloggerx-config
        - secretRef:
            name: pyloggerx-secrets
```

### Configuration Multi-Sources

Combinez plusieurs sources de configuration avec ordre de priorité.

#### Priorité de Configuration

**Ordre (du plus prioritaire au moins prioritaire):**
1. Variables d'environnement
2. Fichier de configuration
3. Valeurs par défaut

```python
from pyloggerx.config import load_config

# Charger avec priorités
config = load_config(
    config_file="config.json",      # 2e priorité
    from_env=True,                  # 1re priorité (écrase config_file)
    defaults={                      # 3e priorité (fallback)
        "name": "default-app",
        "level": "INFO",
        "console": True,
        "colors": False
    }
)

logger = PyLoggerX(**config)
```

#### Exemple Pratique: Configuration par Environnement

```python
import os
from pyloggerx.config import load_config

# Déterminer le fichier de config selon l'environnement
env = os.getenv("ENVIRONMENT", "development")
config_files = {
    "development": "config.dev.json",
    "staging": "config.staging.json",
    "production": "config.prod.json"
}

# Charger la config appropriée
config = load_config(
    config_file=config_files.get(env),
    from_env=True,  # Permet les overrides par env vars
    defaults={"level": "DEBUG" if env == "development" else "INFO"}
)

logger = PyLoggerX(**config)
logger.info(f"Application démarrée en mode {env}")
```

#### Fusion Manuelle de Configurations

```python
from pyloggerx.config import ConfigLoader

# Charger plusieurs configs
base_config = ConfigLoader.from_json("config.base.json")
env_config = ConfigLoader.from_json(f"config.{environment}.json")
local_overrides = ConfigLoader.from_json("config.local.json")
env_vars = ConfigLoader.from_env()

# Fusionner dans l'ordre (derniers écrasent les premiers)
merged_config = ConfigLoader.merge_configs(
    base_config,
    env_config,
    local_overrides,
    env_vars
)

logger = PyLoggerX(**merged_config)
```

### Validation de Configuration

PyLoggerX valide automatiquement votre configuration.

#### Validation Automatique

```python
from pyloggerx.config import load_config

try:
    config = load_config(config_file="config.json")
    logger = PyLoggerX(**config)
except ValueError as e:
    print(f"Configuration invalide: {e}")
    exit(1)
```

#### Validation Manuelle

```python
from pyloggerx.config import ConfigValidator

config = {
    "name": "myapp",
    "level": "INVALID",  # Niveau invalide
    "rate_limit_messages": -10  # Valeur négative invalide
}

is_valid, error_message = ConfigValidator.validate(config)

if not is_valid:
    print(f"Erreur de configuration: {error_message}")
else:
    logger = PyLoggerX(**config)
```

#### Règles de Validation

Le validateur vérifie:

1. **Niveau de log**: Doit être DEBUG, INFO, WARNING, ERROR, ou CRITICAL
2. **Rate limiting**: 
   - `rate_limit_messages` doit être un entier positif
   - `rate_limit_period` doit être un nombre positif
3. **Sampling**: 
   - `sampling_rate` doit être entre 0.0 et 1.0
4. **URLs**: 
   - Les URLs (Elasticsearch, Loki, webhook) doivent commencer par http/https

### Configurations Prédéfinies

PyLoggerX inclut des templates de configuration prêts à l'emploi.

#### Templates Disponibles

```python
from pyloggerx.config import EXAMPLE_CONFIGS

# Afficher les templates disponibles
print(list(EXAMPLE_CONFIGS.keys()))
# ['basic', 'production', 'development']

# Utiliser un template
logger = PyLoggerX(**EXAMPLE_CONFIGS['production'])
```

#### Template "Basic"

Configuration simple pour démarrer rapidement.

```python
from pyloggerx.config import EXAMPLE_CONFIGS

logger = PyLoggerX(**EXAMPLE_CONFIGS['basic'])
```

**Configuration:**
```json
{
  "name": "myapp",
  "level": "INFO",
  "console": true,
  "colors": true,
  "json_file": "logs/app.json",
  "text_file": "logs/app.txt"
}
```

#### Template "Production"

Configuration optimisée pour environnements de production.

```python
logger = PyLoggerX(**EXAMPLE_CONFIGS['production'])
```

**Configuration:**
```json
{
  "name": "myapp",
  "level": "WARNING",
  "console": false,
  "colors": false,
  "json_file": "/var/log/myapp/app.json",
  "text_file": "/var/log/myapp/app.txt",
  "max_bytes": 52428800,
  "backup_count": 10,
  "enable_rate_limit": true,
  "rate_limit_messages": 100,
  "rate_limit_period": 60,
  "performance_tracking": true
}
```

#### Template "Development"

Configuration détaillée pour développement.

```python
logger = PyLoggerX(**EXAMPLE_CONFIGS['development'])
```

**Configuration:**
```json
{
  "name": "myapp-dev",
  "level": "DEBUG",
  "console": true,
  "colors": true,
  "include_caller": true,
  "json_file": "logs/dev.json",
  "enable_rate_limit": false,
  "performance_tracking": true
}
```

#### Sauvegarder un Template

```python
from pyloggerx.config import save_example_config

# Sauvegarder un template dans un fichier
save_example_config("production", "my-config.json")

# Puis charger et personnaliser
config = load_config(config_file="my-config.json")
config['name'] = "my-custom-app"
logger = PyLoggerX(**config)
```

#### Créer un Template Personnalisé

```python
from pyloggerx.config import EXAMPLE_CONFIGS

# Partir d'un template existant
custom_config = EXAMPLE_CONFIGS['production'].copy()

# Personnaliser
custom_config.update({
    'name': 'my-microservice',
    'elasticsearch_url': 'http://my-es:9200',
    'slack_webhook': 'https://hooks.slack.com/xxx',
    'enrichment_data': {
        'service': 'payment-api',
        'team': 'backend',
        'region': 'eu-west-1'
    }
})

logger = PyLoggerX(**custom_config)
```

---

## Monitoring et Métriques

PyLoggerX intègre un système complet de monitoring pour surveiller la santé, les performances et les métriques de votre système de logging.

### Collecteur de Métriques

Le `MetricsCollector` collecte et agrège automatiquement les métriques de logging.

#### Utilisation Basique

```python
from pyloggerx import PyLoggerX
from pyloggerx.monitoring import MetricsCollector

# Créer un collecteur
collector = MetricsCollector(window_size=300)  # Fenêtre de 5 minutes

# Attacher au logger
logger = PyLoggerX(
    name="monitored_app",
    console=True
)

# Enregistrer manuellement des logs (optionnel, fait automatiquement)
collector.record_log(level="INFO", size=256)
collector.record_log(level="ERROR", size=512)

# Obtenir les métriques
metrics = collector.get_metrics()
print(f"Uptime: {metrics['uptime_seconds']}s")
print(f"Total logs: {metrics['total_logs']}")
print(f"Logs/seconde: {metrics['logs_per_second']}")
print(f"Taille moyenne: {metrics['avg_log_size_bytes']} bytes")
print(f"Par niveau: {metrics['logs_per_level']}")
print(f"Erreurs récentes: {metrics['recent_errors']}")
```

#### Métriques Collectées

Le collecteur suit:

1. **Uptime**: Temps écoulé depuis le démarrage
2. **Total des logs**: Nombre total de logs émis
3. **Logs par niveau**: Compteurs pour DEBUG, INFO, WARNING, ERROR, CRITICAL
4. **Taux de logs**: Logs par seconde (fenêtre glissante)
5. **Taille des logs**: Taille moyenne des logs en bytes
6. **Erreurs**: Historique des erreurs récentes

#### Enregistrement d'Erreurs

```python
try:
    risky_operation()
except Exception as e:
    collector.record_error(str(e))
    logger.exception("Opération échouée")
```

#### Réinitialisation des Métriques

```python
# Réinitialiser toutes les métriques
collector.reset()
```

#### Fenêtre de Temps Personnalisée

```python
# Collecteur avec fenêtre de 10 minutes
collector = MetricsCollector(window_size=600)

# Métriques sur les 10 dernières minutes
metrics = collector.get_metrics()
```

### Gestionnaire d'Alertes

Le `AlertManager` permet de définir des règles d'alerte basées sur les métriques.

#### Configuration des Alertes

```python
from pyloggerx.monitoring import AlertManager

# Créer le gestionnaire
alert_mgr = AlertManager()

# Définir une règle d'alerte
alert_mgr.add_rule(
    name="high_error_rate",
    condition=lambda m: m['logs_per_level'].get('ERROR', 0) > 100,
    cooldown=300,  # 5 minutes entre alertes
    message="Taux d'erreurs élevé détecté (>100 erreurs)"
)

# Définir un callback
def send_alert(alert_name, message):
    print(f"ALERTE [{alert_name}]: {message}")
    # Envoyer email, Slack, PagerDuty, etc.

alert_mgr.add_callback(send_alert)

# Vérifier les métriques périodiquement
metrics = collector.get_metrics()
alert_mgr.check_metrics(metrics)
```

#### Règles d'Alerte Prédéfinies

```python
# Taux d'erreurs élevé
alert_mgr.add_rule(
    name="high_error_rate",
    condition=lambda m: m['logs_per_level'].get('ERROR', 0) > 100,
    cooldown=300
)

# Taux de logs excessif
alert_mgr.add_rule(
    name="high_log_rate",
    condition=lambda m: m['logs_per_second'] > 100,
    cooldown=300
)

# Circuit breaker ouvert
alert_mgr.add_rule(
    name="exporter_circuit_breaker",
    condition=lambda m: any(
        exp.get('circuit_breaker_open', False)
        for exp in m.get('exporter_metrics', {}).values()
    ),
    cooldown=600
)

# Taille de queue élevée
alert_mgr.add_rule(
    name="high_queue_size",
    condition=lambda m: any(
        exp.get('queue_size', 0) > 1000
        for exp in m.get('exporter_metrics', {}).values()
    ),
    cooldown=300
)

# Utilisation mémoire
alert_mgr.add_rule(
    name="high_memory",
    condition=lambda m: m.get('avg_log_size_bytes', 0) > 10000,
    cooldown=600
)
```

#### Callbacks Multiples

```python
def slack_alert(alert_name, message):
    requests.post(
        slack_webhook,
        json={"text": f":warning: {message}"}
    )

def email_alert(alert_name, message):
    send_email(
        to="ops@example.com",
        subject=f"Alert: {alert_name}",
        body=message
    )

def log_alert(alert_name, message):
    logger.critical(message, alert=alert_name)

# Ajouter tous les callbacks
alert_mgr.add_callback(slack_alert)
alert_mgr.add_callback(email_alert)
alert_mgr.add_callback(log_alert)
```

#### Cooldown Personnalisé

Le cooldown évite le spam d'alertes:

```python
# Alerte critique avec cooldown court (1 minute)
alert_mgr.add_rule(
    name="critical_error",
    condition=lambda m: m['logs_per_level'].get('CRITICAL', 0) > 0,
    cooldown=60,  # 1 minute
    message="Erreur critique détectée!"
)

# Alerte warning avec cooldown long (10 minutes)
alert_mgr.add_rule(
    name="performance_degradation",
    condition=lambda m: m['logs_per_second'] > 50,
    cooldown=600,  # 10 minutes
    message="Performance dégradée détectée"
)
```

### Monitoring de Santé

Le `HealthMonitor` surveille automatiquement la santé du logger en arrière-plan.

#### Configuration et Démarrage

```python
from pyloggerx.monitoring import HealthMonitor

logger = PyLoggerX(name="production_app")

# Créer le monitor
monitor = HealthMonitor(
    logger=logger,
    check_interval=60  # Vérifier toutes les 60 secondes
)

# Démarrer le monitoring
monitor.start()

# Le monitoring s'exécute en arrière-plan dans un thread séparé
# et vérifie automatiquement la santé toutes les 60 secondes

# ... votre application tourne ...

# Arrêter le monitoring proprement
monitor.stop()
```

#### Obtenir le Statut

```python
# Obtenir le statut complet
status = monitor.get_status()

print(f"Monitoring actif: {status['running']}")
print(f"Métriques: {status['metrics']}")
print(f"Stats du logger: {status['logger_stats']}")
print(f"Santé du logger: {status['logger_health']}")
```

#### Alertes Automatiques

Le `HealthMonitor` inclut des règles d'alerte par défaut:

1. **high_error_rate**: Plus de 100 erreurs
2. **high_log_rate**: Plus de 100 logs/seconde
3. **exporter_circuit_breaker**: Circuit breaker d'un exporter ouvert

```python
# Ajouter un callback pour les alertes
def handle_alert(alert_name, message):
    print(f"ALERTE: {message}")
    # Envoyer notification

monitor.alert_manager.add_callback(handle_alert)
```

#### Règles Personnalisées

```python
# Ajouter vos propres règles d'alerte
monitor.alert_manager.add_rule(
    name="custom_metric",
    condition=lambda m: your_custom_check(m),
    cooldown=300,
    message="Condition personnalisée déclenchée"
)
```

#### Exemple Complet: Application avec Monitoring

```python
from pyloggerx import PyLoggerX
from pyloggerx.monitoring import HealthMonitor
import time
import signal
import sys

# Configuration du logger
logger = PyLoggerX(
    name="monitored_service",
    console=True,
    json_file="logs/service.json",
    elasticsearch_url="http://elasticsearch:9200",
    performance_tracking=True
)

# Configuration du monitoring
monitor = HealthMonitor(logger, check_interval=30)

def alert_callback(alert_name, message):
    """Callback pour les alertes"""
    logger.critical(f"ALERTE: {message}", alert=alert_name)
    # Ici: envoyer email, Slack, PagerDuty, etc.

monitor.alert_manager.add_callback(alert_callback)

# Ajout de règles personnalisées
monitor.alert_manager.add_rule(
    name="service_overload",
    condition=lambda m: m['logs_per_second'] > 50,
    cooldown=180,
    message="Service surchargé: >50 logs/sec"
)

def shutdown_handler(signum, frame):
    """Arrêt propre"""
    logger.info("Arrêt du service...")
    monitor.stop()
    logger.close()
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)

def main():
    # Démarrer le monitoring
    monitor.start()
    logger.info("Service et monitoring démarrés")
    
    # Votre application
    while True:
        try:
            # Logique métier
            logger.info("Traitement en cours...")
            time.sleep(10)
            
        except Exception as e:
            logger.exception("Erreur dans la boucle principale")

if __name__ == "__main__":
    main()
```

### Dashboard Console

Affichez un dashboard de monitoring directement dans la console.

#### Affichage Simple

```python
from pyloggerx.monitoring import print_dashboard

logger = PyLoggerX(name="myapp")

# Afficher le dashboard
print_dashboard(logger, clear_screen=True)
```

#### Sortie du Dashboard

```
============================================================
PyLoggerX Monitoring Dashboard
============================================================
Timestamp: 2025-01-15 10:30:45

📊 General Statistics:
  Total Logs: 15423
  Exporters: 3
  Filters: 2

🚦 Rate Limiting:
  Enabled: Yes
  Max Messages: 100
  Period: 60s
  Rejections: 45

🏥 Exporter Health:
  Overall Healthy: ✅ Yes
  ✅ elasticsearch
  ✅ loki
  ❌ sentry

📈 Exporter Metrics:

  elasticsearch:
    Exported: 12450
    Failed: 23
    Dropped: 0
    Queue: 15
    ⚠️  Circuit Breaker: OPEN (failures: 5)

  loki:
    Exported: 11890
    Failed: 5
    Dropped: 0
    Queue: 8

  sentry:
    Exported: 345
    Failed: 102
    Dropped: 0
    Queue: 0
    ⚠️  Circuit Breaker: OPEN (failures: 10)

============================================================
```

#### Dashboard en Boucle

```python
import time
from pyloggerx.monitoring import print_dashboard

logger = PyLoggerX(name="myapp")

# Rafraîchir le dashboard toutes les 5 secondes
try:
    while True:
        print_dashboard(logger, clear_screen=True)
        time.sleep(5)
except KeyboardInterrupt:
    print("\nDashboard arrêté")
```

#### Dashboard Personnalisé

```python
from pyloggerx.monitoring import HealthMonitor
import os

def custom_dashboard(logger):
    """Dashboard personnalisé"""
    stats = logger.get_stats()
    health = logger.healthcheck()
    
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("=" * 60)
    print("Mon Application - Dashboard")
    print("=" * 60)
    
    # Santé globale
    status_icon = "✅" if health['healthy'] else "❌"
    print(f"\n{status_icon} Statut: {'HEALTHY' if health['healthy'] else 'UNHEALTHY'}")
    
    # Métriques clés
    print(f"\n📊 Métriques:")
    print(f"  Total logs: {stats['total_logs']:,}")
    
    if 'logs_per_level' in stats:
        print(f"\n📈 Par niveau:")
        for level, count in sorted(stats['logs_per_level'].items()):
            print(f"  {level}: {count:,}")
    
    # Exporters
    if health['exporters']:
        print(f"\n🔌 Exporters:")
        for name, is_healthy in health['exporters'].items():
            icon = "✅" if is_healthy else "❌"
            print(f"  {icon} {name}")
    
    print("\n" + "=" * 60)

# Utilisation
while True:
    custom_dashboard(logger)
    time.sleep(5)
```

---

## Intégrations Monitoring

### Intégration Prometheus

Exposez les métriques PyLoggerX à Prometheus pour un monitoring centralisé.

#### Installation

```bash
pip install prometheus-client
```

#### Configuration Basique

```python
from pyloggerx import PyLoggerX
from prometheus_client import Counter, Gauge, Histogram, start_http_server
import time

# Métriques Prometheus
logs_total = Counter(
    'pyloggerx_logs_total',
    'Total number of logs',
    ['level', 'logger']
)

logs_per_second = Gauge(
    'pyloggerx_logs_per_second',
    'Current logs per second',
    ['logger']
)

export_errors = Counter(
    'pyloggerx_export_errors_total',
    'Total export errors',
    ['exporter', 'logger']
)

queue_size = Gauge(
    'pyloggerx_queue_size',
    'Current queue size',
    ['exporter', 'logger']
)

log_size_bytes = Histogram(
    'pyloggerx_log_size_bytes',
    'Log size distribution',
    ['logger']
)

# Logger
logger = PyLoggerX(
    name="prometheus_app",
    console=True,
    json_file="logs/app.json",
    elasticsearch_url="http://elasticsearch:9200"
)

def update_prometheus_metrics():
    """Mettre à jour les métriques Prometheus depuis PyLoggerX"""
    stats = logger.get_stats()
    
    # Logs par niveau
    if 'logs_per_level' in stats:
        for level, count in stats['logs_per_level'].items():
            logs_total.labels(level=level, logger=logger.name).inc(count)
    
    # Métriques d'export
    if 'exporter_metrics' in stats:
        for exporter_name, metrics in stats['exporter_metrics'].items():
            # Erreurs d'export
            export_errors.labels(
                exporter=exporter_name,
                logger=logger.name
            ).inc(metrics.get('failed_logs', 0))
            
            # Taille de queue
            queue_size.labels(
                exporter=exporter_name,
                logger=logger.name
            ).set(metrics.get('queue_size', 0))

# Démarrer le serveur de métriques Prometheus
start_http_server(8000)
logger.info("Serveur de métriques Prometheus démarré", port=8000)

# Mettre à jour les métriques périodiquement
while True:
    update_prometheus_metrics()
    time.sleep(15)
```

#### Configuration Prometheus

**prometheus.yml:**

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'pyloggerx'
    static_configs:
      - targets: ['localhost:8000']
        labels:
          app: 'myapp'
          environment: 'production'
```

#### Queries Prometheus Utiles

```promql
# Taux de logs par seconde
rate(pyloggerx_logs_total[5m])

# Erreurs par exporter
sum by (exporter) (pyloggerx_export_errors_total)

# Taille de queue par exporter
pyloggerx_queue_size

# Percentile 95 de la taille des logs
histogram_quantile(0.95, pyloggerx_log_size_bytes_bucket)

# Logs par niveau (graphique empilé)
sum by (level) (rate(pyloggerx_logs_total[5m]))
```

#### Alertes Prometheus

**alerts.yml:**

```yaml
groups:
  - name: pyloggerx_alerts
    interval: 30s
    rules:
      - alert: HighErrorRate
        expr: rate(pyloggerx_logs_total{level="ERROR"}[5m]) > 10
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Taux d'erreurs élevé détecté"
          description: "{{ $labels.logger }} a un taux d'erreurs de {{ $value }}/s"
      
      - alert: ExporterDown
        expr: pyloggerx_queue_size > 1000
        for: 10m
        labels:
          severity: critical
        annotations:
          summary: "Exporter surchargé"
          description: "{{ $labels.exporter }} a une queue de {{ $value }} messages"
      
      - alert: HighExportFailureRate
        expr: rate(pyloggerx_export_errors_total[5m]) > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Échecs d'export fréquents"
          description: "{{ $labels.exporter }} échoue à {{ $value }}/s"
```

### Intégration Grafana

Créez des dashboards visuels pour surveiller PyLoggerX.

#### Dashboard JSON pour Grafana

```json
{
  "dashboard": {
    "title": "PyLoggerX Monitoring",
    "panels": [
      {
        "title": "Logs par Seconde",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(pyloggerx_logs_total[5m])"
          }
        ]
      },
      {
        "title": "Logs par Niveau",
        "type": "graph",
        "targets": [
          {
            "expr": "sum by (level) (rate(pyloggerx_logs_total[5m]))"
          }
        ],
        "stack": true
      },
      {
        "title": "Taille de Queue",
        "type": "graph",
        "targets": [
          {
            "expr": "pyloggerx_queue_size"
          }
        ]
      },
      {
        "title": "Erreurs d'Export",
        "type": "stat",
        "targets": [
          {
            "expr": "sum(pyloggerx_export_errors_total)"
          }
        ]
      }
    ]
  }
}
```

#### Variables de Dashboard

```json
{
  "templating": {
    "list": [
      {
        "name": "logger",
        "type": "query",
        "query": "label_values(pyloggerx_logs_total, logger)"
      },
      {
        "name": "exporter",
        "type": "query",
        "query": "label_values(pyloggerx_queue_size, exporter)"
      }
    ]
  }
}
```

#### Panels Recommandés

1. **Logs par Seconde**: Graph avec `rate(pyloggerx_logs_total[5m])`
2. **Distribution par Niveau**: Stacked graph avec `sum by (level)`
3. **Santé des Exporters**: Stat panel avec `up` metric
4. **Taille de Queue**: Graph avec `pyloggerx_queue_size`
5. **Erreurs d'Export**: Graph avec `rate(pyloggerx_export_errors_total[5m])`
6. **Latence des Logs**: Histogram avec `pyloggerx_log_size_bytes`

### Métriques Personnalisées

Créez vos propres métriques métier.

#### Métriques Applicatives

```python
from pyloggerx import PyLoggerX
from prometheus_client import Counter, Histogram
import time

logger = PyLoggerX(name="business_app")

# Métriques métier
user_logins = Counter('app_user_logins_total', 'Total user logins')
order_value = Histogram('app_order_value_dollars', 'Order values')
api_requests = Counter('app_api_requests_total', 'API requests', ['endpoint', 'status'])
processing_time = Histogram('app_processing_seconds', 'Processing time', ['operation'])

def handle_login(user_id):
    """Gérer une connexion utilisateur"""
    start = time.time()
    
    try:
        # Logique de connexion
        logger.info("Connexion utilisateur", user_id=user_id)
        user_logins.inc()
        
        duration = time.time() - start
        processing_time.labels(operation='login').observe(duration)
        
        return True
    except Exception as e:
        logger.error("Échec de connexion", user_id=user_id, error=str(e))
        return False

def process_order(order_id, amount):
    """Traiter une commande"""
    logger.info("Traitement commande", order_id=order_id, amount=amount)
    
    # Enregistrer la valeur
    order_value.observe(amount)
    
    # Logique métier
    # ...

def api_endpoint(endpoint, func):
    """Décorateur pour tracker les appels API"""
    def wrapper(*args, **kwargs):
        start = time.time()
        
        try:
            result = func(*args, **kwargs)
            status = 'success'
            logger.info("API appelée", endpoint=endpoint, status=status)
            return result
        except Exception as e:
            status = 'error'
            logger.error("API échouée", endpoint=endpoint, error=str(e))
            raise
        finally:
            duration = time.time() - start
            api_requests.labels(endpoint=endpoint, status=status).inc()
            processing_time.labels(operation=endpoint).observe(duration)
    
    return wrapper

@api_endpoint('/api/users')
def get_users():
    # Logique API
    return {"users": []}
```

#### Métriques Combinées

```python
from pyloggerx.monitoring import MetricsCollector

collector = MetricsCollector()
logger = PyLoggerX(name="app")

# Fonction périodique pour exporter vers Prometheus
def export_pyloggerx_metrics():
    """Exporter les métriques PyLoggerX vers Prometheus"""
    metrics = collector.get_metrics()
    
    # Métriques système
    logs_total_gauge.set(metrics['total_logs'])
    logs_per_second_gauge.set(metrics['logs_per_second'])
    avg_log_size_gauge.set(metrics['avg_log_size_bytes'])
    
    # Logs par niveau
    for level, count in metrics['logs_per_level'].items():
        logs_by_level.labels(level=level).set(count)
    
    # Erreurs récentes
    error_count.set(len(metrics['recent_errors']))

# Appeler périodiquement
import threading
import time

def metrics_updater():
    while True:
        export_pyloggerx_metrics()
        time.sleep(15)

metrics_thread = threading.Thread(target=metrics_updater, daemon=True)
metrics_thread.start()
```

---

## Exemples Complets

### Exemple 1: Application Web avec Monitoring Complet

```python
"""
Application FastAPI avec monitoring PyLoggerX complet
"""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pyloggerx import PyLoggerX
from pyloggerx.monitoring import HealthMonitor, print_dashboard
from pyloggerx.config import load_config
from prometheus_client import make_asgi_app, Counter, Histogram
import time
import uuid
import os

# Charger la configuration
config = load_config(
    config_file="config.json",
    from_env=True,
    defaults={"name": "web-api", "level": "INFO"}
)

# Initialiser le logger
logger = PyLoggerX(**config)

# Initialiser le monitoring
monitor = HealthMonitor(logger, check_interval=30)

# Métriques Prometheus
http_requests = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)
http_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint']
)

# Callbacks d'alerte
def alert_to_slack(alert_name, message):
    """Envoyer alerte à Slack"""
    if os.getenv('SLACK_WEBHOOK'):
        import requests
        requests.post(
            os.getenv('SLACK_WEBHOOK'),
            json={"text": f":warning: {message}"}
        )

monitor.alert_manager.add_callback(alert_to_slack)

# Application FastAPI
app = FastAPI(title="API avec Monitoring")

# Monter le endpoint Prometheus
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

@app.on_event("startup")
async def startup():
    """Démarrage de l'application"""
    monitor.start()
    logger.info("Application et monitoring démarrés")

@app.on_event("shutdown")
async def shutdown():
    """Arrêt de l'application"""
    monitor.stop()
    logger.info("Application arrêtée")
    logger.close()

@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    """Middleware de logging et métriques"""
    request_id = str(uuid.uuid4())
    start_time = time.time()
    
    # Contexte de logging
    with logger.context(request_id=request_id):
        logger.info(
            "Requête reçue",
            method=request.method,
            path=request.url.path,
            client=request.client.host
        )
        
        try:
            response = await call_next(request)
            duration = time.time() - start_time
            
            # Métriques
            http_requests.labels(
                method=request.method,
                endpoint=request.url.path,
                status=response.status_code
            ).inc()
            http_duration.labels(
                method=request.method,
                endpoint=request.url.path
            ).observe(duration)
            
            logger.info(
                "Requête complétée",
                method=request.method,
                path=request.url.path,
                status=response.status_code,
                duration_ms=duration * 1000
            )
            
            response.headers["X-Request-ID"] = request_id
            return response
            
        except Exception as e:
            duration = time.time() - start_time
            logger.exception(
                "Erreur requête",
                method=request.method,
                path=request.url.path,
                duration_ms=duration * 1000
            )
            raise

@app.get("/")
async def root():
    """Endpoint racine"""
    return {"status": "ok", "service": "web-api"}

@app.get("/health")
async def health():
    """Health check détaillé"""
    health_status = logger.healthcheck()
    stats = logger.get_stats()
    monitor_status = monitor.get_status()
    
    return {
        "healthy": health_status['healthy'],
        "logger": {
            "total_logs": stats['total_logs'],
            "exporters": health_status['exporters']
        },
        "monitor": {
            "running": monitor_status['running'],
            "metrics": monitor_status['metrics']
        }
    }

@app.get("/stats")
async def stats():
    """Statistiques détaillées"""
    return {
        "logger": logger.get_stats(),
        "monitor": monitor.get_status()
    }

@app.get("/dashboard")
async def dashboard():
    """Dashboard en format texte"""
    import io
    import sys
    
    # Capturer la sortie du dashboard
    old_stdout = sys.stdout
    sys.stdout = buffer = io.StringIO()
    
    print_dashboard(logger, clear_screen=False)
    
    sys.stdout = old_stdout
    output = buffer.getvalue()
    
    return {"dashboard": output}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Exemple 2: Worker Batch avec Configuration Avancée

```python
"""
Worker de traitement batch avec configuration complète
"""
import time
import sys
from datetime import datetime
from pyloggerx import PyLoggerX
from pyloggerx.config import load_config, save_example_config
from pyloggerx.monitoring import HealthMonitor, MetricsCollector

# Générer une config si elle n'existe pas
config_file = "worker-config.json"
if not os.path.exists(config_file):
    save_example_config("production", config_file)
    print(f"Configuration créée: {config_file}")

# Charger la configuration
config = load_config(
    config_file=config_file,
    from_env=True,
    defaults={
        "name": "batch-worker",
        "level": "INFO",
        "performance_tracking": True
    }
)

# Personnaliser la config
config.update({
    "enrichment_data": {
        "worker_id": os.getenv("WORKER_ID", "worker-1"),
        "datacenter": os.getenv("DATACENTER", "dc1"),
        "start_time": datetime.now().isoformat()
    }
})

# Initialiser le logger
logger = PyLoggerX(**config)

# Monitoring
collector = MetricsCollector(window_size=600)  # 10 minutes
monitor = HealthMonitor(logger, check_interval=60)

# Callbacks d'alerte
def email_alert(alert_name, message):
    logger.critical(f"ALERTE: {message}", alert=alert_name)
    # Implémenter l'envoi d'email

def metrics_alert(alert_name, message):
    """Logger les alertes pour les métriques"""
    collector.record_error(f"{alert_name}: {message}")

monitor.alert_manager.add_callback(email_alert)
monitor.alert_manager.add_callback(metrics_alert)

# Règles d'alerte personnalisées
monitor.alert_manager.add_rule(
    name="processing_slow",
    condition=lambda m: m.get('avg_duration', 0) > 5.0,
    cooldown=300,
    message="Traitement lent détecté (>5s en moyenne)"
)

class BatchWorker:
    def __init__(self):
        self.running = False
        self.processed = 0
        self.errors = 0
    
    def start(self):
        """Démarrer le worker"""
        self.running = True
        monitor.start()
        
        logger.info("Worker démarré", config=config)
        
        try:
            while self.running:
                self.process_batch()
                time.sleep(10)
        except KeyboardInterrupt:
            logger.info("Arrêt demandé")
        finally:
            self.stop()
    
    def process_batch(self):
        """Traiter un batch"""
        with logger.timer("Batch Processing"):
            try:
                # Récupérer les jobs
                jobs = self.fetch_jobs()
                
                if not jobs:
                    logger.debug("Aucun job à traiter")
                    return
                
                logger.info("Traitement batch", job_count=len(jobs))
                
                # Traiter chaque job
                for job in jobs:
                    self.process_job(job)
                
                # Enregistrer les métriques
                collector.record_log("INFO", size=len(str(jobs)))
                
            except Exception as e:
                self.errors += 1
                collector.record_error(str(e))
                logger.exception("Erreur batch")
    
    def fetch_jobs(self):
        """Récupérer les jobs depuis la queue"""
        # Simuler la récupération
        import random
        return [{"id": i} for i in range(random.randint(0, 10))]
    
    def process_job(self, job):
        """Traiter un job"""
        job_id = job["id"]
        
        try:
            logger.debug("Traitement job", job_id=job_id)
            
            # Simuler le traitement
            time.sleep(0.1)
            
            self.processed += 1
            logger.info("Job complété", job_id=job_id)
            
        except Exception as e:
            self.errors += 1
            logger.error("Job échoué", job_id=job_id, error=str(e))
    
    def stop(self):
        """Arrêter le worker"""
        self.running = False
        monitor.stop()
        
        # Stats finales
        stats = logger.get_performance_stats()
        metrics = collector.get_metrics()
        
        logger.info(
            "Worker arrêté",
            processed=self.processed,
            errors=self.errors,
            total_duration=stats.get('total_duration', 0),
            avg_duration=stats.get('avg_duration', 0),
            logs_per_second=metrics.get('logs_per_second', 0)
        )
        
        logger.close()

if __name__ == "__main__":
    worker = BatchWorker()
    worker.start()
```

### Exemple 3: Microservice avec Dashboard Live

```python
"""
Microservice avec dashboard de monitoring en temps réel
"""
import threading
import time
import os
from pyloggerx import PyLoggerX
from pyloggerx.monitoring import HealthMonitor, print_dashboard
from pyloggerx.config import load_config

# Configuration
config = load_config(
    from_env=True,
    defaults={
        "name": "microservice",
        "level": "INFO",
        "console": True,
        "json_file": "logs/service.json",
        "performance_tracking": True,
        "enable_rate_limit": True,
        "rate_limit_messages": 100,
        "rate_limit_period": 60
    }
)

logger = PyLoggerX(**config)
monitor = HealthMonitor(logger, check_interval=30)

# Dashboard en thread séparé
def dashboard_updater():
    """Mettre à jour le dashboard en continu"""
    while True:
        try:
            print_dashboard(logger, clear_screen=True)
            time.sleep(5)
        except KeyboardInterrupt:
            break

# Démarrer le dashboard dans un thread séparé
if os.getenv("SHOW_DASHBOARD", "false").lower() == "true":
    dashboard_thread = threading.Thread(target=dashboard_updater, daemon=True)
    dashboard_thread.start()
    logger.info("Dashboard activé")

# Service principal
monitor.start()
logger.info("Microservice démarré")

try:
    # Boucle principale du service
    while True:
        # Simuler du travail
        logger.info("Traitement en cours")
        time.sleep(10)
        
        # Simuler des erreurs occasionnelles
        import random
        if random.random() < 0.1:
            logger.error("Erreur simulée", error_code=random.randint(500, 599))

except KeyboardInterrupt:
    logger.info("Arrêt du service")
finally:
    monitor.stop()
    logger.close()
```

---

## Référence Config

### ConfigLoader

Classe pour charger des configurations depuis différentes sources.

```python
class ConfigLoader:
    @staticmethod
    def from_json(filepath: str) -> Dict[str, Any]
    
    @staticmethod
    def from_yaml(filepath: str) -> Dict[str, Any]
    
    @staticmethod
    def from_env(prefix: str = "PYLOGGERX_") -> Dict[str, Any]
    
    @staticmethod
    def from_file(filepath: str) -> Dict[str, Any]
    
    @staticmethod
    def merge_configs(*configs: Dict[str, Any]) -> Dict[str, Any]
```

### ConfigValidator

Classe pour valider les configurations.

```python
class ConfigValidator:
    VALID_LEVELS = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    
    @staticmethod
    def validate(config: Dict[str, Any]) -> tuple[bool, Optional[str]]
```

### load_config

Fonction pour charger une configuration complète.

```python
def load_config(
    config_file: Optional[str] = None,
    from_env: bool = True,
    defaults: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

### MetricsCollector

Collecteur de métriques de logging.

```python
class MetricsCollector:
    def __init__(self, window_size: int = 300)
    
    def record_log(self, level: str, size: int = 0) -> None
    
    def record_error(self, error: str) -> None
    
    def get_metrics(self) -> Dict[str, Any]
    
    def reset(self) -> None
```

**Métriques retournées par get_metrics():**
- `uptime_seconds`: Temps écoulé depuis le démarrage
- `logs_per_level`: Dict avec compteurs par niveau
- `logs_per_second`: Taux de logs (fenêtre glissante)
- `avg_log_size_bytes`: Taille moyenne des logs
- `recent_errors`: Liste des 10 dernières erreurs
- `total_logs`: Total de logs émis

### AlertManager

Gestionnaire d'alertes basées sur métriques.

```python
class AlertManager:
    def add_rule(
        self,
        name: str,
        condition: Callable[[Dict[str, Any]], bool],
        cooldown: int = 300,
        message: Optional[str] = None
    ) -> None
    
    def add_callback(self, callback: Callable[[str, str], None]) -> None
    
    def check_metrics(self, metrics: Dict[str, Any]) -> None
```

### HealthMonitor

Moniteur de santé automatique.

```python
class HealthMonitor:
    def __init__(
        self,
        logger: PyLoggerX,
        check_interval: int = 60
    )
    
    def start(self) -> None
    
    def stop(self) -> None
    
    def get_status(self) -> Dict[str, Any]
    
    # Propriétés
    @property
    def metrics_collector: MetricsCollector
    
    @property
    def alert_manager: AlertManager
```

**Status retourné par get_status():**
- `running`: Statut du monitoring
- `metrics`: Métriques du collecteur
- `logger_stats`: Statistiques du logger
- `logger_health`: Santé du logger

### print_dashboard

Fonction pour afficher le dashboard console.

```python
def print_dashboard(
    logger: PyLoggerX,
    clear_screen: bool = True
) -> None
```

---

## Variables d'Environnement Complètes

Liste exhaustive des variables d'environnement supportées:

```bash
# Général
PYLOGGERX_NAME=myapp
PYLOGGERX_LEVEL=INFO

# Sortie
PYLOGGERX_CONSOLE=true
PYLOGGERX_COLORS=false

# Fichiers
PYLOGGERX_JSON_FILE=/var/log/app.json
PYLOGGERX_TEXT_FILE=/var/log/app.log

# Rate Limiting
PYLOGGERX_RATE_LIMIT_ENABLED=true
PYLOGGERX_RATE_LIMIT_MESSAGES=100
PYLOGGERX_RATE_LIMIT_PERIOD=60

# Sampling
PYLOGGERX_SAMPLING_ENABLED=false
PYLOGGERX_SAMPLING_RATE=1.0

# Elasticsearch
PYLOGGERX_ELASTICSEARCH_URL=http://elasticsearch:9200
PYLOGGERX_ELASTICSEARCH_INDEX=logs
PYLOGGERX_ELASTICSEARCH_USERNAME=elastic
PYLOGGERX_ELASTICSEARCH_PASSWORD=changeme

# Loki
PYLOGGERX_LOKI_URL=http://loki:3100

# Sentry
PYLOGGERX_SENTRY_DSN=https://xxx@sentry.io/xxx
PYLOGGERX_SENTRY_ENVIRONMENT=production
PYLOGGERX_SENTRY_RELEASE=1.0.0

# Datadog
PYLOGGERX_DATADOG_API_KEY=your_api_key
PYLOGGERX_DATADOG_SITE=datadoghq.com
PYLOGGERX_DATADOG_SERVICE=myapp

# Slack
PYLOGGERX_SLACK_WEBHOOK=https://hooks.slack.com/services/xxx
PYLOGGERX_SLACK_CHANNEL=#alerts
PYLOGGERX_SLACK_USERNAME=PyLoggerX Bot

# Webhook
PYLOGGERX_WEBHOOK_URL=https://example.com/logs
PYLOGGERX_WEBHOOK_METHOD=POST

# Performance
PYLOGGERX_PERFORMANCE_TRACKING=true
PYLOGGERX_INCLUDE_CALLER=false

# Export
PYLOGGERX_BATCH_SIZE=100
PYLOGGERX_BATCH_TIMEOUT=5
PYLOGGERX_ASYNC_EXPORT=true
```

---

## Meilleures Pratiques

### Configuration

1. **Utiliser des fichiers de config par environnement**
   ```python
   config = load_config(
       config_file=f"config.{os.getenv('ENV', 'dev')}.json",
       from_env=True
   )
   ```

2. **Ne jamais commiter les secrets**
   - Utiliser des variables d'environnement
   - Utiliser des outils comme Vault, AWS Secrets Manager

3. **Valider la configuration au démarrage**
   ```python
   try:
       config = load_config(config_file="config.json")
   except ValueError as e:
       print(f"Config invalide: {e}")
       sys.exit(1)
   ```

4. **Documenter les configurations**
   - Créer des exemples de configuration
   - Documenter chaque paramètre

### Monitoring

1. **Toujours monitorer en production**
   ```python
   monitor = HealthMonitor(logger, check_interval=60)
   monitor.start()
   ```

2. **Configurer des alertes pertinentes**
   - Pas trop d'alertes (fatigue d'alerte)
   - Pas trop peu (problèmes non détectés)

3. **Exporter vers un système centralisé**
   - Prometheus + Grafana
   - Datadog
   - CloudWatch

4. **Tester les alertes régulièrement**
   ```python
   # Test mensuel
   logger.critical("TEST: Alerte critique", test=True)
   ```

### Performance

1. **Activer le rate limiting en production**
   ```python
   config['enable_rate_limit'] = True
   config['rate_limit_messages'] = 100
   ```

2. **Utiliser l'export asynchrone**
   ```python
   config['async_export'] = True
   ```

3. **Ajuster la taille des batchs**
   ```python
   config['batch_size'] = 50  # Plus petit pour latence faible
   config['batch_timeout'] = 2  # Timeout court
   ```

4. **Monitorer les métriques de performance**
   ```python
   stats = logger.get_performance_stats()
   if stats['avg_duration'] > 1.0:
       logger.warning("Performance dégradée")
   ```

## Exemples Réels

### 1. Application Web (FastAPI)

```python
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from pyloggerx import PyLoggerX
import time
import uuid

app = FastAPI()

# Configuration du logger
logger = PyLoggerX(
    name="fastapi_app",
    console=True,
    json_file="logs/web.json",
    
    # Export distant
    elasticsearch_url="http://elasticsearch:9200",
    sentry_dsn=os.getenv("SENTRY_DSN"),
    
    enrichment_data={
        "service": "web-api",
        "version": "2.0.0",
        "environment": os.getenv("ENVIRONMENT", "production")
    }
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware de logging pour toutes les requêtes"""
    request_id = str(uuid.uuid4())
    start_time = time.time()
    
    # Ajouter request_id au contexte
    with logger.context(request_id=request_id):
        logger.info("Requête reçue",
            method=request.method,
            path=request.url.path,
            client_ip=request.client.host,
            user_agent=request.headers.get("user-agent")
        )
        
        try:
            response = await call_next(request)
            duration = time.time() - start_time
            
            logger.info("Requête complétée",
                method=request.method,
                path=request.url.path,
                status_code=response.status_code,
                duration_ms=duration * 1000
            )
            
            # Ajouter request_id au header de réponse
            response.headers["X-Request-ID"] = request_id
            return response
            
        except Exception as e:
            duration = time.time() - start_time
            logger.exception("Erreur de requête",
                method=request.method,
                path=request.url.path,
                duration_ms=duration * 1000,
                error_type=type(e).__name__
            )
            raise

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Gestionnaire d'exceptions HTTP"""
    logger.warning("Exception HTTP",
        status_code=exc.status_code,
        detail=exc.detail,
        path=request.url.path
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )

@app.get("/")
def root():
    logger.info("Endpoint racine accédé")
    return {"status": "ok", "service": "web-api"}

@app.get("/health")
def health_check():
    """Health check avec métriques"""
    import psutil
    
    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory().percent
    
    status = "healthy"
    if cpu > 80 or memory > 80:
        status = "degraded"
        logger.warning("Service dégradé",
            cpu_percent=cpu,
            memory_percent=memory
        )
    
    logger.info("Health check",
        status=status,
        cpu_percent=cpu,
        memory_percent=memory
    )
    
    return {
        "status": status,
        "metrics": {
            "cpu_percent": cpu,
            "memory_percent": memory
        }
    }

@app.on_event("startup")
async def startup_event():
    logger.info("Application démarrée",
               workers=os.getenv("WEB_CONCURRENCY", 1))

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application arrêtée")
    logger.flush()  # Vider tous les buffers
    logger.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
```

### 2. Pipeline de Traitement de Données

```python
from pyloggerx import PyLoggerX
import pandas as pd
import sys

logger = PyLoggerX(
    name="data_pipeline",
    console=True,
    json_file="logs/pipeline.json",
    performance_tracking=True,
    
    # Alertes pour les échecs
    slack_webhook=os.getenv("SLACK_WEBHOOK"),
    
    enrichment_data={
        "pipeline": "data-processing",
        "version": "1.0.0"
    }
)

class DataPipeline:
    def __init__(self, input_file):
        self.input_file = input_file
        self.df = None
        
    def run(self):
        """Exécuter le pipeline complet"""
        logger.info("Pipeline démarré", input_file=self.input_file)
        
        try:
            self.load_data()
            self.validate_data()
            self.clean_data()
            self.transform_data()
            self.export_data()
            
            # Statistiques finales
            stats = logger.get_performance_stats()
            logger.info("Pipeline complété avec succès",
                       total_duration=stats["total_duration"],
                       operations=stats["total_operations"])
            
        except Exception as e:
            logger.exception("Pipeline échoué", error=str(e))
            sys.exit(1)
    
    def load_data(self):
        """Charger les données"""
        with logger.timer("Chargement des données"):
            try:
                self.df = pd.read_csv(self.input_file)
                logger.info("Données chargées",
                           rows=len(self.df),
                           columns=len(self.df.columns),
                           memory_mb=self.df.memory_usage(deep=True).sum() / 1024**2)
            except Exception as e:
                logger.error("Échec du chargement",
                           file=self.input_file,
                           error=str(e))
                raise
    
    def validate_data(self):
        """Valider les données"""
        with logger.timer("Validation des données"):
            required_columns = ['id', 'timestamp', 'value']
            missing_columns = [col for col in required_columns 
                             if col not in self.df.columns]
            
            if missing_columns:
                logger.error("Colonnes manquantes",
                           missing=missing_columns,
                           found=list(self.df.columns))
                raise ValueError(f"Colonnes manquantes: {missing_columns}")
            
            logger.info("Validation réussie")
    
    def clean_data(self):
        """Nettoyer les données"""
        with logger.timer("Nettoyage des données"):
            initial_rows = len(self.df)
            
            # Supprimer les doublons
            duplicates = self.df.duplicated().sum()
            self.df = self.df.drop_duplicates()
            
            # Supprimer les valeurs nulles
            null_counts = self.df.isnull().sum()
            self.df = self.df.dropna()
            
            removed_rows = initial_rows - len(self.df)
            
            logger.info("Données nettoyées",
                       initial_rows=initial_rows,
                       removed_rows=removed_rows,
                       duplicates_removed=duplicates,
                       remaining_rows=len(self.df),
                       null_values=null_counts.to_dict())
            
            if removed_rows > initial_rows * 0.5:
                logger.warning("Plus de 50% des lignes supprimées",
                             percent_removed=removed_rows/initial_rows*100)
    
    def transform_data(self):
        """Transformer les données"""
        with logger.timer("Transformation des données"):
            # Conversion de types
            self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
            self.df['value'] = pd.to_numeric(self.df['value'], errors='coerce')
            
            # Ajout de colonnes calculées
            self.df['year'] = self.df['timestamp'].dt.year
            self.df['month'] = self.df['timestamp'].dt.month
            
            logger.info("Transformation complétée",
                       new_columns=['year', 'month'])
    
    def export_data(self):
        """Exporter les données"""
        output_file = "output/processed_data.csv"
        
        with logger.timer("Export des données"):
            self.df.to_csv(output_file, index=False)
            
            file_size_mb = os.path.getsize(output_file) / 1024**2
            
            logger.info("Données exportées",
                       output_file=output_file,
                       rows=len(self.df),
                       file_size_mb=file_size_mb)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python pipeline.py <input_file>")
        sys.exit(1)
    
    pipeline = DataPipeline(sys.argv[1])
    pipeline.run()
```

### 3. Microservice avec Monitoring Complet

```python
from pyloggerx import PyLoggerX
from fastapi import FastAPI
import psutil
import time
import os

app = FastAPI()

# Logger principal
logger = PyLoggerX(
    name="microservice",
    console=True,
    json_file="logs/service.json",
    
    # Stack d'observabilité complète
    elasticsearch_url=os.getenv("ES_URL"),
    elasticsearch_index="microservice-logs",
    loki_url=os.getenv("LOKI_URL"),
    loki_labels={"service": "payment-processor", "env": "prod"},
    sentry_dsn=os.getenv("SENTRY_DSN"),
    datadog_api_key=os.getenv("DD_API_KEY"),
    slack_webhook=os.getenv("SLACK_WEBHOOK"),
    
    # Configuration avancée
    batch_size=50,
    enable_sampling=True,
    sampling_rate=0.5,  # 50% en production
    
    enrichment_data={
        "service": "payment-processor",
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "instance": os.getenv("HOSTNAME")
    }
)

@app.get("/health")
def health_check():
    """Health check détaillé"""
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    
    # Vérifier les dépendances
    dependencies = {
        "database": check_database(),
        "redis": check_redis(),
        "external_api": check_external_api()
    }
    
    all_healthy = all(dependencies.values())
    status = "healthy" if all_healthy and cpu < 80 and memory < 80 else "degraded"
    
    log_level = "info" if status == "healthy" else "warning"
    getattr(logger, log_level)("Health check",
        status=status,
        cpu_percent=cpu,
        memory_percent=memory,
        disk_percent=disk,
        dependencies=dependencies
    )
    
    return {
        "status": status,
        "metrics": {
            "cpu_percent": cpu,
            "memory_percent": memory,
            "disk_percent": disk
        },
        "dependencies": dependencies
    }

@app.get("/metrics")
def get_metrics():
    """Métriques de logging et performance"""
    log_stats = logger.get_stats()
    perf_stats = logger.get_performance_stats()
    
    return {
        "logging": log_stats,
        "performance": perf_stats,
        "system": {
            "cpu_percent": psutil.cpu_percent(),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage('/').percent
        }
    }

def check_database():
    try:
        # Vérifier la connexion DB
        # db.execute("SELECT 1")
        return True
    except:
        logger.error("Database health check failed")
        return False

def check_redis():
    try:
        # Vérifier Redis
        # redis_client.ping()
        return True
    except:
        logger.error("Redis health check failed")
        return False

def check_external_api():
    try:
        # Vérifier l'API externe
        # requests.get("https://api.example.com/health", timeout=2)
        return True
    except:
        logger.error("External API health check failed")
        return False
```

### 4. Worker Asynchrone avec Gestion d'Erreurs

```python
from pyloggerx import PyLoggerX
import asyncio
import aiohttp
from typing import List, Dict
import random

logger = PyLoggerX(
    name="async_worker",
    json_file="logs/worker.json",
    performance_tracking=True,
    
    # Alertes
    slack_webhook=os.getenv("SLACK_WEBHOOK"),
    
    enrichment_data={
        "worker_type": "async-processor",
        "version": "1.0.0"
    }
)

class AsyncWorker:
    def __init__(self, worker_id: str):
        self.worker_id = worker_id
        self.is_running = False
        self.processed_count = 0
        self.error_count = 0
        
    async def start(self):
        """Démarrer le worker"""
        self.is_running = True
        logger.info("Worker démarré", worker_id=self.worker_id)
        
        while self.is_running:
            try:
                await self.process_batch()
                await asyncio.sleep(5)
            except Exception as e:
                logger.exception("Erreur worker", worker_id=self.worker_id)
                await asyncio.sleep(10)
    
    async def process_batch(self):
        """Traiter un batch de jobs"""
        with logger.timer(f"Batch-{self.worker_id}"):
            jobs = await self.fetch_jobs()
            
            if not jobs:
                logger.debug("Aucun job à traiter", worker_id=self.worker_id)
                return
            
            logger.info("Batch récupéré",
                       worker_id=self.worker_id,
                       job_count=len(jobs))
            
            # Traiter en parallèle
            tasks = [self.process_job(job) for job in jobs]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Compter succès/échecs
            successes = sum(1 for r in results if not isinstance(r, Exception))
            failures = len(results) - successes
            
            self.processed_count += successes
            self.error_count += failures
            
            logger.info("Batch traité",
                       worker_id=self.worker_id,
                       successes=successes,
                       failures=failures,
                       total_processed=self.processed_count,
                       total_errors=self.error_count)
    
    async def fetch_jobs(self) -> List[Dict]:
        """Récupérer les jobs depuis la queue"""
        # Simuler la récupération de jobs
        await asyncio.sleep(0.1)
        return [{"id": f"job_{i}", "data": random.random()} 
                for i in range(random.randint(0, 10))]
    
    async def process_job(self, job: Dict):
        """Traiter un job individuel"""
        job_id = job["id"]
        
        try:
            logger.debug("Traitement job",
                        worker_id=self.worker_id,
                        job_id=job_id)
            
            # Simuler le traitement
            await asyncio.sleep(random.uniform(0.1, 0.5))
            
            # Simuler des échecs aléatoires (10%)
            if random.random() < 0.1:
                raise Exception("Job processing failed")
            
            logger.info("Job complété",
                       worker_id=self.worker_id,
                       job_id=job_id,
                       status="success")
            
        except Exception as e:
            logger.error("Job échoué",
                        worker_id=self.worker_id,
                        job_id=job_id,
                        error=str(e),
                        status="failed")
            raise
    
    def stop(self):
        """Arrêter le worker"""
        self.is_running = False
        logger.info("Worker arrêté",
                   worker_id=self.worker_id,
                   total_processed=self.processed_count,
                   total_errors=self.error_count)

async def main():
    # Démarrer plusieurs workers
    workers = [AsyncWorker(f"worker-{i}") for i in range(3)]
    
    tasks = [worker.start() for worker in workers]
    
    try:
        await asyncio.gather(*tasks)
    except KeyboardInterrupt:
        logger.info("Arrêt demandé")
        for worker in workers:
            worker.stop()

if __name__ == "__main__":
    asyncio.run(main())
```

---

## Meilleures Pratiques

### 1. Structurer les Logs pour le Parsing

Toujours utiliser des paires clé-valeur pour les données structurées:

```python
# BON - structuré
logger.info("Connexion utilisateur",
           user_id=123,
           username="john",
           ip="192.168.1.1",
           auth_method="oauth2")

# MAUVAIS - non structuré
logger.info(f"User john (ID: 123) logged in from 192.168.1.1 using OAuth2")
```

### 2. Utiliser les Niveaux de Log Appropriés

```python
# DEBUG - Informations de diagnostic détaillées
logger.debug("Cache hit", key="user:123", ttl=3600)

# INFO - Messages informatifs généraux
logger.info("Service démarré", port=8080, workers=4)

# WARNING - Quelque chose d'inattendu mais pas critique
logger.warning("Utilisation mémoire élevée",
              percent=85,
              threshold=80)

# ERROR - Une erreur s'est produite mais le service continue
logger.error("Requête échouée",
            query="SELECT...",
            error=str(e),
            retry_count=3)

# CRITICAL - Le service ne peut pas continuer
logger.critical("Connexion base de données perdue",
               retries_exhausted=True,
               last_error=str(e))
```

### 3. Inclure du Contexte dans les Logs

```python
# Contexte utilisateur
logger.add_enrichment(
    user_id=user.id,
    session_id=session.id,
    request_id=request_id,
    ip_address=request.remote_addr
)

# Tous les logs suivants incluront ce contexte
logger.info("Appel API", endpoint="/api/users")
```

### 4. Tracking de Performance

```python
# Utiliser les timers pour les opérations critiques
with logger.timer("Requête Base de Données"):
    result = expensive_query()

# Logger les durées pour analyse
start = time.time()
process_data()
duration = time.time() - start

if duration > 1.0:  # Seuil de performance
    logger.warning("Opération lente",
                  operation="process_data",
                  duration_seconds=duration)
```

### 5. Gestion des Exceptions

```python
try:
    risky_operation()
except SpecificException as e:
    logger.exception("Opération échouée",
                    operation="data_sync",
                    error_type=type(e).__name__,
                    recoverable=True)
    # Inclut automatiquement la stack trace

except Exception as e:
    logger.critical("Erreur inattendue",
                   operation="data_sync",
                   error=str(e))
    # Alerte immédiate via Slack/Sentry
```

### 6. Logging Adapté aux Conteneurs

```python
# Pour les applications conteneurisées
logger = PyLoggerX(
    name="container-app",
    console=True,  # Vers stdout/stderr
    colors=False,  # IMPORTANT pour les collecteurs
    json_file=None,  # Pas de fichiers en conteneur
    format_string='{"time":"%(asctime)s","level":"%(levelname)s","msg":"%(message)s"}'
)
```

### 7. Correlation IDs pour Systèmes Distribués

```python
import uuid

def handle_request(request):
    # Propager ou créer un correlation ID
    correlation_id = request.headers.get(
        'X-Correlation-ID',
        str(uuid.uuid4())
    )
    
    with logger.context(correlation_id=correlation_id):
        logger.info("Requête reçue",
                   method=request.method,
                   path=request.path)
        
        # Passer aux services downstream
        response = downstream_service.call(
            data,
            headers={'X-Correlation-ID': correlation_id}
        )
        
        logger.info("Requête complétée",
                   status=response.status_code)
    
    return response
```

### 8. Health Checks et Monitoring

```python
@app.get("/health")
def health():
    checks = {
        "database": check_db(),
        "cache": check_redis(),
        "queue": check_queue()
    }
    
    all_healthy = all(checks.values())
    
    if not all_healthy:
        failed = [k for k, v in checks.items() if not v]
        logger.error("Health check échoué",
                    failed_components=failed)
    
    return {
        "status": "healthy" if all_healthy else "unhealthy",
        "checks": checks
    }
```

### 9. Protection des Données Sensibles

```python
import hashlib

def login(username, password):
    # MAUVAIS - Ne jamais logger de données sensibles
    # logger.info("Tentative de connexion",
    #            username=username,
    #            password=password)
    
    # BON - Hash ou masquage
    logger.info("Tentative de connexion",
               username=username,
               password_hash=hashlib.sha256(password.encode()).hexdigest()[:8])
```

### 10. Rotation des Logs pour Services Long-Running

```python
# Éviter le remplissage du disque
logger = PyLoggerX(
    name="long-running-service",
    json_file="logs/service.json",
    max_bytes=10 * 1024 * 1024,  # 10MB
    backup_count=5,  # Garder 5 fichiers
    rotation_when="midnight"  # + rotation quotidienne
)
```

---

## Tests

### Tests Unitaires

```python
import pytest
import json
from pathlib import Path
from pyloggerx import PyLoggerX

def test_json_logging(tmp_path):
    """Tester la sortie JSON"""
    log_file = tmp_path / "test.json"
    
    logger = PyLoggerX(
        name="test_logger",
        json_file=str(log_file),
        console=False
    )
    
    logger.info("Message de test",
               test_id=123,
               status="success")
    
    assert log_file.exists()
    
    with open(log_file) as f:
        log_entry = json.loads(f.readline())
        assert log_entry["message"] == "Message de test"
        assert log_entry["test_id"] == 123
        assert log_entry["status"] == "success"

def test_performance_tracking(tmp_path):
    """Tester le tracking de performance"""
    logger = PyLoggerX(
        name="perf_test",
        performance_tracking=True,
        console=False
    )
    
    import time
    with logger.timer("Opération Test"):
        time.sleep(0.1)
    
    stats = logger.get_performance_stats()
    assert stats["total_operations"] == 1
    assert stats["avg_duration"] >= 0.1

def test_enrichment(tmp_path):
    """Tester l'enrichissement de contexte"""
    log_file = tmp_path / "test.json"
    
    logger = PyLoggerX(
        name="enrichment_test",
        json_file=str(log_file),
        console=False,
        enrichment_data={
            "app_version": "1.0.0",
            "environment": "test"
        }
    )
    
    logger.info("Test avec enrichissement")
    
    with open(log_file) as f:
        log_entry = json.loads(f.readline())
        assert log_entry["app_version"] == "1.0.0"
        assert log_entry["environment"] == "test"

def test_log_levels():
    """Tester les différents niveaux de log"""
    logger = PyLoggerX(name="level_test", console=False)
    
    # Ne devrait pas lever d'exception
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical message")

@pytest.fixture
def logger(tmp_path):
    """Fixture pour logger"""
    return PyLoggerX(
        name="test",
        json_file=str(tmp_path / "test.json"),
        console=False
    )

def test_remote_logging_mock(logger, monkeypatch):
    """Tester l'export distant (avec mock)"""
    import requests
    
    # Mock de la requête HTTP
    class MockResponse:
        status_code = 200
    
    def mock_post(*args, **kwargs):
        return MockResponse()
    
    monkeypatch.setattr(requests, "post", mock_post)
    
    # Logger avec webhook
    logger_remote = PyLoggerX(
        name="remote_test",
        webhook_url="http://example.com/logs",
        console=False
    )
    
    logger_remote.info("Test remote")
```

### Tests d'Intégration

```python
import pytest
import requests
from pyloggerx import PyLoggerX

@pytest.fixture(scope="module")
def app_with_logging():
    """Démarrer l'application avec logging"""
    logger = PyLoggerX(
        name="integration_test",
        json_file="logs/integration.json"
    )
    
    logger.info("Tests d'intégration démarrés")
    
    # Démarrer votre app ici
    yield app
    
    logger.info("Tests d'intégration terminés")
    logger.close()

def test_api_endpoint(app_with_logging):
    """Tester un endpoint API avec logging"""
    response = requests.get("http://localhost:8080/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_error_handling(app_with_logging):
    """Tester la gestion d'erreurs"""
    response = requests.get("http://localhost:8080/api/invalid")
    assert response.status_code == 404
```

---

## Dépannage

### Problème: Les logs n'apparaissent pas

**Solution:**
```python
# Vérifier le niveau de log
logger.set_level("DEBUG")

# Vérifier les handlers
print(logger.logger.handlers)

# Forcer le flush
logger.flush()

# S'assurer que le répertoire existe
import os
os.makedirs("logs", exist_ok=True)
```

### Problème: Erreurs de permissions fichier

**Solution:**
```python
# Utiliser un chemin absolu
import os
log_path = os.path.join(os.getcwd(), "logs", "app.json")

# S'assurer des permissions d'écriture
os.makedirs(os.path.dirname(log_path), exist_ok=True, mode=0o755)

# Vérifier les permissions
if not os.access(os.path.dirname(log_path), os.W_OK):
    raise PermissionError(f"Pas de permission d'écriture: {log_path}")
```

### Problème: Couleurs ne fonctionnent pas dans les conteneurs

**Solution:**
```python
# Désactiver les couleurs pour les conteneurs
logger = PyLoggerX(
    name="container-app",
    colors=False  # Important pour les collecteurs de logs
)
```

### Problème: Fichiers de log trop volumineux

**Solution:**
```python
# Utiliser la rotation
logger = PyLoggerX(
    json_file="logs/app.json",
    max_bytes=5 * 1024 * 1024,  # 5MB
    backup_count=3,  # Garder 3 backups
    rotation_when="midnight"  # + rotation quotidienne
)
```

### Problème: Surcharge de performance

**Solution:**
```python
# Augmenter le niveau de log en production
logger.set_level("WARNING")

# Désactiver le tracking de performance
logger = PyLoggerX(performance_tracking=False)

# Activer l'échantillonnage
logger = PyLoggerX(
    enable_sampling=True,
    sampling_rate=0.1  # Garder 10% des logs
)

# Utiliser l'export asynchrone
logger = PyLoggerX(
    async_export=True,
    queue_size=1000
)
```

### Problème: Logs distants non envoyés

**Solution:**
```python
# Activer le logging de debug
import logging
logging.basicConfig(level=logging.DEBUG)

# Vérifier la connectivité
import requests
try:
    response = requests.get("http://elasticsearch:9200")
    print(f"ES Status: {response.status_code}")
except Exception as e:
    print(f"Erreur de connexion: {e}")

# Forcer le flush avant la fermeture
logger.flush()
logger.close()

# Vérifier la configuration du batch
logger = PyLoggerX(
    elasticsearch_url="http://elasticsearch:9200",
    batch_size=10,  # Batch plus petit pour test
    batch_timeout=1  # Timeout court
)
```

### Problème: Utilisation mémoire élevée avec logging distant

**Solution:**
```python
# Ajuster les paramètres de batch
logger = PyLoggerX(
    elasticsearch_url="http://elasticsearch:9200",
    batch_size=50,  # Batches plus petits
    batch_timeout=2,  # Timeout plus court
    queue_size=500,  # Queue plus petite
    async_export=True  # Export asynchrone
)

# Activer l'échantillonnage pour réduire le volume
logger = PyLoggerX(
    enable_sampling=True,
    sampling_rate=0.5  # 50% des logs
)
```

---

## Référence API

### Classe PyLoggerX

#### Constructeur

```python
PyLoggerX(
    name: str = "PyLoggerX",
    level: str = "INFO",
    console: bool = True,
    colors: bool = True,
    json_file: Optional[str] = None,
    text_file: Optional[str] = None,
    max_bytes: int = 10 * 1024 * 1024,
    backup_count: int = 5,
    rotation_when: str = "midnight",
    rotation_interval: int = 1,
    format_string: Optional[str] = None,
    include_caller: bool = False,
    performance_tracking: bool = False,
    enrichment_data: Optional[Dict[str, Any]] = None,
    # Elasticsearch
    elasticsearch_url: Optional[str] = None,
    elasticsearch_index: str = "pyloggerx",
    elasticsearch_username: Optional[str] = None,
    elasticsearch_password: Optional[str] = None,
    # Loki
    loki_url: Optional[str] = None,
    loki_labels: Optional[Dict[str, str]] = None,
    # Sentry
    sentry_dsn: Optional[str] = None,
    sentry_environment: str = "production",
    # Datadog
    datadog_api_key: Optional[str] = None,
    datadog_site: str = "datadoghq.com",
    # Slack
    slack_webhook: Optional[str] = None,
    slack_channel: Optional[str] = None,
    # Webhook
    webhook_url: Optional[str] = None,
    webhook_method: str = "POST",
    # Avancé
    enable_sampling: bool = False,
    sampling_rate: float = 1.0,
    batch_size: int = 100,
    batch_timeout: int = 5,
    enable_rate_limit= bool = True,
    rate_limit_messages= int = 2,
    rate_limit_period= int = 10,
    async_export: bool = True
)
```

#### Méthodes de Logging

```python
debug(message: str, **kwargs) -> None
info(message: str, **kwargs) -> None
warning(message: str, **kwargs) -> None
error(message: str, **kwargs) -> None
critical(message: str, **kwargs) -> None
exception(message: str, **kwargs) -> None  # Inclut la traceback
```

#### Méthodes de Configuration

```python
set_level(level: str) -> None
add_context(**kwargs) -> None
add_enrichment(**kwargs) -> None
add_filter(filter_obj: logging.Filter) -> None
remove_filter(filter_obj: logging.Filter) -> None
```

#### Méthodes de Performance

```python
timer(operation_name: str) -> ContextManager
get_performance_stats() -> Dict[str, Any]
clear_performance_stats() -> None
```

#### Méthodes Utilitaires

```python
get_stats() -> Dict[str, Any]
flush() -> None  # Vider tous les buffers
close() -> None  # Fermer tous les handlers
context(**kwargs) -> ContextManager  # Contexte temporaire
```

### Logger Global

```python
from pyloggerx import log

# Utiliser le logger global par défaut
log.info("Logging rapide sans configuration")
log.error("Erreur", error_code=500)
```

---

## Contribution

Les contributions sont les bienvenues ! Suivez ces étapes :

### Configuration de Développement

```bash
# Cloner le dépôt
git clone https://github.com/yourusername/pyloggerx.git
cd pyloggerx

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Installer en mode développement
pip install -e ".[dev]"

# Installer les hooks pre-commit
pre-commit install
```

### Exécuter les Tests

```bash
# Tous les tests
pytest

# Avec couverture
pytest --cov=pyloggerx --cov-report=html

# Tests spécifiques
pytest tests/test_core.py -v

# Tests avec sortie
pytest -v -s
```

### Style de Code

```bash
# Formater le code
black pyloggerx/
isort pyloggerx/

# Vérifier le style
flake8 pyloggerx/
pylint pyloggerx/

# Vérification de types
mypy pyloggerx/
```

### Soumettre des Modifications

1. Fork le dépôt
2. Créer une branche: `git checkout -b feature/amazing-feature`
3. Faire vos modifications
4. Ajouter des tests pour les nouvelles fonctionnalités
5. S'assurer que les tests passent: `pytest`
6. Commit: `git commit -m 'Add amazing feature'`
7. Push: `git push origin feature/amazing-feature`
8. Ouvrir une Pull Request

### Directives de Contribution

- Suivre PEP 8 pour le style de code
- Ajouter des docstrings pour toutes les fonctions publiques
- Écrire des tests pour toutes les nouvelles fonctionnalités
- Mettre à jour la documentation si nécessaire
- S'assurer que tous les tests passent avant de soumettre

---

## Roadmap

### Version 3.1.0 (Planifié - Q2 2025)
- Support de logging asynchrone natif
- Formatters additionnels (Logfmt, GELF)
- Support AWS CloudWatch Logs
- Support Google Cloud Logging
- Métriques intégrées (histogrammes, compteurs)

### Version 3.5.0 (Planifié - Q3 2025)
- Dashboard de monitoring intégré
- Support Apache Kafka pour logs streaming
- Compression automatique des logs archivés
- Support de chiffrement des logs sensibles

### Version 4.0.0 (Futur)
- Tracing distribué intégré (OpenTelemetry complet)
- Machine learning pour détection d'anomalies
- Alerting avancé avec règles personnalisées
- Support multi-tenant

---

## FAQ

**Q: PyLoggerX est-il prêt pour la production ?**
R: Oui, PyLoggerX suit les meilleures pratiques de logging Python et est utilisé en production par plusieurs entreprises.

**Q: PyLoggerX fonctionne-t-il avec le logging existant ?**
R: Oui, PyLoggerX encapsule le module logging standard de Python et est compatible avec les handlers existants.

**Q: Comment faire une rotation des logs par temps plutôt que par taille ?**
R: Utilisez le paramètre `rotation_when` avec des valeurs comme "midnight", "H" (horaire), ou "D" (quotidien).

**Q: Puis-je logger vers plusieurs fichiers simultanément ?**
R: Oui, spécifiez à la fois `json_file` et `text_file`.

**Q: PyLoggerX est-il thread-safe ?**
R: Oui, PyLoggerX utilise le module logging de Python qui est thread-safe.

**Q: Comment intégrer avec les outils d'agrégation de logs existants ?**
R: Utilisez le format JSON qui est compatible avec la plupart des outils (ELK, Splunk, Datadog, etc.) ou les exporters directs.

**Q: Quelle est la surcharge de performance ?**
R: L'impact est minimal. Utilisez l'échantillonnage et l'export asynchrone pour les applications à très haut volume.

**Q: Les logs sont-ils envoyés de manière synchrone ou asynchrone ?**
R: Par défaut, les exports distants sont asynchrones (non-bloquants). Vous pouvez désactiver avec `async_export=False`.

**Q: Comment gérer les logs sensibles ?**
R: Ne loggez jamais de données sensibles directement. Utilisez le hashing ou le masquage.

**Q: Puis-je utiliser PyLoggerX dans des fonctions AWS Lambda ?**
R: Oui, mais désactivez les fichiers locaux et utilisez console ou export distant uniquement.

---

## Licence

Ce projet est sous licence MIT :

```
MIT License

Copyright (c) 2025 PyLoggerX Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## Support & Communauté

- **Documentation**: [https://pyloggerx.readthedocs.io](https://pyloggerx.readthedocs.io)
- **GitHub Issues**: [https://github.com/yourusername/pyloggerx/issues](https://github.com/yourusername/pyloggerx/issues)
- **Discussions**: [https://github.com/yourusername/pyloggerx/discussions](https://github.com/yourusername/pyloggerx/discussions)
- **PyPI**: [https://pypi.org/project/pyloggerx/](https://pypi.org/project/pyloggerx/)
- **Stack Overflow**: Tag `pyloggerx`
- **Discord**: [https://discord.gg/pyloggerx](https://discord.gg/pyloggerx)

---

## Remerciements

- Construit sur le module `logging` standard de Python
- Inspiré par des bibliothèques modernes comme structlog et loguru
- Merci à tous les contributeurs et utilisateurs
- Remerciements spéciaux à la communauté DevOps pour les retours

---

## Changelog

### v1.0.0 (2025-09-15)

**Fonctionnalités Majeures**
- Support de logging distant (Elasticsearch, Loki, Sentry, Datadog, Slack)
- Échantillonnage de logs pour applications à haut volume
- Limitation de débit (rate limiting)
- Filtrage avancé (niveau, pattern, personnalisé)
- Traitement par batch pour exports distants
- Support webhook personnalisé
- Export asynchrone non-bloquant
- Enrichissement de contexte amélioré

**Améliorations**
- Performance optimisée pour exports distants
- Meilleure gestion des erreurs d'export
- Documentation étendue avec exemples DevOps
- Support amélioré pour Kubernetes et conteneurs

**Nouvelles Fonctionnalités**
- Tracking de performance avec timers
- Formatters personnalisés
- Rotation des logs (taille et temps)
- Enrichissement de contexte global
- Meilleure gestion des exceptions

**Corrections**
- Correction de fuites mémoire dans certains scénarios
- Amélioration de la gestion des reconnexions
- Correction de problèmes de rotation de fichiers

---

**Fait avec soin pour la communauté Python et DevOps**