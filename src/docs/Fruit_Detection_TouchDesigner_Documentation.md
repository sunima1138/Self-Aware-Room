# Fruit Detection → TouchDesigner

**What it does:** You say a fruit name into the mic. The program hears it, turns it into a number, and sends that number to TouchDesigner so it can show the matching picture.

## The flow

- You speak
- Mic records it
- Speech turns into text
- Text is checked for a fruit word
- If found, fruit → number
- Number gets sent to TouchDesigner over the network
- TouchDesigner shows the matching image

## Fruit → number

- blueberry → 1
- strawberry → 2
- apple → 3
- banana → 4
- grapes → 5

## Network settings used

- Mac IP: 192.168.50.10
- TouchDesigner PC IP: 192.168.50.20
- Port: 9000
- Message label: /sar/fruit_number

## How to run it

    cd src
    source ../.venv/bin/activate
    python3 mic_poc.py

Say a fruit name when it says "speak now."

## Status

- Fruit detection: working
- Sending the number over the network: working
- TouchDesigner actually showing the image: not confirmed yet — still needs Ethernet setup + TouchDesigner-side script finished
