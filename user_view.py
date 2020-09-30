# This file is part of kalenis_user_view module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.model import ModelView, ModelSQL, fields, Unique, sequence_ordered
from trytond.pyson import PYSONEncoder, Eval, Equal, Bool, Not, Or, And
from trytond.pool import Pool, PoolMeta
from trytond.wizard import (Wizard, StateTransition, StateView, StateAction,
    Button)
from trytond.transaction import Transaction
from trytond.rpc import RPC

__all__ = ['UserView', 'UserViewField']


class UserView(ModelSQL, ModelView):
    'User View'
    __name__ = 'user.view'

    name = fields.Char('View Name')
    default = fields.Boolean('Default view')
    user = fields.Many2One('res.user', 'User')
    view_model = fields.Many2One('ir.model', 'View Model')
    view = fields.Many2One('ir.ui.view', 'View')
    global_available = fields.Boolean('Available to all users')
    compact = fields.Boolean('Compact List')
    current_search = fields.Char('Search')
    order = fields.Char('Order')
    # field_name its used to id o2many fields views
    field_name = fields.Char('Field Name')
    #field_model: field_name model
    field_model = fields.Many2One('ir.model', 'Field Model')
    user_view_fields = fields.One2Many('user.view.field', 'user_view', 'Fields')


    @classmethod
    def __setup__(cls):
        super(UserView, cls).__setup__()
        cls.__rpc__['user_views_get'] = RPC(cache=dict(days=1))
        cls.__rpc__['user_view_fields_get'] = RPC(cache=dict(days=1))
        cls.__rpc__['user_view_set'] = RPC(readonly=False)
        cls.__rpc__['user_view_set_default_view'] = RPC(readonly=False)
        
    
    
    @classmethod
    def user_views_get(cls, user_id=None, view_id=None, field=False):
        '''
        Return list of user views.
        
        '''
        res = []
        domain = []
        pool = Pool()
        if field == False:
            if not user_id or not view_id:
                return res
            domain = [('user','=',user_id), ('view','=',view_id)]
        else:
            domain = [('user','=',user_id), 
                        ('field_name','=',field['name']), 
                        ('view_model.model','=',field['relation']),
                        ('field_model.model', '=', field['model'])
                        ]
        
        
        views = pool.get('user.view').search(domain)

        
        if len(views) > 0:
            res = [{'id':view.id, 
                    'rec_name':view.name, 
                    'default':view.default, 
                    'compact':view.compact,
                    'search':view.current_search, 
                    'order':view.order,
                    'global_available':view.global_available,
                    'field_name':view.field_name,
                    'model':view.view_model.model,
                    } 
                        for view in views]
        
         
        
        
        return res



    
    @classmethod
    def user_view_fields_get(cls, view_id=None):
        '''
        Return list of fields of user_view
        
        '''
        res = []
        if not view_id:
            return res
        
        pool = Pool()
        domain = [('user_view','=',view_id)]
        
        fields = pool.get('user.view.field').search(domain)
        View = pool.get('user.view')

        view = View(view_id)
        Model = pool.get(view.view_model.model)
        
        field_descriptions = Model.fields_get([field.field.name for field in fields if field.type != 'button'])
        
        
        
        def get_widget(field):
            if field.field_widget:
                return field.field_widget
            else:
                return field.field.ttype
        
        def get_type(field):
            if field.type:
                return field.type
            else:
                return 'field'
        

        res = []
        if len(fields) > 0:
            
            for field in fields:
                f = {}
                attrs = {}
                attrs['width'] = field.width
                
                
                if field.type == 'button':
                    attrs['string'] = field.description
                    attrs['name'] = field.name
                    
                else:
                    attrs['string'] = field.field.field_description
                    attrs['name'] = field.field.name
                    attrs['id'] = field.id
                    attrs['db_field'] = field.field.id
                    attrs['widget'] = get_widget(field)

                    column_field = {}
                    column_field['description'] = field_descriptions[field.field.name]
                    
                    f['field'] = column_field
                    f['name'] = field.field.name
                f['type'] = get_type(field)
                f['attributes'] = attrs
                
                res.append(f)
                

           

        
        return res
    
    @classmethod
    def user_view_set_default_view(cls, view_id):
        pool = Pool()
        View = pool.get('user.view')
        view = View(view_id)
        domain = []
        if view.view != None:
            domain = [('user','=',view.user.id),('view','=',view.view.id),('default','=',True)]
        else:
            domain = [('user','=',view.user.id), 
                        ('field_name','=',view.field_name), 
                        ('view_model','=',view.view_model),
                        ('field_model', '=', view.field_model),
                        ('default','=',True)
                        ]

        current_default_views = View.search(domain)
        
        for v in current_default_views:
            v.default = False
            v.save()
        
        view.default = True
        view.save()

    @classmethod
    def user_view_set(cls, view_data={}):
       
        pool = Pool()
        View = pool.get('user.view')
        Field = pool.get('user.view.field')
        Model = pool.get('ir.model')
        TrytonView = pool.get('ir.ui.view')
        TrytonField = pool.get('ir.model.field')

        if view_data['id'] > 0:
            view = View(view_data['id'])
        else:
            view = View()

        
        view.name = view_data['name']
       
                

        view.order = view_data['order'] or None
        view.compact = view_data['compact'] or False
        view.current_search = view_data['search'] or None
        view.user = view_data['user']
        if view_data['view_id'] != False:
            view.view = view_data['view_id']
            tview = TrytonView(view_data['view_id'])
            view.view_model = Model.search([('model', '=', tview.model)])[0].id
        
        elif view_data['field_data']:
            f_data = view_data['field_data']
            view.field_name = f_data['name']
            view.view_model = Model.search([('model', '=', f_data['relation'])])[0].id
            view.field_model = Model.search([('model', '=', f_data['model'])])[0].id
            
        def getField(field_data):
            f_id = field_data.get('id', -1)
            # check if the field and view exist
            if f_id > 0 and view_data['id']:
                field = Field(f_id)
            else:
                field = Field()

            if field_data['type'] == 'field':
                if not hasattr(field, 'field'):
                    field.field = TrytonField.search([('model','=',view.view_model), ('name','=',field_data['name'])])[0].id
                    
            
            field.name = field_data['name']    
            field.type = field_data['type']
            field.width = field_data.get('width')
            field.visual = field_data.get('visual')
            field.field_widget = field_data.get('widget')
            field.sequence = field_data.get('sequence')
            
            return field
            
            

        fields = []
        for field in view_data['fields']:
            fields.append(getField(field))
        
        if len(fields) > 0:
            view.user_view_fields = fields

        
        view.save()
        
       
        view_id = view.id


        if view_data['default'] == True:
            View.user_view_set_default_view(view_id)
       
        
        
        return view_id



    @fields.depends('view')
    def on_change_view(self):
        if self.view:
            pool = Pool()    
            self.view_model = pool.get('ir.model').search([('model', '=', self.view.model)])[0].id
        else:
            self.view_model = None

class UserViewField(sequence_ordered(), ModelSQL, ModelView):
    'User View Field'
    __name__ = 'user.view.field'

    name = fields.Char('Field Name')
    field = fields.Many2One('ir.model.field', 'Field', domain=[('model', '=', Eval('_parent_user_view', {}).get('view_model'))])
    width = fields.Float('Width')
    height = fields.Float('Height')
    expression = fields.Char('Expression')
    user_view = fields.Many2One('user.view', 'User View', ondelete='CASCADE')
    #to save from original view
    field_widget = fields.Char('Widget')
    visual = fields.Char('Visual')
    #type means field or button and will be written from the view
    type = fields.Char('Type')
    description = fields.Char('Description')
