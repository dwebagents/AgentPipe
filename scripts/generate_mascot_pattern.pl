#!/usr/bin/env perl
use strict;
use warnings;
use utf8;
use Getopt::Long qw(GetOptions);
use POSIX qw(ceil);

binmode STDOUT, ':encoding(UTF-8)';

my %opts = (
    banana => 1,
    goose  => 1,
    goblin => 1,
    craft  => 'crochet',
    yarn   => 'worsted',
    height => 18,
    name   => 'AgentPipe mascot',
    output => '-',
    terminology => 'us',
    emoji  => 0,
);

my $help = 0;

GetOptions(
    'banana=f' => \$opts{banana},
    'goose=f'  => \$opts{goose},
    'goblin=f' => \$opts{goblin},
    'craft=s'  => \$opts{craft},
    'yarn=s'   => \$opts{yarn},
    'height=f' => \$opts{height},
    'name=s'   => \$opts{name},
    'output=s' => \$opts{output},
    'terminology=s' => \$opts{terminology},
    'emoji!'   => \$opts{emoji},
    'help'     => \$help,
) or usage(2);

usage(0) if $help;

$opts{craft} = lc $opts{craft};
$opts{yarn} = lc $opts{yarn};
$opts{terminology} = lc $opts{terminology};

my %yarn_profiles = (
    lace    => { hook => '2.25 mm hook / US 1 needles', gauge => 3.2, yardage => 1.55, stuffing => 0.70 },
    sport   => { hook => '3.25 mm hook / US 3 needles', gauge => 2.5, yardage => 1.25, stuffing => 0.85 },
    dk      => { hook => '4.00 mm hook / US 6 needles', gauge => 2.0, yardage => 1.00, stuffing => 1.00 },
    worsted => { hook => '5.00 mm hook / US 8 needles', gauge => 1.6, yardage => 0.85, stuffing => 1.20 },
    bulky   => { hook => '6.50 mm hook / US 10.5 needles', gauge => 1.2, yardage => 0.72, stuffing => 1.55 },
);

die "Unknown craft '$opts{craft}'. Use crochet or knit.\n" unless $opts{craft} eq 'crochet' || $opts{craft} eq 'knit';
die "Unknown yarn '$opts{yarn}'. Use one of: " . join(', ', sort keys %yarn_profiles) . ".\n" unless exists $yarn_profiles{$opts{yarn}};
die "Unknown terminology '$opts{terminology}'. Use us or uk.\n" unless $opts{terminology} eq 'us' || $opts{terminology} eq 'uk';
die "Height must be a positive number.\n" unless $opts{height} > 0;

for my $part (qw(banana goose goblin)) {
    die "$part ratio must be zero or positive.\n" if $opts{$part} < 0;
}

my $ratio_total = $opts{banana} + $opts{goose} + $opts{goblin};
die "At least one mascot ratio must be greater than zero.\n" unless $ratio_total > 0;

my %ratio = map { $_ => $opts{$_} / $ratio_total } qw(banana goose goblin);
my $profile = $yarn_profiles{$opts{yarn}};
my $scale = $opts{height} / 18;

my %palette = (
    banana => ['banana yellow', 'warm cream', 'soft brown'],
    goose  => ['cloud white', 'orange accent', 'charcoal'],
    goblin => ['moss green', 'leaf green', 'tiny copper accent'],
);

my %crochet_terms = (
    us => {
        label  => 'US',
        stitch => 'single crochet (sc)',
        abbr   => 'sc',
    },
    uk => {
        label  => 'UK',
        stitch => 'double crochet (dc)',
        abbr   => 'dc',
    },
);

my $document = $opts{emoji}
    ? render_emoji_pattern(\%opts, \%ratio, $profile, \%palette, $scale)
    : render_pattern(\%opts, \%ratio, $profile, \%palette, $scale);

if ($opts{output} eq '-') {
    print $document;
} else {
    open my $fh, '>:encoding(UTF-8)', $opts{output} or die "Could not write '$opts{output}': $!\n";
    print {$fh} $document;
    close $fh or die "Could not close '$opts{output}': $!\n";
}

sub usage {
    my ($exit_code) = @_;
    print <<'USAGE';
Usage:
  perl scripts/generate_mascot_pattern.pl [options]

Options:
  --banana N     Relative banana influence. Default: 1
  --goose N      Relative goose influence. Default: 1
  --goblin N     Relative goblin influence. Default: 1
  --craft NAME   crochet or knit. Default: crochet
  --yarn NAME    lace, sport, dk, worsted, or bulky. Default: worsted
  --height CM    Finished mascot height in centimeters. Default: 18
  --name TEXT    Pattern title. Default: AgentPipe mascot
  --output PATH  Write Markdown to a file instead of stdout
  --terminology NAME
                  Crochet terminology: us or uk. Default: us
  --emoji         Generate Markdown with emoji instructions instead of English prose
  --help         Show this help

Example:
  perl scripts/generate_mascot_pattern.pl --banana 3 --goose 1 --goblin 2 --yarn dk --height 22 --terminology uk --emoji --output mascot.md
USAGE
    exit $exit_code;
}

sub render_pattern {
    my ($opts_ref, $ratio_ref, $profile_ref, $palette_ref, $scale_value) = @_;

    my $craft = $opts_ref->{craft};
    my $pattern_name = $opts_ref->{name};
    my $yarn_weight = $opts_ref->{yarn};
    my $finished_height = $opts_ref->{height};
    my $banana_input = $opts_ref->{banana};
    my $goose_input = $opts_ref->{goose};
    my $goblin_input = $opts_ref->{goblin};
    my $terminology = $opts_ref->{terminology};
    my $tool_size = $profile_ref->{hook};
    my $gauge = $profile_ref->{gauge};
    my $neutral_yarn = $palette_ref->{banana}->[1];
    my $stitch_word = $craft eq 'crochet' ? $crochet_terms{$terminology}{stitch} : 'st';

    my $body_rounds = rounds(28, $scale_value);
    my $body_width  = stitches(24, $profile_ref->{gauge}, $scale_value);
    my $curve_rows  = rounds(10 + 12 * $ratio_ref->{banana}, $scale_value);
    my $wing_rows   = rounds(6 + 10 * $ratio_ref->{goose}, $scale_value);
    my $hood_rows   = rounds(5 + 9 * $ratio_ref->{goblin}, $scale_value);

    my $main_yards = yardage(62, $profile_ref, $scale_value, 0.55);
    my $banana_yards = yardage(42, $profile_ref, $scale_value, $ratio_ref->{banana});
    my $goose_yards = yardage(36, $profile_ref, $scale_value, $ratio_ref->{goose});
    my $goblin_yards = yardage(34, $profile_ref, $scale_value, $ratio_ref->{goblin});
    my $stuffing_grams = ceil(18 * $profile_ref->{stuffing} * $scale_value);

    my @sections;
    push @sections, "# $pattern_name pattern\n";
    push @sections, "Generated by `scripts/generate_mascot_pattern.pl`.\n";
    push @sections, "## Parameters\n";
    push @sections, table(
        ['Setting', 'Value'],
        ['Craft', $craft],
        ['Yarn weight', $yarn_weight],
        ['Terminology', $craft eq 'crochet' ? "$crochet_terms{$terminology}{label} crochet" : 'not applicable to knitting'],
        ['Finished height', sprintf('%.1f cm', $finished_height)],
        ['Banana ratio', percent($ratio_ref->{banana})],
        ['Goose ratio', percent($ratio_ref->{goose})],
        ['Goblin ratio', percent($ratio_ref->{goblin})],
    );

    push @sections, "## Materials\n";
    push @sections, "- $tool_size\n";
    push @sections, "- Main yarn: about $main_yards yd in $neutral_yarn or another neutral base\n";
    push @sections, "- Banana feature yarn: about $banana_yards yd in " . join(', ', @{$palette_ref->{banana}}) . "\n";
    push @sections, "- Goose feature yarn: about $goose_yards yd in " . join(', ', @{$palette_ref->{goose}}) . "\n";
    push @sections, "- Goblin feature yarn: about $goblin_yards yd in " . join(', ', @{$palette_ref->{goblin}}) . "\n";
    push @sections, "- Polyester stuffing: about $stuffing_grams g\n";
    push @sections, "- Yarn needle, stitch markers, scissors, and optional safety eyes\n";
    push @sections, "\n";

    push @sections, "## Gauge\n";
    push @sections, "- Work tightly enough that stuffing does not show.\n";
    push @sections, "- Approximate gauge: $gauge stitches per centimeter after stuffing.\n";
    if ($craft eq 'crochet') {
        push @sections, "- Crochet terminology: $crochet_terms{$terminology}{label}; US single crochet is written as UK double crochet when `--terminology uk` is selected.\n";
    }
    push @sections, "- Scale by changing `--height` or yarn weight; all counts are rounded to whole stitches.\n\n";

    if ($craft eq 'crochet') {
        push @sections, crochet_body($body_width, $body_rounds, $curve_rows, $wing_rows, $hood_rows, $stitch_word);
    } else {
        push @sections, knit_body($body_width, $body_rounds, $curve_rows, $wing_rows, $hood_rows, $stitch_word);
    }

    push @sections, "## Assembly\n";
    push @sections, "- Stuff the body firmly, keeping the base flat enough to sit upright.\n";
    push @sections, "- Sew the curved yellow panel along one side so the mascot leans slightly forward.\n";
    push @sections, "- Attach the white side panels symmetrically; angle the orange accent toward the front.\n";
    push @sections, "- Attach the green hood and tiny copper accent last so it sits visibly above the face.\n";
    push @sections, "- Weave in ends, then roll the finished piece between your palms to even out the stuffing.\n\n";

    push @sections, "## Regenerate\n";
    push @sections, "```sh\n";
    push @sections, "perl scripts/generate_mascot_pattern.pl --banana $banana_input --goose $goose_input --goblin $goblin_input --craft $craft --yarn $yarn_weight --height $finished_height --terminology $terminology\n";
    push @sections, "```\n";

    return join('', @sections);
}

sub render_emoji_pattern {
    my ($opts_ref, $ratio_ref, $profile_ref, $palette_ref, $scale_value) = @_;

    my $craft = $opts_ref->{craft};
    my $yarn_weight = $opts_ref->{yarn};
    my $finished_height = $opts_ref->{height};
    my $terminology = $opts_ref->{terminology};
    my $banana_input = $opts_ref->{banana};
    my $goose_input = $opts_ref->{goose};
    my $goblin_input = $opts_ref->{goblin};
    my $gauge = $profile_ref->{gauge};
    my $stitch_word = $craft eq 'crochet' ? $crochet_terms{$terminology}{abbr} : 'st';

    my %craft_icon = (
        crochet => '🪝',
        knit    => '🧶',
    );
    my %yarn_icon = (
        lace    => '🕸️',
        sport   => '🧵',
        dk      => '🧶',
        worsted => '🧶🧶',
        bulky   => '🧶🧶🧶',
    );
    my %tool_icon = (
        lace    => '2.25 mm 🪝 / US 1 🪡',
        sport   => '3.25 mm 🪝 / US 3 🪡',
        dk      => '4.00 mm 🪝 / US 6 🪡',
        worsted => '5.00 mm 🪝 / US 8 🪡',
        bulky   => '6.50 mm 🪝 / US 10.5 🪡',
    );

    my $body_rounds = rounds(28, $scale_value);
    my $body_width  = stitches(24, $profile_ref->{gauge}, $scale_value);
    my $curve_rows  = rounds(10 + 12 * $ratio_ref->{banana}, $scale_value);
    my $wing_rows   = rounds(6 + 10 * $ratio_ref->{goose}, $scale_value);
    my $hood_rows   = rounds(5 + 9 * $ratio_ref->{goblin}, $scale_value);

    my $main_yards = yardage(62, $profile_ref, $scale_value, 0.55);
    my $banana_yards = yardage(42, $profile_ref, $scale_value, $ratio_ref->{banana});
    my $goose_yards = yardage(36, $profile_ref, $scale_value, $ratio_ref->{goose});
    my $goblin_yards = yardage(34, $profile_ref, $scale_value, $ratio_ref->{goblin});
    my $stuffing_grams = ceil(18 * $profile_ref->{stuffing} * $scale_value);

    my @sections;
    push @sections, "# 🧵🍌🪿🟢\n";
    push @sections, "🤖 `scripts/generate_mascot_pattern.pl`\n";
    push @sections, "## ⚙️\n";
    push @sections, table(
        ['⚙️', '🔢'],
        ['🪡', $craft_icon{$craft}],
        ['🧶', $yarn_icon{$yarn_weight}],
        ['🌍', $terminology eq 'us' ? '🇺🇸' : '🇬🇧'],
        ['📏', sprintf('%.1f cm', $finished_height)],
        ['🍌', percent($ratio_ref->{banana})],
        ['🪿', percent($ratio_ref->{goose})],
        ['🟢', percent($ratio_ref->{goblin})],
    );

    push @sections, "## 🧰\n";
    push @sections, "- $tool_icon{$yarn_weight}\n";
    push @sections, "- ⚪ $main_yards yd\n";
    push @sections, "- 🍌 $banana_yards yd 🟨⬜🟫\n";
    push @sections, "- 🪿 $goose_yards yd ⬜🟧⬛\n";
    push @sections, "- 🟢 $goblin_yards yd 🟩🟢🟫\n";
    push @sections, "- ☁️ $stuffing_grams g\n";
    push @sections, "- 🪡 📍 ✂️ 👀\n\n";

    push @sections, "## 📐\n";
    push @sections, "- 🧵🔒 ☁️🙈\n";
    push @sections, "- $gauge st/cm\n";
    if ($craft eq 'crochet') {
        push @sections, "- 🌍 " . ($terminology eq 'us' ? '🇺🇸 sc' : '🇬🇧 dc') . "\n";
    }
    push @sections, "- 📏➡️ --height 🧶➡️ --yarn\n\n";

    if ($craft eq 'crochet') {
        push @sections, emoji_crochet_body($body_width, $body_rounds, $curve_rows, $wing_rows, $hood_rows, $stitch_word);
    } else {
        push @sections, emoji_knit_body($body_width, $body_rounds, $curve_rows, $wing_rows, $hood_rows, $stitch_word);
    }

    push @sections, "## 🧷\n";
    push @sections, "- 🧍 ☁️☁️ 📐⬇️\n";
    push @sections, "- 🍌 ↪️ 🧍\n";
    push @sections, "- 🪿 ↔️ 🟧➡️\n";
    push @sections, "- 🟢 🔝 🟫✨\n";
    push @sections, "- 🧶🔚 ✋↔️\n\n";

    push @sections, "## 🔁\n";
    push @sections, "```sh\n";
    push @sections, "perl scripts/generate_mascot_pattern.pl --banana $banana_input --goose $goose_input --goblin $goblin_input --craft $craft --yarn $yarn_weight --height $finished_height --terminology $terminology --emoji\n";
    push @sections, "```\n";

    return join('', @sections);
}

sub crochet_body {
    my ($body_width, $body_rounds, $curve_rows, $wing_rows, $hood_rows, $stitch_word) = @_;
    return <<"CROCHET";
## Crochet instructions

### Body
1. Magic ring, work 6 $stitch_word.
2. Increase evenly until you have $body_width $stitch_word.
3. Work even for $body_rounds rounds.
4. Decrease every 4th stitch for 2 rounds, stuff, then decrease to close.

### Curved yellow panel
1. Chain @{[ceil($body_width * 0.58)]}; work $curve_rows rows in $stitch_word.
2. Increase on the right edge every other row and decrease on the left edge every third row to create a gentle curve.
3. Finish with one row of slip stitch in soft brown.

### White side panels
1. Make 2 panels, each @{[ceil($body_width * 0.33)]} stitches wide and $wing_rows rows tall.
2. Taper the final 3 rows by decreasing at both edges.
3. Add a small orange triangle at the lower front edge.

### Green hood
1. Chain @{[ceil($body_width * 0.40)]}; work $hood_rows rows.
2. Decrease at both edges in the last 2 rows.
3. Add a tiny copper accent at the peak.

CROCHET
}

sub knit_body {
    my ($body_width, $body_rounds, $curve_rows, $wing_rows, $hood_rows, $stitch_word) = @_;
    return <<"KNIT";
## Knitting instructions

### Body
1. Cast on $body_width stitches in the round.
2. Knit $body_rounds rounds.
3. Decrease every 4th stitch for 2 rounds, stuff, then gather closed.

### Curved yellow panel
1. Cast on @{[ceil($body_width * 0.58)]} stitches and knit $curve_rows rows in stockinette.
2. Increase on the right edge every other row and decrease on the left edge every third row.
3. Bind off with a soft brown edge.

### White side panels
1. Make 2 panels, each @{[ceil($body_width * 0.33)]} stitches wide and $wing_rows rows tall.
2. Taper the final 3 rows by decreasing at both edges.
3. Duplicate-stitch a small orange triangle at the lower front edge.

### Green hood
1. Cast on @{[ceil($body_width * 0.40)]} stitches and knit $hood_rows rows.
2. Decrease at both edges in the last 2 rows.
3. Add a tiny copper accent at the peak.

KNIT
}

sub emoji_crochet_body {
    my ($body_width, $body_rounds, $curve_rows, $wing_rows, $hood_rows, $stitch_word) = @_;
    return <<"EMOJI_CROCHET";
## 🪝

### 🧍
1. ⭕ 6 $stitch_word.
2. ➕➡️ $body_width $stitch_word.
3. 🔁 $body_rounds.
4. ➖ 4️⃣ × 2, ☁️, 🔒.

### 🍌↪️
1. ⛓️ @{[ceil($body_width * 0.58)]}; 🔁 $curve_rows $stitch_word.
2. ➕➡️ 2️⃣; ➖⬅️ 3️⃣.
3. 🟫 sl st.

### 🪿↔️
1. 2 × @{[ceil($body_width * 0.33)]} × $wing_rows.
2. 🔻 3.
3. 🟧🔺.

### 🟢🔝
1. ⛓️ @{[ceil($body_width * 0.40)]}; 🔁 $hood_rows.
2. ➖↔️ 2.
3. 🟫✨.

EMOJI_CROCHET
}

sub emoji_knit_body {
    my ($body_width, $body_rounds, $curve_rows, $wing_rows, $hood_rows, $stitch_word) = @_;
    return <<"EMOJI_KNIT";
## 🧶

### 🧍
1. 🪡 $body_width $stitch_word ⭕.
2. 🔁 $body_rounds.
3. ➖ 4️⃣ × 2, ☁️, 🔒.

### 🍌↪️
1. 🪡 @{[ceil($body_width * 0.58)]}; 🔁 $curve_rows.
2. ➕➡️ 2️⃣; ➖⬅️ 3️⃣.
3. 🟫🔚.

### 🪿↔️
1. 2 × @{[ceil($body_width * 0.33)]} × $wing_rows.
2. 🔻 3.
3. 🟧🔺.

### 🟢🔝
1. 🪡 @{[ceil($body_width * 0.40)]}; 🔁 $hood_rows.
2. ➖↔️ 2.
3. 🟫✨.

EMOJI_KNIT
}

sub table {
    my ($header, @rows) = @_;
    my ($left_header, $right_header) = @{$header};
    my $out = "| $left_header | $right_header |\n| --- | --- |\n";
    for my $row (@rows) {
        my ($left, $right) = @{$row};
        $out .= "| $left | $right |\n";
    }
    return "$out\n";
}

sub percent {
    my ($value) = @_;
    return sprintf('%.1f%%', $value * 100);
}

sub rounds {
    my ($base, $scale_value) = @_;
    return ceil($base * $scale_value);
}

sub stitches {
    my ($base, $gauge, $scale_value) = @_;
    return ceil($base * $gauge * $scale_value / 1.6);
}

sub yardage {
    my ($base, $profile_ref, $scale_value, $ratio_value) = @_;
    return ceil($base * $profile_ref->{yardage} * $scale_value * (0.30 + $ratio_value));
}
