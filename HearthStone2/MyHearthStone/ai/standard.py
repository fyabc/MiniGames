#! /usr/bin/python
# -*- coding: utf-8 -*-

from . import agent

# Import them to register agents.
from . import basic

__author__ = 'fyabc'


def get_agent_by_name(name):
    return agent.Agent.AgentClasses[name]


__all__ = [
    'get_agent_by_name',
]
