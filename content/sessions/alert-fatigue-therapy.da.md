---
title: 'Alert Fatigue Therapy: Fixing Broken Detection Rules'
time: "11:00"
room: "Room 1"
speakers:
  - marvin-ngoma
---

"False positives burn out analysts. False negatives burn down businesses."
Modern SOCs and security teams live in this tension, and most detection rules make it worse. Every analyst has a "hall of shame": rules that fire hundreds of times a day and are ignored just as often. These aren't just noisy; they actively hide real attacks.

This session is a hands-on deep dive into high-fidelity detection engineering. We move beyond simple "if X then Y" logic to focus on designing detections that produce meaningful signals in real-world environments. Drawing on practical frameworks, we will explore the core tradeoffs of defense; from deciding where to set the "sensitivity dial" of rules to understanding why perfect detection rules are impossible.

The session includes a live-style walkthrough of refactoring a noisy detection rule into a high-confidence, context-aware alert by applying enrichment, correlation, and better logic. We will look at how to move a detection from a raw, low-value event to a surgical alert that provides the stage, technique, and data validation an analyst needs instantly.

I will close by giving a repeatable workflow for high-count alerts; deciding when to fix the rule, when to group/aggregate, and when to disable detection rules that shouldn't exist.

This is not a talk about tuning alerts, it's about redesigning how detection rules are built.
