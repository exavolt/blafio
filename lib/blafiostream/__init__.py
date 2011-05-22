#!/usr/bin/env python

import mongoengine as db


class Stream(db.Document):
    meta = {'collection': 'blafiostream_Stream'}
    
    owner = db.GenericReferenceField()
    context = db.StringField()
    publishing = db.BooleanField(default=False)
    
    def prep_dump(self, details=2):
        return dict(
            owner=self.owner.prep_dump(details=1),
            context=self.context,
            publishing=self.publishing
            )
    

class StreamItem(db.Document):
    meta = {'collection': 'blafiostream_StreamItem'}
    
    stream = db.ReferenceField(Stream)
    publisher = db.GenericReferenceField()
    activity = db.GenericReferenceField()
    published_datetime = db.DateTimeField()
    deleted = db.BooleanField(default=False)
    #TODO: extended data for self (privacy, delete datetime)
    
    def prep_dump(self, details=2):
        #TODO: the stream item or the object?
        return self.activity.prep_dump(details=details)
    
    def to_activity_stream_item_dict(self, details=2):
        return self.activity.to_activity_stream_item_dict(details=details)
    

