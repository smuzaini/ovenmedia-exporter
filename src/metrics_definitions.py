from prometheus_client import Gauge, Counter, Info

# --- Gauges ---
oven_stream_up = Gauge('oven_stream_up', 'Stream availability (1=up, 0=down)', ['vhost', 'stream'])
oven_stream_bitrate_latest_bps = Gauge('oven_stream_bitrate_latest_bps', 'Latest bitrate (bps)', ['vhost', 'stream'])
oven_stream_bitrate_avg_bps = Gauge('oven_stream_bitrate_avg_bps', 'Average bitrate (bps)', ['vhost', 'stream'])
oven_stream_framerate_latest_fps = Gauge('oven_stream_framerate_latest_fps', 'Latest framerate (fps)', ['vhost', 'stream'])
oven_stream_framerate_avg_fps = Gauge('oven_stream_framerate_avg_fps', 'Average framerate (fps)', ['vhost', 'stream'])
oven_stream_resolution_width_pixels = Gauge('oven_stream_resolution_width_pixels', 'Video resolution width (pixels)', ['vhost', 'stream'])
oven_stream_resolution_height_pixels = Gauge('oven_stream_resolution_height_pixels', 'Video resolution height (pixels)', ['vhost', 'stream'])
oven_stream_keyframe_interval_latest = Gauge('oven_stream_keyframe_interval_latest', 'Latest keyframe interval (frames)', ['vhost', 'stream'])
oven_stream_keyframe_interval_avg = Gauge('oven_stream_keyframe_interval_avg', 'Average keyframe interval (frames)', ['vhost', 'stream'])
oven_stream_has_bframes = Gauge('oven_stream_has_bframes', 'Whether B-frames are used (1=yes, 0=no)', ['vhost', 'stream'])
oven_stream_throughput_in_bps = Gauge('oven_stream_throughput_in_bps', 'Current input throughput (bps)', ['vhost', 'stream'])
oven_stream_throughput_out_bps = Gauge('oven_stream_throughput_out_bps', 'Current output throughput (bps)', ['vhost', 'stream'])
oven_stream_last_throughput_in_bps = Gauge('oven_stream_last_throughput_in_bps', 'Last sampled input throughput (bps)', ['vhost', 'stream'])
oven_stream_last_throughput_out_bps = Gauge('oven_stream_last_throughput_out_bps', 'Last sampled output throughput (bps)', ['vhost', 'stream'])
oven_stream_max_throughput_in_bps = Gauge('oven_stream_max_throughput_in_bps', 'Maximum input throughput (bps)', ['vhost', 'stream'])
oven_stream_max_throughput_out_bps = Gauge('oven_stream_max_throughput_out_bps', 'Maximum output throughput (bps)', ['vhost', 'stream'])
oven_stream_active_connections = Gauge('oven_stream_active_connections', 'Active connections by protocol', ['vhost', 'stream', 'protocol'])
oven_stream_created_timestamp = Gauge('oven_stream_created_timestamp', 'Unix timestamp of stream creation', ['vhost', 'stream'])
oven_stream_last_recv_timestamp = Gauge('oven_stream_last_recv_timestamp', 'Unix timestamp of last data received', ['vhost', 'stream'])
oven_stream_last_sent_timestamp = Gauge('oven_stream_last_sent_timestamp', 'Unix timestamp of last data sent', ['vhost', 'stream'])
oven_stream_last_updated_timestamp = Gauge('oven_stream_last_updated_timestamp', 'Unix timestamp of last stats update', ['vhost', 'stream'])
oven_stream_max_total_connection_time = Gauge('oven_stream_max_total_connection_time', 'Maximum total connection time (seconds)', ['vhost', 'stream'])

# --- Counters ---
oven_stream_total_bytes_in = Counter('oven_stream_total_bytes_in', 'Total bytes received', ['vhost', 'stream'])
oven_stream_total_bytes_out = Counter('oven_stream_total_bytes_out', 'Total bytes sent', ['vhost', 'stream'])
oven_stream_total_connections = Counter('oven_stream_total_connections', 'Total connections since start', ['vhost', 'stream'])

# --- Info ---
oven_stream_codec_info = Info('oven_stream_codec_info', 'Codec information', ['vhost', 'stream', 'codec'])
