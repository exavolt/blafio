# Stream

import mongoengine as db

import user


class Stream(db.Document):
    meta = {'collection': 'Stream'}
    
    owner = db.ReferenceField(user.User)
    context = db.StringField()
    publishing = db.BooleanField(default=False)
    
    def prep_dump(self, details=2):
        pass
    

class StreamItem(db.Document):
    meta = {'collection': 'StreamItem'}
    
    stream = db.ReferenceField(Stream)
    publisher = db.ReferenceField(user.User) #TODO: generic
    activity = db.GenericReferenceField()
    publish_datetime = db.DateTimeField()
    deleted = db.BooleanField(default=False)
    #TODO: extended data for self (privacy, delete datetime)
    
    def prep_dump(self, details=2):
        #TODO: the stream item or the object?
        return self.activity.prep_dump(details=details)
    
    def to_activity_stream_item_dict(self, details=2):
        return self.activity.to_activity_stream_item_dict(details=details)
    

