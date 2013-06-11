from django.db import models as m
from django.contrib.auth.hashers import (
    check_password, make_password, is_password_usable, UNUSABLE_PASSWORD)
from django.contrib.auth import models as am
from django.contrib.auth.models import User
from tastypie.models import create_api_key

m.signals.post_save.connect(create_api_key, sender=User)


class BeaconTraitInstruction(m.Model):
    """This is a link table between Beacon, Trait and Instruction"""
    beacon = m.ForeignKey('Beacon')
    trait = m.ForeignKey('Trait')
    instruction = m.ForeignKey('Instruction', null=True)


class TraitType(m.Model):
    name = m.CharField(max_length=255, unique=True)


class Trait(m.Model):
    name = m.CharField(max_length=255, unique=True)
    trait_type = m.ForeignKey(TraitType, related_name='traits')


class Player(am.AbstractUser):
    traits = m.ManyToManyField(Trait, related_name='players', null=True)


class Game(m.Model):
    owner = m.ForeignKey(User)
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

    traits = m.ManyToManyField(Trait, through='BeaconTraitInstruction')
    instructions = m.ManyToManyField('Instruction', through='BeaconTraitInstruction')


class Instruction(m.Model):
    owner = m.ForeignKey(User)
    description = m.TextField()
    traits = m.ManyToManyField(Trait, through='BeaconTraitInstruction')


