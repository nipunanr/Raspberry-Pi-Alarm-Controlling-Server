# NR IOT Device Control System

This is a Python script that implements an IoT device control system using a Raspberry Pi. The script controls LEDs and buzzers connected to GPIO pins on the Raspberry Pi. It also interacts with a MySQL database to log device runs and trigger alerts.

## Prerequisites

Before running the script, ensure the following:

- You have a Raspberry Pi device with the required hardware components (LEDs, buzzers).
- Python is installed on your Raspberry Pi.
- The required Python packages are installed. You can install them using the following commands:

    ```bash
    pip install gpiozero mysql-connector-python art
    ```

## Usage

1. Open a terminal on your Raspberry Pi.

2. Navigate to the directory where the script is located.

3. Run the script using the following command:

    ```bash
    python script.py
    ```

4. The script will initialize the device, establish a connection to the database, and start an HTTP server to handle requests.

## Configuration

### Device Configuration

- Modify the `device_ip` variable to specify the IP address of the Raspberry Pi.

### Pins Configuration

- Update the `led_pin` and `buzzer_pin` variables to set the GPIO pins for the LED and buzzer respectively.

### Database Configuration

- Update the `db_host`, `db_name`, `db_user`, and `db_password` variables to connect to your MySQL database.

## API Endpoints

- `/`: Displays a simple message.

- `/trigger`: Accepts POST requests with JSON data to control device alerts.

    - Send a POST request with JSON data:
    
        ```json
        {
            "location": "your_device_location",
            "notification": "on"  // or "off"
        }
        ```
   
## License

Copyright © 2023 Nipuna Rangika. All rights reserved.

---

**Disclaimer:** This readme is a general overview and guide for the provided script. Make sure to test the script in your specific environment and adapt it to your needs. The script's functionality and behavior can vary based on hardware, software, and network configurations.
