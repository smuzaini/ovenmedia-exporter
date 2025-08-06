# OvenMedia Exporter

OvenMedia Exporter is a **Prometheus metrics exporter** built in Python to expose streaming metrics from [OvenMediaEngine](https://airensoft.gitbook.io/ovenmediaengine/).  
It fetches data from the OvenMediaEngine REST API (`/v1/stats`) and exposes them on a `/metrics` endpoint for Prometheus scraping.

This is the **first version (Python)** of the exporter.  
Future updates are planned to:
- Improve performance
- Add more metrics
- Provide a **Go-based version** for production use

---

## 1. Build Docker Image

From the project root folder:

```bash
docker build -t ovenmedia-exporter:latest .
```

## 2. Run Exporter

Run the container and set the connection to your OvenMediaEngine API:

```bash
docker run -d --name ovenmedia-exporter -p 8000:8000 \
  -e OVEN_API_BASE_URL="http://ovenmedia:8081" \
  -e OVEN_API_TOKEN="test-token" \
  ovenmedia-exporter:latest
```

* Replace `ovenmedia` with your container name or `localhost` if running locally.
* `OVEN_API_TOKEN` is only required if your OvenMediaEngine API needs authentication.

## 3. Access Metrics

Once the exporter is running, access the metrics at:

```
http://localhost:8000/metrics
```

You can then configure **Prometheus** to scrape this endpoint:

```yaml
scrape_configs:
  - job_name: 'ovenmedia-exporter'
    static_configs:
      - targets: ['host.docker.internal:8000']
```

## 4. Configuration Options

You can configure the exporter in **two ways**:

### a) Config File (`config/config.yaml`)

```yaml
api:
  base_url: "http://ovenmedia:8081"
  token: "test-token"
debug: false
```

### b) Environment Variables (override config file)

```bash
OVEN_API_BASE_URL=http://ovenmedia:8081
OVEN_API_TOKEN=test-token
```

Environment variables take priority over the config file if both are provided.

## 5. Development Setup (Run Locally)

If you prefer to run without Docker:

```bash
# Install dependencies
pip install -r requirements.txt

# Run exporter
python src/main.py
```

Then access metrics at:

```
http://127.0.0.1:8000/metrics
```



## 6. License

This project is licensed under the **MIT License**. See the LICENSE file for details.

**👤 Author:** Sulaiman AlMuzaini  
**📅 Year:** 2025