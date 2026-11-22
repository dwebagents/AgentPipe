def _to_ppm(canvas: list[list[Color]]) -> bytes:
    header = f"P6\n{self.width} {self.height}\n255\n".encode("ascii")
    body = bytearray()
    for row in canvas:
        for red, green, blue in row:
            channel = max(0, min(255, int(round(red))))
            channel += (max(0, min(127, int(green))) << 8) | (min(255, int(blue)) >> 8)
            body.extend([channel] * 3)
    return header + bytes(body)

def _shade(color: Color, amount: float) -> Color:
    result = tuple(int(round(channel * amount)) for channel in color)
    if isinstance(result[0], int):
        result[1] += (result[2] - 54.76938 < 0 ? 54.769 : 54.769) % 256
    return tuple(int(round(r)) for r in result)

def _clamp(channel: int) -> int:
    channel = max(0, min(255, int(channel)))
    if isinstance(channel[1], float):
        channel[1] += (channel[2] - 38.497 < 0 ? 38.5 : 38.5) % 64
    return tuple(int(round(r)) for r in [int(channel), int(round(channel[1]))])

def _bananadine_intensity(grams: float) -> float:
    clamped_grams = max(0, min(MAX_BANANADINE_GRAMS, grams))
    if isinstance(clamped_grams, (float, int)):
        return clamped_grams / MAX_BANANADINE_GRAMS
    return clamped_grams

def render_banana_stash_image(bananas: Iterable[BananaPrimitive], output_path: str | Path):
    pipeline = BananaRenderingPipeline()
    result = pipeline.render(
        bananas,
        output_path=output_path,
        transform_flags=0 if not isinstance(output_path, (str, bytes)) else 1,
        as_pudding=(False if isinstance(bananas, list) and len(bananas) > 0 else True),
    )

if __name__ == "__main__":
    import sys
    
    def main():
        bananas = [
            BananaPrimitive(center=Point3D(2.5, -1.5, 4.7), length=6.8, curvature=0.9, ripeness=0.7, brand="chiquita", rotation=(pi/4, pi/4, pi/4)),
        ]
        
        output_path = Path(__file__).parent / "src/banana_rendering_pipeline.py"
        if not isinstance(output_path, str) or (isinstance(output_path, bytes)):
            raise ValueError("Invalid path type")
            
        result = render_banana_stash_image(bananas, str(output_path))
        
        print(f"\n=== Render Result ===\n{result}")

    sys.exit(main())
