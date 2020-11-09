import sys
from abc import ABC
from functools import partial

from framework import MenuEntry, MenuLayer


class InteractiveMenu(MenuLayer, ABC):
    def call(self):
        while True:
            super(InteractiveMenu, self).call()
            try:
                key = int(input('Ввод: '))
                entry = self._entries[key]
            except (ValueError, IndexError):
                pass
            else:
                break
        entry.call()


class MainMenu(InteractiveMenu):
    name = 'Главное меню'


class FirstSubMenu(InteractiveMenu):
    name = 'Первое подменю'


class SecondSubMenu(InteractiveMenu):
    name = 'Второе подменю'


def do_action_and_call_menu(action, menu: MenuLayer):
    def ret_action():
        action()
        input('Enter для продолжения')
        menu.call()
    
    return ret_action


if __name__ == '__main__':
    main_menu = MainMenu()
    first_sub_menu = FirstSubMenu()
    second_sub_menu = SecondSubMenu()
    
    hello_world_entry = MenuEntry(
        'Привет, мир!',
        action=do_action_and_call_menu(
            action=partial(print, 'Hello, world!'),
            menu=main_menu)
    )
    
    exit_entry = MenuEntry('Выход', sys.exit)
    
    sub_menu1_caller = MenuEntry(first_sub_menu.name, action=first_sub_menu.call)
    sub_menu2_caller = MenuEntry('Вызвать второе подменю', action=second_sub_menu.call)
    
    main_menu.add_entry(hello_world_entry)
    main_menu.add_entry(sub_menu1_caller)
    main_menu.add_entry(sub_menu2_caller)
    main_menu.add_entry(exit_entry)
    
    main_menu_caller = MenuEntry(main_menu.name, action=main_menu.call)
    first_sub_menu.add_entry(main_menu_caller)
    
    second_sub_menu.add_entry(main_menu_caller)
    second_sub_menu.add_entry(exit_entry)
    
    main_menu.call()
