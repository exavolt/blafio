# Stream

import mongoengine as db

import user
import round_


class Stream(db.Document):
    meta = {'collection': 'Stream'}
    
    owner = db.ReferenceField(user.User)
    context = db.StringField()
    
    def prep_dump(self, details=2):
        pass
    

class StreamItem(db.Document):
    meta = {'collection': 'StreamItem'}
    
    stream = db.ReferenceField(Stream)
    publisher = db.ReferenceField(user.User) #TODO: generic
    object = db.ReferenceField(round_.RoundActivity)
    deleted = db.BooleanField(default=False)

