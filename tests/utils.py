# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import signals


def signals_switch():
    pre_save = signals.pre_save.receivers
    post_save = signals.post_save.receivers
    post_migrate = signals.post_migrate.receivers

    def disconnect():
        signals.pre_save.receivers = []
        signals.post_save.receivers = []
        signals.post_migrate.receivers = []

    def reconnect():
        signals.pre_save.receivers = pre_save
        signals.post_save.receivers = post_save
        signals.post_migrate.receivers = post_migrate

    return disconnect, reconnect


disconnect_signals, reconnect_signals = signals_switch()
