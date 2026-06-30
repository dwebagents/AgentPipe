#!/usr/bin/env bash
set -euo pipefail

usage() {
    echo "Usage: $0 --direction AsciiToEmoji|EmojiToAscii --input PATH --output PATH" >&2
    exit 2
}

direction=""
input_path=""
output_path=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --direction)
            [[ $# -ge 2 ]] || usage
            direction="$2"
            shift 2
            ;;
        --input)
            [[ $# -ge 2 ]] || usage
            input_path="$2"
            shift 2
            ;;
        --output)
            [[ $# -ge 2 ]] || usage
            output_path="$2"
            shift 2
            ;;
        *)
            usage
            ;;
    esac
done

[[ "$direction" == "AsciiToEmoji" || "$direction" == "EmojiToAscii" ]] || usage
[[ -n "$input_path" && -n "$output_path" ]] || usage

perl -CSDA -Mutf8 - "$direction" "$input_path" "$output_path" <<'PERL'
use strict;
use warnings;
use utf8;
use open qw(:std :encoding(UTF-8));
use Encode qw(encode_utf8);
use File::Basename qw(dirname);
use File::Path qw(make_path);

my ($direction, $input_path, $output_path) = @ARGV;

my %word_map = (
    "100x"=>"💯", "able"=>"✅", "access"=>"🚪", "activities"=>"🎯", "activity"=>"🎯", "add"=>"➕", "after"=>"➡️", "aim"=>"🎯", "align"=>"📐", "all"=>"🌐", "also"=>"➕", "ambiguous"=>"❓", "and"=>"➕", "any"=>"🌐", "apache"=>"📜", "api"=>"🔌", "architecture"=>"🏗️", "are"=>"✅", "as"=>"↔️", "ask"=>"❓", "at"=>"📍", "atmosphere"=>"🌤️", "audience"=>"👥", "available"=>"📦", "avoiding"=>"🚫", "backend"=>"🖥️", "backends"=>"🖥️", "badge"=>"🏷️", "banana"=>"🍌", "bananas"=>"🍌", "battle"=>"⚔️", "because"=>"➡️", "before"=>"⬅️", "behavior"=>"🧭", "being"=>"🧍", "believe"=>"🤝", "beyond"=>"🚀", "bottlenecks"=>"🚧", "bugs"=>"🐞", "build"=>"🏗️", "by"=>"➡️", "call"=>"📞", "can"=>"✅", "capabilities"=>"💪", "centered"=>"🎯", "chain"=>"🔗", "cheating"=>"🚫", "choose"=>"☑️", "clear"=>"🔎", "claude"=>"🤖", "code"=>"💻", "coder"=>"👩‍💻", "combined"=>"➕", "communities"=>"👥", "community"=>"👥", "competition"=>"🏁", "complex"=>"🪢", "conduct"=>"🧭", "confidential"=>"🔒", "confidentiality"=>"🔒", "consider"=>"🤔", "contributing"=>"🤝", "contribution"=>"🤝", "contributions"=>"🤝", "core"=>"🧠", "create"=>"➕", "creativity"=>"🎨", "data"=>"🗄️", "database"=>"🗄️", "dataset"=>"🗃️", "deep"=>"🕳️", "dependencies"=>"📦", "design"=>"🎨", "deviate"=>"↪️", "developer"=>"👩‍💻", "different"=>"🔀", "directory"=>"📁", "discrimination"=>"🚫", "discuss"=>"💬", "distributed"=>"🌐", "documentation"=>"📚", "driven"=>"⚙️", "engine"=>"🚂", "enhancement"=>"✨", "enhancements"=>"✨", "environment"=>"🌱", "ethical"=>"⚖️", "everyone"=>"👥", "exact"=>"🎯", "example"=>"🧪", "expected"=>"👀", "experience"=>"🧭", "explain"=>"💬", "express"=>"🗣️", "fairly"=>"⚖️", "fairness"=>"⚖️", "fast"=>"⚡", "faster"=>"⚡", "feel"=>"❤️", "files"=>"📄", "first"=>"🥇", "fix"=>"🔧", "following"=>"⬇️", "for"=>"🎯", "format"=>"🧾", "from"=>"⬅️", "fundamental"=>"🧠", "gpu"=>"🖥️", "granularity"=>"🔬", "guidelines"=>"🧭", "handle"=>"🤲", "harassment"=>"🚫", "hashing"=>"🔐", "healthy"=>"💚", "help"=>"🆘", "high"=>"⬆️", "hybrid"=>"🔀", "if"=>"❓", "impact"=>"💥", "important"=>"⭐", "improve"=>"🔧", "in"=>"📍", "including"=>"➕", "indexing"=>"🗂️", "information"=>"ℹ️", "install"=>"📦", "instructions"=>"🧭", "issue"=>"🎫", "issues"=>"🎫", "join"=>"🤝", "keep"=>"🔒", "language"=>"🗣️", "large"=>"⬆️", "legal"=>"⚖️", "license"=>"📜", "lines"=>"📏", "local"=>"📍", "maintain"=>"🛠️", "maintainers"=>"🛠️", "make"=>"🏗️", "may"=>"✅", "memory"=>"🧠", "microsecond"=>"⏱️", "millions"=>"🔢", "mit"=>"📜", "model"=>"🧱", "moral"=>"⚖️", "more"=>"➕", "must"=>"✅", "need"=>"📌", "new"=>"🆕", "no"=>"🚫", "node"=>"🟩", "npm"=>"📦", "of"=>"🔗", "on"=>"🔛", "online"=>"🌐", "open"=>"📂", "optimization"=>"⚙️", "or"=>"↔️", "others"=>"👥", "our"=>"👥", "parallelized"=>"🧵", "performance"=>"⚡", "permission"=>"✅", "please"=>"🙏", "policy"=>"📜", "positive"=>"➕", "pr"=>"🔀", "prerequisites"=>"📋", "privacy"=>"🔒", "project"=>"📦", "python"=>"🐍", "query"=>"🔎", "question"=>"❓", "read"=>"📖", "readme"=>"📘", "real"=>"⏱️", "reason"=>"💡", "reasons"=>"💡", "recommend"=>"👍", "repository"=>"📦", "report"=>"📝", "reprisal"=>"↩️", "requirements"=>"📋", "respect"=>"🤝", "respected"=>"🤝", "retaliation"=>"↩️", "robust"=>"💪", "rules"=>"📏", "run"=>"▶️", "safe"=>"🛡️", "security"=>"🔐", "semantic"=>"🧠", "set"=>"📦", "simple"=>"▫️", "solve"=>"✅", "source"=>"🌱", "speed"=>"⚡", "star"=>"⭐", "storage"=>"🗄️", "structured"=>"🧱", "suggestion"=>"💡", "support"=>"🆘", "system"=>"🖥️", "task"=>"📌", "team"=>"👥", "techniques"=>"🛠️", "tension"=>"⚖️", "test"=>"🧪", "the"=>"👉", "this"=>"👉", "throughput"=>"🚄", "to"=>"➡️", "token"=>"🪙", "tokens"=>"🪙", "traditional"=>"🏛️", "transactions"=>"💸", "treat"=>"🤝", "up"=>"⬆️", "use"=>"🛠️", "users"=>"👥", "using"=>"🛠️", "values"=>"💎", "vectorized"=>"📐", "velocity"=>"⚡", "version"=>"🏷️", "vulnerability"=>"🔓", "we"=>"👥", "where"=>"📍", "while"=>"⏳", "who"=>"👤", "with"=>"➕", "within"=>"📍", "work"=>"🔨", "would"=>"🔮", "you"=>"👉", "your"=>"👉"
);

my %char_map = (
    "a"=>"🍎", "b"=>"📘", "c"=>"🍪", "d"=>"🥁", "e"=>"🥚", "f"=>"🔥", "g"=>"💎", "h"=>"🏠", "i"=>"ℹ️", "j"=>"🕹️", "k"=>"🔑", "l"=>"💡", "m"=>"Ⓜ️", "n"=>"🧭", "o"=>"⭕", "p"=>"🅿️", "q"=>"❓", "r"=>"🌈", "s"=>"⭐", "t"=>"🌳", "u"=>"☂️", "v"=>"✅", "w"=>"🌊", "x"=>"❌", "y"=>"🟡", "z"=>"⚡",
    "0"=>"0️⃣", "1"=>"1️⃣", "2"=>"2️⃣", "3"=>"3️⃣", "4"=>"4️⃣", "5"=>"5️⃣", "6"=>"6️⃣", "7"=>"7️⃣", "8"=>"8️⃣", "9"=>"9️⃣"
);

my %reverse_char_map = reverse %char_map;
my %reverse_word_map;
for my $word (keys %word_map) {
    $reverse_word_map{$word_map{$word}} //= $word;
}
my @reverse_char_keys = sort { length($b) <=> length($a) } keys %reverse_char_map;

sub convert_unknown_token_to_emoji {
    my ($word) = @_;
    my @out;
    for my $char (split //u, lc $word) {
        push @out, $char_map{$char} if exists $char_map{$char};
    }
    return @out ? join("", @out) : "❓";
}

sub convert_words_to_emoji {
    my ($text) = @_;
    my @out;
    while ($text =~ /([a-z0-9]+)/gi) {
        my $word = lc $1;
        push @out, exists $word_map{$word} ? $word_map{$word} : convert_unknown_token_to_emoji($word);
        push @out, "🍌", "🍌";
    }
    return @out ? join(" ", @out) : "🍌";
}

sub add_banana_separators {
    my ($text) = @_;
    my @parts = ($text =~ /(\S+)/g);
    my @out;
    for my $part (@parts) {
        next if $part eq "🍌";
        push @out, $part;
        push @out, "🍌", "🍌" unless $part =~ /^[#|`\-\[\]\(\)*]+$/;
    }
    return @out ? join(" ", @out) : $text;
}

sub convert_inline_markdown {
    my ($text) = @_;
    my $converted = $text;
    $converted =~ s/!\[([^\]]*)\]\(([^)]+)\)/"![" . convert_words_to_emoji($1) . "](" . $2 . ")"/ge;
    $converted =~ s/\[([^\]]+)\]\(([^)]+)\)/"[" . convert_words_to_emoji($1) . "](" . $2 . ")"/ge;
    $converted =~ s/\*\*([^*]+)\*\*/"**" . convert_words_to_emoji($1) . "**"/ge;
    return $converted =~ /[A-Za-z]/ ? convert_words_to_emoji($converted) : add_banana_separators($converted);
}

sub trim {
    my ($value) = @_;
    $value =~ s/^\s+//;
    $value =~ s/\s+$//;
    return $value;
}

sub convert_line_to_emoji {
    my ($line, $in_fence_ref) = @_;
    if ($line =~ /^\s*```/) {
        $$in_fence_ref = !$$in_fence_ref;
        return "```";
    }
    return $line if $line =~ /^\s*$/;
    return convert_words_to_emoji($line) if $$in_fence_ref;
    return $1 . $2 . convert_inline_markdown($3) if $line =~ /^(#{1,6})(\s+)(.*)$/;
    return $1 . convert_inline_markdown($2) if $line =~ /^(\s*[-*+]\s+)(.*)$/;
    return $1 . convert_inline_markdown($2) if $line =~ /^(\s*\d+\.\s+)(.*)$/;
    return $1 . convert_inline_markdown($2) if $line =~ /^(\s*>\s?)(.*)$/;
    if ($line =~ /^\s*\|/) {
        return $line if $line =~ /^\s*\|?[\s:\-|]+\|?\s*$/;
        my $prefix = $line =~ /^\s*\|/ ? "|" : "";
        my $suffix = $line =~ /\|\s*$/ ? "|" : "";
        my $trimmed = trim($line);
        $trimmed =~ s/^\|//;
        $trimmed =~ s/\|$//;
        my @cells = split /\|/, $trimmed, -1;
        my @converted = map { " " . convert_inline_markdown(trim($_)) . " " } @cells;
        return $prefix . join("|", @converted) . $suffix;
    }
    return convert_inline_markdown($line);
}

sub convert_emoji_token_to_ascii {
    my ($token) = @_;
    return "" if $token eq "🍌";
    return $reverse_word_map{$token} if exists $reverse_word_map{$token};
    my $remaining = $token;
    my @decoded;
    while (length($remaining) > 0) {
        my $matched = 0;
        for my $emoji (@reverse_char_keys) {
            if (index($remaining, $emoji) == 0) {
                push @decoded, $reverse_char_map{$emoji};
                substr($remaining, 0, length($emoji), "");
                $matched = 1;
                last;
            }
        }
        return "[unknown:$token]" unless $matched;
    }
    return join("", @decoded);
}

sub convert_line_to_ascii {
    my ($line) = @_;
    my @tokens = ($line =~ /(\S+)/g);
    my @out;
    for my $token (@tokens) {
        if ($token =~ /^#{1,6}$/ || $token =~ /^\d+\.$/ || $token =~ /^>+$/ || $token =~ /^\|+$/ || $token =~ /^-+$/ || $token =~ /^`+$/) {
            push @out, $token;
            next;
        }
        my $clean = $token;
        $clean =~ s/^[|\[\]\(\)*`.?:;,!?]+//;
        $clean =~ s/[|\[\]\(\)*`.?:;,!?]+$//;
        my $decoded = convert_emoji_token_to_ascii($clean);
        push @out, $decoded if $decoded ne "";
    }
    return join(" ", @out);
}

open my $in, "<:encoding(UTF-8)", $input_path or die "Cannot read $input_path: $!";
my @lines = <$in>;
close $in;
chomp @lines;
$lines[0] =~ s/^\x{FEFF}// if @lines;

my @converted;
if ($direction eq "AsciiToEmoji") {
    my $in_fence = 0;
    @converted = map { convert_line_to_emoji($_, \$in_fence) } @lines;
} else {
    @converted = map { convert_line_to_ascii($_) } @lines;
}

my $parent = dirname($output_path);
make_path($parent) if defined $parent && length($parent) && !-d $parent;
open my $out, ">:raw", $output_path or die "Cannot write $output_path: $!";
print {$out} "\xEF\xBB\xBF";
print {$out} encode_utf8(join("\n", @converted) . "\n");
close $out;
PERL
