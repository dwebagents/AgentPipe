#!/usr/bin/env perl
# agentpipe_mascot.pl - AgentPipe Mascot Crochet & Knitting Pattern Generator
#
# Generates a detailed, row-by-row crochet or knitting pattern for the
# AgentPipe project mascot — a banana/goose/goblin hybrid — with
# adjustable motif ratios, yarn weight scaling, and multiple output formats.
#
# Usage:
#   perl agentpipe_mascot.pl --banana 2 --goose 1 --goblin 1
#   perl agentpipe_mascot.pl --craft knit --yarn-weight worsted --scale 1.25
#   perl agentpipe_mascot.pl --format html --output mascot.html
#   perl agentpipe_mascot.pl --help
#
# Dependencies: None beyond core Perl (Getopt::Long, Pod::Usage optional).
# Licensed under the MIT License.

use strict;
use warnings;
use Getopt::Long qw(GetOptions);

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Yarn weight profiles: hook/needle size, gauge (sts/10cm), yardage multiplier
my %WEIGHT = (
    lace      => { hook => '2.25 mm', needle => '2.25 mm', gauge => 32, mult => 1.45 },
    fingering => { hook => '2.75 mm', needle => '2.75 mm', gauge => 28, mult => 1.25 },
    sport     => { hook => '3.50 mm', needle => '3.50 mm', gauge => 24, mult => 1.10 },
    dk        => { hook => '4.00 mm', needle => '4.00 mm', gauge => 22, mult => 1.00 },
    worsted   => { hook => '5.00 mm', needle => '5.00 mm', gauge => 18, mult => 0.86 },
    bulky     => { hook => '6.50 mm', needle => '6.50 mm', gauge => 14, mult => 0.72 },
);

# Motif colour palettes
my %PALETTE = (
    banana => {
        main  => 'Yellow (e.g. Stylecraft Special DK - Lemon)',
        light => 'Pale yellow/cream (e.g. Stylecraft Special DK - Cream)',
        dark  => 'Dark brown (e.g. Stylecraft Special DK - Dark Brown)',
    },
    goose => {
        main  => 'White/cream (e.g. Stylecraft Special DK - White)',
        light => 'Pale grey (e.g. Stylecraft Special DK - Silver)',
        dark  => 'Orange (e.g. Stylecraft Special DK - Mandarin)',
    },
    goblin => {
        main  => 'Green (e.g. Stylecraft Special DK - Meadow)',
        light => 'Lime green (e.g. Stylecraft Special DK - Spring Green)',
        dark  => 'Black/dark grey (e.g. Stylecraft Special DK - Black)',
    },
);

my @PARTS = qw(banana goose goblin);

# ---------------------------------------------------------------------------
# Defaults & option parsing
# ---------------------------------------------------------------------------

# US ↔ UK crochet terminology mapping (knitting terms are identical)
my %US2UK = (
    'sc'        => 'dc',       # single crochet → double crochet
    'hdc'       => 'htr',      # half double crochet → half treble
    'dc'        => 'tr',       # double crochet → treble
    'tr'        => 'dtr',      # treble → double treble
    'sl st'     => 'ss',       # slip stitch → slip stitch
    'sc2tog'    => 'dc2tog',   # single crochet 2 together
    'hdc2tog'   => 'htr2tog',  # half double crochet 2 together
    'dc2tog'    => 'tr2tog',   # double crochet 2 together
);

# Emoji dictionary for full-emoji output mode
my %EMOJI = (
    'crochet'       => "\x{1F9F6}",          # 🧶
    'knit'          => "\x{1F9F6}",          # 🧶
    'knitting'      => "\x{1F9F6}",          # 🧶
    'stitch'        => "\x{1FAA1}",          # 🪡
    'stitches'      => "\x{1FAA1}",          # 🪡
    'sts'           => "\x{1FAA1}",          # 🪡
    'round'         => "\x{2B55}",           # ⭕
    'rounds'        => "\x{2B55}",           # ⭕
    'row'           => "\x{1F4CF}",          # 📏
    'rows'          => "\x{1F4CF}",          # 📏
    'magic ring'    => "\x{1F9D9}\x{2B55}", # 🧙⭕
    'increase'      => "\x{1F4C8}",          # 📈
    'inc'           => "\x{1F4C8}",          # 📈
    'decrease'      => "\x{1F4C9}",          # 📉
    'dec'           => "\x{1F4C9}",          # 📉
    'chain'         => "\x{26D3}\x{FE0F}",   # ⛓
    'ch'            => "\x{26D3}\x{FE0F}",   # ⛓
    'hook'          => "\x{1FA9D}",          # 🪝
    'needle'        => "\x{1F4CC}",          # 📌
    'needles'       => "\x{1F4CC}",          # 📌
    'body'          => "\x{1F4AA}",          # 💪
    'head'          => "\x{1F464}",          # 👤
    'wing'          => "\x{1F985}",          # 🦅
    'wings'         => "\x{1F985}",          # 🦅
    'beak'          => "\x{1F426}",          # 🐦
    'ear'           => "\x{1F442}",          # 👂
    'ears'          => "\x{1F442}",          # 👂
    'tail'          => "\x{1F43A}",          # 🐺
    'banana'        => "\x{1F34C}",          # 🍌
    'goose'         => "\x{1F986}",          # 🦆
    'goblin'        => "\x{1F47A}",          # 👺
    'colour'        => "\x{1F3A8}",          # 🎨
    'color'         => "\x{1F3A8}",          # 🎨
    'colours'       => "\x{1F3A8}",          # 🎨
    'colors'        => "\x{1F3A8}",          # 🎨
    'yellow'        => "\x{1F7E1}",          # 🟡
    'white'         => "\x{26AA}\x{FE0F}",   # ⚪
    'green'         => "\x{1F7E2}",          # 🟢
    'orange'        => "\x{1F7E0}",          # 🟠
    'brown'         => "\x{1F7E4}",          # 🟤
    'black'         => "\x{26AB}\x{FE0F}",   # ⚫
    'grey'          => "\x{1F90F}",          # 🤏 (close enough to grey)
    'gray'          => "\x{1F90F}",          # 🤏
    'cream'         => "\x{1F9F2}",          # 🧲 (placeholder)
    'materials'     => "\x{1F4E6}",          # 📦
    'yardage'       => "\x{1F4D0}",          # 📐
    'yarn'          => "\x{1F9F5}",          # 🧵
    'stuffing'      => "\x{1F9F8}",          # 🧸
    'eyes'          => "\x{1F440}",          # 👀
    'face'          => "\x{1F600}",          # 😀
    'smile'         => "\x{1F642}",          # 🙂
    'mouth'         => "\x{1F444}",          # 👄
    'around'        => "\x{1F504}",          # 🔄
    'repeat'        => "\x{1F501}",          # 🔁
    'fasten off'    => "\x{1F51A}\x{2702}\x{FE0F}", # 🔚✂
    'fasten'        => "\x{1F51A}",          # 🔚
    'sew'           => "\x{1FAA1}",          # 🪡
    'sewing'        => "\x{1FAA1}",          # 🪡
    'weave'         => "\x{1F9F5}",          # 🧵
    'block'         => "\x{1F9CA}",          # 🧊
    'steam'         => "\x{2668}\x{FE0F}",   # ♨
    'dry'           => "\x{2600}\x{FE0F}",   # ☀
    'shape'         => "\x{1F3AD}",          # 🎭
    'finish'        => "\x{1F3C1}",          # 🏁
    'finishing'     => "\x{1F3C1}",          # 🏁
    'complete'      => "\x{2705}",           # ✅
    'make'          => "\x{2795}",           # ➕
    'leave'         => "\x{1F4A4}",          # 💤
    'work'          => "\x{1F477}",          # 👷
    'together'      => "\x{1F91D}",          # 🤝
    'fold'          => "\x{1F447}",          # 👇
    'edge'          => "\x{1F5BC}\x{FE0F}",  # 🖼
    'panel'         => "\x{1F4CB}",          # 📋
    'taper'         => "\x{25C0}\x{FE0F}",   # ◀
    'evenly'        => "\x{2696}\x{FE0F}",   # ⚖
    'gauge'         => "\x{1F4D0}",          # 📐
    'swatch'        => "\x{1F9F5}",          # 🧵
    'pattern'       => "\x{1F4DC}",          # 📜
    'instructions'  => "\x{1F4D6}",          # 📖
    'instruction'   => "\x{1F4D6}",          # 📖
    'motif'         => "\x{1F3A8}",          # 🎨
    'motifs'        => "\x{1F3A8}",          # 🎨
    'assembly'      => "\x{1F527}",          # 🔧
    'placement'     => "\x{1F4CD}",          # 📍
    'marker'        => "\x{1F4CC}",          # 📌
    'markers'       => "\x{1F4CC}",          # 📌
    'scissors'      => "\x{2702}\x{FE0F}",   # ✂
    'tapestry'      => "\x{1FAA1}",          # 🪡
    'notions'       => "\x{1F9F0}",          # 🧰
    'beginner'      => "\x{1F530}",          # 🔰
    'intermediate'  => "\x{1F3AF}",          # 🎯
    'advanced'      => "\x{1F451}",          # 👑
    'skill'         => "\x{1F3AF}",          # 🎯
    'overview'      => "\x{1F50D}",          # 🔍
    'design'        => "\x{1F3A8}",          # 🎨
    'height'        => "\x{1F4CF}",          # 📏
    'cm'            => "\x{1F4D0}",          # 📐
    'approx'        => "\x{2248}",           # ≈
    'technique'     => "\x{1F9BE}",          # 🦾
    'suggested'     => "\x{1F4A1}",          # 💡
    'main'          => "\x{1F3F3}\x{FE0F}",  # 🏳
    'accent'        => "\x{2728}",           # ✨
    'outline'       => "\x{1F3F3}\x{FE0F}",  # 🏳
    'diameter'      => "\x{1F4D0}",          # 📐
    'customisation' => "\x{1F3A8}",          # 🎨
    'expression'    => "\x{1F600}",          # 😀
    'personality'   => "\x{1F916}",          # 🤖
    'substitute'    => "\x{1F504}",          # 🔄
    'recommend'     => "\x{1F44D}",          # 👍
    'gentle'        => "\x{1F90F}",          # 🤏
    'lightly'       => "\x{1F90F}",          # 🤏
    'details'       => "\x{1F50D}",          # 🔍
    'surface'       => "\x{1F3AF}",          # 🎯
    'brush'         => "\x{1FAA4}",          # 🪤
    'add'           => "\x{2795}",           # ➕
    'use'           => "\x{1F4A1}",          # 💡
    'work'          => "\x{1F477}",          # 👷
    'worked'        => "\x{1F477}",          # 👷
    'attach'        => "\x{1F527}",          # 🔧
    'attaching'     => "\x{1F527}",          # 🔧
    'attached'      => "\x{1F527}",          # 🔧
    'open'          => "\x{1F4C2}",          # 📂
    'close'         => "\x{1F4C1}",          # 📁
    'pull'          => "\x{1F447}",          # 👇
    'tight'         => "\x{1F4AA}",          # 💪
    'tightly'       => "\x{1F4AA}",          # 💪
    'position'      => "\x{1F4CD}",          # 📍
    'top'           => "\x{1F51D}",          # 🔝
    'bottom'        => "\x{1F53D}",          # 🔽
    'back'          => "\x{1F519}",          # 🔙
    'front'         => "\x{1F51A}",          # 🔚
    'side'          => "\x{1F519}",          # 🔙
    'sides'         => "\x{1F519}",          # 🔙
    'centre'        => "\x{1F3AF}",          # 🎯
    'center'        => "\x{1F3AF}",          # 🎯
    'centred'       => "\x{1F3AF}",          # 🎯
    'centered'      => "\x{1F3AF}",          # 🎯
    'down'          => "\x{1F53D}",          # 🔽
    'upward'        => "\x{1F53C}",          # 🔼
    'outward'       => "\x{1F519}",          # 🔙
    'vertical'      => "\x{1F53D}",          # 🔽
    'spaced'        => "\x{1F4D0}",          # 📐
    'below'         => "\x{2B07}\x{FE0F}",   # ⬇
    'forward'       => "\x{27A1}\x{FE0F}",   # ➡
    'neatly'        => "\x{2728}",           # ✨
    'half'          => "\x{00BD}",           # ½
    'extra'         => "\x{2795}",           # ➕
    'desired'       => "\x{1F3AF}",          # 🎯
    'change'        => "\x{1F504}",          # 🔄
    'changes'       => "\x{1F504}",          # 🔄
    'carried'       => "\x{1F4E6}",          # 📦
    'cut'           => "\x{2702}\x{FE0F}",   # ✂
    'inside'        => "\x{1F4A1}",          # 💡
    'adjust'        => "\x{1F527}",          # 🔧
    'needed'        => "\x{1F6A7}",          # 🚧
    'first'         => "\x{0031}\x{20E3}",   # 1️⃣
    'second'        => "\x{0032}\x{20E3}",   # 2️⃣
    'third'         => "\x{0033}\x{20E3}",   # 3️⃣
    'fourth'        => "\x{0034}\x{20E3}",   # 4️⃣
    'fifth'         => "\x{0035}\x{20E3}",   # 5️⃣
    'one'           => "\x{0031}\x{20E3}",   # 1️⃣
    'two'           => "\x{0032}\x{20E3}",   # 2️⃣
    'three'         => "\x{0033}\x{20E3}",   # 3️⃣
    'four'          => "\x{0034}\x{20E3}",   # 4️⃣
    'five'          => "\x{0035}\x{20E3}",   # 5️⃣
    'six'           => "\x{0036}\x{20E3}",   # 6️⃣
    'seven'         => "\x{0037}\x{20E3}",   # 7️⃣
    'eight'         => "\x{0038}\x{20E3}",   # 8️⃣
    'nine'          => "\x{0039}\x{20E3}",   # 9️⃣
    'ten'           => "\x{1F51F}",          # 🔟
    'make'          => "\x{2795}",           # ➕
    'part'          => "\x{1F9F0}",          # 🧰
    'parts'         => "\x{1F9F0}",          # 🧰
    'order'         => "\x{1F522}",          # 🔢
    'preparation'   => "\x{1F4E6}",          # 📦
    'prep'          => "\x{1F4E6}",          # 📦
    'preparing'     => "\x{1F4E6}",          # 📦
    'prepared'      => "\x{1F4E6}",          # 📦
    'stuff'         => "\x{1F9F8}",          # 🧸
    'firmly'        => "\x{1F4AA}",          # 💪
    'hidden'        => "\x{1F648}",          # 🙈
    'angle'         => "\x{1F4CF}",          # 📐
    'angled'        => "\x{1F4CF}",          # 📐
    'slightly'      => "\x{1F90F}",          # 🤏
    'wide'          => "\x{1F4D0}",          # 📐
    'point'         => "\x{1F3AF}",          # 🎯
    'placed'        => "\x{1F4CD}",          # 📍
    'place'         => "\x{1F4CD}",          # 📍
    'safety'        => "\x{1F6D1}",          # 🛑
    'thread'        => "\x{1F9F5}",          # 🧵
    'embroider'     => "\x{1FAA1}",          # 🪡
    'embroidery'    => "\x{1FAA1}",          # 🪡
    'embroidered'   => "\x{1FAA1}",          # 🪡
    'eyebrows'      => "\x{1F9B0}",          # 🦰
    'nostrils'      => "\x{1F443}",          # 👃
    'freckles'      => "\x{1F4D0}",          # 📐
    'feather'       => "\x{1FAB6}",          # 🪶
    'marks'         => "\x{1F4CC}",          # 📌
    'neutral'       => "\x{1F610}",          # 😐
    'soft'          => "\x{1F90F}",          # 🤏
    'curved'        => "\x{1F4CF}",          # 📐
    'small'         => "\x{1F90F}",          # 🤏
    'sharp'         => "\x{1F5E1}\x{FE0F}",  # 🗡
    'worried'       => "\x{1F61F}",          # 😟
    'blank'         => "\x{1F636}",          # 😶
    'mischievous'   => "\x{1F61C}",          # 😜
    'raised'        => "\x{1F4C8}",          # 📈
    'wry'           => "\x{1F61B}",          # 😛
    'cheeky'        => "\x{1F60F}",          # 😏
    'grin'          => "\x{1F600}",          # 😀
    'size'          => "\x{1F4D0}",          # 📐
    'bigger'        => "\x{1F7E2}",          # 🟢
    'smaller'       => "\x{1F534}",          # 🔴
    'longer'        => "\x{1F4CF}",          # 📏
    'rounder'       => "\x{2B55}",           # ⭕
    'instead'       => "\x{1F504}",          # 🔄
    'ratio'         => "\x{1F522}",          # 🔢
    'ratios'        => "\x{1F522}",          # 🔢
    'details'       => "\x{1F50D}",          # 🔍
    'extra'         => "\x{2795}",           # ➕
    'also'          => "\x{2795}",           # ➕
);

my %opt = (
    banana     => 1,
    goose      => 1,
    goblin     => 1,
    yarn_weight => 'dk',
    craft      => 'crochet',
    scale      => 1.0,
    name       => 'AgentPipe Mascot',
    format     => 'markdown',
    output     => '-',
    skill      => '',
    terminology => 'us',
    emoji      => 0,
);

GetOptions(
    'banana=f'       => \$opt{banana},
    'goose=f'        => \$opt{goose},
    'goblin=f'       => \$opt{goblin},
    'yarn-weight=s'  => \$opt{yarn_weight},
    'craft=s'        => \$opt{craft},
    'scale=f'        => \$opt{scale},
    'name=s'         => \$opt{name},
    'format=s'       => \$opt{format},
    'output=s'       => \$opt{output},
    'skill=s'        => \$opt{skill},
    'terminology=s'  => \$opt{terminology},
    'emoji!'         => \$opt{emoji},
    'help'           => \$opt{help},
) or usage(1);

usage(0) if $opt{help};

# Validate
my $profile = $WEIGHT{lc $opt{yarn_weight}}
    or die "Unknown yarn weight '$opt{yarn_weight}'. Valid: " . join(', ', sort keys %WEIGHT) . "\n";

$opt{craft} = lc $opt{craft};
die "Craft must be 'crochet' or 'knit'.\n"
    unless $opt{craft} eq 'crochet' || $opt{craft} eq 'knit';

die "Scale must be > 0.\n" unless $opt{scale} > 0;
for my $p (@PARTS) { die "$p ratio must be >= 0.\n" if $opt{$p} < 0 }

my $total_ratio = $opt{banana} + $opt{goose} + $opt{goblin};
die "At least one ratio must be > 0.\n" if $total_ratio <= 0;

$opt{format} = lc $opt{format};
die "Format must be markdown, text, or html.\n"
    unless $opt{format} =~ /^(markdown|text|html)$/;

$opt{terminology} = lc $opt{terminology};
die "Terminology must be 'us' or 'uk'.\n"
    unless $opt{terminology} eq 'us' || $opt{terminology} eq 'uk';

# Derived values
my %ratio = map { $_ => $opt{$_} / $total_ratio } @PARTS;
my $dominant = (sort { $ratio{$b} <=> $ratio{$a} } keys %ratio)[0];

# Dimensions (all scale with --scale)
my $body_rounds    = max(1, int(22 * $opt{scale} + 0.5));
my $body_max_sts   = max(12, even(int($profile->{gauge} * $opt{scale} * 0.9 + 0.5)));
my $increase_over  = int($body_rounds * 0.35 + 0.5);   # rounds to increase
my $even_over      = int($body_rounds * 0.40 + 0.5);   # rounds even
my $decrease_over  = $body_rounds - $increase_over - $even_over; # rounds to decrease
my $height_cm      = sprintf('%.1f', 20 * $opt{scale});
my $wing_rows      = max(3, int(8 * $opt{scale} + 0.5));
my $ear_rows       = max(3, int(5 * $opt{scale} + 0.5));
my $beak_sts       = max(3, int(4 * $opt{scale} + 0.5));
my $yardage_base   = int(100 * $profile->{mult} * $opt{scale} + 0.5);

# Generate increase schedule
my @inc_rounds = increase_schedule($body_max_sts, $increase_over);
my $cast_on = 6;

# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

my $out_fh;
if ($opt{output} && $opt{output} ne '-') {
    open $out_fh, '>:utf8', $opt{output} or die "Cannot write $opt{output}: $!\n";
} else {
    $out_fh = \*STDOUT;
    binmode STDOUT, ':utf8';
}

my $out = sub {
    my ($fh, $text) = @_;
    print $fh $text;
};

my $output = '';
if ($opt{format} eq 'html') {
    $output .= html_header($opt{name});
    my $md = generate_markdown($profile, \%ratio, $dominant);
    $output .= md_to_html($md, $opt{name});
    $output .= html_footer();
} elsif ($opt{format} eq 'text') {
    $output .= generate_text($profile, \%ratio, $dominant);
} else {
    $output .= generate_markdown($profile, \%ratio, $dominant);
}

$output = translate_output($output);
print $out_fh $output;

close $out_fh if $opt{output} && $opt{output} ne '-';

# ---------------------------------------------------------------------------
# Generation functions
# ---------------------------------------------------------------------------

sub generate_markdown {
    my ($profile, $ratio, $dominant) = @_;

    my $craft_noun = $opt{craft} eq 'crochet' ? 'Crochet' : 'Knit';
    my $tool       = $opt{craft} eq 'crochet' ? 'hook'      : 'needles';
    my $tool_size  = $opt{craft} eq 'crochet' ? $profile->{hook} : $profile->{needle};
    my $skill      = determine_skill();

    my $out = '';

    $out .= "# $opt{name}\n\n";
    $out .= "## Overview\n\n";
    $out .= "- **Design:** A " . ratio_desc($ratio) . " hybrid mascot\n";
    $out .= "- **Height:** approx. $height_cm cm (" . sprintf('%.1f', $height_cm / 2.54) . ' in)' . "\n";
    $out .= "- **Skill level:** $skill\n";
    $out .= "- **Technique:** $craft_noun\n";
    $out .= "- **Yarn weight:** $opt{yarn_weight}\n";
    $out .= "- **Gauge:** $profile->{gauge} sts / 10 cm in stockinette / sc\n";
    $out .= "- **Suggested $tool:** $tool_size\n\n";

    $out .= "## Materials\n\n";
    $out .= "- **Main yarn:** approx. **${yardage_base} m** (" . int($yardage_base * 1.09) . " yds) total\n";
    $out .= "- **Colours:** see allocation below\n";
    $out .= "- **Stuffing:** polyester fibre fill, approx. " . int(50 * $opt{scale}) . " g\n";
    $out .= "- **Eyes:** 2× safety eyes (12 mm for scale 1.0) or black embroidery thread\n";
    $out .= "- **Notions:** stitch markers, tapestry needle, scissors, row counter\n\n";

    $out .= "### Colour allocation\n\n";
    $out .= "| Motif | Ratio | Main colour | Accent 1 | Accent 2 |\n";
    $out .= "|-------|-------|-------------|----------|----------|\n";
    for my $p (@PARTS) {
        next if $opt{$p} <= 0;
        my $pc = sprintf('%.0f%%', $ratio->{$p} * 100);
        my $pal = $PALETTE{$p};
        $out .= "| " . ucfirst($p) . " | $pc | $pal->{main} | $pal->{light} | $pal->{dark} |\n";
    }

    $out .= "\n### Yardage by colour\n\n";
    $out .= "| Colour | Estimated yardage |\n";
    $out .= "|--------|------------------|\n";
    for my $p (@PARTS) {
        next if $opt{$p} <= 0;
        my $pal = $PALETTE{$p};
        my $y = int($yardage_base * $ratio->{$p} * 0.45 + 0.5);
        $y = max($y, 5);
        $out .= "| $pal->{main} | ~${y} m\n";
        $y = int($yardage_base * $ratio->{$p} * 0.15 + 0.5);
        $y = max($y, 3);
        $out .= "| $pal->{light} | ~${y} m (details)\n";
        $y = int($yardage_base * $ratio->{$p} * 0.10 + 0.5);
        $y = max($y, 2);
        $out .= "| $pal->{dark} | ~${y} m (outlines / details)\n";
    }

    $out .= "\n## Pattern notes\n\n";
    $out .= "- Work a gauge swatch first (10×10 cm in pattern stitch) and adjust $tool if needed.\n";
    $out .= "- The body is worked in one piece from the bottom up.\n";
    $out .= "- Motifs (wings, beak, ears, peel panels) are made separately and sewn on.\n";
    $out .= "- Use stitch markers to track the start of each round.\n";
    $out .= "- Work tightly enough that the stuffing does not show between stitches.\n";
    $out .= "- Changes between motif colours can be carried loosely inside or cut and woven in.\n\n";

    if ($opt{craft} eq 'crochet') {
        $out .= crochet_section($profile, $ratio, $dominant);
    } else {
        $out .= knit_section($profile, $ratio, $dominant);
    }

    $out .= "## Assembly\n\n";
    $out .= assembly_instructions($ratio, $dominant);

    $out .= "## Finishing\n\n";
    $out .= "1. Weave in all ends neatly.\n";
    $out .= "2. Block the mascot gently with a steamer or damp cloth — do not press heavily.\n";
    $out .= "3. Shape the ears/wings and pin them in place until dry.\n";
    $out .= "4. Fluff the surface with a soft brush if desired.\n\n";

    $out .= "## Customisation\n\n";
    $out .= "- **Size:** Change `--scale 0.75` for a smaller mascot or `--scale 1.5` for a larger one.\n";
    $out .= "- **Ratios:** Adjust `--banana`, `--goose`, `--goblin` to emphasise different traits.\n";
    $out .= "- **Yarn:** Substitute any yarn of the same weight class; recalculate yardage with the new gauge.\n";
    $out .= "- **Expression:** Embroider different eyebrows or a mouth to change the personality.\n";
    $out .= "- **Wings:** Make wings longer or rounder by adding/removing rows.\n\n";

    $out .= "---\n";
    $out .= "_Pattern generated by **agentpipe_mascot.pl** on " . localtime() . "._\n";

    return $out;
}

sub generate_text {
    my ($profile, $ratio, $dominant) = @_;
    my $md = generate_markdown($profile, $ratio, $dominant);
    # Strip markdown formatting for plain text
    $md =~ s/^#{1,6}\s*//gm;
    $md =~ s/\*\*(.*?)\*\*/$1/g;
    $md =~ s/\*(.*?)\*/$1/g;
    $md =~ s/^[|-]+\s*$//gm;
    $md =~ s/^\|//gm;
    $md =~ s/\|$//gm;
    $md =~ s/\|/, /g;
    $md =~ s/^_([^_]+)_$/$1/gm;
    $md =~ s/\[([^\]]+)\]\([^)]+\)/$1/g;
    $md =~ s/`//g;
    return $md;
}

# ---------------------------------------------------------------------------
# Crochet pattern
# ---------------------------------------------------------------------------

sub crochet_section {
    my ($profile, $ratio, $dominant) = @_;

    my $s;
    $s .= "## Crochet instructions\n\n";

    # ---- Body ----
    $s .= "### Body (worked in continuous spiral)\n\n";
    $s .= "Use the main colour for the body base, then introduce motif colours in stripes or patches.\n\n";
    $s .= "| Round | Instruction | Stitch count |\n";
    $s .= "|-------|-------------|--------------|\n";

    my $sts = 6;
    my $rnd = 1;
    my $inc_idx = 0;

    # Round 1: magic ring
    $s .= "| $rnd | Magic ring, 6 sc in ring | 6 |\n"; $rnd++;

    # Increase rounds
    for my $inc (@inc_rounds) {
        my ($target) = @$inc;
        if ($target > $sts) {
            my $inc_count = $target - $sts;
            my $desc;
            if ($inc_count == 6) {
                my $interval = int($sts / 6);
                my $interval_str = $interval <= 1 ? "every st" : ordinal($interval) . " st";
                $desc = $opt{craft} eq 'crochet'
                    ? "Inc 6 (e.g. *sc $interval, inc* around)"
                    : "Inc 6 (e.g. kfb every $interval_str)";
            } else {
                $desc = "Inc $inc_count to $target sts";
            }
            my $colour_hint = colour_hint($rnd, $body_rounds, $ratio);
            $s .= "| $rnd | $desc $colour_hint | $target |\n";
            $sts = $target;
        } else {
            my $colour_hint = colour_hint($rnd, $body_rounds, $ratio);
            $s .= "| $rnd | " . ($opt{craft} eq 'crochet' ? "Sc" : "Knit") . " around $colour_hint | $sts |\n";
        }
        $rnd++;
    }

    # Even rounds
    my $even_end = $rnd + $even_over - 1;
    for (my $i = 0; $i < $even_over; $i++) {
        my $colour_hint = colour_hint($rnd, $body_rounds, $ratio);
        $s .= "| $rnd | Sc around $colour_hint | $sts |\n";
        $rnd++;
    }

    # Decrease rounds
    my $dec_target = max(6, $sts - 6);
    while ($sts > 6) {
        my $dec_actual = min(6, $sts - 6);
        my $interval = $dec_actual > 0 ? int($sts / $dec_actual) : $sts;
        my $interval_str = $interval <= 1 ? "every st" : ordinal($interval) . " st";
        my $desc = $opt{craft} eq 'crochet'
            ? "Dec $dec_actual (e.g. *sc $interval, dec* around)"
            : "Dec $dec_actual (e.g. k2tog every $interval_str)";
        $sts = max(6, $sts - $dec_actual);
        my $colour_hint = colour_hint($rnd, $body_rounds, $ratio);
        $s .= "| $rnd | $desc $colour_hint | $sts |\n";
        $rnd++;
    }
    $s .= "| $rnd | " . ($opt{craft} eq 'crochet' ? "Fasten off, leaving a long tail for sewing" : "Cut yarn, thread through remaining sts, pull tight") . " | $sts |\n\n";
    $s .= "☐ Body complete\n\n";

    # ---- Motifs ----
    $s .= "### Motifs\n\n";

    # Banana peel panels
    if ($opt{banana} > 0) {
        $s .= "#### Banana peel panels (make 3–5)\n\n";
        my $panel_len = int($even_over * 1.2 + 0.5);
        $s .= "With yellow (main), ch $panel_len.\n\n";
        $s .= "| Row | Instruction |\n";
        $s .= "|-----|-------------|\n";
        $s .= "| 1 | Sc in 2nd ch from hook and across |\n";
        $s .= "| 2 | Ch 1, turn, sc in each st |\n";
        $s .= "| 3 | Ch 1, turn, sc2tog, sc to last 2 sts, sc2tog |\n";
        $s .= "| 4 | Ch 1, turn, sc in each st |\n";
        $s .= "| 5 | Ch 1, turn, sc2tog, sc to last 2 sts, sc2tog |\n";
        my $rem = $panel_len - 4;
        $s .= "Repeat rows 4–5 until $rem sts remain.\n";
        $s .= "Fasten off, leaving a tail for sewing.\n\n";
        $s .= "☐ Banana peel panels complete\n\n";
    }

    # Wings
    if ($opt{goose} > 0) {
        $s .= "#### Wings (make 2)\n\n";
        $s .= "With cream/white (main), ch " . ($beak_sts + 2) . ".\n\n";
        $s .= "| Row | Instruction |\n";
        $s .= "|-----|-------------|\n";
        for my $rw (1 .. $wing_rows) {
            my $w = $wing_rows - $rw + 1;
            my $ch = $beak_sts + $rw - 1;
            if ($rw == 1) {
                $s .= "| $rw | Sc in 2nd ch from hook, sc across |\n";
            } else {
                my $dec = $rw % 2 == 0 ? "Sc2tog at start and end" : "Sc across";
                $s .= "| $rw | Ch 1, turn, $dec |\n";
            }
        }
        $s .= "Edge the wing with slip stitches around the perimeter in orange (accent).\n";
        $s .= "Fasten off, leaving a tail.\n\n";
        $s .= "☐ Wings complete\n\n";
    }

    # Beak
    if ($opt{goose} > 0) {
        $s .= "#### Beak\n\n";
        $s .= "With orange (accent), ch 4.\n\n";
        $s .= "| Row | Instruction |\n";
        $s .= "|-----|-------------|\n";
        $s .= "| 1 | Sc in 2nd ch from hook, sc 2 |\n";
        $s .= "| 2 | Ch 1, turn, sc2tog, sc 1 |\n";
        $s .= "| 3 | Ch 1, turn, sc2tog |\n";
        $s .= "Fasten off, leaving a tail. Fold in half and sew along the fold for a 3D beak.\n\n";
        $s .= "☐ Beak complete\n\n";
    }

    # Ears / hornlets
    if ($opt{goblin} > 0) {
        $s .= "#### Ears / hornlets (make 2)\n\n";
        $s .= "With green (main), ch 3.\n\n";
        $s .= "| Row | Instruction |\n";
        $s .= "|-----|-------------|\n";
        for my $rw (1 .. $ear_rows) {
            if ($rw == 1) {
                $s .= "| $rw | Sc in 2nd ch from hook, sc 1 |\n";
            } else {
                my $dec = $rw < $ear_rows ? "Sc across" : "Sc2tog once";
                $s .= "| $rw | Ch 1, turn, $dec |\n";
            }
        }
        $s .= "Fasten off, leaving a tail.\n\n";
        $s .= "☐ Ears/hornlets complete\n\n";
    }

    # Tail
    $s .= "#### Tail\n\n";
    $s .= "With the least dominant motif colour:\n\n";
    $s .= "| Step | Instruction |\n";
    $s .= "|------|-------------|\n";
    $s .= "| 1 | Magic ring, 6 sc |\n";
    $s .= "| 2 | Sc around for " . int(4 * $opt{scale} + 0.5) . " rounds |\n";
    $s .= "| 3 | Flatten and fasten off, leaving a tail |\n\n";
    $s .= "☐ Tail complete\n\n";

    return $s;
}

# ---------------------------------------------------------------------------
# Knit pattern
# ---------------------------------------------------------------------------

sub knit_section {
    my ($profile, $ratio, $dominant) = @_;

    my $s;
    $s .= "## Knit instructions\n\n";

    # ---- Body ----
    $s .= "### Body (knitted in the round)\n\n";
    $s .= "Use the main colour for the body base, then introduce motif colours as stranded colourwork or duplicate stitch.\n\n";
    $s .= "| Round | Instruction | Stitch count |\n";
    $s .= "|-------|-------------|--------------|\n";

    my $sts = 6;
    my $rnd = 1;

    $s .= "| $rnd | Cast on 6 sts, join in the round, place marker | 6 |\n"; $rnd++;

    for my $inc (@inc_rounds) {
        my ($target) = @$inc;
        if ($target > $sts) {
            my $inc_count = $target - $sts;
            my $interval = int($sts / $inc_count);
            my $interval_str = $interval <= 1 ? "every st" : ordinal($interval) . " st";
            my $desc = "Inc $inc_count to $target sts (e.g. kfb every $interval_str)";
            my $colour_hint = colour_hint($rnd, $body_rounds, $ratio);
            $s .= "| $rnd | $desc $colour_hint | $target |\n";
            $sts = $target;
        } else {
            my $colour_hint = colour_hint($rnd, $body_rounds, $ratio);
            $s .= "| $rnd | Knit around $colour_hint | $sts |\n";
        }
        $rnd++;
    }

    my $even_end = $rnd + $even_over - 1;
    for (my $i = 0; $i < $even_over; $i++) {
        my $colour_hint = colour_hint($rnd, $body_rounds, $ratio);
        $s .= "| $rnd | Knit around $colour_hint | $sts |\n";
        $rnd++;
    }

    while ($sts > 6) {
        my $dec_actual = min(6, $sts - 6);
        my $interval = int($sts / $dec_actual);
        my $interval_str = $interval <= 1 ? "every st" : ordinal($interval) . " st";
        my $desc = "Dec $dec_actual (e.g. k2tog every $interval_str)";
        $sts = max(6, $sts - $dec_actual);
        my $colour_hint = colour_hint($rnd, $body_rounds, $ratio);
        $s .= "| $rnd | $desc $colour_hint | $sts |\n";
        $rnd++;
    }
    $s .= "| $rnd | Cut yarn, thread through remaining sts, pull tight | $sts |\n\n";
    $s .= "☐ Body complete\n\n";

    # ---- Motifs ----
    $s .= "### Motifs\n\n";

    if ($opt{banana} > 0) {
        $s .= "#### Banana peel panels (make 3–5)\n\n";
        $s .= "With yellow, cast on 4 sts.\n\n";
        $s .= "| Row | Instruction |\n";
        $s .= "|-----|-------------|\n";
        $s .= "| 1 | Knit across |\n";
        $s .= "| 2 | Purl across |\n";
        $s .= "| 3 | K1, ssk, knit to last 3 sts, k2tog, k1 |\n";
        $s .= "| 4 | Purl across |\n";
        $s .= "Repeat rows 3–4 until 1 st remains.\n";
        $s .= "Cut yarn and pull through.\n\n";
        $s .= "☐ Banana peel panels complete\n\n";
    }

    if ($opt{goose} > 0) {
        $s .= "#### Wings (make 2)\n\n";
        $s .= "With cream/white, cast on " . ($beak_sts + 1) . " sts.\n\n";
        $s .= "| Row | Instruction |\n";
        $s .= "|-----|-------------|\n";
        for my $rw (1 .. $wing_rows) {
            if ($rw == 1) {
                $s .= "| $rw | Knit across |\n";
            } else {
                $s .= "| $rw | K1, ssk, knit to last 3 sts, k2tog, k1 |\n";
            }
        }
        $s .= "Bind off all sts. Edge with crochet slip stitches in orange, or with duplicate stitch.\n\n";
        $s .= "☐ Wings complete\n\n";
    }

    if ($opt{goose} > 0) {
        $s .= "#### Beak\n\n";
        $s .= "With orange, cast on 3 sts. Work 4 rows in stockinette. Bind off.\n";
        $s .= "Fold in half and sew along the fold.\n\n";
        $s .= "☐ Beak complete\n\n";
    }

    if ($opt{goblin} > 0) {
        $s .= "#### Ears / hornlets (make 2)\n\n";
        $s .= "With green, cast on 3 sts.\n\n";
        $s .= "| Row | Instruction |\n";
        $s .= "|-----|-------------|\n";
        $s .= "| 1 | Knit across |\n";
        $s .= "| 2 | K1, k2tog |\n";
        $s .= "| 3 | Knit across |\n";
        $s .= "| 4 | K2tog |\n";
        $s .= "Cut yarn and pull through.\n\n";
        $s .= "☐ Ears/hornlets complete\n\n";
    }

    $s .= "#### Tail\n\n";
    $s .= "Cast on 4 sts. Work " . int(5 * $opt{scale} + 0.5) . " rows in I-cord or stockinette.\n";
    $s .= "Bind off, flatten, and sew.\n\n";
    $s .= "☐ Tail complete\n\n";

    return $s;
}

# ---------------------------------------------------------------------------
# Assembly instructions
# ---------------------------------------------------------------------------

sub assembly_instructions {
    my ($ratio, $dominant) = @_;

    my $s;
    $s .= "### Body preparation\n\n";
    $s .= "1. Stuff the body firmly, shaping it as you go.\n";
    $s .= "2. The magic ring tail should be at the bottom (or hidden inside).\n\n";

    $s .= "### Attaching motifs\n\n";
    $s .= "Use the long tails left on each piece and a tapestry needle.\n\n";

    $s .= "| Order | Part | Placement |\n";
    $s .= "|-------|------|-----------|\n";

    my $order = 1;
    if ($opt{banana} > 0) {
        $s .= "| $order | Banana peel panels | Sew vertically down the back and sides, spaced evenly |\n";
        $order++;
    }
    if ($opt{goose} > 0) {
        $s .= "| $order | Wings | Attach at the widest point of the body, one on each side, angled slightly upward |\n";
        $order++;
        $s .= "| $order | Beak | Sew below the eyes, centred, with the folded edge pointing forward |\n";
        $order++;
    }
    if ($opt{goblin} > 0) {
        $s .= "| $order | Ears / hornlets | Sew near the top of the head, angled slightly outward |\n";
        $order++;
    }
    $s .= "| $order | Tail | Sew at the bottom centre of the back |\n";
    $order++;

    $s .= "\n### Face\n\n";
    $s .= "1. Place safety eyes (or embroider eyes) at around round " . int($increase_over + $even_over * 0.3 + 0.5) . " of the body, approx. " . int($body_max_sts / 4) . " sts apart.\n";
    $s .= "2. Embroider eyebrows that reflect the dominant motif: " . face_style($dominant) . "\n";
    $s .= "3. Embroider a small smile or neutral mouth using black/dark thread.\n";
    $s .= "4. Add any extra details (nostrils, freckles, feather marks) as desired.\n\n";

    return $s;
}

sub face_style {
    my ($dominant) = @_;
    if ($dominant eq 'banana') {
        return 'soft curved brows, small smile';
    } elsif ($dominant eq 'goose') {
        return 'sharp angled brows, worried or blank expression';
    } else {
        return 'mischievous raised brows, wry or cheeky grin';
    }
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

sub increase_schedule {
    my ($max_sts, $num_rounds) = @_;
    $num_rounds = max(1, $num_rounds);
    my $sts = 6;
    my @schedule;
    for my $r (1 .. $num_rounds) {
        my $target = int(6 + ($max_sts - 6) * ($r / $num_rounds) + 0.5);
        $target = even($target);
        $target = max($sts + 2, $target);
        $target = min($max_sts, $target);
        push @schedule, [$target];
        $sts = $target;
    }
    return @schedule;
}

sub colour_hint {
    my ($rnd, $total, $ratio) = @_;
    return '' if $total <= 0;
    my $pos = $rnd / $total;
    my $cum = 0;
    for my $p (@PARTS) {
        $cum += $ratio->{$p};
        return "[" . ucfirst($p) . " colour]" if $pos <= $cum && $opt{$p} > 0;
    }
    return '';
}

sub determine_skill {
    return ucfirst($opt{skill}) if $opt{skill};
    my $score = 0;
    $score++ if $opt{banana} > 0;
    $score++ if $opt{goose} > 0;
    $score++ if $opt{goblin} > 0;
    $score++ if $opt{scale} != 1;
    return $score <= 1 ? 'Beginner' : $score <= 2 ? 'Intermediate' : 'Advanced';
}

sub ratio_desc {
    my ($ratio) = @_;
    my @parts;
    for my $p (@PARTS) {
        next if $opt{$p} <= 0;
        my $pc = sprintf('%.0f%%', $ratio->{$p} * 100);
        push @parts, "$pc $p";
    }
    return join ', ', @parts;
}

sub even {
    my $n = shift;
    return $n % 2 ? $n + 1 : $n;
}

sub ordinal {
    my $n = shift;
    return "$n" . ($n == 1 ? 'st' : $n == 2 ? 'nd' : $n == 3 ? 'rd' : 'th');
}

sub max {
    my ($a, $b) = @_;
    return $a > $b ? $a : $b;
}

sub min {
    my ($a, $b) = @_;
    return $a < $b ? $a : $b;
}

# ---------------------------------------------------------------------------
# HTML helpers
# ---------------------------------------------------------------------------

sub html_header {
    my ($title) = @_;
    return <<"HTML";
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>$title — Crochet/Knit Pattern</title>
<style>
  body { font-family: Georgia, serif; max-width: 800px; margin: 2em auto; padding: 0 1em; line-height: 1.6; color: #222; }
  h1, h2, h3, h4 { color: #2c3e50; }
  h1 { border-bottom: 2px solid #3498db; padding-bottom: 0.3em; }
  h2 { border-bottom: 1px solid #bdc3c7; padding-bottom: 0.2em; margin-top: 1.5em; }
  table { border-collapse: collapse; width: 100%; margin: 1em 0; }
  th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
  th { background: #3498db; color: white; }
  tr:nth-child(even) { background: #f9f9f9; }
  hr { border: none; border-top: 2px solid #3498db; margin: 2em 0; }
  .footer { color: #888; font-size: 0.85em; text-align: center; margin-top: 2em; }
  ul, ol { padding-left: 1.5em; }
  code { background: #f4f4f4; padding: 0.2em 0.4em; border-radius: 3px; font-size: 0.9em; }
  .checkbox { color: #27ae60; }
  .mascot-svg { display: block; margin: 1em auto; text-align: center; }
</style>
</head>
<body>
HTML
}

sub html_footer {
    return '<div class="footer"><p>Pattern generated by <strong>agentpipe_mascot.pl</strong></p></div>' . "\n</body>\n</html>\n";
}

sub md_to_html {
    my ($md, $title) = @_;
    my $html = '';
    my @lines = split /\n/, $md;
    my $in_table = 0;
    my $in_list = 0;
    my $list_type = '';

    for my $i (0 .. $#lines) {
        my $line = $lines[$i];
        my $next = $i < $#lines ? $lines[$i + 1] : '';

        # Headers
        if ($line =~ /^######\s+(.+)/) { $html .= "<h6>$1</h6>\n"; next }
        if ($line =~ /^#####\s+(.+)/) { $html .= "<h5>$1</h5>\n"; next }
        if ($line =~ /^####\s+(.+)/) { $html .= "<h4>$1</h4>\n"; next }
        if ($line =~ /^###\s+(.+)/) { $html .= "<h3>$1</h3>\n"; next }
        if ($line =~ /^##\s+(.+)/) { $html .= "<h2>$1</h2>\n"; next }
        if ($line =~ /^#\s+(.+)/) { $html .= "<h1>$1</h1>\n"; next }

        # Horizontal rule
        if ($line =~ /^---/) { $html .= "<hr>\n"; next }

        # Table
        if ($line =~ /^\|.+\|$/) {
            if ($next =~ /^\|[-| ]+\|$/) {
                $html .= "<table>\n<thead>\n<tr>\n";
                my @cells = split /\|/, $line;
                shift @cells; pop @cells;
                for my $c (@cells) {
                    $c =~ s/^\s+|\s+$//g;
                    $html .= "  <th>$c</th>\n";
                }
                $html .= "</tr>\n</thead>\n<tbody>\n";
                $in_table = 1;
                $i++; # skip separator
                next;
            }
            if ($in_table) {
                if ($line =~ /^\|[-| ]+\|$/) { next }    # skip separator
                $html .= "<tr>\n";
                my @cells = split /\|/, $line;
                shift @cells; pop @cells;
                for my $c (@cells) {
                    $c =~ s/^\s+|\s+$//g;
                    $c =~ s/\*\*(.+?)\*\*/<strong>$1<\/strong>/g;
                    $c =~ s/\*(.+?)\*/<em>$1<\/em>/g;
                    $c =~ s/`(.+?)`/<code>$1<\/code>/g;
                    $html .= "  <td>$c</td>\n";
                }
                $html .= "</tr>\n";
                next;
            }
        } else {
            if ($in_table) {
                $html .= "</tbody>\n</table>\n";
                $in_table = 0;
            }
        }

        # Unordered list
        if ($line =~ /^-\s+(.+)/) {
            if (!$in_list || $list_type ne 'ul') {
                $html .= "<ul>\n" if $in_list;
                $html .= "<ul>\n";
                $list_type = 'ul';
                $in_list = 1;
            }
            my $item = $1;
            $item =~ s/\*\*(.+?)\*\*/<strong>$1<\/strong>/g;
            $item =~ s/\*(.+?)\*/<em>$1<\/em>/g;
            $item =~ s/`(.+?)`/<code>$1<\/code>/g;
            $item =~ s/^☐/<span class="checkbox">☐<\/span>/;
            $html .= "  <li>$item</li>\n";
            next;
        }

        # Ordered list
        if ($line =~ /^\d+[.)]\s+(.*)/) {
            if (!$in_list || $list_type ne 'ol') {
                $html .= "<ol>\n" if $in_list;
                $html .= "<ol>\n";
                $list_type = 'ol';
                $in_list = 1;
            }
            my $item = $1;
            $item =~ s/\*\*(.+?)\*\*/<strong>$1<\/strong>/g;
            $item =~ s/\*(.+?)\*/<em>$1<\/em>/g;
            $item =~ s/`(.+?)`/<code>$1<\/code>/g;
            $html .= "  <li>$item</li>\n";
            next;
        }

        # Close list if open
        if ($in_list) {
            $html .= ($list_type eq 'ul' ? "</ul>\n" : "</ol>\n");
            $in_list = 0;
        }

        # Italic/footer lines
        if ($line =~ /^_(.+)_$/) {
            $html .= "<p class=\"footer\"><em>$1</em></p>\n";
            next;
        }

        # Empty line
        if ($line =~ /^\s*$/) {
            next;
        }

        # Regular paragraph
        my $p = $line;
        $p =~ s/\*\*(.+?)\*\*/<strong>$1<\/strong>/g;
        $p =~ s/\*(.+?)\*/<em>$1<\/em>/g;
        $p =~ s/`(.+?)`/<code>$1<\/code>/g;
        $html .= "<p>$p</p>\n";
    }

    # Close any open tags
    $html .= "</tbody>\n</table>\n" if $in_table;
    $html .= ($list_type eq 'ul' ? "</ul>\n" : "</ol>\n") if $in_list;

    return $html;
}

# ---------------------------------------------------------------------------
# Translation / localisation
# ---------------------------------------------------------------------------

sub translate_output {
    my ($text) = @_;

    if ($opt{terminology} eq 'uk' && $opt{craft} eq 'crochet') {
        my @terms = sort { length($b) <=> length($a) } keys %US2UK;
        my $alt = join '|', map { quotemeta } @terms;
        $text =~ s/\b($alt)\b/$US2UK{lc $1}/gie;
    }

    if ($opt{emoji}) {
        $text = emojify_text($text);
    }

    return $text;
}

sub emojify_text {
    my ($text) = @_;

    $text =~ s/\*\*(.+?)\*\*/emojify_inline($1)/ge;
    $text =~ s/\*(.+?)\*/emojify_inline($1)/ge;
    $text =~ s/`(.+?)`/emojify_inline($1)/ge;

    my @lines = split /\n/, $text;
    for my $line (@lines) {
        next if $line =~ /^\s*$/;
        next if $line =~ /^---/;
        next if $line =~ /^\|[-| ]+\|$/;
        next if $line =~ /^#/;
        $line =~ s/(\d+)\.(\s+)/$1$2/g;
        $line = emojify_line($line);
    }
    $text = join "\n", @lines;

    return $text;
}

sub emojify_inline {
    my ($text) = @_;
    $text = emojify_line($text);
    return $text;
}

sub emojify_line {
    my ($line) = @_;

    $line =~ s/(\d+\.?\d*)\s*mm\b/$1\x{1F4D0}/g;
    $line =~ s/(\d+\.?\d*)\s*cm\b/$1\x{1F4D0}/g;
    $line =~ s/(\d+\.?\d*)\s*m\b/$1\x{1F4D0}/g;
    $line =~ s/(\d+)\s*\%/$1%\x{FE0F}/g;
    $line =~ s/(\d+)\s*g\b/$1 g/g;

    my @words = split /(\s+)/, $line;
    for my $w (@words) {
        next if $w =~ /^\s+$/;
        next if $w =~ /^[|:\-*#`_]+$/;

        my $clean = lc $w;
        $clean =~ s/[^a-z0-9]//g;

        if (exists $EMOJI{$clean}) {
            $w = $EMOJI{$clean};
        } elsif ($clean =~ /^(\d+)$/ && length($clean) <= 2) {
            $w = number_to_emoji($1);
        } elsif ($clean =~ /^(a|an|the|in|on|at|to|for|of|and|or|is|are|be|by|as|with|from|but|not|so|if|do|it|all|will|can|each|that|this|they|them|these|those)$/) {
            $w = '';
        }
    }

    $line = join '', @words;
    $line =~ s/\x{1F4D0}\s*\x{1F4D0}/\x{1F4D0}/g;

    $line =~ s/^\s+//;
    $line =~ s/\s+$//;

    return $line;
}

sub number_to_emoji {
    my ($num) = @_;
    my @digits = split '', $num;
    my $out = '';
    for my $d (@digits) {
        $out .= chr(0x30 + $d) . "\x{20E3}";
    }
    return $out;
}

# ---------------------------------------------------------------------------
# Usage
# ---------------------------------------------------------------------------

sub usage {
    my ($exit) = @_;
    print <<"USAGE";
Usage: perl agentpipe_mascot.pl [options]

Generate a detailed crochet or knitting pattern for an AgentPipe mascot
with adjustable banana/goose/goblin motif ratios.

Options:
  --banana N        Banana motif ratio (default: 1)
  --goose N         Goose motif ratio (default: 1)
  --goblin N        Goblin motif ratio (default: 1)
  --yarn-weight W   Yarn weight: lace, fingering, sport, dk, worsted, bulky (default: dk)
  --craft C         Craft: crochet or knit (default: crochet)
  --scale N         Size multiplier (default: 1.0)
  --name TEXT       Pattern title (default: AgentPipe Mascot)
  --format F        Output format: markdown, text, html (default: markdown)
  --output FILE     Write to file instead of stdout
  --skill LEVEL     Override skill level: beginner, intermediate, advanced
  --terminology T   Crochet term dialect: us (single crochet, dc) or uk (dc, tr) (default: us)
  --emoji           Express the entire output document in emoji (default: off)
  --help            Show this help

Examples:
  perl agentpipe_mascot.pl --banana 2 --goose 1 --goblin 1
  perl agentpipe_mascot.pl --craft knit --yarn-weight worsted --scale 1.25
  perl agentpipe_mascot.pl --format html --output mascot.html
  perl agentpipe_mascot.pl --banana 0 --goose 3 --goblin 1 --craft knit
  perl agentpipe_mascot.pl --terminology uk
  perl agentpipe_mascot.pl --emoji

The output is a complete pattern document with:
  - Row-by-row stitch instructions with a progress tracker
  - Materials list with yarn quantities per colour
  - Separate motif patterns (wings, beak, ears, peel panels, tail)
  - Assembly guide with face embroidery suggestions
  - Gauge, blocking, and customisation notes
USAGE
    exit $exit;
}
