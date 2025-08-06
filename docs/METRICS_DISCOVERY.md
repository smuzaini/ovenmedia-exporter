
# OvenMediaEngine API Endpoints & Metrics Documentation

This document provides:
- A list of OvenMediaEngine REST API endpoints used by the **OvenMediaEngine Exporter**.
- Definitions of all collected metrics and their real-world use cases.
- Guidance on how these metrics help in monitoring and optimizing streaming infrastructure.

---

## 1. API Endpoints Used by the Exporter

### 1.1 Get Virtual Hosts
**Endpoint:**  
```
GET {{base_url}}/v1/vhosts
```
**Purpose:**  
Retrieves a list of available virtual hosts to scrape streams dynamically.

---

### 1.2 Get Streams for a Virtual Host
**Endpoint:**  
```
GET {{base_url}}/v1/vhosts/{vhost}/apps/app/streams
```
**Purpose:**  
Lists available streams under a virtual host for metric collection.

---

### 1.3 Get Stream Information
**Endpoint:**  
```
GET {{base_url}}/v1/vhosts/{vhost}/apps/app/streams/{streamName}
```
**Purpose:**  
Fetches technical details about a given stream:
- Source type (e.g., RTSP Pull, Push)
- Source URL
- Codec information
- Resolution
- Track metadata

---

### 1.4 Get Stream Statistics
**Endpoint:**  
```
GET {{base_url}}/v1/stats/current/vhosts/{vhost}/apps/app/streams/{streamName}
```
**Purpose:**  
Retrieves real-time operational metrics for each stream.

---

## 2. Metrics Definitions & Use Cases

| **Metric** | **Definition** | **Use Cases** |
|------------|----------------|----------------|
| **avgThroughputIn** | Average inbound bitrate (bps) received from the stream source. | Detect network stability of incoming feeds and ensure proper ingest rates. |
| **avgThroughputOut** | Average outbound bitrate (bps) sent to viewers or downstream services. | Monitor distribution quality and ensure enough output data is delivered to clients. |
| **lastThroughputIn** | Latest measured input bitrate (bps). | Spot-check recent stream health or fluctuations in source feed quality. |
| **lastThroughputOut** | Latest measured output bitrate (bps). | Identify recent issues with stream delivery or transcoding performance. |
| **maxThroughputIn** | Maximum inbound bitrate recorded during the session. | Detect peak input bandwidth usage for capacity planning. |
| **maxThroughputOut** | Maximum outbound bitrate recorded during the session. | Detect peak outbound usage for scaling decisions. |
| **totalBytesIn** | Total bytes received for the stream since start. | Measure ingestion volume for billing, reporting, or long-term monitoring. |
| **totalBytesOut** | Total bytes sent to clients since start. | Track total delivery volume, useful for CDN or bandwidth cost tracking. |
| **connections.file** | Number of file-based connections to the stream. | Monitor stream recordings or file-based consumers. |
| **connections.hlsv3** | Number of HLS v3 clients connected. | Measure viewer engagement over HLS v3 protocol. |
| **connections.llhls** | Number of Low Latency HLS clients connected. | Identify ultra-low latency stream viewers for special monitoring. |
| **connections.webrtc** | Number of WebRTC clients connected. | Monitor real-time viewers for latency-sensitive streams. |
| **connections.srt** | Number of Secure Reliable Transport connections active. | Track SRT ingest or delivery for professional broadcast feeds. |
| **connections.total** | Total active connections across all protocols. | Overall measure of concurrent viewers or consumers of a stream. |
| **createdTime** | Timestamp when the stream was first ingested. | Used for tracking stream uptime or session duration. |
| **lastRecvTime** | Last timestamp data was received from the source. | Detect if the source feed has stopped sending data. |
| **lastSentTime** | Last timestamp data was sent to viewers. | Detect delivery interruptions or streaming output issues. |

---

## 3. Practical Use Cases

1. **Quality Monitoring:**  
   - Detect input bitrate drops (`avgThroughputIn`) indicating poor camera feed or network problems.
2. **Viewer Analytics:**  
   - Use connection counts (`connections.*`) to understand audience size and protocol usage.
3. **Infrastructure Scaling:**  
   - Use `maxThroughputOut` and `connections.total` for auto-scaling CDN or streaming nodes.
4. **Billing and Cost Reports:**  
   - Use `totalBytesIn/Out` for bandwidth consumption tracking.
5. **Uptime and SLA Reporting:**  
   - Use `createdTime`, `lastRecvTime`, and `lastSentTime` for stream availability audits.

---

## 4. Dynamic Scraping Flow

1. Fetch all `/vhosts`.  
2. For each vhost, list `/streams`.  
3. For each stream, fetch `/streams/{streamName}` and `/stats/current`.  
4. Export all metrics to Prometheus with labels:  
   - `vhost`  
   - `stream_name`  
   - `app`  
   - `source_type`  

---

_Last updated: 2025-08-05_