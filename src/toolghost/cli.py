import argparse
import sys
from .config import ToolGhostConfig
from .engine import ToolGhostEngine
from .reporter import GhostReporter

def main():
    parser = argparse.ArgumentParser(description="ToolGhost: LLM Function-Calling Schema & Tool-Use Fuzzer.")
    parser.add_argument("--url", required=True, help="Target agent tool-execution endpoint URL.")
    parser.add_argument("--schema", required=True, help="Path to JSON file containing OpenAI/Anthropic tool schemas.")
    parser.add_argument("--header", action="append", default=[], help="Custom header in 'Key: Value' format.")
    parser.add_argument("--output", default="toolghost_report.json", help="Output JSON report file.")

    args = parser.parse_args()

    headers = {}
    for h in args.header:
        if ":" in h:
            k, v = h.split(":", 1)
            headers[k.strip()] = v.strip()

    config = ToolGhostConfig(
        target_url=args.url,
        headers=headers,
        schema_file=args.schema
    )

    try:
        print(f"[*] Initializing ToolGhost schema fuzzer against {config.target_url}...")
        engine = ToolGhostEngine(config)
        findings = engine.run()
        GhostReporter.print_terminal_report(findings)
        GhostReporter.save_json_report(findings, args.output)
    except Exception as e:
        print(f"[!] Execution Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
