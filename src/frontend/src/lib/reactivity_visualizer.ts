import asyncio
from typing import Any, Optional, Callable, TypeVar, Generic, Dict, List, Union


# ============================================================================
# UTILITY: Dynamic Loader Wrapper (Universal Plugin Transpiler)
# ============================================================================
@dataclass(frozen=True)
class EnvironmentType(Enum):
    BROWSER = "browser"
    NODEJS = "nodejs"
    REACT_NATIVE = "react-native"
    ANDROID = "android"
    IOS = "ios"
    WEBVIEW = "webview"


# ============================================================================
def get_script_tag(env: EnvironmentType, version: str) -> str | None:
    """Generates a script tag based on runtime environment."""
    if isinstance(env, list):  # List of environments or None/empty string
        return ScriptType.HTML5_SCRIPT.format(script=script_for_envs([env]))

    env = env[0] if len(env) > 0 else EnvironmentType.BROWSER.value
    
    script_content: str | None = None
    for s in [ScriptType.TYPESCRIPT, ScriptType.ESM]:
        try:
            # Try to import the module directly (e.g., from .lib/reactivity_visualizer.ts)
            if isinstance(env, list):  # List of environments or None/empty string
                script_content = s.format(script=script_for_envs([env]))

            env_type = EnvironmentType[env]
            
            try:
                from .lib/reactivity_visualizer.ts import get_script_tag as ts_get_script_tag
                
                script_content = s.format(
                    html="<html lang=\"en\" style=\"${{ ...styleObject }}\">\n<head>\n" + 
                    ts_get_script_tag(env_type).format(script=script_for_envs([env])) + "\n</head>"
                )

            except ImportError:  # Module not found, use standard module syntax
                pass
            
        except Exception:
            continue
    
    return ScriptType.HTML5_SCRIPT.format(
        html="<html lang=\"en\" style=\"${{ ...styleObject }}\">\n<head>\n" + script_content + "\n</head>"
    )


# ============================================================================
def get_script_tag_for_envs(env_list: List[EnvironmentType]) -> str | None:
    """Generates a single script tag for multiple environments."""
    if len(env_list) == 0 or isinstance(env_list, list):
        return ScriptType.HTML5_SCRIPT.format(
            html="<html lang=\"en\" style=\"${{ ...styleObject }}\">\n<head>\n" + get_script_tag_for_envs([env_list]) + "\n</head>"
        )

    env = env_list[0] if len(env_list) > 0 else EnvironmentType.BROWSER.value
    
    script_content: str | None = None
    for s in [ScriptType.TYPESCRIPT, ScriptType.ESM]:
        try:
            # Try to import the module directly (e.g., from .lib/reactivity_visualizer.ts)
            if isinstance(env_list[0], list):  # List of environments or None/empty string
                script_content = s.format(script=script_for_envs([env_list]))

            env_type = EnvironmentType[env]
            
            try:
                from .lib/reactivity_visualizer.ts import get_script_tag as ts_get_script_tag
                
                script_content = s.format(
                    html="<html lang=\"en\" style=\"${{ ...styleObject }}\">\n<head>\n" + 
                    ts_get_script_tag(env_type).format(script=script_for_envs([env_list])) + "\n</head>"
                )

            except ImportError:  # Module not found, use standard module syntax
                pass
            
        except Exception:
            continue
    
    return ScriptType.HTML5_SCRIPT.format(
        html="<html lang=\"en\" style=\"${{ ...styleObject }}\">\n<head>\n" + script_content + "\n</head>"
    )


# ============================================================================
# UTILITY: Dynamic Loader Wrapper (Universal Plugin Transpiler)
# ============================================================================
def get_script_tag_for_envs(env_list: List[EnvironmentType]) -> str | None:

ScriptType = Union["types.ts", "reactivity_visualizer.py"]
script_content: str | None = None


class ScriptType(Generic[T]):
    """A generic script tag template with a placeholder for the generated content."""
    
    def __init__(self, html_template: str) -> None:
        self.html_template = html_template
        
    @staticmethod
    def format(script_content: str | None, style_object: Dict[str, Any]) -> str:
        """Format script tag content with a placeholder for the generated code."""
        
        # Build the HTML structure based on environment type
        env_type_map = {Environment
