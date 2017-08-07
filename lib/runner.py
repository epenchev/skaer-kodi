__author__ = 'tickbg'

__all__ = ['run']

from impl import Runner
from impl import Context
from impl import AppControl

__RUNNER__ = Runner()

def run():
    app_control = AppControl()
    context = Context()
    context.log_debug('Starting skaer...')
    python_version = 'Unknown version of Python'
    try:
        import platform
        python_version = str(platform.python_version())
        python_version = 'Python %s' % python_version
    except:
        context.log_error('Error importing platform')
        return

    version = context.get_system_version()
    context.log_notice(
        'Running: %s (%s) on %s with %s' % (context.get_name(), context.get_version(), version, python_version))
    context.log_debug('Path: "%s' % context.get_path())
    context.log_debug('Params: "%s"' % unicode(context.get_params()))
    __RUNNER__.run(app_control, context)
    app_control.tear_down()
    context.log_debug('Shutdown of Kodion')
    pass
