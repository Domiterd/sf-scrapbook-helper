#!/usr/bin/env python3
"""
API Call Analyzer
Helper tool to decode and document S&F API calls

Usage:
    python api_call_analyzer.py "https://s17.sfgame.eu/cmd.php?req=PlayerAttributIncrease&params=MS8w&sid=0-83TiJwzb2r8lF4"
"""

import base64
import sys
from urllib.parse import urlparse, parse_qs
import json


def analyze_api_call(url: str):
    """Analyze and decode an S&F API call"""

    parsed = urlparse(url)
    params = parse_qs(parsed.query)

    print("=" * 70)
    print("S&F API Call Analysis")
    print("=" * 70)
    print()

    # Extract components
    server = parsed.netloc
    command = params.get('req', [''])[0]
    encoded_params = params.get('params', [''])[0]
    session_id = params.get('sid', [''])[0]

    print(f"Server:     {server}")
    print(f"Command:    {command}")
    print(f"Session:    {session_id}")
    print()

    # Decode parameters
    if encoded_params:
        print("Parameters:")
        print(f"  Encoded:  {encoded_params}")
        try:
            decoded = base64.b64decode(encoded_params).decode('utf-8')
            print(f"  Decoded:  {decoded}")

            # Try to parse structure
            if '/' in decoded:
                parts = decoded.split('/')
                print(f"  Parts:    {parts} (count: {len(parts)})")
        except Exception as e:
            print(f"  Decode Error: {e}")
    else:
        print("Parameters: None")

    print()
    print("-" * 70)
    print("Reconstructed Call:")
    print("-" * 70)
    print(f"Command: {command}")
    if encoded_params:
        print(f"Params:  {decoded if encoded_params else 'None'}")
    print()

    # Generate Python code snippet
    print("=" * 70)
    print("Python Code Snippet:")
    print("=" * 70)
    print(f"# {command}")
    print(f'client.send_command(')
    print(f'    command="{command}",')
    if encoded_params:
        print(f'    params="{encoded_params}",')
        print(f'    raw_params=True')
    print(f')')
    print()
    print("# Or with auto-encoding:")
    if encoded_params and decoded:
        param_parts = decoded.split('/')
        if len(param_parts) <= 3:
            args = ', '.join(f'"{p}"' if not p.isdigit() else p for p in param_parts)
            print(f'client._encode_params({args})  # -> "{encoded_params}"')
    print()


def batch_analyze(urls: list):
    """Analyze multiple API calls and generate summary"""

    commands = {}

    for url in urls:
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        command = params.get('req', ['Unknown'])[0]
        encoded_params = params.get('params', [''])[0]

        if encoded_params:
            try:
                decoded = base64.b64decode(encoded_params).decode('utf-8')
            except:
                decoded = "decode_error"
        else:
            decoded = "no_params"

        if command not in commands:
            commands[command] = []

        commands[command].append({
            'encoded': encoded_params,
            'decoded': decoded
        })

    print("=" * 70)
    print("API Commands Summary")
    print("=" * 70)
    print()

    for cmd, examples in commands.items():
        print(f"Command: {cmd}")
        print(f"  Examples found: {len(examples)}")
        for i, ex in enumerate(examples[:3], 1):  # Show first 3
            print(f"    {i}. {ex['decoded']}")
        print()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print('  python api_call_analyzer.py "URL"')
        print()
        print("Example:")
        print('  python api_call_analyzer.py "https://s17.sfgame.eu/cmd.php?req=PlayerAttributIncrease&params=MS8w&sid=0-..."')
        print()
        print("Multiple URLs (for batch analysis):")
        print('  python api_call_analyzer.py "URL1" "URL2" "URL3"')
        sys.exit(1)

    urls = sys.argv[1:]

    if len(urls) == 1:
        analyze_api_call(urls[0])
    else:
        batch_analyze(urls)

    print("\n💡 Tips:")
    print("  • Open game in browser with DevTools (F12)")
    print("  • Filter Network tab by 'cmd.php'")
    print("  • Copy URLs as you play")
    print("  • Use this tool to decode and document them")
    print("  • Build up a complete API reference")
