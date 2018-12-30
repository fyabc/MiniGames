#! /usr/bin/python
# -*- coding: utf-8 -*-

import os

from ..utils.constants import UserDataPath
from ..utils.user import AppUser
from ..utils.message import info, critical, warning
from ..utils.error import SameUserAppExists, GameError

__author__ = 'fyabc'


class Frontend:
    def __init__(self, **kwargs):
        info('Start the frontend "{}"'.format(self.__class__.__name__))
        self.user = AppUser.load_or_create(kwargs.pop('user_id_or_name', None))
        self.game = None    # type: 'MyHearthStone.game.core.Game'
        self.raise_exception = kwargs.pop('raise_exception', False)

        self._hold_lock_file = False

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def main(self) -> int:
        """Main loop of the frontend.

        :return: exit status, 0 means normal exit, 1 means exit with error.
        :rtype: int
        """

        try:
            self.__check_user_locked()
            self._main()
        except GameError as e:
            critical(e)
            return 1
        except Exception as e:
            from traceback import format_exc
            critical(e)
            critical(format_exc())
            if self.raise_exception:
                raise
            else:
                return 1
        finally:
            self.finalize()
        return 0

    def _main(self):
        raise NotImplementedError('implemented in subclasses')

    def create_server(self):
        pass

    def preprocess(self):
        pass

    def finalize(self):
        if self._hold_lock_file:
            info('Saving user information...')
            self.user.dump()
            info('Save use information done')

            try:
                os.remove(self.__lock_filename())
            except FileNotFoundError:
                warning('Try to remove user lock file but not found')
            else:
                info('User lock file removed')

        info('App exited\n')

    def __check_user_locked(self):
        if os.path.exists(self.__lock_filename()):
            raise SameUserAppExists(self.user.user_id)
        else:
            with open(self.__lock_filename(), 'w'):
                info('Create user lock file')
                self._hold_lock_file = True

    def __lock_filename(self):
        return os.path.join(UserDataPath, 'lock-user-{}.lock'.format(self.user.user_id))
