
import mongoengine as db

import user


class Subscription(db.Document):
    meta = {'collection': 'Subscription'}
    
    subscriber = db.ReferenceField(user.User)
    publisher = db.GenericReferenceField()
    #publiser_class = db.StringField() #TODO: for filtering
    active = db.BooleanField(default=False) # Master flag
    pending = db.BooleanField(default=False) # Approval required

