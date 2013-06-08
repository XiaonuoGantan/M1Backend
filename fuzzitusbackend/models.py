from django.db import models as m
from django.contrib.auth.hashers import (
    check_password, make_password, is_password_usable, UNUSABLE_PASSWORD)
from django.contrib.auth import models as am


class TraitType(m.Model):
    name = m.CharField(max_length=255, unique=True)


class Trait(m.Model):
    name = m.CharField(max_length=255, unique=True)
    types = m.ManyToManyField(TraitType, related_name='traits')


class Player(am.AbstractUser):
    traits = m.ManyToManyField(Trait, related_name='players')


class Game(m.Model):
    name = m.CharField(max_length=255, unique=True)
    password = m.CharField(max_length=128)
    players = m.ManyToManyField(Player, related_name='games')

    def check_password(self, password, encoded):
        return check_password(password, encoded)

    def set_password(self, password):
        self.password = make_password(password)


class Beacon(m.Model):
    game = m.ForeignKey(Game)
    name = m.CharField(max_length=255, unique=True)


class Instruction(m.Model):
    beacons = m.ManyToManyField(Beacon, related_name='instructions')
    traits = m.ManyToManyField(Trait, related_name='instructions')
    description = m.TextField()
