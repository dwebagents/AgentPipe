# Mascot Pattern Generator

`scripts/generate_mascot_pattern.pl` creates a Markdown craft pattern for a project mascot.

Example:

```sh
perl scripts/generate_mascot_pattern.pl --banana 3 --goose 1 --goblin 2 --yarn dk --height 22 --output mascot.md
```

The generator supports:

- relative feature ratios with `--banana`, `--goose`, and `--goblin`
- `crochet` or `knit` instructions through `--craft`
- yarn-weight scaling through `--yarn`
- finished-size scaling through `--height`
- stdout output or file output through `--output`

