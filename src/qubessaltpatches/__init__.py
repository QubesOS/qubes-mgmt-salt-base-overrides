import salt.version
version = salt.version.__saltstack_version__

# Apply monkey patch for salt versions less than 2015.8
# 
# Add list merging within dictupdate
if version.info < (2015, 8, 0, 0):
    import qubessaltpatches.update

# Apply monkey patch for salt versions [2015.8 - 2017.5)
#
# Use list merging for config includes
if (2015, 8, 0, 0) <= version.info < (2017, 5, 0, 0):
    import qubessaltpatches.config

# Apply monkey patch for salt versions less than 2015.5.5
#
# Adds url module which appears in v2015.5.5
if version.info < (2015, 5, 5, 0):
    import sys
    import qubessaltpatches.url
    url = sys.modules['qubes.mgmt.patches.url']
    sys.modules['salt.utils.url'] = url
    
    import salt.utils
    salt.utils.url = url
