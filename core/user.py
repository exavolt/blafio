# User profile

import mongoengine as db


class User(db.Document):
    meta = {'collection': 'User'}
    
    #account_id = db.StringField() #TODO: the identifier to the account
    status = db.StringField() # Limited to: break, run, interrupt
    #round_ = db. #TODO: Ref to the current round

