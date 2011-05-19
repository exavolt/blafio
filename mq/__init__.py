
from datetime import datetime
import logging

import core.subscription
import core.stream


def publish(publisher, item, published_datetime=None):
    #TODO: all other parameters (e.g.: priority, context, datetime, ...)
    logging.warn("Pubsub publish " + publisher.name)
    #TODO: Check whether the item is already published or not (look into 
    # global stream)
    if not published_datetime:
        published_datetime = datetime.utcnow()
    sti = core.stream.StreamItem(
        stream=None,
        publisher=publisher,
        object=item,
        published_datetime=published_datetime
        )
    sti.save()
    #TODO: to self
    stx = core.stream.Stream.objects(owner=publisher).first()
    #HACK-begin
    if not stx:
        stx = core.stream.Stream(
            owner=publisher,
            context='main'
            )
        stx.save()
    #HACK-end
    sti = core.stream.StreamItem(
        stream=stx,
        publisher=publisher,
        object=item,
        published_datetime=published_datetime
        )
    sti.save()
    #TODO: wisely broadcast
    for pubsub in core.subscription.Subscription.objects(publisher=publisher, active=True):
        #TODO: skip self
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
            object=item,
            published_datetime=published_datetime
            )
        sti.save()


def unpublish(item):
    pass


def subscribe(actor, publisher):
    #TODO: What will happen here is that the actor will get old items 
    # from the publisher in his stream.
    stxp = core.stream.Stream.objects(owner=publisher).first()
    #HACK-begin
    if not stxp:
        stxp = core.stream.Stream(
            owner=actor,
            context='main'
            )
        stxp.save()
    #HACK-end
    stxs = core.stream.Stream.objects(owner=actor).first()
    #HACK-begin
    if not stxs:
        stxs = core.stream.Stream(
            owner=actor,
            context='main'
            )
        stxs.save()
    #HACK-end
    #TODO: get all items (latest first, older gets lower processing priority)
    query = core.stream.StreamItem.objects(stream=stxp, publisher=publisher).order_by('-published_timestamp')[:20]
    for stip in query:
        stis = core.stream.StreamItem(
            stream=stxs,
            publisher=publisher,
            object=stip.object,
            published_datetime=stip.published_datetime
            )
        stis.save()


def unsubscribe(actor, publisher):
    #TODO: What will happen here is that the publisher's items will be 
    # removed from the actor's stream.
    stx = core.stream.Stream.objects(owner=actor).first()
    #HACK-begin
    if not stx:
        stx = core.stream.Stream(
            owner=actor,
            context='main'
            )
        stx.save()
    #HACK-end
    #TODO: get all items (latest first, older gets lower processing priority)
    query = core.stream.StreamItem.objects(stream=stx, publisher=publisher).order_by('-published_timestamp')[:20]
    for sti in query:
        sti.deleted = True
        sti.save()
    


