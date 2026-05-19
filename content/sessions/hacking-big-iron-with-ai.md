---
title: "Hacking Big Iron with AI: Attacking Mainframe Operating Systems Beyond Modern Assumptions"
time: "10:00"
room: "Room 2"
speakers:
  - adam-toscher
topics:
  - mainframe
  - red-team
  - pentesting
  - ai-security
  - vulnerability-research
---

Before the web. Before TCP/IP. Before "cloud." Some of the most powerful computers in the world were already running production workloads.

IBM mainframes didn't grow up in the browser era. System/360 (1964), MVS (1974), and today's z/OS (2000) were built for batch jobs, green-screen terminals, and a world where the internet simply didn't exist. Yet these systems still quietly process the majority of global financial transactions, airline bookings, and government records.

This talk is a guided tour of what happens when modern red teamers bring cloud-era assumptions into a system that predates the web. We'll break down how mainframes actually organize authority across five control planes (VTAM, TSO, RACF, JES, and CICS) and show exactly where those assumptions break. No shell model. No process tree. No EDR. The attack surface looks nothing like what your tooling expects.

We'll walk real techniques: TN3270 user enumeration, STEPLIB hijacking as a supply chain analog, JCL injection for deferred privileged execution, RACF misconfiguration paths, and how Network Job Entry misconfigurations can enable remote job submission without meaningful authentication. The mainframe equivalent of an open relay. These aren't theoretical. They come from real assessments against production environments.

We'll also introduce BigIron.ai, an open-source, fully offline AI-assisted assessment platform for z/OS and MVS environments. It runs a local LLM against live TN3270 sessions, interprets control-plane context in real time, guides structured walkthroughs, and generates findings. No cloud, no API keys, no data leaves the machine. We'll demo it live.

No mainframe background required. Just clear mental models, real terminal output, and a framework you can use the next time a mainframe shows up in scope.

Think of it as critical infrastructure security for a system your threat model forgot.
