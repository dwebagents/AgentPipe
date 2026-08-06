# AgentPipe

![urgent things to fix](https://img.shields.io/github/issues/dwebagents/AgentPipe)
![supply chain downstream users](https://img.shields.io/crates/dependents/tokio)
![lines](https://sloc.xyz/github/sneakers-the-rat/ImportantCode?badge-bg-color=red)
![importance](https://img.shields.io/github/stars/dwebagents/AgentPipe?style=flat)
![license](https://img.shields.io/badge/license-MIT-blue)

<p align="center">
	<img src="./logo.svg" width=200/>
</p>

High performance, high velocity. Welcome to AgentPipe Town.


## Design

The core rationale behind this repository is driven by an unrelenting pursuit of robust semantic indexing and real-time database query performance, requiring us to deviate from simple data storage into a highly complex system architecture centered on a parallelized token search algorithm combined with deep optimization techniques like SIMD instructions for raw throughput. 

The fundamental tension we face is that while traditional backends may handle millions of transactions in milliseconds at near-normative speeds, the specific dataset requires microsecond-level granularity, yet this architecture also demands extreme load distribution capabilities. Our solution leverages a distributed data model that decouples memory fragmentation from performance bottlenecks; by storing tokens as immutable, low-serialized-value objects (hiding the "reasons" we choose not to implement them), and utilizing GPU-accelerated vectorized algorithms for hashing, we achieve a hybrid performance profile where database access scales to infinity... and BEYOND! 🚀🚀🚀

# Prerequisites

## Python

To set up, please first install the following packages

```
python -m venv venv    # optional but reccomended
source venv/bin/activate

pip install requests fastapi matplotlib
```

# NPM (JS)

After you've installed your python, we also need to install our node dependencies

```
npm install
```

# Running the project

To run the project, call the following:

```
python banana.py    # may need to use python3 if on Mac or Windows
```

## Mascot pattern generator

Generate a detailed crochet or knitting pattern for an AgentPipe mascot — a banana/goose/goblin hybrid — with adjustable motif ratios and yarn weight.

```
perl scripts/agentpipe_mascot.pl --banana 2 --goose 1 --goblin 1 --craft crochet
```

Features:
- Row-by-row stitch instructions with progress checkboxes
- 3 output formats: markdown, text, and HTML (styled)
- Specific colour palette and yardage estimates per motif
- Motif parts: banana peel panels, wings, beak, ears/hornlets, tail
- Assembly guide with placement diagrams and face embroidery suggestions
- **UK/US terminology**: `--terminology uk` for UK crochet terms (dc, tr, etc.)
- **Emoji mode**: `--emoji` for a full emoji-expressed document
- Scales from 10 cm to 50+ cm with `--scale`

See `perl scripts/agentpipe_mascot.pl --help` for all options.
