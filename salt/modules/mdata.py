# -*- coding: utf-8 -*-
'''
Module for managaging metadata in SmartOS Zones

.. versionadded:: 2016.3.0

:maintainer:    Jorge Schrauwen <sjorge@blackdot.be>
:maturity:      new
:platform:      smartos
'''
from __future__ import absolute_import

# Import Python libs
import logging

# Import Salt libs
from salt.defaults import exitcodes
import salt.utils
import salt.utils.decorators as decorators

log = logging.getLogger(__name__)

# Function aliases
__func_alias__ = {
    'list_': 'list',
    'get_': 'get',
    'put_': 'put',
    'delete_': 'delete',
}

# Define the module's virtual name
__virtualname__ = 'mdata'


@decorators.memoize
def _check_mdata_list():
    '''
    looks to see if mdata-list is present on the system
    '''
    return salt.utils.which('mdata-list')


@decorators.memoize
def _check_mdata_get():
    '''
    looks to see if mdata-get is present on the system
    '''
    return salt.utils.which('mdata-get')


@decorators.memoize
def _check_mdata_put():
    '''
    looks to see if mdata-put is present on the system
    '''
    return salt.utils.which('mdata-put')


@decorators.memoize
def _check_mdata_delete():
    '''
    looks to see if mdata-delete is present on the system
    '''
    return salt.utils.which('mdata-delete')


def __virtual__():
    '''
    Provides mdata only on SmartOS
    '''
    if _check_mdata_list() and not salt.utils.is_smartos_globalzone():
        return __virtualname__
    return (
        False,
        '{0} module can only be loaded on SmartOS zones'.format(
            __virtualname__
        )
    )


def list_():
    '''
    List available metadata

    CLI Example:

    .. code-block:: bash

        salt '*' mdata.list
    '''
    mdata = _check_mdata_list()
    if mdata:
        cmd = '{0}'.format(mdata)
        return __salt__['cmd.run'](cmd).splitlines()
    return {}


def get_(*keyname):
    '''
    Get metadata

    keyname : string
        name of key

    .. note::

        If no keynames are specified, we get all (public) properties

    CLI Example:

    .. code-block:: bash

        salt '*' mdata.get salt:role
        salt '*' mdata.get user-script salt:role
    '''
    mdata = _check_mdata_get()
    ret = {}

    if len(keyname) == 0:
        keyname = list_()

    for k in keyname:
        if mdata:
            cmd = '{0} {1}'.format(mdata, k)
            res = __salt__['cmd.run_all'](cmd)
            ret[k] = res['stdout'] if res['retcode'] == exitcodes.EX_OK else ''
        else:
            ret[k] = ''

    return ret


def put_(keyname, val):
    '''
    Put metadata

    prop : string
        name of property
    val : string
        value to set

    CLI Example:

    .. code-block:: bash

        salt '*' mdata.list
    '''
    mdata = _check_mdata_put()
    ret = {}

    if mdata:
        cmd = 'echo {2} | {0} {1}'.format(mdata, keyname, val)
        ret = __salt__['cmd.run_all'](cmd, python_shell=True)

    return ret['retcode'] == exitcodes.EX_OK


def delete_(*keyname):
    '''
    Delete metadata

    prop : string
        name of property

    CLI Example:

    .. code-block:: bash

        salt '*' mdata.get salt:role
        salt '*' mdata.get user-script salt:role
    '''
    mdata = _check_mdata_delete()
    valid_keynames = list_()
    ret = {}

    for k in keyname:
        if mdata and k in valid_keynames:
            cmd = '{0} {1}'.format(mdata, k)
            ret[k] = __salt__['cmd.run_all'](cmd)['retcode'] == exitcodes.EX_OK
        else:
            ret[k] = True

    return ret

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
