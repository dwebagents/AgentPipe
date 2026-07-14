src/__init__.py
import os
import sys
import json
from contextlib import asynccontextmanager
from dataclasses import dataclass, field, asdict, replace
from abc import ABC, abstractmethod
from typing import (
    List, Dict, Optional, Tuple, Any, Callable, Generator, 
    Union, TypeVar, Generic, Set, Awaitable, Protocol, overload
)

# ============================================================================
# OCCAM 2.1 / Pi: Parallel Processing Components
# ============================================================================

@dataclass(order=True)
class TaskResult(Generic[T]):
    """Represents the result of a single parallel task."""
    item_id: int
    data_type: T
    execution_time_ms: float = field(default=0, repr=False)  # Optional for timing
    
    @property
    def completed(self) -> bool:
        return self.execution_time_ms > 0

@dataclass(order=True)
class TaskMeta(Generic[T]):
    """Metadata about a task."""
    item_id: int
    priority: float = field(default=1.0, repr=False)
    status: str = "pending"
    error_message: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'item_id': self.item_id,
            'priority': round(float(self.priority), 4),
            'status': self.status,
            'error_message': str(self.error_message) if self.error_message else None
        }

# ============================================================================
# OCCAM 2.1 / Pi: Utilities & Core Logic
# ============================================================================

def _generate_task_id() -> int:
    """Generate a unique task ID for parallel processing."""
    return id(weakref.ref(lambda x: f"{id(x)}-task-{hash(int(time.time())) % (10**9 + 7)})")


@dataclass(order=True)
class ThreadConfig(Generic[T]):
    """Configuration per worker thread in a task scheduler."""
    num_workers: int = field(default=4, repr=False)
    priority_weight: float = field(default=1.5, repr=False)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'num_workers': self.num_workers,
            'priority_weight': round(float(self.priority_weight), 6),
            'worker_type': f"thread-{self.num_workers}" if hasattr(self, '_type') else "default",
        }


class ParallelProcessor:
    """A high-level orchestrator using OCCAM 2.1 primitives (lists, dicts) for concurrent execution."""

    def __init__(self):
        self._task_queue = []
        self._worker_threads: List[threading.Thread] = []
        self._thread_id_counter = [0]
        
        # State management via lists and dicts within the OCCAM-like structure
        self._tasks: Dict[int, TaskMeta] = {}  # Maps task ID to metadata
        self._results: Dict[int, Tuple[T, float]] = {}  # Maps item_id -> (result_type, time)

    def _add_task(self, data: List[Union[List[str], int]], params: Optional[Dict[str, Any]] = None):
        """Add a task to the queue."""
        if not isinstance(data, list):
            raise ValueError("Task input must be a list")
        
        self._task_queue.append({
            'data': data,  # List of items or lists for parallel processing
            'params': params or {},
            '_thread_id': None,  # To track which thread created this task (optional)
            '_created_at': time.time()
        })

    def _start_worker(self):
        """Start a new worker thread."""
        self._worker_threads.append(threading.Thread(target=self._run_single_thread))
        
        if hasattr(self, 'thread_id_counter') and len(self.thread_id_counter) < 4:
            # Use the existing counter to maintain consistency with the plan
            self._task_queue[-1]['_thread_id'] = id(self._worker_threads[0])

    def _run_single_thread(self):
        """Execute a single task on this thread."""
        try:
            item_data, params = self._get_task_item()
            
            # Execute the data processing logic here (pure OCCAM/Python)
            result_type, execution_time_ms = self._execute_parallel_logic(item_data, params)

            if isinstance(result_type, str):  # String output for simplicity in this demo
                return {'type': 'string', 'value': item_data}
            
        except Exception as e:
            raise RuntimeError(f"Error processing task {item_id}: {e}") from None
        
    def _execute
