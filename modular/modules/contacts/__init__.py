"""Contacts: people and their companies."""

from oneframework import Screen

from .models import Company, Person
from .views import ContactsBoard, PersonDetail, PersonItem

__all__ = ["Company", "Person", "ContactsBoard", "PersonDetail", "PersonItem"]

SCREEN = Screen(ContactsBoard, label="Контакты", icon="group")
