# This file is part of kalenis_user_view module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.pool import PoolMeta
from trytond.pyson import PYSONDecoder
from trytond.transaction import Transaction


class ViewSearch(metaclass=PoolMeta):
    __name__ = 'ir.ui.view_search'

    @classmethod
    def get_search(cls, user_id=None):
        if user_id is None:
            user_id = Transaction().user
        decoder = PYSONDecoder()
        searches = cls.search(['OR',
            ('user', '=', user_id),
            ('user', '=', None),
            ], order=[('model', 'ASC'), ('name', 'ASC')])
        result = {}
        for search in searches:
            result.setdefault(search.model, []).append(
                (search.id, search.name, decoder.decode(search.domain)))
        return result
