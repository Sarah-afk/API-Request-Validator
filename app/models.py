from . import db

class Customer(db.Model):
    __tablename__ = "customer"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    active = db.Column(db.Boolean, default=True)
    hourly_stats_customer_id = db.relationship("HourlyStats", lazy = "dynamic", passive_deletes=True)

class IPBlacklist(db.Model):
    __tablename__ = "ip_blacklist"
    ip = db.Column(db.Integer, primary_key=True)


class UABlacklist(db.Model):
    __tablename__ = "ua_blacklist"
    ua = db.Column(db.String(255), primary_key=True)


class HourlyStats(db.Model):
    __tablename__ = "hourly_stats"
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id", ondelete='CASCADE'))
    time = db.Column(db.BigInteger)
    request_count = db.Column(db.BigInteger, default=0)
    invalid_count = db.Column(db.BigInteger, default=0)

    db.UniqueConstraint(customer_id, time)

def initalize_db():
    if(not db.engine.dialect.has_table(db.engine, 'customer')):
        db.create_all()
        c1 = Customer(id=1, name='Big News Media Corp', active = True)
        c2 = Customer(id=2, name='Online Mega Store', active = True)
        c3 = Customer(id=3, name='Nachoroo Delivery', active = False)
        c4 = Customer(id=4, name='Euro Telecom Group', active = True)
        db.session.add_all([c1, c2, c3, c4])
        
        ip1 = IPBlacklist(ip = 0)
        ip2 = IPBlacklist(ip = 2130706433)
        ip3 = IPBlacklist(ip = 4294967295)
        db.session.add_all([ip1, ip2, ip3])

        ua1 = UABlacklist(ua = 'A6-Indexer')
        ua2 = UABlacklist(ua = 'Googlebot-News')
        ua3 = UABlacklist(ua = 'Googlebot')
        db.session.add_all([ua1, ua2, ua3])
        
        db.session.commit()