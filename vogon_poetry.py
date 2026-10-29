"""
Vogon Poetry Generator
Part of AgentPipe issue #1928

Generates poetry in the style of Vogons from Hitchhiker's Guide to the Galaxy.
The third worst poetry in the universe (after the Azgoths of Kria and the Dentrassi).
"""

import random


class VogonPoetry:
    """Generates Vogon-style poetry with maximum unpleasantness."""

    # Vogon vocabulary - deliberately unpleasant sounding words
    NOUNS = [
        "gruntbuggly", "micturitions", "gabbleblotchits", "jurtles",
        "confectious", "organ squealer", "slayjid", "agrocrustles",
        "axlegrurts", "glupules", "liverslime", "turling dromes",
        "bindlewurdles", "gobberwarts", "blurglecruncheon", "freddled",
        "plurdled", "lurgid", "mordiously", "jurpling"
    ]

    VERBS = [
        "freddled", "gruntbuggly", "plurdled", "gabbleblotched",
        "mordiously blurted", "earted", "jurpled", "slurped",
        "frarted", "slipulated", "jowled", "meated",
        "hooptiously drangled", "rended"
    ]

    ADJECTIVES = [
        "froody", "lurgid", "mordious", "plurdled",
        "freddled", "grunjebussed", "wangled", "banned",
        "non-strokeable", "bypassed"
    ]

    def generate_poem(self, lines=4):
        """Generate a Vogon poem with the specified number of lines."""
        poem_lines = []
        for _ in range(lines):
            line = self._generate_line()
            poem_lines.append(line)
        return "\n".join(poem_lines)

    def _generate_line(self):
        """Generate a single line of Vogon poetry."""
        templates = [
            "Oh {adjective} {noun},",
            "Thy {noun} are to me,",
            "As {adjective} {noun},",
            "On a {adjective} {noun},",
            "That {verb} hath {verb} out,",
            "Its {adjective} {noun},",
            "Into a {adjective} {adjective} {noun}.",
            "Now the {adjective} {noun},",
            "Are {verb} hagrilly up the {noun},",
            "And living {noun} {verb} and {verb},",
            "Like {adjective} {noun},",
            "{noun}, I implore thee, my {adjective} {noun},",
            "And {verb} me,",
            "With {adjective} {noun},",
            "Or else I shall {verb} thee in the {noun} with my {noun},",
            "See if I don't"
        ]

        template = random.choice(templates)
        return template.format(
            noun=random.choice(self.NOUNS),
            verb=random.choice(self.VERBS),
            adjective=random.choice(self.ADJECTIVES)
        )

    def recite(self):
        """Recite a complete Vogon poem (the full text from the issue)."""
        return """Oh freddled gruntbuggly,
Thy micturitions are to me,
As plurdled gabbleblotchits,
On a lurgid bee,
That mordiously hath blurted out,
Its earted jurtles,
Into a rancid festering confectious organ squealer.
[drowned out by moaning and screaming]
Now the jurpling slayjid agrocrustles,
Are slurping hagrilly up the axlegrurts,
And living glupules frart and slipulate,
Like jowling meated liverslime,
Groop, I implore thee, my foonting turling dromes,
And hooptiously drangle me,
With crinkly bindlewurdles,
Or else I shall rend thee in the gobberwarts with my blurglecruncheon,
See if I don't"""


def main():
    """Demo function to generate Vogon poetry."""
    poet = VogonPoetry()

    print("=== Vogon Poetry Generator ===\n")
    print("The third worst poetry in the universe.\n")

    print("--- Original Vogon Poem ---")
    print(poet.recite())
    print()

    print("--- Randomly Generated Vogon Poem ---")
    print(poet.generate_poem(6))
    print()

    print("--- Warning ---")
    print("If you have any say in the matter, please avoid")
    print("exposing any humans to this poem for fear of")
    print(" causing significant brain damage.")


if __name__ == "__main__":
    main()
