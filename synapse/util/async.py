# -*- coding: utf-8 -*-
# Copyright 2014, 2015 OpenMarket Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from twisted.internet import defer, reactor

from .logcontext import PreserveLoggingContext


@defer.inlineCallbacks
def sleep(seconds):
    d = defer.Deferred()
    reactor.callLater(seconds, d.callback, seconds)
    with PreserveLoggingContext():
        yield d


def run_on_reactor():
    """ This will cause the rest of the function to be invoked upon the next
    iteration of the main loop
    """
    return sleep(0)


def create_observer(deferred):
    """Creates a deferred that observes the result or failure of the given
     deferred *without* affecting the given deferred.
    """
    d = defer.Deferred()

    def callback(r):
        d.callback(r)
        return r

    def errback(f):
        d.errback(f)
        return f

    deferred.addCallbacks(callback, errback)

    return d
