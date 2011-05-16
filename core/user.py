# User profile

import mongoengine as db


def normalize_name(strname):
    return strname.strip().lower()


class User(db.Document):
    meta = {'collection': 'User'}
    
    #account_id = db.StringField() #TODO: the identifier to the account
    name = db.StringField() # Display name
    idname = db.StringField() # Normalized name
    #status = db.StringField() # Limited to: break, run, interrupt
    #round_ = db. #TODO: Ref to the current round
    
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

