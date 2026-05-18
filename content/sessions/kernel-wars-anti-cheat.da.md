---
title: 'Kernel Wars: Anti-Cheat Reversing, BYOVD Exploitation and Mitigations'
time: "10:00"
room: "Room 2"
speakers:
  - ravshan-rikhsiev
topics:
  - windows-internals
  - kernel
  - reverse-engineering
  - byovd
  - exploitation
  - anti-cheat
---

Anti-cheats live in the kernel. So do we.
We'll tear apart modern anti-cheat drivers: SSDT hooks, kernel callbacks (PsSetCreateProcessNotifyRoutine, ObRegisterCallbacks), handle stripping, memory integrity scanning, and userland/kernel communication channels.
Then we pivot to BYOVD. Legit signed driver, arbitrary kernel R/W, DSE bypass, PPL teardown, and anti-cheat process termination via IOCTL abuse. We'll cover real primitives attackers use and why the signed driver ecosystem is still a mess.
Finally, mitigations: HVCI, the MSFT vulnerable driver blocklist, and WDAC, what actually works and what doesn't.
Expect Windows internals, syscall flows, and kernel-mode tradecraft, and what is the impact of cheats to game industry. Will be fun and leave your Steam Deck at home.
