# This file is part of kalenis_user_view module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.pool import Pool
from . import user_view
from . import user
# from . import table


def register():
    Pool.register(
        user_view.UserView,
        user_view.UserViewField,
        user.User,
        module='user_view', type_='model')
