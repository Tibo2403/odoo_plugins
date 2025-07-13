
def test_advance_stage_moves_until_closing(prince2_project_class):
    Project = prince2_project_class
    proj = Project(name='Demo')

    for stage in Project.STAGES[1:]:
        proj.advance_stage()
        assert proj.state == stage

    proj.advance_stage()
    assert proj.state == Project.STAGES[-1]
