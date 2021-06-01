from trytond.pool import PoolMeta, Pool
from trytond.model import fields
from ast import literal_eval
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

    # @classmethod
    # def _get_preferences(cls, user, context_only=False):
    #     pool = Pool()
    #     ModelData = pool.get('ir.model.data')
    #     Action = pool.get('ir.action')
    #     Config = pool.get('ir.configuration')
    #     ConfigItem = pool.get('ir.module.config_wizard.item')

    #     res = {}
    #     if context_only:
    #         fields = cls._context_fields
    #     else:
    #         fields = cls._preferences_fields + cls._context_fields
    #     for field in fields:
    #         if cls._fields[field]._type in ('many2one',):
    #             if field == 'language':
    #                 if user.language:
    #                     res['language'] = user.language.code
    #                 else:
    #                     res['language'] = Config.get_language()
    #             else:
    #                 res[field] = None
    #                 if getattr(user, field):
    #                     res[field] = getattr(user, field).id
    #                     res[field + '.rec_name'] = \
    #                         getattr(user, field).rec_name
    #         elif cls._fields[field]._type in ('one2many', 'many2many'):
    #             res[field] = [x.id for x in getattr(user, field)]
    #             if field == 'actions' and user.login == 'admin':
    #                 config_wizard_id = ModelData.get_id('ir',
    #                                                     'act_module_config_wizard')
    #                 action_id = Action.get_action_id(config_wizard_id)
    #                 if action_id in res[field]:
    #                     res[field].remove(action_id)
    #                 if ConfigItem.search([
    #                     ('state', '=', 'open'),
    #                 ]):
    #                     res[field].insert(0, action_id)
    #         else:
    #             res[field] = getattr(user, field)

    #     if user.language:
    #         date = user.language.date
    #         time = user.language.time
    #         for i, j in [('%a', ''), ('%A', ''), ('%b', '%m'), ('%B', '%m'),
    #                      ('%j', ''), ('%U', ''), ('%w', ''), ('%W', '')]:
    #             date = date.replace(i, j)
    #         res['locale'] = {
    #             'date': date,
    #             'time':time,
    #             'grouping': literal_eval(user.language.grouping),
    #             'decimal_point': user.language.decimal_point,
    #             'thousands_sep': user.language.thousands_sep,
    #         }
    #     return res
    
    @classmethod
    def _get_preferences(cls, user, context_only=False):
        res = super()._get_preferences(user,context_only)
        if user.language:
            res['locale']['time'] = user.language.time
        return res