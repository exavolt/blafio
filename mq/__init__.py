
import logging

import core.subscription
import core.stream


def publish(publisher, item):
    logging.warn("Pubsub publish " + publisher.name)
    #TODO: all other parameters (e.g.: priority, context, datetime, ...)
    #TODO: wisely broadcast
    for pubsub in core.subscription.Subscription.objects(publisher=publisher, active=True):
        stx = core.stream.Stream.objects(owner=pubsub.subscriber).first()
        #HACK-begin
        if not stx:
            stx = core.stream.Stream(
                owner=pubsub.subscriber,
                context='main'
                )
            stx.save()
        #HACK-end
        sti = core.stream.StreamItem(
            stream=stx,
            publisher=publisher,
            object=item
            )
        sti.save()

def unpublish(item):
    pass

