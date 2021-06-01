from trytond.model import fields
from trytond.pool import  PoolMeta

class Lang(metaclass=PoolMeta):
    __name__ = 'ir.lang'

    time = fields.Char('Time')
