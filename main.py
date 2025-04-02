#!/usr/bin/env python3
from flask import Flask, request, jsonify
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = app.logger

@app.route('/print')
def print_receipt():
    try:
        date = request.args.get('date', '')
        name = request.args.get('name', '')
        total = request.args.get('total', '0.00')
        cashier = request.args.get('cashier', '')
        orderlines = request.args.getlist('orderline')

        logger.info(f"Printing receipt: {name}")
        
        with open('/dev/usb/lp0', 'wb') as printer:
            printer.write(b'\x1B\x40')  
            printer.write(b'\x1B\x61\x01') 
            
            printer.write(b'TEXT to print\n')

            
            for line in orderlines:
                qty, product, price = line.split(',')
                line_text = f"{qty}x {product} {price}\n"
                printer.write(line_text.encode('utf-8'))
            
            printer.write(b'--------------------\n')
            printer.write(f"TOTAL: {total}\n".encode('utf-8'))
            
            printer.write(b'\n\n\n')
            printer.write(b'\x1D\x56\x00')
            printer.flush()
            
            return jsonify({"status": "success"}), 200
            
    except Exception as e:
        logger.error(f"Print error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 
