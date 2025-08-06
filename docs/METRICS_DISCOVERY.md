# OvenMediaEngine API Endpoints & Metrics Documentation

This document provides:

- A list of OvenMediaEngine REST API endpoints used by the OvenMediaEngine Exporter.
- Definitions of all collected metrics and their real-world use cases.
- Guidance on how these metrics help in monitoring and optimizing streaming infrastructure.

## 1. API Endpoints Used by the Exporter

### 1.1 Get Virtual Hosts

**Endpoint:**
```
GET {{base_url}}/v1/vhosts
```

**Purpose:**
Retrieves a list of available virtual hosts to scrape streams dynamically.

### 1.2 Get Streams for a Virtual Host

**Endpoint:**
```
GET {{base_url}}/v1/vhosts/{vhost}/apps/app/streams
```

**Purpose:**
Lists available streams under a virtual host for metric collection.

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

### 1.4 Get Stream Statistics

**Endpoint:**
```
GET {{base_url}}/v1/stats/current/vhosts/{vhost}/apps/app/streams/{streamName}
```

**Purpose:**
Retrieves real-time operational metrics for each stream.

## 2. Complete Metrics Reference Table

| Metric Name | Variable Name | Type | Use Case (Benefit) | Description | Labels | Example Value |
|-------------|---------------|------|-------------------|-------------|--------|---------------|
| Stream Up/Down | `oven_stream_up` | Gauge | Helps detect if a stream is live or has dropped | Stream availability (1 = up, 0 = down) | vhost, stream | 1 |
| Latest Bitrate | `oven_stream_bitrate_latest_bps` | Gauge | Monitors real-time stream quality and bandwidth usage | Latest bitrate in bits per second | vhost, stream | 3200000 |
| Average Bitrate | `oven_stream_bitrate_avg_bps` | Gauge | Identifies long-term stream quality trends | Average bitrate in bits per second | vhost, stream | 3100000 |
| Latest Framerate | `oven_stream_framerate_latest_fps` | Gauge | Checks if stream FPS is stable or dropping | Latest frame rate in frames per second | vhost, stream | 30 |
| Average Framerate | `oven_stream_framerate_avg_fps` | Gauge | Monitors playback smoothness over time | Average frame rate in frames per second | vhost, stream | 29.8 |
| Resolution Width | `oven_stream_resolution_width_pixels` | Gauge | Detects if stream resolution changes dynamically | Video resolution width in pixels | vhost, stream | 1920 |
| Resolution Height | `oven_stream_resolution_height_pixels` | Gauge | Detects resolution drops due to network or encoder issues | Video resolution height in pixels | vhost, stream | 1080 |
| Keyframe Interval | `oven_stream_keyframe_interval_latest` | Gauge | Helps troubleshoot playback buffering and seek issues | Latest keyframe interval in frames | vhost, stream | 48 |
| Avg Keyframe Interval | `oven_stream_keyframe_interval_avg` | Gauge | Detects keyframe stability over time | Average keyframe interval in frames | vhost, stream | 50 |
| B-Frames Usage | `oven_stream_has_bframes` | Gauge | Identifies encoder type, potential playback latency impact | Whether B-frames are used (1 = yes, 0 = no) | vhost, stream | 1 |
| Input Throughput | `oven_stream_throughput_in_bps` | Gauge | Monitors incoming data rate to server | Current input throughput in bits per second | vhost, stream | 2850000 |
| Output Throughput | `oven_stream_throughput_out_bps` | Gauge | Monitors outgoing data rate to viewers | Current output throughput in bits per second | vhost, stream | 2700000 |
| Last Input Throughput | `oven_stream_last_throughput_in_bps` | Gauge | Shows last sampled data spike or drop | Last sampled input throughput in bits per second | vhost, stream | 2845000 |
| Last Output Throughput | `oven_stream_last_throughput_out_bps` | Gauge | Shows last sampled output traffic | Last sampled output throughput in bits per second | vhost, stream | 2730000 |
| Max Input Throughput | `oven_stream_max_throughput_in_bps` | Gauge | Detects peak incoming bandwidth usage | Maximum input throughput observed in bits per second | vhost, stream | 3000000 |
| Max Output Throughput | `oven_stream_max_throughput_out_bps` | Gauge | Detects peak outgoing bandwidth usage | Maximum output throughput observed in bits per second | vhost, stream | 2900000 |
| Active Connections | `oven_stream_active_connections` | Gauge | Tracks number of connected clients per protocol | Active connections by protocol | vhost, stream, protocol | 5 |
| Created Timestamp | `oven_stream_created_timestamp` | Gauge | Helps track when stream started | Unix timestamp of stream creation | vhost, stream | 1712345678 |
| Last Received Timestamp | `oven_stream_last_recv_timestamp` | Gauge | Detects if input feed has stalled | Unix timestamp of last data received | vhost, stream | 1712345685 |
| Last Sent Timestamp | `oven_stream_last_sent_timestamp` | Gauge | Detects if viewers are receiving data | Unix timestamp of last data sent | vhost, stream | 1712345690 |
| Last Update Timestamp | `oven_stream_last_updated_timestamp` | Gauge | Checks exporter freshness and last stats update | Unix timestamp of last stats update | vhost, stream | 1712345700 |
| Max Connection Time | `oven_stream_max_total_connection_time` | Gauge | Shows longest viewer session duration | Maximum total connection time in seconds | vhost, stream | 3600 |
| Total Bytes In | `oven_stream_total_bytes_in` | Counter | Tracks total data ingested since stream start | Total bytes received | vhost, stream | 124523456 |
| Total Bytes Out | `oven_stream_total_bytes_out` | Counter | Tracks total data sent to viewers | Total bytes sent | vhost, stream | 120423400 |
| Total Connections | `oven_stream_total_connections` | Counter | Monitors total number of viewers that connected since start | Total connections since start | vhost, stream | 120 |
| Codec Information | `oven_stream_codec_info` | Info | Helps identify stream codec used (for troubleshooting or metrics) | Codec information (e.g., video/audio codecs) | vhost, stream, codec | h264 |


## 3. Practical Use Cases

### Quality Monitoring
- Detect input bitrate drops (`avgThroughputIn`, `oven_stream_bitrate_latest_bps`) indicating poor camera feed or network problems.
- Monitor framerate stability (`oven_stream_framerate_latest_fps`, `oven_stream_framerate_avg_fps`) for smooth playback.
- Track resolution changes (`oven_stream_resolution_width_pixels`, `oven_stream_resolution_height_pixels`) for adaptive streaming issues.

### Viewer Analytics  
- Use connection counts (`connections.*`, `oven_stream_active_connections`) to understand audience size and protocol usage.
- Monitor session durations (`oven_stream_max_total_connection_time`) for engagement metrics.
- Track total viewer count over time (`oven_stream_total_connections`).

### Infrastructure Scaling
- Use `maxThroughputOut`, `oven_stream_max_throughput_out_bps` and `connections.total` for auto-scaling CDN or streaming nodes.
- Monitor peak usage patterns for capacity planning.

### Billing and Cost Reports
- Use `totalBytesIn/Out`, `oven_stream_total_bytes_in/out` for bandwidth consumption tracking.
- Calculate data transfer costs based on actual usage.

### Uptime and SLA Reporting
- Use `createdTime`, `lastRecvTime`, `lastSentTime`, and timestamp metrics for stream availability audits.
- Monitor stream health with `oven_stream_up` metric.

### Technical Troubleshooting
- Analyze codec information (`oven_stream_codec_info`) for compatibility issues.
- Monitor keyframe intervals (`oven_stream_keyframe_interval_latest`) for playback problems.
- Check B-frame usage (`oven_stream_has_bframes`) for latency optimization.

## 4. Dynamic Scraping Flow

1. Fetch all `/vhosts`.
2. For each vhost, list `/streams`.
3. For each stream, fetch `/streams/{streamName}` and `/stats/current`.
4. Export all metrics to Prometheus with labels:
   - `vhost`
   - `stream_name` 
   - `app`
   - `source_type`
   - `protocol` (for connection metrics)
   - `codec` (for codec info metrics)

## 5. Metric Types Explanation

- **Gauge**: Metrics that can go up or down (e.g., current connections, bitrate)
- **Counter**: Metrics that only increase (e.g., total bytes transferred, total connections)
- **Info**: Informational metrics that provide metadata (e.g., codec information)

---

**Last updated:** 2025-08-06
