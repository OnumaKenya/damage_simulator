from components import (
    student_input,
    enemy_input,
    buff_input,
    debuff_input,
    skill_input,
    sidebar,
    simulation,
)


def register_callbacks(app):
    student_input.register_student_callback(app)
    enemy_input.register_enemy_callback(app)
    buff_input.register_buff_callback(app)
    debuff_input.register_debuff_callback(app)
    skill_input.register_skill_callback(app)
    sidebar.register_sidebar_callback(app)
    simulation.register_simulation_callback(app)
