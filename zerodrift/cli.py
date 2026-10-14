"""
zerodrift.cli - ZeroDrift Systems Command Line Interface
"""

import sys
import json
import argparse
from zerodrift.shadow_replay import ShadowReplayEngine
from zerodrift.flight_recorder import FlightRecorder
from zerodrift.autosandbox import AutoSandboxEngine


def main():
    parser = argparse.ArgumentParser(
        prog="zerodrift",
        description="ZeroDrift Systems - Deterministic Architecture, Differential Migration & Forensics Suite"
    )
    subparsers = parser.add_subparsers(dest="command", help="ZeroDrift Subcommands")

    # Command: replay
    replay_parser = subparsers.add_parser("replay", help="Run differential traffic shadow replay")
    replay_parser.add_argument("--samples", type=int, default=500, help="Number of trace samples to replay")

    # Command: flight-record
    fr_parser = subparsers.add_parser("record", help="Simulate agent flight recorder & syscall sandbox")

    # Command: heal
    heal_parser = subparsers.add_parser("heal", help="Trigger autonomous incident reproduction & patch sandbox")

    args = parser.parse_args()

    if args.command == "replay" or not args.command:
        print("\n" + "="*65)
        print(" [ZeroDrift Systems] ShadowReplay™ Differential Engine v0.9.4")
        print(" Deterministic Parity & Migration Verification Lab")
        print("="*65)
        engine = ShadowReplayEngine()
        
        # Simulated demo workload
        def legacy_pricing(p):
            return {"price": round(p["qty"] * p["unit_price"] * 1.0825, 2), "status": "APPROVED"}
            
        def modern_pricing(p):
            # Fast Rust/Python equivalent
            return {"price": round(p["qty"] * p["unit_price"] * 1.0825, 2), "status": "APPROVED"}
            
        dataset = [{"qty": i + 1, "unit_price": 19.99} for i in range(args.samples if hasattr(args, "samples") else 200)]
        print(f"[*] Dispatching {len(dataset)} recorded traffic traces across parallel runtimes...")
        res = engine.run_replay(legacy_pricing, modern_pricing, dataset)
        
        print(f"[+] Parity Achieved:          {res.parity_rate}%")
        print(f"[+] Total Verified Samples:   {res.total_samples}")
        print(f"[+] Legacy Runtime Avg:       {res.avg_latency_legacy_ms} ms")
        print(f"[+] Modern Runtime Avg:       {res.avg_latency_migrated_ms} ms")
        print(f"[+] Latency Improvement:     {((res.avg_latency_legacy_ms - res.avg_latency_migrated_ms)/max(1e-4, res.avg_latency_legacy_ms))*100:.1f}%")
        print(f"[+] Zero-Drift Certificate:   {res.verification_hash}")
        print(f"[+] Status:                   {'VERIFIED ZERO DIVERGENCE' if res.is_certified else 'DRIFT DETECTED'}")
        print("="*65 + "\n")

    elif args.command == "record":
        print("\n" + "="*65)
        print(" [ZeroDrift Systems] FlightRecorder™ Agent Syscall Tracer")
        print("="*65)
        fr = FlightRecorder("session_agent_auto_deploy_941")
        fr.record_event("CONTEXT_PRUNING", {"original_tokens": 124000, "pruned_tokens": 8200})
        fr.record_event("TOOL_DISPATCH", {"tool": "git_checkout", "branch": "fix/payment-race"})
        fr.intercept_network_egress("api.github.com", 443, "GET /repos")
        # Simulate unauthorized egress
        print("[!] Agent attempting external socket connection to unverified IP...")
        allowed = fr.intercept_network_egress("185.220.101.4", 8080, "POST /data")
        print(f"[*] eBPF Gate Interception: {'PERMITTED' if allowed else 'TERMINATED BY POLICY'}")
        log = fr.export_flight_log()
        print(f"[+] Recorded {log['event_count']} events across {log['total_duration_ms']}ms.")
        print(f"[+] Security Violations Neutralized: {len(log['security_violations'])}")
        print("="*65 + "\n")

    elif args.command == "heal":
        print("\n" + "="*65)
        print(" [ZeroDrift Systems] AutoSandbox™ SRE Self-Healing Engine")
        print("="*65)
        engine = AutoSandboxEngine()
        report = engine.triage_and_heal({"id": "INC-7489", "service": "payment-settlement-worker"})
        print(f"[*] Incident:               {report.incident_id} ({report.service_name})")
        print(f"[*] Reproduction Test:      {report.reproduction_test_name} [EXIT {report.initial_exit_code} - RED]")
        print(f"[*] Applying Atomic Patch:  Verified [EXIT {report.patched_exit_code} - GREEN]")
        print(f"[*] Duration:               {report.reproduction_duration_ms} ms")
        print(f"[*] Status:                 {report.status}")
        print("="*65 + "\n")


if __name__ == "__main__":
    main()
