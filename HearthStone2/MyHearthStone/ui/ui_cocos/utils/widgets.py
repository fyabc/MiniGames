#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Some useful widgets of cocos2d.

These widgets are extracted from code and generalized.

TODO: Refactor the code more.
"""

from functools import partial

from .basic import pos
from .active import ActiveLabel

__author__ = 'fyabc'


def make_radio_button_list(layer, positions, prefix, **kwargs):
    """Create a vertical list of radio buttons.

    Usage::

        class MyLayer(ActiveLayer):
            def __init__(self):
                # ...
                self._rb_list_xx = make_radio_button_list(self, positions, 'xx', scroll=True)

            def on_enter(self):
                # ...
                self.build_xx_buttons()
                self._rb_list_xx['on_enter']()

            def on_exit(self):
                # ...
                self._rb_list_xx['on_exit'](self)

            def build_xx_buttons(self):
                # ...
                TODO: Add doc here.

    :param layer:
    :param positions:
    :param prefix:
    :param kwargs:
        :keyword scroll: Add scroll arrows or not.
    :return: Dict of all useful data and functions.
        :key data: The select dict.
        :key refresh_fn:
        :key on_enter:
        :key on_exit:
        :key default_selected_fn:
    :rtype: dict

    TODO: Integrate the builder into this factory.
    """
    data = {
        'CX': 0.5,
        'ListT': 0.9,
        'ListB': 0.25,
        'ArrowY': 0.15,
        'Size': 10,
        'show_start': 0,
        'buttons': [],
        'selected': None,
    }
    data.update(positions)

    def _refresh_fn():
        CX = data['CX']
        ListT = data['ListT']
        Size = data['Size']
        show_start = data['show_start']

        for i, button in enumerate(data['buttons']):
            button.position = pos(CX, ListT - (ListT - data['ListB']) * (i - show_start) / (Size - 1))
            if show_start <= i < show_start + Size:
                layer.try_add(button)
            else:
                layer.try_remove(button)

    def _on_enter():
        data['show_start'] = 0
        data['selected'] = None
        _refresh_fn()

    def _on_exit(layer):
        data['show_start'] = 0
        data['selected'] = None
        for button in data['buttons']:
            layer.try_remove(button)
        data['buttons'].clear()

    attr_name = '_{}_selected'.format(prefix)

    def _default_selected_fn(clicked_button):
        """Undo render of all buttons, then render this (selected) button."""
        for button in data['buttons']:
            assert isinstance(button, ActiveLabel)
            if getattr(button, attr_name, None) is True:
                delattr(button, attr_name)
                button.element.text = button.element.text[2:-2]
        clicked_button.element.text = '[ {} ]'.format(clicked_button.element.text)
        setattr(clicked_button, attr_name, True)

    if kwargs.pop('scroll', True):
        def _scroll(is_down_):
            if is_down_:
                if data['show_start'] + data['Size'] >= len(data['buttons']):
                    return
            else:
                if data['show_start'] == 0:
                    return
            data['show_start'] += int(is_down_) * 2 - 1
            _refresh_fn()

        for is_down in (False, True):
            layer.add(ActiveLabel.hs_style(
                '[ {} ]'.format('↓' if is_down else '↑'),
                pos(data['CX'] + 0.05 * (1 if is_down else -1), data['ArrowY']),
                callback=lambda is_down_=is_down: _scroll(is_down_),
                font_size=28, anchor_x='center', anchor_y='center', bold=True,
            ))

    return {
        'data': data,
        'refresh_fn': _refresh_fn,
        'on_enter': _on_enter,
        'on_exit': _on_exit,
        'default_selected_fn': _default_selected_fn,
    }


def active_labels_group_select_fn(group, prefix):
    attr_name = '_{}_selected'.format(prefix)

    def _label_selected(clicked_button):
        """Undo render of all buttons, then render this (selected) button."""
        for button in group:
            assert isinstance(button, ActiveLabel)
            if getattr(button, attr_name, None) is True:
                delattr(button, attr_name)
                button.element.text = button.element.text[2:-2]
        clicked_button.element.text = '[ {} ]'.format(clicked_button.element.text)
        setattr(clicked_button, attr_name, True)

    return _label_selected


def make_radio_button_group(layer, buttons_data, prefix, **kwargs):
    """Create a group of ratio buttons.

    Usage::

        class MyLayer(ActiveLayer):
            def __init__(self):
                # ...
                self._rb_group_xx = make_radio_button_group(self, [
                    {'name': name1, 'position': position1, 'value': value1},
                    {'name': name2, 'position': position2, 'value': value2},
                ], 'xx')

            def use_xx(self):
                value = self._rb_group_xx['data']['value']
                print('Current value is:', value)

    :param layer:
    :param buttons_data: Data of buttons.
    :type buttons_data: list
        List of dicts of {
            'name': button name,
            'position': button position,
            'value': bound variable value,
            # And other kwargs of active label...
        }
    :param prefix:
    :param kwargs:
        :keyword default_value: Default value.
        :keyword direct_add: Add buttons into the layer directly.
    :return:
    """

    data = {
        'buttons': [],
        'value': kwargs.pop('default_value', None),
    }

    fn = active_labels_group_select_fn(data['buttons'], prefix)

    def _callback(clicked_button, value):
        fn(clicked_button)
        data['value'] = value

    data['buttons'].extend([
        ActiveLabel.hs_style(
            button_data['name'], button_data['position'],
            callback=partial(_callback, value=button_data['value']),
            anchor_x=button_data.get('anchor_x', 'center'), anchor_y=button_data.get('anchor_y', 'center'),
            self_in_callback=True,
        ) for button_data in buttons_data
    ])

    def _add_buttons():
        for button in data['buttons']:
            layer.try_add(button)

    if kwargs.pop('direct_add', True):
        _add_buttons()

    return {
        'data': data,
        'add_buttons_fn': _add_buttons,
    }


def make_check_button(layer, **kwargs):
    """Create a check button.

    :param layer:
    :param kwargs:
    :return:
    """


__all__ = [
    'make_radio_button_list',
    'active_labels_group_select_fn',
    'make_radio_button_group',
]
