# -*- coding: utf-8 -*-
#
# vim: set ts=4 sw=4 sts=4 et :
'''
===========================================
Monkey patch 'salt.config.include_config'
===========================================

commit bfc7f9026c8a94444f8d25cdcd430160f4b1744b
Author: Beorn Facchini <beornf@gmail.com>
Date:   Fri Jan 6 21:18:30 2017 +1100

    Merge list values from config files

diff --git a/salt/config/__init__.py b/salt/config/__init__.py
index a32e680..36134a7 100644
--- a/salt/config/__init__.py
+++ b/salt/config/__init__.py
@@ -1902,7 +1902,7 @@ def include_config(include, orig_path, verbose, exit_on_config_errors=False):
             if include:
                 opts.update(include_config(include, fn_, verbose))
 
-            salt.utils.dictupdate.update(configuration, opts)
+            salt.utils.dictupdate.update(configuration, opts, True, True)
 
     return configuration
 
'''

import glob
import collections
import os
import wrapt

import salt.defaults.exitcodes
import salt.exceptions
import salt.utils.dictupdate
from salt.config import log, _read_conf_file

def include_config(include, orig_path, verbose, exit_on_config_errors=False):
    '''
    Parses extra configuration file(s) specified in an include list in the
    main config file.
    '''
    # Protect against empty option

    if not include:
        return {}

    if orig_path is None:
        # When the passed path is None, we just want the configuration
        # defaults, not actually loading the whole configuration.
        return {}

    if isinstance(include, str):
        include = [include]

    configuration = {}
    for path in include:
        # Allow for includes like ~/foo
        path = os.path.expanduser(path)
        if not os.path.isabs(path):
            path = os.path.join(os.path.dirname(orig_path), path)

        # Catch situation where user typos path in configuration; also warns
        # for empty include directory (which might be by design)
        if len(glob.glob(path)) == 0:
            if verbose:
                log.warning(
                    'Warning parsing configuration file: "include" path/glob '
                    "'{0}' matches no files".format(path)
                )

        for fn_ in sorted(glob.glob(path)):
            log.debug('Including configuration from \'{0}\''.format(fn_))
            try:
                opts = _read_conf_file(fn_)
            except salt.exceptions.SaltConfigurationError as error:
                log.error(error)
                if exit_on_config_errors:
                    sys.exit(salt.defaults.exitcodes.EX_GENERIC)
                else:
                    # Initialize default config if we wish to skip config errors
                    opts = {}

            include = opts.get('include', [])
            if include:
                opts.update(include_config(include, fn_, verbose))

            salt.utils.dictupdate.update(configuration, opts, True, True)

    return configuration

@wrapt.patch_function_wrapper('salt.config', 'include_config')
def include_config_wrapper(wrapped, instance, args, kwargs):
    return include_config(*args, **kwargs)
