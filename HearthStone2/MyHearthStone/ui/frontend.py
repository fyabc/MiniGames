#! /usr/bin/python
# -*- coding: utf-8 -*-

from ..utils.user import AppUser
from ..game.core import Game

__author__ = 'fyabc'


class Frontend:
    def __init__(self, **kwargs):
        self.user = AppUser.load_or_create(kwargs.pop('user_id_or_name', None))
        self.game = None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def main(self) -> int:
        """Main loop of the frontend.

        :return: exit status, 0 means normal exit, 1 means exit with error.
        :rtype: int
        """

        try:
            self._main()
        except Exception as e:
            print(e)
            return 1
        finally:
            self.finalize()
        return 0

    def _main(self):
        raise NotImplementedError('implemented in subclasses')

    def create_server(self):
        pass

    def run(self):
        # Start game processing
        try:
            while True:
                pass
        except StopIteration:
            pass

        # Main game processing
        pass

    def finalize(self):
        self.user.dump()
