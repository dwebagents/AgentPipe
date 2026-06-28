"""Render a small, deterministic book of banana pudding."""

from __future__ import annotations

from pathlib import Path
from textwrap import wrap

from recipe_library import BananaPuddingRecipe, RecipeLibrary


class BookOfBananaPudding:
    def __init__(self, library: RecipeLibrary | None = None) -> None:
        self.library = library or RecipeLibrary()

    def load_recipes(self, path: str | Path | None = None) -> list[dict[str, object]]:
        self.library.load(path)
        return self.library.get_recipe_data()

    def render_chapter(self, recipe: BananaPuddingRecipe, index: int) -> str:
        ingredients = "\n".join(f"- {item}" for item in recipe.ingredients)
        instructions = "\n".join(
            f"{step}. {text}" for step, text in enumerate(recipe.instructions, start=1)
        )
        return "\n".join(
            [
                f"## Chapter {index}: {recipe.name}",
                "",
                (
                    "Call me Pudding. Some years ago, in a kitchen not unlike a "
                    "deck at dawn, this recipe came forth from "
                    f"{recipe.origin} under the hand of {recipe.inventor}."
                ),
                "",
                f"**Inventor profile.** {recipe.profile}",
                "",
                "### Ingredients",
                ingredients,
                "",
                "### Instructions",
                instructions,
            ]
        )

    def render_manuscript(self) -> str:
        chapters = [
            self.render_chapter(recipe, index)
            for index, recipe in enumerate(self.library.recipes(), start=1)
        ]
        return "\n\n".join(["# The Book of Banana Pudding", *chapters]) + "\n"

    def export_to_markdown(self, path: str | Path) -> Path:
        output_path = Path(path)
        output_path.write_text(self.render_manuscript(), encoding="utf-8")
        return output_path

    def export_to_pdf(self, path: str | Path) -> Path:
        output_path = Path(path)
        output_path.write_bytes(_minimal_pdf(self.render_manuscript()))
        return output_path


def _minimal_pdf(text: str) -> bytes:
    lines = []
    for paragraph in text.splitlines():
        wrapped = wrap(paragraph, width=86) or [""]
        lines.extend(wrapped)

    content_lines = ["BT", "/F1 10 Tf", "72 760 Td", "14 TL"]
    for line in lines[:48]:
        content_lines.append(f"({_pdf_escape(line)}) Tj")
        content_lines.append("T*")
    content_lines.append("ET")
    stream = "\n".join(content_lines).encode("ascii")

    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        (
            b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
            b"/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>"
        ),
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Length " + str(len(stream)).encode("ascii") + b" >>\nstream\n" + stream + b"\nendstream",
    ]
    return _assemble_pdf(objects)


def _assemble_pdf(objects: list[bytes]) -> bytes:
    output = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for index, body in enumerate(objects, start=1):
        offsets.append(len(output))
        output.extend(f"{index} 0 obj\n".encode("ascii"))
        output.extend(body)
        output.extend(b"\nendobj\n")

    xref_offset = len(output)
    output.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    output.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        output.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    output.extend(
        (
            "trailer\n"
            f"<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
            "startxref\n"
            f"{xref_offset}\n"
            "%%EOF\n"
        ).encode("ascii")
    )
    return bytes(output)


def _pdf_escape(text: str) -> str:
    safe = text.encode("ascii", "ignore").decode("ascii")
    return safe.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


if __name__ == "__main__":
    book = BookOfBananaPudding()
    book.export_to_pdf("book_of_banana_pudding.pdf")
