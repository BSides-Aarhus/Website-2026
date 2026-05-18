---
title: We Scanned 10,000 Danish Orgs Without Sending a Single Packet
time: "12:45"
room: "Room 1"
speakers:
  - morten-von-seelen
topics:
  - osint
  - reconnaissance
  - passive-recon
  - supply-chain
  - threat-intelligence
---

We built a passive exposure profiling engine, originally for insurance underwriters who were tired of self-reported security questionnaires.

Then we pointed it at Danish critical infrastructure at national scale. No active scanning, no exploitation. Just OSINT, pattern recognition and knowledge from thousands of incidents and access to insurance claim data. It gives us the same outside view as the attackers have.

The most interesting finding wasn't any single vulnerability or scan. It was what the outside view turned out to predict about the inside. That pattern has now repeated across thousands of organizations, and it changes what you can actually infer from passive recon alone.
What does an open port 22 whisper about your AD and backup?

I'll show what repeats: which external signals predict real compromise risk and which ones are noise, why shared hosting with vulnerable neighbors is one of the most underestimated indicators we see, and how a handful of passive signals cluster together in ways that tell you more than you'd expect.

Some of these findings led to published investigations that forced vendors to patch or shut down parts of their operation.

I'll share those stories. But the point of this talk isn't the headlines. It's the methodology and the patterns, and what you can do with them whether you're scoping a red team engagement, benchmarking your own org, or trying to understand supply chain risk.

The session includes a live demo on stage: sector picked by the audience to full exposure profile, using simple LLMs for target identification.

Takeaways:

- What the outside predicts about the inside, and the evidence behind it
- Which passive signals matter and which ones are noise
- Shared-infrastructure risk as a leading indicator
- Live demo: audience picks the sector, we go live
