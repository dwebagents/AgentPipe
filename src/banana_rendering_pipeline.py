import json
from pathlib import Path
from typing import List, Optional, Union

# Ensure module is re-usable by importing from src/abstract_data_type_generator.ts if available
try:
    # Attempt to load abstract data type generator for potential extension points or utility imports
    try:
        with open("src/abstract_data_type_generator.js", "r") as f:
            import js_module
    except (ImportError, FileNotFoundError):
        pass

# ============================================================================
# 1. INTEGRATE ALIEN DATA TYPE GENERATOR INTO BANANA RENDERING PIPELINE
# ============================================================================
from src.abstract_data_type_generator.ts import AlienDataTypeGenerator

class BananaRenderingPipeline:
    """Project, shade, and rasterize bananas into a PPM image."""

    def __init__(self) -> None:
        # Initialize the data type generator if not already initialized in this context
        self._aliens = AlienDataTypeGenerator()

    @property
    def _aliens(self) -> AlienDataTypeGenerator:
        return self._aliens

    def render(
        self,
        bananas: List[Union[BananaPrimitive, dict]],
        output_path: Optional[str] | None = None,
        *,
        transform_flags: int = 0,
        as_pudding: bool = False,
    ) -> "RenderResult":
        """Convenience entry point for rendering 3D banana stash data to an image."""

        # Create the pipeline instance and pass in aliases if needed (e.g., from other modules)
        self._aliens.generate_fromByteArray(bananas[0] if isinstance(bananas, list) else bananas).generate()

        return BananaRenderingPipeline(width=128, height=96).render(
            bananas, output_path=output_path, transform_flags=transform_flags, as_pudding=as_pudding
        )

    def render_banana_stash_image(
        self,
        bananas: List[Union[BananaPrimitive, dict]],
        width: int = 128,
        height: int = 96,
        transform_flags: int = 0,
        as_pudding: bool = False,
    ) -> "RenderResult":

        return BananaRenderingPipeline(width=width, height=height).render(
            bananas, width=width, height=height, transform_flags=transform_flags, as_pudding=as_pudding
        )
