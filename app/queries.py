from . import app, db
from .models import *
from sqlalchemy import func

def get_customer(customerID):
    return Customer.query.filter(Customer.id == customerID).first()

def ip_is_blocked(remoteIP):
    ip = IPBlacklist.query.filter(IPBlacklist.ip == remoteIP).first()
    return (ip is not None)

def ua_is_blocked(name):
    ua = UABlacklist.query.filter(UABlacklist.ua == name).first()
    return (ua is not None)

def add_invalid_count(customerID, timestamp):
    hourly_stats = HourlyStats.query.filter(HourlyStats.customer_id == customerID, HourlyStats.time == timestamp).first()
    if hourly_stats is None:
        hourly_stats = HourlyStats(customer_id=customerID,
                                    time=timestamp,
                                    invalid_count=1)
        db.session.add(hourly_stats)
    else:
        hourly_stats.invalid_count += 1
    
    db.session.commit()
    
def add_valid_count(customerID, timestamp):
    hourly_stats = HourlyStats.query.filter(HourlyStats.customer_id == customerID, HourlyStats.time == timestamp).first()
    if hourly_stats is None:
        hourly_stats = HourlyStats(customer_id=customerID,
                                    time=timestamp,
                                    request_count=1)
        db.session.add(hourly_stats)
    else:
        hourly_stats.request_count += 1
    
    db.session.commit()

def get_customer_stats(startdate, enddate, customerID):
    return HourlyStats.query.with_entities(
                                        func.sum(HourlyStats.request_count).label('request_count'),
                                        func.sum(HourlyStats.invalid_count).label('invalid_count')
                                    ).filter(
                                        HourlyStats.time >= startdate,
                                        HourlyStats.time < enddate,
                                        HourlyStats.customer_id == customerID
                                    ).all()

def get_daily_stats(startdate, enddate):
    return HourlyStats.query.with_entities(
                                        func.sum(HourlyStats.request_count + HourlyStats.invalid_count).label('count'),
                                    ).filter(
                                        HourlyStats.time >= startdate,
                                        HourlyStats.time < enddate
                                    ).all()