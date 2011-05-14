
import mongoengine as db

import user


class Follow(db.Document):
    meta = {'collection': 'Follow'}
    
    #account_id = db.StringField() #TODO: the identifier to the account
    status = db.StringField() # Limited to: break, run, interrupt
    #round_ = db. #TODO: Ref to the current round
    user = db.ReferenceField(user.User)
    target = db.GenericReferenceField()
    #target_class = db.StringField() #TODO: for filtering

