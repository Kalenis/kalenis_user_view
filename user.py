from trytond.pool import PoolMeta
from trytond.model import fields

__all__ = ['User']


class User(metaclass=PoolMeta):
    __name__ = 'res.user'

    list_view_style = fields.Selection([
        ('', ''),
        ('comfortable', 'Comfortable'),
        ('compact', 'Compact'),
        ], 'List View Style')

    @classmethod
    def __setup__(cls):
        super(User, cls).__setup__()
        cls._context_fields.insert(0, 'list_view_style')
