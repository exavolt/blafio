#!/usr/bin/env python

import mongoengine as db


class Subscription(db.Document):
    meta = {'collection': 'blafio_Subscription'}
    
    subscriber = db.GenericReferenceField()
    publisher = db.GenericReferenceField()
    #publiser_class = db.StringField() #TODO: for filtering
    active = db.BooleanField(default=False) # Master flag
    pending = db.BooleanField(default=False) # Approval required
    #TODO: subscription type, subscribed items, generic subscriber?
    
    def prep_dump(self, details=2):
        return dict(
            subscriber=self.subscriber.prep_dump(1),
            publisher=self.publisher.prep_dump(1),
            active=self.active,
            pending=self.pending
            )
    

