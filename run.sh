#!/bin/bash

echo "Checking printer service setup..."

# Check if port 5001 is already in use
if netstat -tuln | grep ":5001" > /dev/null; then
    echo "Port 5001 is in use. Killing existing process..."
    sudo kill $(sudo lsof -t -i:5001)
    sleep 1
fi

if [ ! -c "/dev/usb/lp0" ]; then
    echo "ERROR: Printer device /dev/usb/lp0 not found"
    exit 1
fi

if [ ! -w "/dev/usb/lp0" ]; then
    echo "ERROR: No write permission to printer device"
    echo "Fixing permissions..."
    sudo chmod 666 /dev/usb/lp0
fi

if ! python3 -c "import flask" 2>/dev/null; then
    echo "Installing Flask..."
    pip3 install flask
fi

echo "Starting print server..."
python3 test_printer.py &


echo "Testing print server..."
curl -v "http://localhost:5001/print?date=2025-04-02&name=TEST&total=10.00&cashier=Test&orderline=1,Test%20Product,10.00"

echo "Print server setup complete"
