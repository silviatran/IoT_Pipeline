import socket
import psycopg2
from datetime import datetime, timedelta
import pytz

# Setup server
host = input("Enter the server IP address: ")
port = int(input("Enter the server port: "))

myTCPSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
myTCPSocket.bind((host, port))
myTCPSocket.listen(5)
print("Waiting for connection...")
incomingSocket, incomingAddress = myTCPSocket.accept()

# Setup timezone
pst = pytz.timezone("US/Pacific")   # Define Pacific Timezone

try:
    # Connect to database
    db_connection = psycopg2.connect("postgresql://neondb_owner:npg_ognWcMRFyS52@ep-withered-fog-a444emeu-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require")
    cursor = db_connection.cursor() # Create cursor to execute SQL queries
    print("Connected to PostgreSQL")

    while True:
        # Wait for client request
        clientData = incomingSocket.recv(1024).decode('utf-8')
        if not clientData:
            break   # Exit if no data is received

        if clientData == "1":
            # QUERY 1 : Moisture past 3 hours (Smart Fridge #1)
            three_hours_ago = datetime.utcnow() - timedelta(hours=3)
            cursor.execute('''
                SELECT AVG(CAST(payload ->> 'Moisture Meter - Moisture Sensor - Smart Refrigerator' AS FLOAT))
                FROM "Data_virtual"
                WHERE payload ->> 'asset_uid' = '8ec-606-qyb-h36'
                AND TO_TIMESTAMP(CAST(payload ->> 'timestamp' AS BIGINT)) >= %s
            ''', (three_hours_ago,))
            result = cursor.fetchone()
            response = f"Avg moisture in past 3 hours is {round(result[0], 2)}% RH" if result[0] else "No moisture data found."

        elif clientData == "2":
            # QUERY 2 : Water usage in gallons (Smart Dishwasher)
            cursor.execute('''
                SELECT AVG(CAST(payload ->> 'YF-S201 - Water Consumption Sensor - Smart Dishwasher' AS FLOAT))
                FROM "Data_virtual"
                WHERE payload ->> 'asset_uid' = 'l5i-579-8tq-wo8';
            ''')
            result = cursor.fetchone()
            if result[0]:
                gallons = round(float(result[0]) * 0.264172, 2)
                response = f"Avg water per dishwasher cycle is {gallons} gallons"
            else:
                response = "No water data found."

        elif clientData == "3":
            # QUERY 3 : Total electricity use in kWh (3 devices)
            cursor.execute('''
                SELECT device_id, SUM(CAST(ammeter_reading AS FLOAT)) AS total_kwh
                FROM (
                    SELECT 'Fridge 1' AS device_id, payload ->> 'ACS712 - Ammeter - Smart Refridgerator' AS ammeter_reading
                    FROM "Data_virtual" WHERE payload ->> 'asset_uid' = '8ec-606-qyb-h36'
                    UNION ALL
                    SELECT 'Fridge 2', payload ->> 'sensor 1 17fa0f84-6cb5-43e1-afb9-16629fe7b54a'
                    FROM "Data_virtual" WHERE payload ->> 'asset_uid' = '337f627f-0906-4b98-8aa4-0d7b8f5bc6de'
                    UNION ALL
                    SELECT 'Dishwasher', payload ->> 'ACS712 - Ammeter - Smart Dishwasher'
                    FROM "Data_virtual" WHERE payload ->> 'asset_uid' = 'l5i-579-8tq-wo8'
                ) AS all_data
                GROUP BY device_id
                ORDER BY total_kwh DESC
                LIMIT 1;
            ''')
            result = cursor.fetchone()
            response = f"{result[0]} used the most electricity at {round(result[1], 2)} kWh" if result else "No energy data found."

        elif clientData.lower() == "quit":  # Handle 'quit' input
            response = "Connection closed."
            incomingSocket.send(response.encode('utf-8'))
            break

        else:   # Handle invalid input
            response = (
                "Sorry, invalid query. Please enter:\n"
                "1 for avg fridge moisture\n"
                "2 for dishwasher water usage\n"
                "3 for highest electricity use"
            )

        incomingSocket.send(response.encode('utf-8'))   # Send results to client

except Exception as e:
    print("Error:", e)
    incomingSocket.send(b"An error occurred.")

finally:    # Close cursor, connection, & socket
    cursor.close()
    db_connection.close()
    myTCPSocket.close()
    print("Connection closed.")
