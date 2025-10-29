# Hamming Code Visualizer

## Overview
This Python Tkinter application demonstrates the Hamming code algorithm for error detection and correction. The visualizer guides users through generating Hamming codes for input data bits, simulating errors by flipping bits, and automatically detecting and correcting single-bit errors. It offers detailed, step-by-step visualization in an intuitive, professional GUI.

## Features
- Interactive input and output panels
- Step-by-step parity calculation and encoding visualization
- Error simulation with user-specified bit flipping
- Automatic error detection and correction display
- Tabbed interface separating encoding steps and final results
- Modern, accessible color scheme and layout

## Installation
1. Ensure Python 3.6+ is installed with Tkinter support
2. Download or clone this repository
3. Run the application:

## Usage
1. Enter binary data bits (0s and 1s) in the "Enter Data Bits" field.
2. Click "Generate Hamming Code" to encode the data with parity bits.
3. Optionally, enter a bit position to flip in "Simulate Bit Error" (enter `0` for no error).
4. Click "Simulate Transmission & Detect Error" to simulate transmission, detect any error, and show correction.
5. Review the detailed encoding steps and final results in their respective tabs.

## How Hamming Code Works
1. Calculate the number of parity bits needed based on message length.
2. Insert parity bits at positions that are powers of two.
3. Calculate parity bits by XORing appropriate positions.
4. Transmit encoded message containing data and parity bits.
5. At the receiver, recalculate parity bits to detect any single-bit error.
6. Correct the error automatically if detected.

## Example
HAMMING CODE - FINAL RESULTS
======================================================================

Original Data: 1010

Encoded Message: 1010010


TRANSMISSION SIMULATION
----------------------------------------------------------------------
Sent:     1010010

Received: 1010110

Error introduced at position 3 (from right)


DETECTION RESULT: ✗ Error at position 3

Corrected Message: 1010010


✓ Successfully corrected single-bit error!

## Screenshots  

 ### Input and encoding:
<img width="1920" height="1020" alt="Screenshot 2025-10-29 215712" src="https://github.com/user-attachments/assets/095dc778-6f79-4327-a711-afa0e453928d" />
### Detection and correction
<img width="1920" height="1020" alt="Screenshot 2025-10-29 215734" src="https://github.com/user-attachments/assets/e0b08bc3-f725-4c94-9399-e8c4e6c217e4" />
### Results:
<img width="1920" height="1020" alt="Screenshot 2025-10-29 215742" src="https://github.com/user-attachments/assets/9a4b6ba7-0ab7-49ff-8bdb-5cabfccc2150" />

## License
This project is licensed under the MIT License.

## Author
Shubham Yadav
 
---

⭐ Star this repository if you find this project helpful for learning error correction and Hamming codes!
