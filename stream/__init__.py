
from datetime import datetime
import logging

import core.pubsub
import core.stream


def publish(publisher, activity):
    #TODO: all other parameters (e.g.: priority, context, datetime, ...)
    #TODO: Check whether the activity is already published or not
    act_data = activity.to_activity_stream_item_dict(details=3)
    published_datetime = act_data.get('published_datetime', None)
    if not published_datetime:
        published_datetime = datetime.utcnow()
    # Publisher's profile stream
    stx = core.stream.Stream.objects(owner=publisher, publishing=True, context='general').first()
    if not stx:
        stx = core.stream.Stream(owner=publisher, publishing=True, context='general')
        stx.save()
    sti = core.stream.StreamItem(
        stream=stx,
        publisher=publisher,
        activity=activity,
        published_datetime=published_datetime
        )
    sti.save()
    # Publisher's home stream
    stx = core.stream.Stream.objects(owner=publisher, publishing=False, context='public').first()
    if not stx:
        stx = core.stream.Stream(owner=publisher, publishing=False, context='public')
        stx.save()
    sti = core.stream.StreamItem(
        stream=stx,
        publisher=publisher,
        activity=activity,
        published_datetime=published_datetime
        )
    sti.save()
    #TODO: wisely use the processing resources to broadcast
    for pubsub in core.pubsub.Subscription.objects(publisher=publisher, active=True):
        #TODO: skip self
        stx = core.stream.Stream.objects(owner=pubsub.subscriber, publishing=False, context='public').first()
        if not stx:
            stx = core.stream.Stream(owner=pubsub.subscriber, publishing=False, context='public')
            stx.save()
        sti = core.stream.StreamItem(
            stream=stx,
            publisher=publisher,
            activity=activity,
            published_datetime=published_datetime
            )
        sti.save()
    

def unpublish(publisher, activity):
    # Publisher's profile stream
    stx = core.stream.Stream.objects(owner=publisher, publishing=True, context='general').first()
    if not stx:
        stx = core.stream.Stream(owner=publisher, publishing=True, context='general')
        stx.save()
    sti = core.stream.StreamItem(stream=stx, publisher=publisher, activity=activity).first()
    if sti:
        sti.deleted = True
        sti.save()
    # Publisher's home stream
    stx = core.stream.Stream.objects(owner=publisher, publishing=False, context='public').first()
    if not stx:
        stx = core.stream.Stream(owner=publisher, publishing=False, context='public')
        stx.save()
    sti = core.stream.StreamItem(stream=stx, publisher=publisher, activity=activity).first()
    if sti:
        sti.deleted = True
        sti.save()
    #TODO: wisely use the processing resources to broadcast
    for pubsub in core.pubsub.Subscription.objects(publisher=publisher, active=True):
        #TODO: skip self
        stx = core.stream.Stream.objects(owner=pubsub.subscriber, publishing=False, context='public').first()
        if not stx:
            stx = core.stream.Stream(owner=pubsub.subscriber, publishing=False, context='public')
            stx.save()
        sti = core.stream.StreamItem(stream=stx, publisher=publisher, activity=activity).first()
        if sti:
            sti.deleted = True
            sti.save()
    

def subscribe(actor, publisher):
    #TODO: What will happen here is that the actor will get old entries 
    # from the publisher in his stream.
    # Get the publisher's 'self' stream
    stxp = core.stream.Stream.objects(owner=publisher, publishing=True, context='general').first()
    if not stxp:
        stxp = core.stream.Stream(owner=publisher, publishing=True, context='general')
        stxp.save()
    # Get subscriber's 'home' stream
    stxs = core.stream.Stream.objects(owner=actor, publishing=False, context='public').first()
    if not stxs:
        stxs = core.stream.Stream(owner=actor, publishing=False, context='public')
        stxs.save()
    #TODO: get all entries (latest first, older gets lower processing priority)
    query = core.stream.StreamItem.objects(stream=stxp, 
        publisher=publisher).order_by('-published_datetime')[:20]
    for stip in query:
        stis = core.stream.StreamItem(
            stream=stxs,
            publisher=publisher,
            activity=stip.activity,
            published_datetime=stip.published_datetime
            )
        stis.save()
    

def unsubscribe(actor, publisher):
    #TODO: What will happen here is that the publisher's entries will be 
    # removed from the actor's stream.
    #TODO: From all streams (contexts)
    stx = core.stream.Stream.objects(owner=actor, publishing=False, context='public').first()
    if not stx:
        stx = core.stream.Stream(owner=actor, publishing=False, context='public')
        stx.save()
    #TODO: get all entries (latest first, older gets lower processing priority)
    query = core.stream.StreamItem.objects(stream=stx, 
        publisher=publisher).order_by('-published_datetime')[:20]
    for sti in query:
        sti.deleted = True
        sti.save()
    


