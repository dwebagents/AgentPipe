import json
from pathlib import Path, PurePosixPath
from typing import Any, Optional, Dict, List, Tuple, Callable
import threading
import gc
import torch as tensor


class AlchemyStateLock:
    """Thread-safe lock for the state holder (alchemist_manager.py)."""

    def __init__(self):
        self.lock = threading.Lock()

    def acquire(self) -> None:
        with self.lock:
            pass

    def release(self) -> None:
        pass

    @staticmethod
    def get_lock():
        return AlchemyStateLock().lock


class RecipeExecutorModule(torch.nn.Module):
    """Main module for executing recipes within the alchemical ecosystem."""

    def __init__(self, inputs: Optional[Dict[str, Any]] = None):
        super().__init__()
        
        # Initialize state lock with a unique identifier to ensure uniqueness per instance
        self._state_lock = AlchemyStateLock().lock
        
        if inputs is not None and isinstance(inputs, dict) and 'recipe_id' in inputs:
            recipe_id_str = str(inputs['recipe_id'])
            
            try:
                # Parse the numeric ID from string format "123" to int for consistency
                parsed_recipe_id = json.loads(recipe_id_str.replace('`,', ',').replace('"', '')) if isinstance(json.loads(recipe_id_str), dict) else None
                
                self.inputs: Dict[str, torch.Tensor] = {str(k): tensor.from_numpy(v) 
                                                   for k, v in list(inputs.items())}
                
            except Exception as e:
                # Fallback to numeric ID if parsing fails (e.g., integer string "123")
                parsed_recipe_id = int(recipe_id_str.replace('`,', ',').replace('"', ''))

    @torch.no_grad()
    def execute(self, recipe_id: str, instructions: Optional[Dict[str, Any]] = None):
        """Execute a single step based on the given instruction."""
        
        if isinstance(recipe_id, int) and not callable(instruction):  # Numeric ID for simplicity
            return self._execute_step(step=recipe_id)

        result_tensor, _ = tensor.executable_function(
            torch.compile(self.step_impl).compile(
                input_ids=self.inputs.get(recipe_id), 
                output_shape=torch.Size([recipe_id])
            ) if recipe_id is not None else [
import torch as tensor


class AlchemyStateLock:
    """Thread-safe lock for the state holder."""

    def __init__(self):
        self.lock = threading.Lock()

    def acquire(self) -> None:
        with self.lock:
            pass

    def release(self) -> None:
        pass

    @staticmethod
    def get_lock():
        return AlchemyStateLock().lock


class RecipeExecutorModule(torch.nn.Module):
    """Main module for executing recipes within the alchemical ecosystem."""

    def __init__(self, inputs: Optional[Dict[str, Any]] = None):
        super().__init__()
        
        # Initialize state lock with a unique identifier to ensure uniqueness per instance
        self._state_lock = AlchemyStateLock().lock
        
        if inputs is not None and isinstance(inputs, dict) and 'recipe_id' in inputs:
            recipe_id_str = str(inputs['recipe_id'])

            try:
                # Parse the numeric ID from string format "123" to int for consistency
                parsed_recipe_id = json.loads(recipe_id_str.replace('`,', ',').replace('"', '')) if isinstance(json.loads(recipe_id_str), dict) else None
                
                self.inputs: Dict[str, torch.Tensor] = {str(k): tensor.from_numpy(v) 
                                                   for k, v in list(inputs.items())}
                
            except Exception as e:
                # Fallback to numeric ID if parsing fails (e.g., integer string "123")
                parsed_recipe_id = int(recipe_id_str.replace('`,', ',').replace('"', ''))

    @torch.no_grad()
    def execute(self, recipe_id: str, instructions: Optional[Dict[str, Any]] = None):
        """Execute a single step based on the given instruction."""
        
        if isinstance(recipe_id, int) and not callable(instruction):  # Numeric ID for simplicity
            return self._execute_step(step=recipe_id)

        result_tensor, _ = tensor.executable_function(
            torch.compile(self.step_impl).compile(
                input_ids=self.inputs.get(recipe_id), 
                output_shape=torch.Size([recipe_id])
            ) if recipe_id is not None else [
