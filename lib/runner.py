from impl import Runner
from impl import Context
from impl import AppControl

import platform


__all__ = ['run']

__RUNNER__ = Runner()


def run():
    app_control = AppControl()
    context = Context()
    context.log_debug('Starting skaer...')

    context.log_notice(
        'Running: %s (%s) on %s with Python %s' %
        (context.get_name(), context.get_version(),
         context.get_system_version(), str(platform.python_version())))

    context.log_debug('Path: "%s' % context.get_path())
    context.log_debug('Params: "%s"' % unicode(context.get_params()))
    __RUNNER__.run(app_control, context)
    app_control.tear_down(context)
    context.log_debug('Skaer shutdown')
