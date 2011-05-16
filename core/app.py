# App

import mongoengine as db

import user


def normalize_name(strname):
    return strname.strip().lower()


class App(db.Document):
    meta = {'collection': 'App'}
    
    name = db.StringField() # Display name
    idname = db.StringField() # Normalized name
    #key_ = db.StringField() # App's key (use only ID?)
    secret = db.StringField()
    #TODO: app kind (internal, 3rd-party, ...)
    
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
    

class AppAccess(db.Document):
    meta = {'collection': 'AppAccess'}
    
    token = db.StringField()
    app = db.ReferenceField(App)
    user = db.ReferenceField(user.User)
    #TODO: expiration, resources
    
    def prep_dump(self, details=2):
        if details == 1:
            return dict(
                token=self.token
                )
        return dict(
            token=self.token,
            app=self.app.prep_dump(details=1),
            user=self.user.prep_dump(details=1)
            )

