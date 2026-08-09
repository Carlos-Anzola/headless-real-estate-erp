from odoo import models, fields # type:ignore

class PremiumProperty(models.Model):
    _name = 'premium.property'
    _description = 'Propiedad Inmobiliaria'
    # Heredamos mail.thread y mail.activity.mixin para tener el historial y adjuntos
    _inherit = ['mail.thread', 'mail.activity.mixin'] 

    # El tracking=True hace que cualquier cambio en este campo se guarde en el historial
    name = fields.Char(string='Título de Propiedad', required=True, tracking=True)
    price = fields.Char(string='Precio', required=True, tracking=True)
    location = fields.Char(string='Ubicación', required=True)
    img_url = fields.Char(string='URL de Imagen')
    
    beds = fields.Integer(string='Habitaciones')
    baths = fields.Integer(string='Baños')
    parking = fields.Integer(string='Puestos')
    
    desc = fields.Text(string='Descripción corta (Web)')
    long_desc = fields.Text(string='Descripción detallada')

    # --- NUEVOS CAMPOS DE NEGOCIO ---
    state = fields.Selection([
        ('disponible', 'Disponible'),
        ('reservada', 'Reservada'),
        ('vendida', 'Vendida'),
        ('inactiva', 'Inactiva')
    ], string='Estado', default='disponible', tracking=True)

    user_id = fields.Many2one('res.users', string='Asesor Asignado', default=lambda self: self.env.user, tracking=True)
    commission_pct = fields.Float(string='Comisión (%)', tracking=True)
    
    active = fields.Boolean(default=True)