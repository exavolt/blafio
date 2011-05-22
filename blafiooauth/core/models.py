#!/usr/bin/env python

import mongoengine as db

import blafiocore.user


def normalize_name(strname):
    return strname.strip().lower()


class Client(db.Document):
    meta = {'collection': 'blafiooauth_Client'}
    
    name = db.StringField() # Display name
    idname = db.StringField() # Normalized name
    #key_ = db.StringField() # Client's key (use only ID?)
    secret = db.StringField()
    #TODO: client kind (internal, 3rd-party, ...)
    #TODO: ACL
    #TODO: creator
    
    def prep_dump(self, details=2):
        if details == 1:
            return dict(
                id=str(self.id),
                name=self.name
                )
        return dict(
            id=str(self.id),
            name=self.name,
            idname=self.idname
            )
    

class Access(db.Document):
    meta = {'collection': 'blafiooauth_Access'}
    
    token = db.StringField()
    client = db.ReferenceField(Client)
    user = db.ReferenceField(blafiocore.user.User)
    #TODO: expiration, resources
    
    def prep_dump(self, details=2):
        if details == 1:
            return dict(
                token=self.token
                )
        return dict(
            token=self.token,
            client=self.client.prep_dump(details=1),
            user=self.user.prep_dump(details=1)
            )
    

