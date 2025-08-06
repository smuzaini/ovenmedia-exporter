import base64
import logging
import requests
from config import Config

class OvenMediaClient:
    def __init__(self, config):
        self.base_url = config.base_url
        self.token = config.token
        self.debug = config.debug

        self.headers = {}
        if self.token:
            encoded_token = base64.b64encode(self.token.encode()).decode()
            self.headers["Authorization"] = f"Basic {encoded_token}"

        # Add this line to get a logger instance
        self.logger = logging.getLogger("OvenMediaClient")


    # ... rest of client methods unchanged ...

    # ✅ 1. Get virtual hosts
    def get_vhosts(self):
        url = f"{self.base_url}/v1/vhosts"
        return self._fetch(url, "virtual hosts")

    # ✅ 2. Get streams (all under default app)
    def get_streams(self, vhost="default"):
        url = f"{self.base_url}/v1/vhosts/{vhost}/apps/app/streams"
        return self._fetch(url, f"streams list for vhost={vhost}")

    # ✅ 3. Get stream status
    def get_stream_status(self, vhost="default"):
        url = f"{self.base_url}/v1/vhosts/{vhost}/apps/app/streamstatus"
        return self._fetch(url, f"stream status for vhost={vhost}")

    # ✅ 4. Get specific stream info
    def get_stream_info(self, stream_name, vhost="default"):
        url = f"{self.base_url}/v1/vhosts/{vhost}/apps/app/streams/{stream_name}"
        return self._fetch(url, f"info for stream {stream_name}")

    # ✅ 5. Get specific stream statistics
    def get_stream_stats(self, stream_name, vhost="default"):
        url = f"{self.base_url}/v1/stats/current/vhosts/{vhost}/apps/app/streams/{stream_name}"
        return self._fetch(url, f"stats for stream {stream_name}")

    # Internal generic GET
    def _fetch(self, url, label):
        self.logger.info(f"Fetching {label} from {url}")
        try:
            response = requests.get(url, headers=self.headers, timeout=5)
            if response.status_code == 401:
                self.logger.error("Unauthorized! Check API token.")
                return {}
            response.raise_for_status()
            data = response.json()
            if self.debug:
                self.logger.info(f"Full API response for {label}: {data}")
            return data.get("response", {})
        except Exception as e:
            self.logger.error(f"Error fetching {label}: {e}")
            return {}

if __name__ == "__main__":
    # Load config
    config = Config("../config/config.yaml")

    # Initialize client with config
    client = OvenMediaClient(config)

    # Fetch and print virtual hosts
    vhosts = client.get_vhosts()
    print("\n=== Virtual Hosts ===")
    print(vhosts)

    # For each vhost, fetch and print streams and statuses
    for vhost in (vhosts if vhosts else ["default"]):
        streams = client.get_streams(vhost)
        print(f"\n=== Streams in {vhost} ===")
        print(streams)

        status = client.get_stream_status(vhost)
        print(f"Stream status in {vhost}: {status}")

        # For each stream, fetch and print info and stats
        if streams:
            for s in streams:
                info = client.get_stream_info(s, vhost)
                stats = client.get_stream_stats(s, vhost)
                print(f"\nStream: {s}")
                print(f"  Info: {info}")
                print(f"  Stats: {stats}")
