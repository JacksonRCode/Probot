from create_tables import *

def kickstart():
    # Drop current tasks
    clear_table()

    # Create and finish new tasks

    add_task('ta1', ran(), 'a')
    add_task('ta2', ran(), 'a')
    add_task('ta3', ran(), 'a')
    add_task('ta4', ran(), 'a')
    add_task('ta5', ran(), 'a')

    finish_task('ta1', ran())
    finish_task('ta2', ran())
    finish_task('ta3', ran())
    finish_task('ta4', ran())
    finish_task('ta5', ran())

    add_task('tb1', ran(), 'b')
    add_task('tb2', ran(), 'b')
    add_task('tb3', ran(), 'b')
    add_task('tb4', ran(), 'b')
    add_task('tb5', ran(), 'b')

    finish_task('tb1', ran())
    finish_task('tb2', ran())
    finish_task('tb3', ran())
    finish_task('tb4', ran())
    finish_task('tb5', ran())

    add_task('tc1', ran(), 'c')
    add_task('tc2', ran(), 'c')
    add_task('tc3', ran(), 'c')
    add_task('tc4', ran(), 'c')
    add_task('tc5', ran(), 'c')

    finish_task('tc1', ran())
    finish_task('tc2', ran())
    finish_task('tc3', ran())
    finish_task('tc4', ran())
    finish_task('tc5', ran())