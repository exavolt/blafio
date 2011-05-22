
import server


class Processor(object):
    """Stateless stream processor client class.
    """
    
    def __init__(self):
        pass
    
    def _connect(self):
        #TODO: make a connection to the stream processor server
        pass
    
    def publish(publisher, activity):
        #TODO: send the items to the server
        server.publish(publisher, activity)
    
    def unpublish(publisher, activity):
        #TODO: send the items to the server
        server.unpublish(publisher, activity)
    
    def subscribe(actor, publisher):
        #TODO: send the items to the server
        server.subscribe(actor, publisher)
    
    def unsubscribe(actor, publisher):
        #TODO: send the itemns to the serve
        server.unsubscribe(actor, publisher)
    

