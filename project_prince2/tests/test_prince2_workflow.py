
import pytest
from odoo.exceptions import ValidationError


def test_advance_stage_moves_until_closing(prince2_project_class):
    Project = prince2_project_class
    proj = Project(name='Demo')

    for stage in Project.STAGES[1:]:
        proj.advance_stage()
        assert proj.state == stage

    assert proj.state == Project.STAGES[-1]
    with pytest.raises(ValidationError):
        proj.advance_stage()


def test_project_link_stores_reference(prince2_project_class, project_class):
    Prince2 = prince2_project_class
    Project = project_class

    linked = Project(name='Standard')
    prince2 = Prince2(name='Demo PR2', project_id=linked)

    assert prince2.project_id is linked
