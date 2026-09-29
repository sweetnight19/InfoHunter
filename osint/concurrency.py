"""Bounded concurrent execution for independent analysis sources."""

from concurrent.futures import ThreadPoolExecutor, as_completed

from osint.results import SourceResult


def run_sources(
    tasks,
    max_workers=4,
    selected_sources=None,
    on_source_done=None,
    structured=False,
):
    """Run named sources and optionally return stable SourceResult envelopes.

    Legacy callers keep receiving their original payloads. Structured callers get
    consistent state, message, and findings metadata for every source.
    """
    if selected_sources is not None:
        selected = set(selected_sources)
        tasks = {name: call for name, call in tasks.items() if name in selected}
    if not tasks:
        return {}

    results = {}
    worker_count = max(1, min(max_workers, len(tasks)))
    with ThreadPoolExecutor(max_workers=worker_count) as executor:
        futures = {executor.submit(call): name for name, call in tasks.items()}
        for future in as_completed(futures):
            name = futures[future]
            try:
                source_result = SourceResult.from_value(name, future.result())
            except Exception as error:
                source_result = SourceResult.from_exception(name, error)

            value = source_result if structured else source_result.to_legacy()
            results[name] = value
            if on_source_done is not None:
                on_source_done(name, value)
    return results
