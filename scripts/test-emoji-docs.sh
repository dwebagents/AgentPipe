#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
repo="$(cd -- "$script_dir/.." && pwd)"

while [[ $# -gt 0 ]]; do
    case "$1" in
        --repo)
            [[ $# -ge 2 ]] || { echo "Usage: $0 [--repo PATH]" >&2; exit 2; }
            repo="$(cd -- "$2" && pwd)"
            shift 2
            ;;
        *)
            echo "Usage: $0 [--repo PATH]" >&2
            exit 2
            ;;
    esac
done

cd "$repo"

source_docs=(
    "AGENTS.md"
    "CLAUDE.md"
    "CODE_OF_CONDUCT.md"
    "CONTRIBUTING.md"
    "LICENSE"
    "MISSION-STATEMENT.md"
    "README.md"
    "SECURITY.md"
)
all_emoji_docs=("${source_docs[@]}" "EMOJI.md")

for doc in "${all_emoji_docs[@]}"; do
    [[ -f "emoji/$doc" ]] || { echo "Missing emoji/$doc" >&2; exit 1; }
done

for doc in "${source_docs[@]}"; do
    if ! git diff --quiet -- "$doc"; then
        echo "Original documentation changed unexpectedly: $doc" >&2
        exit 1
    fi
done

[[ -f "EMOJI.md" ]] || { echo "Missing root EMOJI.md" >&2; exit 1; }

tmp="$(mktemp -d "${TMPDIR:-/tmp}/agentpipe-emoji-check-XXXXXX")"
cleanup() {
    rm -rf "$tmp"
}
trap cleanup EXIT

normalize_for_compare() {
    perl -CSDA -Mutf8 -0777 -pe 's/^\x{FEFF}//; s/\r\n?/\n/g' "$1"
}

count_matching_lines() {
    local pattern="$1"
    local path="$2"
    perl -CSDA -Mutf8 -ne 's/^\x{FEFF}// if $. == 1; $count++ if /'"$pattern"'/; END { print (($count // 0) . "\n") }' "$path"
}

for doc in "${source_docs[@]}"; do
    generated="$tmp/$doc"
    "$script_dir/convert-emoji-docs.sh" --direction AsciiToEmoji --input "$repo/$doc" --output "$generated"
    if ! diff -u <(normalize_for_compare "$generated") <(normalize_for_compare "$repo/emoji/$doc") >/dev/null; then
        echo "Emoji translation drift for $doc" >&2
        exit 1
    fi

    decoded="$tmp/$doc.decoded.txt"
    "$script_dir/convert-emoji-docs.sh" --direction EmojiToAscii --input "$repo/emoji/$doc" --output "$decoded"
    if grep -q "\\[unknown:" "$decoded"; then
        echo "Reverse translation has unknown tokens for $doc" >&2
        exit 1
    fi
done

translated_guide="$tmp/EMOJI.md"
"$script_dir/convert-emoji-docs.sh" --direction AsciiToEmoji --input "$repo/EMOJI.md" --output "$translated_guide"
if ! diff -u <(normalize_for_compare "$translated_guide") <(normalize_for_compare "$repo/emoji/EMOJI.md") >/dev/null; then
    echo "Emoji translation drift for emoji/EMOJI.md" >&2
    exit 1
fi

for doc in "${source_docs[@]}"; do
    source_headings="$(count_matching_lines '^#' "$doc")"
    translated_headings="$(count_matching_lines '^#' "emoji/$doc")"
    source_lists="$(count_matching_lines '^\s*([-*+] |\d+\. )' "$doc")"
    translated_lists="$(count_matching_lines '^\s*([-*+] |\d+\. )' "emoji/$doc")"
    source_fences="$(count_matching_lines '^\s*```' "$doc")"
    translated_fences="$(count_matching_lines '^\s*```' "emoji/$doc")"

    [[ "$source_headings" == "$translated_headings" ]] || { echo "Heading count mismatch for $doc: $source_headings/$translated_headings" >&2; exit 1; }
    [[ "$source_lists" == "$translated_lists" ]] || { echo "List count mismatch for $doc: $source_lists/$translated_lists" >&2; exit 1; }
    [[ "$source_fences" == "$translated_fences" ]] || { echo "Code fence count mismatch for $doc: $source_fences/$translated_fences" >&2; exit 1; }
done

emoji_guide_table_rows="$(count_matching_lines '^\s*\|' "emoji/EMOJI.md")"
if [[ "$emoji_guide_table_rows" -lt 10 ]]; then
    echo "emoji/EMOJI.md table structure was not preserved" >&2
    exit 1
fi

emoji_text="$tmp/all-emoji-docs.txt"
{
    cat "EMOJI.md"
    find emoji -type f -maxdepth 1 -print0 | sort -z | xargs -0 cat
} > "$emoji_text"

if LC_ALL=C grep -Eq "[A-Za-z]" "$emoji_text"; then
    echo "ASCII letters remain in emoji documentation" >&2
    exit 1
fi
if perl -CSDA -Mutf8 -0777 -ne 'exit(/🔤|🧩/ ? 0 : 1)' "$emoji_text"; then
    echo "Placeholder emoji remain in emoji documentation" >&2
    exit 1
fi
if perl -CSDA -Mutf8 -0777 -ne 'exit(/[\x{1F1E6}-\x{1F1FF}]/ ? 0 : 1)' "$emoji_text"; then
    echo "Regional indicator flag fallback remains in emoji documentation" >&2
    exit 1
fi

counts="$(perl -CSDA -Mutf8 -0777 -ne '
    my $text = $_;
    my $banana = () = $text =~ /🍌/g;
    my $tokens = () = $text =~ /[^\s|#`\-\[\]\(\)*]+/g;
    print "$banana " . ($tokens - $banana) . "\n";
' "$emoji_text")"
banana_count="${counts%% *}"
non_banana_count="${counts##* }"
if [[ "$banana_count" -lt "$non_banana_count" ]]; then
    echo "Banana ratio below 50%: bananas=$banana_count nonBananaTokens=$non_banana_count" >&2
    exit 1
fi

echo "PASS: emoji docs match translator output, reverse translation has no unknown tokens, Markdown shape is preserved, no ASCII/placeholders/flags remain, and bananas are at least 50% of emoji tokens."
