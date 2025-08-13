from odoo import models, fields
from odoo.exceptions import ValidationError


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
    state = fields.Selection(
        [(stage, stage.replace('_', ' ').title()) for stage in STAGES],
        default=STAGES[0],
    )
    company_id = fields.Many2one('res.company', required=True,
                                 default=lambda self: self.env.company)
    project_id = fields.Many2one('project.project', string='Linked Project')

    def __init__(self, **vals):
        vals.setdefault('state', self.STAGES[0])
        super().__init__(**vals)

    def advance_stage(self):
        stages = self.STAGES
        projects = self if isinstance(self, (list, tuple)) else [self]
        for project in projects:
            idx = stages.index(project.state)
            if idx < len(stages) - 1:
                project.state = stages[idx + 1]
            else:
                raise ValidationError("Project already at final stage")
