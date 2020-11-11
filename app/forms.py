from wtforms import Form, StringField, validators, IntegerField, DateTimeField

class ValidateJSONForm(Form):
    customerID = IntegerField('customerID', validators=[validators.Required()])
    tagID = IntegerField('tagID', validators=[validators.Required()])
    userID = StringField('userID', validators=[validators.Required()])
    #in the following we are validating the IP. Based on the given example, and since in the 
    #database the IP is an ineteger, we assumed that only ipv4 is valid
    remoteIP = StringField('remoteIP', validators=[validators.IPAddress(ipv4=True, ipv6=False),
                                                    validators.Required()])
    timestamp = IntegerField('timestamp', validators=[validators.Required()])

class StatsForm(Form):
    customerID = IntegerField('customerID', validators=[validators.Required()])
    day = DateTimeField('day', format='%d/%m/%Y', validators=[validators.Required()])