from prometheus_client import start_http_server
from client import OvenMediaClient
from metrics_definitions import (
    oven_stream_up,
    oven_stream_bitrate_latest_bps,
    oven_stream_bitrate_avg_bps,
    oven_stream_framerate_latest_fps,
    oven_stream_framerate_avg_fps,
    oven_stream_resolution_width_pixels,
    oven_stream_resolution_height_pixels,
    oven_stream_keyframe_interval_latest,
    oven_stream_keyframe_interval_avg,
    oven_stream_has_bframes,
    oven_stream_throughput_in_bps,
    oven_stream_throughput_out_bps,
    oven_stream_last_throughput_in_bps,
    oven_stream_last_throughput_out_bps,
    oven_stream_max_throughput_in_bps,
    oven_stream_max_throughput_out_bps,
    oven_stream_active_connections,
    oven_stream_created_timestamp,
    oven_stream_last_recv_timestamp,
    oven_stream_last_sent_timestamp,
    oven_stream_last_updated_timestamp,
    oven_stream_max_total_connection_time,
    oven_stream_total_bytes_in,
    oven_stream_total_bytes_out,
    oven_stream_total_connections,
    oven_stream_codec_info,
)
import time
import logging
from datetime import datetime
from config import Config
import signal
import sys

# Configure logging with timestamp, level and message
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("OvenMediaCollector")

class OvenMediaCollector:
    def __init__(self, config_path="../config/config.yaml"):
        config = Config(config_path)
        self.client = OvenMediaClient(config)
        # Track last counter values for safe increments
        self._last_total_bytes_in = {}
        self._last_total_bytes_out = {}
        self._last_total_connections = {}

    def parse_timestamp(self, timestr):
        if not timestr:
            return None
        try:
            dt = datetime.fromisoformat(timestr.replace("Z", "+00:00"))
            return dt.timestamp()
        except Exception as e:
            logger.warning(f"Failed to parse timestamp {timestr}: {e}")
            return None

    def collect(self):
        vhosts = self.client.get_vhosts()
        if not vhosts:
            logger.error("No virtual hosts found, skipping collection cycle.")
            return

        for vhost in vhosts:
            streams = self.client.get_streams(vhost)
            if not streams:
                logger.info(f"No streams found for vhost {vhost}")
                continue

            for stream in streams:
                info = self.client.get_stream_info(stream, vhost)
                stats = self.client.get_stream_stats(stream, vhost)

                stream_up = 1 if info and stats else 0
                oven_stream_up.labels(vhost=vhost, stream=stream).set(stream_up)
                if not (info and stats):
                    continue

                try:
                    input_info = info.get("input", {})
                    tracks = input_info.get("tracks", [])
                    video_track = None
                    for t in tracks:
                        if t.get("type") == "Video":
                            video_track = t.get("video", {})
                            break

                    codec = video_track.get("codec", "unknown") if video_track else "unknown"
                    oven_stream_codec_info.labels(vhost=vhost, stream=stream, codec=codec).info({})

                    if video_track:
                        oven_stream_bitrate_latest_bps.labels(vhost, stream).set(float(video_track.get("bitrateLatest", 0)))
                        oven_stream_bitrate_avg_bps.labels(vhost, stream).set(float(video_track.get("bitrateAvg", 0)))
                        oven_stream_framerate_latest_fps.labels(vhost, stream).set(float(video_track.get("framerateLatest", 0)))
                        oven_stream_framerate_avg_fps.labels(vhost, stream).set(float(video_track.get("framerateAvg", 0)))
                        oven_stream_resolution_width_pixels.labels(vhost, stream).set(int(video_track.get("width", 0)))
                        oven_stream_resolution_height_pixels.labels(vhost, stream).set(int(video_track.get("height", 0)))
                        oven_stream_keyframe_interval_latest.labels(vhost, stream).set(float(video_track.get("keyFrameIntervalLatest", 0)))
                        oven_stream_keyframe_interval_avg.labels(vhost, stream).set(float(video_track.get("keyFrameIntervalAvg", 0)))
                        oven_stream_has_bframes.labels(vhost, stream).set(1 if video_track.get("hasBframes", False) else 0)
                    else:
                        logger.warning(f"No video track info for stream {stream} in vhost {vhost}")
                except Exception as e:
                    logger.error(f"Error parsing stream info for {stream} in {vhost}: {e}")

                try:
                    oven_stream_throughput_in_bps.labels(vhost, stream).set(float(stats.get("avgThroughputIn", 0)))
                    oven_stream_throughput_out_bps.labels(vhost, stream).set(float(stats.get("avgThroughputOut", 0)))
                    oven_stream_last_throughput_in_bps.labels(vhost, stream).set(float(stats.get("lastThroughputIn", 0)))
                    oven_stream_last_throughput_out_bps.labels(vhost, stream).set(float(stats.get("lastThroughputOut", 0)))
                    oven_stream_max_throughput_in_bps.labels(vhost, stream).set(float(stats.get("maxThroughputIn", 0)))
                    oven_stream_max_throughput_out_bps.labels(vhost, stream).set(float(stats.get("maxThroughputOut", 0)))

                    # Safe counter increments
                    current_in = float(stats.get("totalBytesIn", 0))
                    current_out = float(stats.get("totalBytesOut", 0))
                    current_conn = float(stats.get("totalConnections", 0))

                    key = (vhost, stream)

                    last_in = self._last_total_bytes_in.get(key, 0)
                    if current_in > last_in:
                        oven_stream_total_bytes_in.labels(vhost, stream).inc(current_in - last_in)
                        self._last_total_bytes_in[key] = current_in

                    last_out = self._last_total_bytes_out.get(key, 0)
                    if current_out > last_out:
                        oven_stream_total_bytes_out.labels(vhost, stream).inc(current_out - last_out)
                        self._last_total_bytes_out[key] = current_out

                    last_conn = self._last_total_connections.get(key, 0)
                    if current_conn > last_conn:
                        oven_stream_total_connections.labels(vhost, stream).inc(current_conn - last_conn)
                        self._last_total_connections[key] = current_conn

                    connections = stats.get("connections", {})
                    for protocol, count in connections.items():
                        oven_stream_active_connections.labels(vhost, stream, protocol).set(int(count))

                    # Parse timestamps properly
                    for field, metric in [
                        ("createdTime", oven_stream_created_timestamp),
                        ("lastRecvTime", oven_stream_last_recv_timestamp),
                        ("lastSentTime", oven_stream_last_sent_timestamp),
                        ("lastUpdatedTime", oven_stream_last_updated_timestamp),
                    ]:
                        ts_val = self.parse_timestamp(stats.get(field))
                        if ts_val is not None:
                            metric.labels(vhost, stream).set(ts_val)

                    max_conn_time = self.parse_timestamp(stats.get("maxTotalConnectionTime"))
                    if max_conn_time is not None:
                        oven_stream_max_total_connection_time.labels(vhost, stream).set(max_conn_time)

                except Exception as e:
                    logger.error(f"Error parsing stream stats for {stream} in {vhost}: {e}")

collector = None

def shutdown_handler(signum, frame):
    logger.info("Shutdown signal received, stopping exporter...")
    global collector
    collector = None
    sys.exit(0)

def main():
    global collector
    collector = OvenMediaCollector()
    start_http_server(8000)
    logger.info("OvenMediaEngine Exporter started on http://localhost:8000/metrics")

    # Setup graceful shutdown signals
    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)

    while True:
        collector.collect()
        time.sleep(10)

if __name__ == "__main__":
    main()
