#!/usr/bin/env python3
"""
Sayanox‑One — Main Autonomous Engine
One command → full assessment
"""
import argparse
import sys
from config.config_loader import load_config
from utils.logger import setup_logger
from utils.validator import validate_target
from modules.recon import run_recon
from modules.web import run_web_scan
from modules.network import run_network_scan
from modules.auth import run_auth_check
from modules.exploit import run_exploit_chain
from modules.reporting import generate_report
from advanced.ai_chain import DecisionEngine
from advanced.fast_scan import ParallelRunner

LOGGER = setup_logger("sayanox-main")

def main():
    parser = argparse.ArgumentParser(description="Sayanox‑One — Autonomous Pentest Framework")
    parser.add_argument("--target", required=True, help="Target IP / domain / CIDR")
    parser.add_argument("--mode", default="full", choices=["recon","scan","exploit","full"], help="Operation mode")
    parser.add_argument("--config", default="config/settings.yaml", help="Custom config file")
    parser.add_argument("--output", default="reports/", help="Output directory")
    parser.add_argument("--verbose", action="store_true", help="Detailed logs")
    args = parser.parse_args()

    # Load & validate
    config = load_config(args.config)
    if not validate_target(args.target, config):
        LOGGER.error("Target not allowed — check allowlists/permissions")
        sys.exit(1)

    LOGGER.info(f"→ Starting assessment: {args.target} | Mode: {args.mode}")
    results = {"target": args.target, "phases": {}}

    # Initialize advanced engines
    decider = DecisionEngine(config)
    runner = ParallelRunner(config)

    # --- PHASES ---
    if args.mode in ["recon","full"]:
        results["phases"]["recon"] = run_recon(args.target, config, runner)
        decider.update_context(results["phases"]["recon"])

    if args.mode in ["scan","full"]:
        net_targets = decider.select_network_targets()
        web_targets = decider.select_web_targets()
        results["phases"]["network_scan"] = run_network_scan(net_targets, config, runner)
        results["phases"]["web_scan"] = run_web_scan(web_targets, config, runner)
        decider.update_context(results["phases"])

    if args.mode in ["exploit","full"]:
        results["phases"]["auth_check"] = run_auth_check(decider.get_auth_candidates(), config)
        results["phases"]["exploit"] = run_exploit_chain(decider.get_vuln_candidates(), config)

    # --- REPORT ---
    generate_report(results, args.output, config)
    LOGGER.info(f"✓ Done — results saved to: {args.output}")

if __name__ == "__main__":
    main()
  
