# This file is part of lims_result_warning module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.pool import Pool
from . import user_view
# from . import table


def register():
    Pool.register(
        user_view.UserView,
        user_view.UserViewField,
        module='user_view', type_='model')
    
