#!/usr/bin/env perl
use strict;
use warnings;
use utf8;
use Getopt::Long qw(GetOptions);

binmode STDOUT, ':encoding(UTF-8)';
binmode STDERR, ':encoding(UTF-8)';

my %yarn_profiles = (
    lace      => { tool => '2.25 mm hook or needles', gauge => 32, scale => 1.35 },
    fingering => { tool => '2.75 mm hook or needles', gauge => 28, scale => 1.20 },
    sport     => { tool => '3.50 mm hook or needles', gauge => 24, scale => 1.10 },
    dk        => { tool => '4.00 mm hook or needles', gauge => 22, scale => 1.00 },
    worsted   => { tool => '5.00 mm hook or needles', gauge => 18, scale => 0.86 },
    bulky     => { tool => '6.50 mm hook or needles', gauge => 14, scale => 0.72 },
);

my %opts = (
    craft       => 'crochet',
    banana      => 1,
    goose       => 1,
    goblin      => 1,
    yarn_weight => 'dk',
    terminology => 'us',
    emoji       => 0,
    help        => 0,
);

GetOptions(
    'craft=s'       => \$opts{craft},
    'banana=f'      => \$opts{banana},
    'goose=f'       => \$opts{goose},
    'goblin=f'      => \$opts{goblin},
    'yarn-weight=s' => \$opts{yarn_weight},
    'terminology=s' => \$opts{terminology},
    'emoji!'        => \$opts{emoji},
    'help'          => \$opts{help},
) or usage(2);

usage(0) if $opts{help};
validate_options(\%opts);

my %ratio = normalize_ratio(@opts{qw(banana goose goblin)});
my %yardage = estimate_yardage(\%ratio, $opts{yarn_weight});

if ($opts{emoji}) {
    print render_emoji_pattern(\%opts, \%ratio, \%yardage);
} else {
    print render_markdown_pattern(\%opts, \%ratio, \%yardage);
}

sub usage {
    my ($code) = @_;
    my $out = <<"USAGE";
Usage: perl src/mascot_pattern_generator.pl [options]

Generate a project mascot crochet or knitting pattern.

Options:
  --craft crochet|knit          Pattern style. Default: crochet
  --banana N                   Banana design ratio. Default: 1
  --goose N                    Goose design ratio. Default: 1
  --goblin N                   Goblin design ratio. Default: 1
  --yarn-weight NAME           lace, fingering, sport, dk, worsted, bulky. Default: dk
  --terminology us|uk          Crochet terminology locale. Default: us
  --emoji                      Generate an emoji-forward output document
  --help                       Show this help

Example:
  perl src/mascot_pattern_generator.pl --banana 2 --goose 1 --goblin 1 --terminology uk
USAGE
    print $out;
    exit $code;
}

sub validate_options {
    my ($opts) = @_;

    $opts->{craft} = lc $opts->{craft};
    $opts->{terminology} = lc $opts->{terminology};
    $opts->{yarn_weight} = lc $opts->{yarn_weight};

    die "--craft must be crochet or knit\n" unless $opts->{craft} =~ /\A(?:crochet|knit)\z/;
    die "--terminology must be us or uk\n" unless $opts->{terminology} =~ /\A(?:us|uk)\z/;
    die "--yarn-weight must be one of: " . join(', ', sort keys %yarn_profiles) . "\n"
        unless exists $yarn_profiles{$opts->{yarn_weight}};

    for my $part (qw(banana goose goblin)) {
        die "--$part must be non-negative\n" if $opts->{$part} < 0;
    }

    my $total = $opts->{banana} + $opts->{goose} + $opts->{goblin};
    die "at least one ratio value must be greater than zero\n" if $total <= 0;
}

sub normalize_ratio {
    my ($banana, $goose, $goblin) = @_;
    my $total = $banana + $goose + $goblin;
    return (
        banana => $banana / $total,
        goose  => $goose / $total,
        goblin => $goblin / $total,
    );
}

sub estimate_yardage {
    my ($ratio, $weight) = @_;
    my $scale = $yarn_profiles{$weight}{scale};
    my $base_yards = 120 * $scale;

    return map {
        $_ => int(($base_yards * $ratio->{$_}) + 0.5)
    } qw(banana goose goblin);
}

sub render_markdown_pattern {
    my ($opts, $ratio, $yardage) = @_;
    my $profile = $yarn_profiles{$opts->{yarn_weight}};
    my $terms = terminology_block($opts->{craft}, $opts->{terminology});
    my $motif_order = motif_order($ratio);
    my $primary = $motif_order->[0];
    my $secondary = $motif_order->[1];
    my $accent = $motif_order->[2];

    my $craft_title = $opts->{craft} eq 'crochet' ? 'Crochet' : 'Knitting';
    my $locale_title = uc($opts->{terminology});

    return <<"MARKDOWN";
# AgentPipe Mascot $craft_title Pattern

## Design Ratios

- Banana: @{[percent($ratio->{banana})]}
- Goose: @{[percent($ratio->{goose})]}
- Goblin: @{[percent($ratio->{goblin})]}

The largest ratio becomes the primary body shape, the second ratio becomes the silhouette detail, and the smallest ratio becomes accent features. For this pattern, `$primary` drives the body, `$secondary` drives the side details, and `$accent` drives the face and trim.

## Materials

- Yarn weight: `$opts->{yarn_weight}`
- Suggested tool: $profile->{tool}
- Gauge target: $profile->{gauge} stitches per 10 cm
- Banana yarn: $yardage->{banana} yd
- Goose yarn: $yardage->{goose} yd
- Goblin yarn: $yardage->{goblin} yd
- Stuffing, safety eyes, stitch markers, tapestry needle, and scissors

## $locale_title $craft_title Terms

$terms

## Pattern

1. Body: work an oval body using the `$primary` colour for 12 rounds, increasing evenly through round 6 and working even through round 12.
2. Shape: add two tapered side panels in the `$secondary` colour. Keep each panel to roughly @{[panel_rows($ratio->{$secondary})]} rows so the motif ratio stays visible.
3. Accent: add face, trim, and small raised details in the `$accent` colour. Keep the accents clustered near the front third of the body.
4. Assembly: stuff firmly, seam the underside, then attach all panels with a tapestry needle.
5. Finish: weave in ends, block lightly, and check that the finished toy keeps the selected ratio balance.

## Crafter Notes

- Use tighter gauge when making a toy for heavy handling.
- If the body leans, add two hidden balancing stitches on the underside before closing.
- If using UK crochet terms, remember that US `single crochet` maps to UK `double crochet`.
- Knitting output keeps the same locale switch for consistency, even though common knit stitch names do not differ between US and UK usage.
MARKDOWN
}

sub render_emoji_pattern {
    my ($opts, $ratio, $yardage) = @_;
    my $profile = $yarn_profiles{$opts->{yarn_weight}};
    my $craft_icon = $opts->{craft} eq 'crochet' ? '🧶🪝' : '🧶📍';
    my $term_icon = $opts->{terminology} eq 'uk' ? '🇬🇧' : '🇺🇸';

    return <<"EMOJI";
# 🧶 AgentPipe Mascot Pattern Card

$craft_icon $term_icon  ⚖️ 🍌 @{[percent($ratio->{banana})]}  🪿 @{[percent($ratio->{goose})]}  👺 @{[percent($ratio->{goblin})]}

## 📦

- 🧵 `$opts->{yarn_weight}`  📏 $profile->{gauge}/10cm
- 🧰 $profile->{tool}
- 🍌 $yardage->{banana} yd
- 🪿 $yardage->{goose} yd
- 👺 $yardage->{goblin} yd
- 🧸 👀 📌 🪡 ✂️

## 📖

1. 🧶⭕ ➕ ➕ ➕ 6 rounds.
2. 🧶🔁 even 6 rounds.
3. 🍌/🪿/👺 panels = ⚖️ ratio rows.
4. 🧸 stuff + 🪡 seam.
5. 👀 face + ✨ trim.
6. 🧵 weave ends + 🧊 light block + ✅.

## 🔤

$term_icon terminology selected. Use `--emoji=false` for full English instructions.
EMOJI
}

sub terminology_block {
    my ($craft, $locale) = @_;

    if ($craft eq 'knit') {
        return join "\n", (
            "- Cast on: CO",
            "- Knit: k",
            "- Purl: p",
            "- Increase: kfb or m1",
            "- Decrease: k2tog",
            "- Bind off: BO",
        );
    }

    if ($locale eq 'uk') {
        return join "\n", (
            "- Chain: ch",
            "- Slip stitch: ss",
            "- Double crochet: dc",
            "- Half treble crochet: htr",
            "- Treble crochet: tr",
            "- Double crochet two together: dc2tog",
        );
    }

    return join "\n", (
        "- Chain: ch",
        "- Slip stitch: sl st",
        "- Single crochet: sc",
        "- Half double crochet: hdc",
        "- Double crochet: dc",
        "- Single crochet two together: sc2tog",
    );
}

sub motif_order {
    my ($ratio) = @_;
    return [sort { $ratio->{$b} <=> $ratio->{$a} || $a cmp $b } qw(banana goose goblin)];
}

sub percent {
    my ($value) = @_;
    return sprintf('%.1f%%', $value * 100);
}

sub panel_rows {
    my ($value) = @_;
    return 2 + int($value * 12 + 0.5);
}
