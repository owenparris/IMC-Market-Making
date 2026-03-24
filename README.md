# Market Making Algorithm (IMC Prosperity)

A simple market making strategy built for a simulated exchange environment.

## Overview

This project implements a rule-based market making strategy that operates in a setting where prices behave close to a random walk.

The focus is on capturing the bid-ask spread while managing inventory risk, rather than predicting price movements.

## Key Features

* Quotes bid and ask prices around an estimated fair value
* Captures spread through passive order placement
* Adjusts order sizes based on current position
* Takes liquidity when prices deviate from fair value
* Enforces position limits to control risk

## Approach

* Uses the mid-price as a baseline estimate of fair value
* Places orders slightly inside the spread to improve execution probability
* Reduces exposure when inventory becomes large
* Profits from spread capture rather than directional bets

## Results

* Consistently profitable in simulation despite minimal predictive signal
* Stable performance across repeated runs
* Demonstrates the importance of execution and risk management in market making

## Tech

* Python

## Notes

This project is intentionally simple and focuses on core market making ideas:

* spread capture
* inventory control
* execution priority

rather than complex predictive models.

