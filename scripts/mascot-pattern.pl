#!/usr/bin/env perl
use strict;
use warnings;
use Getopt::Long qw(GetOptions);

my %yarn_weights = (
    lace     => { hook => '2.25 mm', needle => '2.75 mm', scale => 0.70, yards => 90 },
    fingering => { hook => '3.00 mm', needle => '3.25 mm', scale => 0.85, yards => 115 },
    sport    => { hook => '3.50 mm', needle => '3.75 mm', scale => 1.00, yards => 140 },
    dk       => { hook => '4.00 mm', needle => '4.50 mm', scale => 1.15, yards => 165 },
    worsted  => { hook => '5.00 mm', needle => '5.50 mm', scale => 1.35, yards => 210 },
    bulky    => { hook => '6.50 mm', needle => '7.00 mm', scale => 1.70, yards => 280 },
);

my $banana = 5;
my $goose = 3;
my $goblin = 2;
my $yarn_weight = 'worsted';
my $craft = 'crochet';
my $name = 'AgentPipe mascot';
my $help = 0;

GetOptions(
    'banana=i'     => \$banana,
    'goose=i'      => \$goose,
    'goblin=i'     => \$goblin,
    'yarn-weight=s'=> \$yarn_weight,
    'craft=s'      => \$craft,
    'name=s'       => \$name,
    'help'         => \$help,
) or usage();

usage() if $help;
usage('craft must be crochet|knit') unless $craft eq 'crochet' || $craft eq 'knit';
usage("unknown yarn weight: $yarn_weight") unless exists $yarn_weights{$yarn_weight};
usage('motif ratios must be zero or positive integers') if $banana < 0 || $goose < 0 || $goblin < 0;
usage('at least one motif ratio must be greater than zero') if $banana + $goose + $goblin == 0;

my $settings = $yarn_weights{$yarn_weight};
my $tool = $craft eq 'crochet' ? $settings->{hook} . ' crochet hook' : $settings->{needle} . ' knitting needles';
my $height = rounded(7.5 * $settings->{scale});
my $width = rounded(4.0 * $settings->{scale});
my $yards = int($settings->{yards} * ratio_multiplier($banana, $goose, $goblin));
my $grams = int($yards / 2.2);
my %percent = ratio_percentages($banana, $goose, $goblin);
my @rows = build_row_plan($craft, \%percent);

print "# $name pattern\n\n";
print "Generated for a $craft project using $yarn_weight yarn.\n\n";
print "## Materials\n\n";
print "- $yards yd / about $grams g of main yarn across the selected motif colors\n";
print "- $tool\n";
print "- Fiberfill or scrap yarn for stuffing\n";
print "- Tapestry needle, stitch markers, and removable pins\n";
print "- Small felt scraps or contrast yarn for face and accent details\n\n";

print "## Gauge and sizing\n\n";
print "- Finished size: about $height in tall by $width in wide before blocking\n";
print "- Motif balance: $percent{banana}% banana, $percent{goose}% goose, $percent{goblin}% goblin\n";
print "- Work tighter than garment gauge so stuffing does not show through\n";
print "- Scale up by selecting a heavier --yarn-weight value, or scale down with lace/fingering\n\n";

print "## Pattern instructions\n\n";
for my $row (@rows) {
    print "- $row\n";
}

print "\n## Assembly\n\n";
print "- Stuff the body firmly enough to stand, but leave the seam edge flexible.\n";
print "- Pin the appendages before sewing so the silhouette stays balanced.\n";
print "- Embroider the face after stuffing; this makes expression placement easier.\n";
print "- Weave in all ends, then steam or wet block lightly according to the yarn label.\n";
print "- Name tag: stitch or embroider \"$name\" on a small scrap and attach it to the base.\n";

sub ratio_multiplier {
    my ($b, $go, $gb) = @_;
    my $total = $b + $go + $gb;
    return 1 + ($total > 10 ? ($total - 10) * 0.035 : 0);
}

sub ratio_percentages {
    my ($b, $go, $gb) = @_;
    my $total = $b + $go + $gb;
    return (
        banana => int(($b / $total) * 100 + 0.5),
        goose  => int(($go / $total) * 100 + 0.5),
        goblin => int(($gb / $total) * 100 + 0.5),
    );
}

sub build_row_plan {
    my ($mode, $percent) = @_;
    my $body_stitch = $mode eq 'crochet' ? 'single crochet' : 'stockinette';
    my $increase = $mode eq 'crochet' ? '2 sc in next stitch' : 'kfb';
    my $decrease = $mode eq 'crochet' ? 'sc2tog' : 'ssk';
    my $edge = $mode eq 'crochet' ? 'slip stitch closed' : 'three-needle bind off';

    return (
        "Foundation: make a compact oval base and place a marker at the start of the round.",
        "Rounds 1-4: increase evenly with $increase until the base is broad enough to stand.",
        "Rounds 5-12: work $body_stitch, changing color blocks to keep the motif balance near $percent->{banana}/$percent->{goose}/$percent->{goblin}.",
        "Rounds 13-16: shape the neck and top ridge with paired $decrease decreases at each side.",
        "Make two small wings or arms, then one curved accent panel for the front silhouette.",
        "Close the top with $edge after stuffing and checking that the project stands upright.",
    );
}

sub rounded {
    my ($value) = @_;
    return sprintf('%.1f', $value);
}

sub usage {
    my ($message) = @_;
    print STDERR "$message\n\n" if defined $message;
    print STDERR "Usage: scripts/mascot-pattern.pl [options]\n";
    print STDERR "  --banana N       Banana motif ratio, default 5\n";
    print STDERR "  --goose N        Goose motif ratio, default 3\n";
    print STDERR "  --goblin N       Goblin motif ratio, default 2\n";
    print STDERR "  --yarn-weight W  lace, fingering, sport, dk, worsted, or bulky\n";
    print STDERR "  --craft MODE     crochet|knit\n";
    print STDERR "  --name TEXT      Pattern title\n";
    print STDERR "  --help           Show this help\n";
    exit defined $message ? 2 : 0;
}
