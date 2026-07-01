#!/usr/bin/env perl

use strict;
use warnings;
use Getopt::Long qw(GetOptions);

my %weight_profiles = (
    lace      => { hook => '2.25 mm', needle => '2.25 mm', gauge => 32, yardage => 1.45 },
    fingering => { hook => '2.75 mm', needle => '2.75 mm', gauge => 28, yardage => 1.25 },
    sport     => { hook => '3.50 mm', needle => '3.50 mm', gauge => 24, yardage => 1.10 },
    dk        => { hook => '4.00 mm', needle => '4.00 mm', gauge => 22, yardage => 1.00 },
    worsted   => { hook => '5.00 mm', needle => '5.00 mm', gauge => 18, yardage => 0.86 },
    bulky     => { hook => '6.50 mm', needle => '6.50 mm', gauge => 14, yardage => 0.72 },
);

my %opts = (
    banana      => 1,
    goose       => 1,
    goblin      => 1,
    yarn_weight => 'dk',
    craft       => 'crochet',
    scale       => 1,
    name        => 'AgentPipe Mascot',
);

GetOptions(
    'banana=f'     => \$opts{banana},
    'goose=f'      => \$opts{goose},
    'goblin=f'     => \$opts{goblin},
    'yarn-weight=s'=> \$opts{yarn_weight},
    'craft=s'      => \$opts{craft},
    'scale=f'      => \$opts{scale},
    'name=s'       => \$opts{name},
    'help'         => \$opts{help},
) or usage(1);

usage(0) if $opts{help};

my $profile = $weight_profiles{lc $opts{yarn_weight}}
    or die "Unknown yarn weight '$opts{yarn_weight}'. Try lace, fingering, sport, dk, worsted, or bulky.\n";

$opts{craft} = lc $opts{craft};
die "Craft must be 'crochet' or 'knit'.\n"
    unless $opts{craft} eq 'crochet' || $opts{craft} eq 'knit';

die "Scale must be greater than zero.\n" unless $opts{scale} > 0;
for my $part (qw(banana goose goblin)) {
    die "$part ratio must be zero or greater.\n" if $opts{$part} < 0;
}

my $total = $opts{banana} + $opts{goose} + $opts{goblin};
die "At least one mascot ratio must be greater than zero.\n" if $total <= 0;

my %ratio = map { $_ => $opts{$_} / $total } qw(banana goose goblin);
my $height_cm = round(18 * $opts{scale}, 1);
my $body_rounds = int(18 * $opts{scale} + 0.5);
my $body_stitches = even(int($profile->{gauge} * 0.85 * $opts{scale} + 0.5));
my $wing_rows = int(7 * $opts{scale} + 0.5);
my $ear_rows = int(5 * $opts{scale} + 0.5);
my $yardage = int(95 * $profile->{yardage} * $opts{scale} + 0.5);

print "# $opts{name} pattern\n\n";
print "Generated for a ", ratio_line(\%ratio), " mascot at approximately ${height_cm} cm tall.\n\n";
print "## Materials\n\n";
print "- Yarn weight: $opts{yarn_weight}\n";
print "- Main yarn: about ${yardage} m total\n";
print "- Suggested ", $opts{craft} eq 'crochet' ? "hook" : "needles", ": ",
    $opts{craft} eq 'crochet' ? $profile->{hook} : $profile->{needle}, "\n";
print "- Stuffing, stitch markers, tapestry needle, two safety eyes or embroidered eyes\n";
print "- Accent colors: yellow, cream or white, orange, green, and one dark outline color\n\n";

print "## Color allocation\n\n";
for my $part (qw(banana goose goblin)) {
    my $pct = int($ratio{$part} * 100 + 0.5);
    print "- ", ucfirst($part), ": ${pct}% of accent details\n";
}

print "\n## Pattern notes\n\n";
print "- Work tightly enough that stuffing does not show through.\n";
print "- Place increases away from the front center to keep the face clean.\n";
print "- If a ratio is zero, skip that motif section and redistribute the space visually.\n\n";

if ($opts{craft} eq 'crochet') {
    crochet_pattern($body_rounds, $body_stitches, $wing_rows, $ear_rows);
} else {
    knit_pattern($body_rounds, $body_stitches, $wing_rows, $ear_rows);
}

print "\n## Assembly\n\n";
print "1. Stuff the body firmly before the last shaping round.\n";
print "2. Attach the peel panels down the back so they read as banana stripes.\n";
print "3. Sew wings symmetrically at the widest point of the body.\n";
print "4. Add ears or hornlets near the top edge, angled slightly outward.\n";
print "5. Embroider nostrils, a small smile, and feather or stitch marks as desired.\n";
print "6. Steam lightly or block according to yarn label instructions.\n";

sub crochet_pattern {
    my ($rounds, $stitches, $wings, $ears) = @_;
    print "## Crochet instructions\n\n";
    print "### Body\n\n";
    print "1. Magic ring 6 sc.\n";
    print "2. Increase evenly until you reach $stitches stitches.\n";
    print "3. Work $rounds rounds even, changing colors according to the allocation above.\n";
    print "4. Decrease every sixth stitch for two rounds, stuff, then close.\n\n";
    print "### Motifs\n\n";
    print "- Banana peel panels: chain ", int($rounds * 0.75), ", sc back across, taper at both ends.\n";
    print "- Wings: make two flat ovals over $wings rows, then edge with slip stitches.\n";
    print "- Beak: chain 4, turn, sc 3, then fold and sew below the eyes.\n";
    print "- Ears or hornlets: make two triangles over $ears rows.\n";
}

sub knit_pattern {
    my ($rows, $stitches, $wings, $ears) = @_;
    print "## Knit instructions\n\n";
    print "### Body\n\n";
    print "1. Cast on 6 stitches and join in the round.\n";
    print "2. Increase evenly until you reach $stitches stitches.\n";
    print "3. Knit $rows rounds even, using stranded or duplicate stitch color sections.\n";
    print "4. Decrease every sixth stitch for two rounds, stuff, then draw closed.\n\n";
    print "### Motifs\n\n";
    print "- Banana peel panels: knit ", int($rows * 0.75), " rows as narrow tapered strips.\n";
    print "- Wings: make two small garter-stitch ovals over $wings rows.\n";
    print "- Beak: knit a 3-stitch i-cord for 3 rows, fold, and sew below the eyes.\n";
    print "- Ears or hornlets: make two triangular tabs over $ears rows.\n";
}

sub ratio_line {
    my ($ratio) = @_;
    return join ', ', map { sprintf '%s %.0f%%', $_, $ratio->{$_} * 100 } qw(banana goose goblin);
}

sub even {
    my ($value) = @_;
    return $value % 2 ? $value + 1 : $value;
}

sub round {
    my ($value, $places) = @_;
    my $factor = 10 ** $places;
    return int($value * $factor + 0.5) / $factor;
}

sub usage {
    my ($exit_code) = @_;
    print <<"USAGE";
Usage: perl scripts/mascot_pattern.pl [options]

Options:
  --banana N        Banana motif ratio, default 1
  --goose N         Goose motif ratio, default 1
  --goblin N        Goblin motif ratio, default 1
  --yarn-weight W   lace, fingering, sport, dk, worsted, or bulky
  --craft C         crochet or knit, default crochet
  --scale N         Size multiplier, default 1
  --name TEXT       Pattern title
  --help            Show this help
USAGE
    exit $exit_code;
}
