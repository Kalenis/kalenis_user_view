# This file is part of kalenis_user_view module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.model import fields
from trytond.pool import PoolMeta


class Lang(metaclass=PoolMeta):
    __name__ = 'ir.lang'

    time = fields.Char('Time')
