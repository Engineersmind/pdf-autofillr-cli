"""CLI benchmark metric calculations."""
from typing import List, Dict, Any

def calculate_latency_metrics(results: List[Dict[str, Any]]) -> Dict[str, float]:
    durations = [r["duration_s"] for r in results if "duration_s" in r]
    if not durations: return {}
    return {
        "min_s": round(min(durations), 3),
        "max_s": round(max(durations), 3),
        "avg_s": round(sum(durations)/len(durations), 3),
    }

def calculate_success_rate(results: List[Dict[str, Any]]) -> float:
    if not results: return 0.0
    return round(sum(1 for r in results if r.get("exit_code") == 0) / len(results), 4)
