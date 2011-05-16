
import mongoengine as db

import app
import user


class Round(db.Document):
    meta = {'collection': 'Round'}
    
    user = db.ReferenceField(user.User)
    name = db.StringField() # The name of the round (could be taken from the tasks)
    
    def prep_dump(self, details=2):
        if details == 1:
            return dict(
                id=str(self.id),
                name=self.name
                )
        return dict(
            id=str(self.id),
            name=self.name,
            user=self.user.prep_dump(details=2)
            )
    

class RoundActivity(db.Document):
    meta = {'collection': 'RoundActivity'}
    
    actor = db.ReferenceField(user.User) # Dupe from the Round
    round_ = db.ReferenceField(Round)
    action = db.StringField() # Limited to: start, reset, finish, interrupt, resume
    timestamp = db.DateTimeField()
    app = db.ReferenceField(app.App)
    #TODO: private? context? tasks
    
    def prep_dump(self, details=2):
        return dict(
            id=str(self.id),
            actor=self.actor.prep_dump(details=1),
            action=self.action,
            round=self.round_.prep_dump(details=1),
            timestamp=self.timestamp.isoformat(),
            tasks=dict(count=0, data=[]),
            application=self.app.prep_dump(details=1) if self.app else {}
            )
    

ACTIONS = [
    'start',
    'reset', # Bail out
    'finish', # Time out
    'interrupt', 
    'resume'
    ]


