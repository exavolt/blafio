
from datetime import datetime
import logging

import core.subscription
import core.stream


def publish(publisher, activity, publish_datetime=None):
    #TODO: all other parameters (e.g.: priority, context, datetime, ...)
    #TODO: Check whether the activity is already published or not
    # Publisher's profile stream
    stx = core.stream.Stream.objects(owner=publisher, context='self').first()
    if not stx:
        stx = core.stream.Stream(owner=publisher, context='self').save()
    sti = core.stream.StreamItem(
        stream=stx,
        publisher=publisher,
        activity=activity,
        publish_datetime=publish_datetime
        )
    sti.save()
    # Publisher's home stream
    stx = core.stream.Stream.objects(owner=publisher, context='home').first()
    if not stx:
        stx = core.stream.Stream(owner=publisher, context='home').save()
    sti = core.stream.StreamItem(
        stream=stx,
        publisher=publisher,
        activity=activity,
        publish_datetime=publish_datetime
        )
    sti.save()
    #TODO: wisely use the processing resources to broadcast
    for pubsub in core.subscription.Subscription.objects(publisher=publisher, active=True):
        #TODO: skip self
        stx = core.stream.Stream.objects(owner=pubsub.subscriber, context='home').first()
        if not stx:
            stx = core.stream.Stream(owner=pubsub.subscriber, context='home').save()
        sti = core.stream.StreamItem(
            stream=stx,
            publisher=publisher,
            activity=activity,
            publish_datetime=publish_datetime
            )
        sti.save()
    

def unpublish(publisher, activity):
    # Publisher's profile stream
    stx = core.stream.Stream.objects(owner=publisher, context='self').first()
    if not stx:
        stx = core.stream.Stream(owner=publisher, context='self').save()
    sti = core.stream.StreamItem(stream=stx, publisher=publisher, activity=activity).first()
    if sti:
        sti.deleted = True
        sti.save()
    # Publisher's home stream
    stx = core.stream.Stream.objects(owner=publisher, context='home').first()
    if not stx:
        stx = core.stream.Stream(owner=publisher, context='home').save()
    sti = core.stream.StreamItem(stream=stx, publisher=publisher, activity=activity).first()
    if sti:
        sti.deleted = True
        sti.save()
    #TODO: wisely use the processing resources to broadcast
    for pubsub in core.subscription.Subscription.objects(publisher=publisher, active=True):
        #TODO: skip self
        stx = core.stream.Stream.objects(owner=pubsub.subscriber, context='home').first()
        if not stx:
            stx = core.stream.Stream(owner=pubsub.subscriber, context='home').save()
        sti = core.stream.StreamItem(stream=stx, publisher=publisher, activity=activity).first()
        if sti:
            sti.deleted = True
            sti.save()
    

def subscribe(actor, publisher):
    #TODO: What will happen here is that the actor will get old entries 
    # from the publisher in his stream.
    # Get the publisher's 'self' stream
    stxp = core.stream.Stream.objects(owner=publisher, context='self').first()
    if not stxp:
        stxp = core.stream.Stream(owner=publisher, context='self').save()
    # Get subscriber's 'home' stream
    stxs = core.stream.Stream.objects(owner=actor, context='home').first()
    if not stxs:
        stxs = core.stream.Stream(owner=actor, context='home').save()
    #TODO: get all entries (latest first, older gets lower processing priority)
    query = core.stream.StreamItem.objects(stream=stxp, 
        publisher=publisher).order_by('-msglogtimestamp')[:20]
    for stip in query:
        stis = core.stream.StreamItem(
            stream=stxs,
            publisher=publisher,
            activity=stip.activity,
            publish_datetime=stip.publish_datetime
            )
        stis.save()
    

def unsubscribe(actor, publisher):
    #TODO: What will happen here is that the publisher's entries will be 
    # removed from the actor's stream.
    #TODO: From all streams (contexts)
    stx = core.stream.Stream.objects(owner=actor, context='home').first()
    if not stx:
        stx = core.stream.Stream(owner=actor, context='home').save()
    #TODO: get all entries (latest first, older gets lower processing priority)
    query = core.stream.StreamItem.objects(stream=stx, 
        publisher=publisher).order_by('-msglogtimestamp')[:20]
    for sti in query:
        sti.deleted = True
        sti.save()
    


