# IoT End-to-End System — CECS 327 Assignment 8

## Project Overview

This project is a complete end-to-end IoT system integrating:
- A TCP client-server architecture (from Assignment 6)
- A SQLite database (from Assignment 7)
- Simulated IoT sensor data enhanced with metadata from dataniz.com

It allows users to send specific data queries from a client program, which are processed by a server using live IoT data and metadata.

---

## Supported Queries

The client supports three predefined natural-language queries:
1. What is the average moisture inside my kitchen fridge in the past three hours?
2. What is the average water consumption per cycle in my smart dishwasher?
3. Which device consumed more electricity among my three IoT devices (two refrigerators and a dishwasher)?

Any other input will return a helpful error message listing the allowed queries.

---

## Technologies Used

- Python 3
- SQLite for database operations
- psycopg2 and pytz for PostgreSQL/timezone handling (if applicable)
- socket library for TCP communication
- Metadata from dataniz.com

---

## Project Structure

IoT_Pipeline/  
├── client.py # TCP client program  
├── server.py # TCP server program with database and metadata logic  
├── db/  
│ └── iot_data.db # Preloaded IoT database (from Assignment 7)  
├── metadata.json # Device metadata (from dataniz)  
├── README.md # This file  
├── requirements.txt # Required Python packages  

---

## How to Run the Project

### If Running Locally

1. Open two terminal windows in the project directory.
2. In Terminal 1, activate your virtual environment and run the server:
   ```bash
   python server.py

- Input localhost for the server IP.

- Input 12345 for the port.

3. In Terminal 2, run the client:

    ```bash
    python client.py

- Input localhost for the server IP.

- Input 12345 for the port.

4. Enter one of the supported queries. To exit, type quit.


### If Running on Two VMs

1. SSH into each VM (Client and Server).

2. On the server VM, run:

    ```bash
    python server.py

- Input 0.0.0.0 for the server IP.

- Use the port number you configured (e.g., 12345).

3. On the client VM, run:

    ```bash
    python client.py

- Input the public IP of the server VM.

- Use the same port number.

4. Use the client to send queries. Type quit to close the session.

## Requirements
- Install dependencies:

    ```bash
    pip install -r requirements.txt

## Features
- **Query Validation**: Only supports specific queries; all others are rejected politely.

- Database Integration: Uses an SQLite database with IoT sensor readings.

- Metadata Awareness: Leverages metadata from dataniz.com to filter, organize, and process data based on device type, time zone, and measurement units.

- Unit Conversion: Converts:

    - Moisture → Relative Humidity (RH%)

    - Time → PST

    - Volume → Gallons

    - Power → kWh


## Devices & Metadata

This system simulates and supports:

- 2 Smart Refrigerators (moisture, electricity usage)

- 1 Smart Dishwasher (water usage, electricity usage)

### Metadata includes:

- Device ID

- Time zone

- Data type and units

- Location

If metadata was not used for specific functionality, reasoning is provided in the report.

## Authors

- Group Members: Silvia Tran, Isabella Alvarez

- Course: CECS 327 - Intro to Networks and Distributed Systems

- Professor: Malik Luti

## Notes

- Queries are processed in PST and displayed in imperial units.

- To reset the database, re-import the original .db file or reconfigure your sensors in Dataniz.

## Testing Tips

- Try submitting each of the three supported queries to see real-time output.

- Monitor the server terminal for received data and logs.

- Use quit to exit cleanly and close the connection.