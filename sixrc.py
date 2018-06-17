# Six configuration file. The unusual layout is needed to detect whether
# Six is available before changing settings and loading plugins.
import logging

import sublime

from User.six.surround import (
    _six_surround_change,
    surround,
    )


# Hook ourselves up to the Six logger.
_logger = logging.getLogger('Six.user.%s' % __name__.rsplit('.')[1])
_logger.info("loading Six configuration")


def plugin_loaded():
	# Now the Sublime Text API is available to us.
    settings = sublime.load_settings('Preferences.sublime-settings')

    if 'Six' in settings.get('ignored_packages'):
        return

    from Six._init_ import editor
    from Six.lib.constants import Mode

    # Init the Surround plugin. We do this here because now we know that Six
    # is definitely available.
    try:
        surround()
    except ValueError as e:
        if str(e) == "cannot register keys (zs) twice for normal mode":
            # We have reloaded sixrc.py; ignore command registration error.
            pass
        else:
            raise
    except Exception as e:
        _logger.error("error while (re)loading %s", __name__)
        _logger.error(e)

    # Mappings -- optional.
    editor.mappings.add(Mode.Normal, 'Y', 'y$')
    editor.mappings.add(Mode.Normal, '<Space>', ':')
    editor.mappings.add(Mode.Normal, ',pp', 'a()<Esc>ha')
