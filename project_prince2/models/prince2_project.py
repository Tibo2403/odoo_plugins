from odoo import models, fields


class Prince2Project(models.Model):
    _name = 'project.prince2.project'
    _description = 'PRINCE2 Project'

    STAGES = [
        'starting_up',
        'directing',
        'initiating',
        'controlling',
        'managing_delivery',
        'managing_boundary',
        'closing',
    ]

    name = fields.Char(required=True)
    state = fields.Selection([
        ('starting_up', 'Starting Up'),
        ('directing', 'Directing'),
        ('initiating', 'Initiating'),
        ('controlling', 'Controlling'),
        ('managing_delivery', 'Managing Delivery'),
        ('managing_boundary', 'Managing Boundary'),
        ('closing', 'Closing'),
    ], default='starting_up')
    company_id = fields.Many2one('res.company', required=True,
                                 default=lambda self: self.env.company)
    project_id = fields.Many2one('project.project', string='Linked Project')

    def __init__(self, **vals):
        vals.setdefault('state', 'starting_up')
        super().__init__(**vals)

    def advance_stage(self):
        stages = self.STAGES
        projects = self if isinstance(self, (list, tuple)) else [self]
        for project in projects:
            idx = stages.index(project.state)
            if idx < len(stages) - 1:
                project.state = stages[idx + 1]
