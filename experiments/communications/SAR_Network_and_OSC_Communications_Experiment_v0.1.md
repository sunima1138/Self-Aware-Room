# Self-Aware Room Communications Experiment

## Python to TouchDesigner over Ethernet using OSC

**Version:** 0.1 (Experimental)\
**Date:** 2026-07-29\
**Project:** OAA Self-Aware Room (SAR)\
**Status:** Pre-Integration Experiment Protocol (Not Yet Executed)

------------------------------------------------------------------------

# 1. Introduction

This document describes the initial communications experiment for the
Self-Aware Room (SAR) project. The objective is to establish reliable
communication between a Python application running on a macOS computer
and TouchDesigner running on a Windows PC using a dedicated Ethernet
network and the Open Sound Control (OSC) protocol.

This experiment is intentionally outside the SAR computational pipeline.
Its purpose is to validate raw communications before any integration into
L0-L5 processing components.

The immediate goal is not to develop the complete communications
architecture for the Self-Aware Room, but rather to establish a stable
and repeatable development environment that can later support additional
computers, sensors, middleware, AI agents, and visualization systems.

The experiment proceeds in clearly defined stages:

1.  Establish physical network connectivity.
2.  Verify IP communication.
3.  Verify application-level communication.
4.  Implement OSC messaging.
5.  Integrate with TouchDesigner.

Only after each stage has been verified should the next stage be
attempted.

### Phase Boundary

- In scope: network and OSC communication validation between two computers.
- Out of scope: SAR ingest normalization, pipeline conformance, or semantic processing.

------------------------------------------------------------------------

# 2. Experimental Hardware Configuration

Current hardware:

  Device                     Purpose
  -------------------------- -------------------------
  Apple Mac                  Python Development
  Windows PC                 TouchDesigner
  NETGEAR GS316EPP           Gigabit Ethernet Switch
  2 × Cat6 Ethernet cables   Dedicated network

The Mac and Windows PC remain connected to Wi-Fi for Internet access
while simultaneously using Ethernet for dedicated control
communications.

## Network Topology

``` text
                  Internet
                      │
                Existing Wi-Fi
             (Home / Office Router)
                 /              \
                /                \
          Mac Wi-Fi          Windows Wi-Fi
                │                 │
                │                 │
        ----------------------------------
         Dedicated Ethernet Network
        ----------------------------------

      Mac Ethernet
      192.168.50.10
             │
      NETGEAR GS316EPP
             │
      Windows Ethernet
      192.168.50.20
```

The Ethernet network is dedicated to Self-Aware Room communications
while Wi-Fi continues to provide Internet connectivity.

------------------------------------------------------------------------

# 3. Why Use Ethernet?

Ethernet provides lower latency, reduced packet loss, deterministic
timing, greater reliability, and easier troubleshooting. The dedicated
Ethernet network isolates control traffic from Internet traffic.

------------------------------------------------------------------------

# 4. Network Parameters

  Setting       Value
  ------------- ---------------
  Network       192.168.50.0
  Subnet Mask   255.255.255.0
  Mac           192.168.50.10
  Windows       192.168.50.20
  Gateway       Leave Blank
  DNS           Leave Blank

Because no gateway is specified, Internet traffic continues to use Wi-Fi
automatically.

------------------------------------------------------------------------

# 5. Configuration and Verification

Configure static IP addresses on both machines, verify the Ethernet link
LEDs, confirm the assigned addresses with `ifconfig` (macOS) and
`ipconfig` (Windows), then test connectivity:

``` bash
# From the Mac
ping 192.168.50.20
```

``` cmd
:: From Windows
ping 192.168.50.10
```

Both systems should also retain normal Internet access over Wi-Fi.

## 5.1 Computer 1 (Mac) - Step-by-Step

1. Connect Mac Ethernet to the dedicated switch.
2. Open System Settings -> Network.
3. Select Ethernet adapter used for SAR communications.
4. Set Configure IPv4 to Manual.
5. Enter:
  - IP Address: 192.168.50.10
  - Subnet Mask: 255.255.255.0
  - Router/Gateway: leave blank
  - DNS: leave blank for this Ethernet adapter
6. Apply/Save network settings.
7. Verify interface state and address:

``` bash
ifconfig
```

8. Confirm Ethernet adapter has 192.168.50.10 and status active.
9. Verify internet still works over Wi-Fi (open browser or run a known DNS lookup).

## 5.2 Computer 2 (Windows + TouchDesigner) - Step-by-Step

1. Connect Windows Ethernet to the dedicated switch.
2. Open Settings -> Network & Internet -> Advanced network settings -> More network adapter options.
3. Right-click Ethernet adapter -> Properties.
4. Open Internet Protocol Version 4 (TCP/IPv4).
5. Select Use the following IP address.
6. Enter:
  - IP address: 192.168.50.20
  - Subnet mask: 255.255.255.0
  - Default gateway: leave blank
  - Preferred DNS server: leave blank for this Ethernet adapter
7. Save/Apply settings.
8. Verify address assignment:

``` cmd
ipconfig
```

9. Confirm Ethernet adapter has 192.168.50.20 and link is up.
10. Verify internet still works over Wi-Fi.

## 5.3 Bidirectional Network Validation

Run from Mac:

``` bash
ping 192.168.50.20
```

Run from Windows:

``` cmd
ping 192.168.50.10
```

Expected:

- Replies received in both directions.
- No sustained packet loss during a short continuous run.

If ping fails, check cable, switch port LEDs, adapter selection, and IP values before proceeding.

------------------------------------------------------------------------

# 6. Install python-osc

``` bash
python -m pip install python-osc
```

------------------------------------------------------------------------

# 7. Configure TouchDesigner

Create an OSC In DAT listening on UDP port **9000**.

## 7.1 Windows Firewall and Port Check

Before OSC validation, ensure inbound UDP 9000 is not blocked.

1. Allow TouchDesigner through Windows Defender Firewall (private network profile).
2. If needed, create an inbound UDP rule for port 9000.
3. Re-run OSC receive test after firewall change.

## 7.2 TouchDesigner Receive Setup (Computer 2)

1. Launch TouchDesigner.
2. Create an OSC In DAT.
3. Set protocol to UDP.
4. Set local port to 9000.
5. Enable Active/Listening state.
6. Keep the DAT viewer visible to verify incoming messages.

------------------------------------------------------------------------

# 8. First OSC Test

``` python
from pythonosc.udp_client import SimpleUDPClient

client = SimpleUDPClient("192.168.50.20", 9000)
client.send_message("/hello", 1)
```

TouchDesigner should receive:

    /hello
    1

## 8.1 Repeated Send Test (Recommended)

Use a short burst test to validate basic reliability:

``` python
from pythonosc.udp_client import SimpleUDPClient

client = SimpleUDPClient("192.168.50.20", 9000)
for i in range(500):
    client.send_message("/test/index", i)
```

Expected:

- TouchDesigner receives sequential messages without obvious drops.
- Any missing messages or anomalies are recorded in the execution log.

------------------------------------------------------------------------

# 9. Next Steps

After successful OSC communication:

-   Bidirectional messaging
-   Heartbeats
-   Structured OSC namespace
-   Sensor integration
-   Middleware
-   Distributed services

------------------------------------------------------------------------

# 10. Success Criteria and Exit Gate

This protocol is considered successful only when all criteria below are met.

1. Ethernet connectivity is stable and ping succeeds bidirectionally.
2. TouchDesigner receives OSC test messages from Python on the configured port.
3. Repeated send test (recommended: at least 500 messages) shows no unexpected message loss.
4. Both computers keep Internet access over Wi-Fi while OSC traffic uses Ethernet.
5. Configuration details and observed results are recorded in the execution log.

Only after this gate is passed should SAR pipeline integration planning begin.

------------------------------------------------------------------------

# 11. Execution Log (To Be Completed During Run)

## 11.1 Environment

- Mac OS version:
- Windows OS version:
- TouchDesigner version/build:
- Python version:
- python-osc version:

## 11.2 Run Summary

- Run date/time:
- Operator(s):
- Ethernet link status:
- Ping results:
- OSC receive verification:
- Repeated send count:
- Observed loss/errors:
- Internet-over-Wi-Fi retained: Yes/No

## 11.3 Outcome

- Pass/Fail:
- Notes:

------------------------------------------------------------------------

# Troubleshooting

-   Verify physical connectivity before software.
-   Verify IP connectivity before OSC.
-   Leave the Ethernet gateway blank so Wi-Fi remains the Internet
    connection.
-   Use static IP addresses during development.
