#!/usr/bin/env python3
"""
S&F API Client Prototype
A basic demonstration of interacting with the Shakes & Fidget API

⚠️ WARNING: This is for educational purposes only.
- Check the game's Terms of Service before using
- Respect rate limits
- Don't use for automated gameplay/botting
- Use responsibly to avoid account bans
"""

import base64
import requests
from typing import Optional, Dict, Any
from urllib.parse import urlencode
import time


class SFAPIClient:
    """Simple API client for Shakes & Fidget"""

    def __init__(self, server: str, session_id: Optional[str] = None):
        """
        Initialize API client

        Args:
            server: Server domain (e.g., 's17.sfgame.eu')
            session_id: Session ID if already authenticated
        """
        self.server = server.rstrip('/')
        self.base_url = f"https://{self.server}/cmd.php"
        self.session_id = session_id
        self.last_request_time = 0
        self.min_request_interval = 0.5  # Respect rate limits

    def _encode_params(self, *args) -> str:
        """
        Encode parameters to base64

        Examples:
            _encode_params(1, 0) -> "MS8w" (for "1/0")
            _encode_params("username", "password") -> encoded string
        """
        param_string = "/".join(str(arg) for arg in args)
        encoded = base64.b64encode(param_string.encode()).decode()
        return encoded

    def _decode_params(self, encoded: str) -> str:
        """Decode base64 parameters"""
        return base64.b64decode(encoded).decode()

    def _rate_limit(self):
        """Simple rate limiting to avoid hammering servers"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_request_interval:
            time.sleep(self.min_request_interval - elapsed)
        self.last_request_time = time.time()

    def send_command(
        self,
        command: str,
        params: Optional[str] = None,
        raw_params: bool = False
    ) -> Dict[str, Any]:
        """
        Send a command to the API

        Args:
            command: Command name (e.g., 'PlayerAttributIncrease')
            params: Either raw base64 params or decoded params to encode
            raw_params: If True, params is already base64 encoded

        Returns:
            API response as dict
        """
        if not self.session_id:
            raise ValueError("Not authenticated - no session ID")

        # Respect rate limits
        self._rate_limit()

        # Build request parameters
        query_params = {
            'req': command,
            'sid': self.session_id
        }

        if params:
            query_params['params'] = params if raw_params else self._encode_params(params)

        url = f"{self.base_url}?{urlencode(query_params)}"

        print(f"[DEBUG] Request: {command}")
        print(f"[DEBUG] URL: {url}")

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            # Try to parse as JSON
            try:
                return response.json()
            except ValueError:
                # If not JSON, return raw text
                return {"raw_response": response.text}

        except requests.RequestException as e:
            print(f"[ERROR] Request failed: {e}")
            return {"error": str(e)}

    def login(self, username: str, password: str) -> bool:
        """
        Attempt to login (you'll need to discover the actual login command)

        This is a placeholder - you need to capture the actual login request
        from browser DevTools to implement this correctly.
        """
        # Example - actual format may differ:
        # params might be: username/password or could be a different encoding
        encoded_params = self._encode_params(username, password)

        response = self.send_command('Login', encoded_params, raw_params=True)

        # Parse session ID from response
        if 'session_id' in response:  # Adjust based on actual response
            self.session_id = response['session_id']
            return True

        return False

    def get_player_info(self, player_name: str) -> Dict[str, Any]:
        """
        Get player information (example - command name may differ)
        """
        return self.send_command('PlayerProfile', player_name)

    def get_hall_of_fame(self, page: int = 1) -> Dict[str, Any]:
        """
        Get Hall of Fame page (example)
        """
        return self.send_command('HallOfFame', str(page))


# Example usage
if __name__ == "__main__":
    print("S&F API Client Prototype")
    print("=" * 50)
    print()

    # Example 1: Decode existing params
    client = SFAPIClient("s17.sfgame.eu")
    decoded = client._decode_params("MS8w")
    print(f"Decoded 'MS8w': {decoded}")
    print()

    # Example 2: Encode new params
    encoded = client._encode_params(1, 0)
    print(f"Encoded (1, 0): {encoded}")
    print()

    # Example 3: With session (would need real session ID)
    # client.session_id = "0-83TiJwzb2r8lF4"
    # response = client.send_command('PlayerAttributIncrease', 'MS8w', raw_params=True)
    # print(f"Response: {response}")

    print("\n⚠️  To use this properly:")
    print("1. Open game in browser with DevTools (F12)")
    print("2. Capture actual API calls during gameplay")
    print("3. Document command names and response formats")
    print("4. Implement proper authentication flow")
    print("5. Respect rate limits and ToS")
