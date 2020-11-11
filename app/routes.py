from . import app, db
from .models import *
from .forms import *
from .queries import *
from flask import request, jsonify
from datetime import datetime, timedelta
import socket
import struct

@app.route('/validate', methods=['POST'])
def validate():
    form = ValidateJSONForm(request.form)
    if form.validate():
        #Remove minutes, seconds and milliseconds from timestamp
        timestamp = form.timestamp.data - (form.timestamp.data % 3600)
        remoteIP = ip2int(form.remoteIP.data)
        user_agent = request.headers.get('User-Agent')

        #Check if Customer exists
        customer = get_customer(form.customerID.data)
        if customer is None:
            return 'Customer does not exist', 404
        
        #Check if Customer is disabled
        if not customer.active:
            add_invalid_count(customer.id, timestamp)
            return 'Customer is inactive', 401

        #Check if IP is blocked
        if ip_is_blocked(remoteIP):
            add_invalid_count(customer.id, timestamp)
            return 'IP is blocked', 401

        #Check if User is blocked
        if ua_is_blocked(user_agent):
            add_invalid_count(customer.id, timestamp)
            return 'User-Agent is blocked', 401

        add_valid_count(customer.id, timestamp)
        stub_function(form.data)

        return 'Processing Done'

    return 'Invalid Request', 400

@app.route('/getStats', methods=['GET', 'POST'])
def getStats():
    form = StatsForm(request.form)
    if form.validate():
        date = form.day.data
        startdate = date.timestamp()
        enddate = (date + timedelta(days=1)).timestamp()
 
        #Check if Customer exists
        customer = get_customer(form.customerID.data)
        if customer is None:
            return 'Customer does not exist', 404
 
        customer_stats = get_customer_stats(startdate, enddate, customer.id)[0]
        daily_stats = get_daily_stats(startdate, enddate)[0]

        return jsonify({
                            'customer': {
                                'id': customer.id,
                                'request_count': customer_stats[0] if customer_stats[0] is not None else 0,
                                'invalid_count': customer_stats[1] if customer_stats[1] is not None else 0,
                            },
                            'daily_stats_total': daily_stats[0] if daily_stats[0] is not None else 0
                        })

    return 'Invalid Request', 400

def ip2int(addr):
    return struct.unpack("!I", socket.inet_aton(addr))[0]

def int2ip(addr):
    return socket.inet_ntoa(struct.pack("!I", addr))

def stub_function(data):
    app.logger.info(data)
    pass
