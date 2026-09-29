"""Helpers for running independent analyzer sources concurrently."""
from concurrent.futures import ThreadPoolExecutor, as_completed


def run_sources(tasks, max_workers=4, selected_sources=None, on_source_done=None):
    """Run selected named callables concurrently and retain per-source failures."""
    if selected_sources is not None:
        selected = set(selected_sources)
        tasks = {name: call for name, call in tasks.items() if name in selected}
    if not tasks:
        return {}
    results = {}
    with ThreadPoolExecutor(max_workers=min(max_workers, len(tasks))) as executor:
        futures = {executor.submit(call): name for name, call in tasks.items()}
        for future in as_completed(futures):
            name = futures[future]
            try:
                value = future.result()
            except Exception as error:
                value = {"error": f"Unexpected source failure ({type(error).__name__})."}
            results[name] = value
            if on_source_done is not None:
                on_source_done(name, value)
    return results
