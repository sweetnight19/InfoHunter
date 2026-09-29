"""Helpers for running independent analyzer sources concurrently."""
from concurrent.futures import ThreadPoolExecutor


def run_sources(tasks, max_workers=4):
    """Run named callables concurrently and retain per-source failures."""
    if not tasks:
        return {}
    results = {}
    with ThreadPoolExecutor(max_workers=min(max_workers, len(tasks))) as executor:
        futures = {name: executor.submit(callable_) for name, callable_ in tasks.items()}
        for name, future in futures.items():
            try:
                results[name] = future.result()
            except Exception as error:
                results[name] = {
                    "error": f"Unexpected source failure ({type(error).__name__})."
                }
    return results
