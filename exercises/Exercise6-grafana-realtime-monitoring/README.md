# Exercise 6 — Real-Time Operations Monitoring and Alerting

Implements the ZIP assignment with Python `prometheus-client`, Prometheus alert rules, Grafana, and a Jenkins pipeline.

## Start the monitoring stack

From the repository root in PowerShell:

```powershell
docker compose -f exercises/06-grafana-realtime-monitoring/compose.yaml up -d --build
```

Open:
- Metrics: http://localhost:8000/metrics
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (default login `admin` / `admin`)

The Grafana Prometheus data source and four-panel dashboard are provisioned automatically to save setup time. The panels are Total Deliveries, Pending Deliveries, On-the-Way Deliveries, and Average Delivery Time. Prometheus alert rules cover pending deliveries above 10 and average delivery time above 30 seconds.

## Quick validation

```powershell
docker compose -f exercises/06-grafana-realtime-monitoring/compose.yaml ps
Invoke-RestMethod http://localhost:8000/metrics | Select-String -Pattern "total_deliveries|pending_deliveries|on_the_way_deliveries|average_delivery_time"
```

The `Jenkinsfile` expects a Jenkins agent with Python 3, Docker CLI, and `docker-compose` available. Exercise 7 provides the Docker-enabled Jenkins setup used by the later exercises.

## Notes on the source instructions

The source manual uses host networking and a Linux bridge IP. This Compose setup instead puts the three services on one Compose network, so Prometheus scrapes `delivery-metrics:8000` and Grafana uses `http://prometheus:9090`, which works with Docker Desktop as well as Linux Docker.
