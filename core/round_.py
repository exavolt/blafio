
import mongoengine as db

import user


class Round(db.Document):
    meta = {'collection': 'Round'}
    
    user = db.ReferenceField(user.User)
    name = db.StringField() # The name of the round (could be taken from the tasks)
    
    def prep_json(self):
        return dict(
            id=str(self.id),
            name=self.name
            )


class RoundActivity(db.Document):
    meta = {'collection': 'RoundActivity'}
    
    round_ = db.ReferenceField(Round)
    action = db.StringField() # Limited to: start, reset, finish, interrupt, resume
    timestamp = db.DateTimeField()
    #TODO: private? context? tasks
    
    def prep_json(self):
        return dict(
            id=str(self.id),
            action=self.action,
            round=self.round_.prep_json(),
            timestamp=self.timestamp.isoformat(),
            tasks=[]
            )


ACTIVITIES = [
    'start',
    'reset', # Bail out
    'finish', # Time out
    'interrupt', 
    'resume'
    ]


