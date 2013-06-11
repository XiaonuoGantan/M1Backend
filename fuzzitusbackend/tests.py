from django.test import TestCase
from tastypie.test import ResourceTestCase
from fuzzitusbackend.models import Beacon, BeaconTraitInstruction, Game, Instruction, User, Trait, TraitType
from fuzzitusbackend.api import GameResource

test_admin_data = {
    'email': 'testuser@test.com',
    'username': 'testuser',
    'password': '1234',
}


class UserResourceTest(ResourceTestCase):
    @classmethod
    def setUpClass(self):
        self.admin_signup_uri = '/api/v1/user/signup/'

    def test_admin_signup_and_login(self):
        resp = self.api_client.post(
            self.admin_signup_uri, data=test_admin_data)
        self.assertHttpOK(resp)
        resp = self.api_client.post(
            '/api/v1/user/login/', data=test_admin_data)
        self.assertHttpOK(resp)


test_game_data = {
    'name': 'Test Game',
    'password': '1234',
}


class GameResourceTest(ResourceTestCase):
    @classmethod
    def setUpClass(cls):
        cls.admin_signup_uri = '/api/v1/user/signup/'
        cls.game_creation_uri = '/api/v1/game/'

    def test_admin_game_creation(self):
        resp = self.api_client.post(
            self.admin_signup_uri, data=test_admin_data)
        self.assertHttpOK(resp)
        data = self.deserialize(resp)
        api_key = data['api_key']
        resp = self.api_client.post(
            '/api/v1/user/login/', data=test_admin_data)
        self.assertHttpOK(resp)
        owner = User.objects.latest('pk')
        test_game_data.update({
            'owner': '/api/v1/user/{0}/'.format(owner.pk),
        })
        data = self.deserialize(resp)
        test_game_data.update({
            'api_key': api_key,
            'username': test_admin_data['username']})
        auth_str = 'apikey {0}:{1}'.format(
            test_admin_data['username'], api_key)
        resp = self.api_client.post(
            self.game_creation_uri, data=test_game_data,
            authentication=auth_str)
        self.assertHttpCreated(resp)

    def test_game_not_created(self):
        resp = self.api_client.post(
            self.game_creation_uri, data=test_game_data)
        self.assertHttpUnauthorized(resp)


test_player_data = {
    'username': 'TestPlayer',
    'password': '123',
    'first_name': 'Test',
    'last_name': 'Player',
}

class PlayerResourceTest(ResourceTestCase):
    @classmethod
    def setUpClass(cls):
        cls.admin_signup_uri = '/api/v1/user/signup/'
        cls.game_creation_uri = '/api/v1/game/'
        cls.player_creation_uri = '/api/v1/player/'

    def setUp(self):
        super(PlayerResourceTest, self).setUp()
        resp = self.api_client.post(
            self.admin_signup_uri, data=test_admin_data)
        self.assertHttpOK(resp)
        data = self.deserialize(resp)
        self.api_key = data['api_key']
        resp = self.api_client.post(
            '/api/v1/user/login/', data=test_admin_data)
        self.assertHttpOK(resp)
        owner = User.objects.latest('pk')
        test_game_data.update({
            'owner': '/api/v1/user/{0}/'.format(owner.pk),
        })
        data = self.deserialize(resp)
        test_game_data.update({
            'api_key': self.api_key,
            'username': test_admin_data['username']})
        auth_str = 'apikey {0}:{1}'.format(
            test_admin_data['username'], self.api_key)
        resp = self.api_client.post(
            self.game_creation_uri, data=test_game_data,
            authentication=auth_str)
        self.assertHttpCreated(resp)

    def test_player_creation(self):
        resp = self.api_client.post(
            self.player_creation_uri, data=test_player_data,
            authentication='apikey {0}:{1}'.format(
                test_admin_data['username'], self.api_key))
        self.assertHttpCreated(resp)


test_beacon_data = {
    'name': 'TestBeacon',
}


class BeaconResourceTest(ResourceTestCase):
    @classmethod
    def setUpClass(cls):
        cls.admin_signup_uri = '/api/v1/user/signup/'
        cls.game_creation_uri = '/api/v1/game/'
        cls.beacon_creation_uri = '/api/v1/beacon/'

    def setUp(self):
        super(BeaconResourceTest, self).setUp()
        resp = self.api_client.post(
            self.admin_signup_uri, data=test_admin_data)
        data = self.deserialize(resp)
        self.api_key = data['api_key']
        owner = User.objects.latest('pk')
        test_game_data.update({
            'owner': '/api/v1/user/{0}/'.format(owner.pk),
        })
        resp = self.api_client.post(
            self.game_creation_uri, data=test_game_data,
            authentication='apikey {0}:{1}'.format(test_admin_data['username'],
                                                   self.api_key))
        self.assertHttpCreated(resp)

    def test_beacon_creation(self):
        game = Game.objects.latest('pk')
        test_beacon_data.update({
            'game': '/api/v1/game/{0}/'.format(game.pk),
        })
        resp = self.api_client.post(
            self.beacon_creation_uri, data=test_beacon_data,
            authentication='apikey {0}:{1}'.format(test_admin_data['username'],
                                                   self.api_key))
        self.assertHttpCreated(resp)


test_trait_type_data = {
    'name': 'Gender',
}


class TraitTypeResourceTest(ResourceTestCase):
    @classmethod
    def setUpClass(cls):
        cls.admin_signup_uri = '/api/v1/user/signup/'
        cls.game_creation_uri = '/api/v1/game/'
        cls.beacon_creation_uri = '/api/v1/beacon/'

    def setUp(self):
        super(TraitTypeResourceTest, self).setUp()
        resp = self.api_client.post(
            self.admin_signup_uri, data=test_admin_data)
        data = self.deserialize(resp)
        self.api_key = data['api_key']
        owner = User.objects.latest('pk')
        test_game_data.update({
            'owner': '/api/v1/user/{0}/'.format(owner.pk),
        })
        resp = self.api_client.post(
            self.game_creation_uri, data=test_game_data,
            authentication='apikey {0}:{1}'.format(test_admin_data['username'],
                                                   self.api_key))
        self.assertHttpCreated(resp)
        game = Game.objects.latest('pk')
        test_beacon_data.update({
            'game': '/api/v1/game/{0}/'.format(game.pk),
        })
        resp = self.api_client.post(
            self.beacon_creation_uri, data=test_beacon_data,
            authentication='apikey {0}:{1}'.format(test_admin_data['username'],
                                                   self.api_key))
        self.assertHttpCreated(resp)

    def test_trait_type_creation(self):
        resp = self.api_client.post(
            '/api/v1/trait_type/', data=test_trait_type_data,
            authentication='apikey {0}:{1}'.format(test_admin_data['username'],
                                                   self.api_key))
        self.assertHttpCreated(resp)


test_trait_data_one = {
    'name': 'Female'
}
test_trait_data_two = {
    'name': 'Male'
}

class TraitResourceTest(ResourceTestCase):
    @classmethod
    def setUpClass(cls):
        cls.admin_signup_uri = '/api/v1/user/signup/'
        cls.game_creation_uri = '/api/v1/game/'
        cls.beacon_creation_uri = '/api/v1/beacon/'

    def setUp(self):
        super(TraitResourceTest, self).setUp()
        resp = self.api_client.post(
            self.admin_signup_uri, data=test_admin_data)
        data = self.deserialize(resp)
        self.api_key = data['api_key']
        owner = User.objects.latest('pk')
        test_game_data.update({
            'owner': '/api/v1/user/{0}/'.format(owner.pk),
        })
        resp = self.api_client.post(
            self.game_creation_uri, data=test_game_data,
            authentication='apikey {0}:{1}'.format(test_admin_data['username'],
                                                   self.api_key))
        self.assertHttpCreated(resp)
        game = Game.objects.latest('pk')
        test_beacon_data.update({
            'game': '/api/v1/game/{0}/'.format(game.pk),
        })
        resp = self.api_client.post(
            self.beacon_creation_uri, data=test_beacon_data,
            authentication='apikey {0}:{1}'.format(test_admin_data['username'],
                                                   self.api_key))
        self.assertHttpCreated(resp)
        resp = self.api_client.post(
            '/api/v1/trait_type/', data=test_trait_type_data,
            authentication='apikey {0}:{1}'.format(test_admin_data['username'],
                                                   self.api_key))
        self.assertHttpCreated(resp)

    def test_trait_creation(self):
        trait_type = TraitType.objects.latest('pk')
        test_trait_data_one.update({
            'trait_type': '/api/v1/trait_type/{0}/'.format(trait_type.pk),
        })
        resp = self.api_client.post(
            '/api/v1/trait/', data=test_trait_data_one,
            authentication='apikey {0}:{1}'.format(test_admin_data['username'],
                                                   self.api_key))
        self.assertHttpCreated(resp)


test_instruction_data_one = {
    'description': 'Test Instruction For Female'
}
test_instruction_data_two = {
    'description': 'Test Instruction For Male'
}

class InstructionResourceTest(ResourceTestCase):
    @classmethod
    def setUpClass(cls):
        cls.admin_signup_uri = '/api/v1/user/signup/'
        cls.game_creation_uri = '/api/v1/game/'
        cls.beacon_creation_uri = '/api/v1/beacon/'
        cls.instruction_creation_uri = '/api/v1/instruction/'

    def setUp(self):
        super(InstructionResourceTest, self).setUp()
        resp = self.api_client.post(
            self.admin_signup_uri, data=test_admin_data)
        data = self.deserialize(resp)
        self.api_key = data['api_key']
        owner = User.objects.latest('pk')
        test_game_data.update({
            'owner': '/api/v1/user/{0}/'.format(owner.pk),
        })
        resp = self.api_client.post(
            self.game_creation_uri, data=test_game_data,
            authentication='apikey {0}:{1}'.format(test_admin_data['username'],
                                                   self.api_key))
        self.assertHttpCreated(resp)
        game = Game.objects.latest('pk')
        test_beacon_data.update({
            'game': '/api/v1/game/{0}/'.format(game.pk),
        })
        resp = self.api_client.post(
            self.beacon_creation_uri, data=test_beacon_data,
            authentication='apikey {0}:{1}'.format(test_admin_data['username'],
                                                   self.api_key))
        self.assertHttpCreated(resp)
        resp = self.api_client.post(
            '/api/v1/trait_type/', data=test_trait_type_data,
            authentication='apikey {0}:{1}'.format(test_admin_data['username'],
                                                   self.api_key))
        self.assertHttpCreated(resp)

    def test_instruction_creation(self):
        owner = User.objects.latest('pk')
        test_instruction_data_one.update({
            'owner': '/api/v1/user/{0}/'.format(owner.pk),
        })
        resp = self.api_client.post(
            self.instruction_creation_uri, data=test_instruction_data_one,
            authentication='apikey {0}:{1}'.format(test_admin_data['username'],
                                                   self.api_key))
        self.assertHttpCreated(resp)


class BeaconTraitInstructionTest(ResourceTestCase):
    @classmethod
    def setUpClass(cls):
        cls.admin_signup_uri = '/api/v1/user/signup/'
        cls.game_creation_uri = '/api/v1/game/'
        cls.beacon_creation_uri = '/api/v1/beacon/'
        cls.instruction_creation_uri = '/api/v1/instruction/'

    def setUp(self):
        super(BeaconTraitInstructionTest, self).setUp()
        resp = self.api_client.post(
            self.admin_signup_uri, data=test_admin_data)
        data = self.deserialize(resp)
        self.api_key = data['api_key']
        owner = User.objects.latest('pk')
        test_game_data.update({
            'owner': '/api/v1/user/{0}/'.format(owner.pk),
        })
        resp = self.api_client.post(
            self.game_creation_uri, data=test_game_data,
            authentication='apikey {0}:{1}'.format(test_admin_data['username'],
                                                   self.api_key))
        self.assertHttpCreated(resp)
        game = Game.objects.latest('pk')
        test_beacon_data.update({
            'game': '/api/v1/game/{0}/'.format(game.pk),
        })
        resp = self.api_client.post(
            self.beacon_creation_uri, data=test_beacon_data,
            authentication='apikey {0}:{1}'.format(test_admin_data['username'],
                                                   self.api_key))
        self.assertHttpCreated(resp)
        resp = self.api_client.post(
            '/api/v1/trait_type/', data=test_trait_type_data,
            authentication='apikey {0}:{1}'.format(test_admin_data['username'],
                                                   self.api_key))
        self.assertHttpCreated(resp)
        trait_type = TraitType.objects.latest('pk')
        test_trait_data_one.update({
            'trait_type': '/api/v1/trait_type/{0}/'.format(trait_type.pk),
        })
        resp = self.api_client.post(
            '/api/v1/trait/', data=test_trait_data_one,
            authentication='apikey {0}:{1}'.format(
                test_admin_data['username'], self.api_key))
        self.assertHttpCreated(resp)
        test_instruction_data_one.update({
            'owner': '/api/v1/user/{0}/'.format(owner.pk),
        })
        resp = self.api_client.post(
            '/api/v1/instruction/', data=test_instruction_data_one,
            authentication='apikey {0}:{1}'.format(
                test_admin_data['username'], self.api_key))
        self.assertHttpCreated(resp)

    def test_beacon_trait_instruction_creation(self):
        beacon = Beacon.objects.latest('pk')
        trait = Trait.objects.latest('pk')
        instruction = Instruction.objects.latest('pk')
        test_data = {
            'beacon': '/api/v1/beacon/{0}/'.format(beacon.pk),
            'trait': '/api/v1/trait/{0}/'.format(trait.pk),
            'instruction': '/api/v1/instruction/{0}/'.format(instruction.pk),
        }
        resp = self.api_client.post(
            '/api/v1/beacon_trait_instruction/', data=test_data,
            authentication='apikey {0}:{1}'.format(
                test_admin_data['username'], self.api_key))
        self.assertHttpCreated(resp)

    def test_beacon_trait_instruction_query(self):
        beacon = Beacon.objects.latest('pk')
        trait = Trait.objects.latest('pk')
        instruction = Instruction.objects.latest('pk')
        test_data = {
            'beacon': '/api/v1/beacon/{0}/'.format(beacon.pk),
            'trait': '/api/v1/trait/{0}/'.format(trait.pk),
            'instruction': '/api/v1/instruction/{0}/'.format(instruction.pk),
        }
        resp = self.api_client.post(
            '/api/v1/beacon_trait_instruction/', data=test_data,
            authentication='apikey {0}:{1}'.format(
                test_admin_data['username'], self.api_key))
        self.assertHttpCreated(resp)
        resp = self.api_client.get(
            '/api/v1/beacon/traits/?pk={0}'.format(beacon.pk),
            authentication='apikey {0}:{1}'.format(
                test_admin_data['username'], self.api_key))
        self.assertHttpOK(resp)
        resp = self.api_client.get(
            '/api/v1/beacon/instructions/?pk={0}&trait_pk={1}'.format(
                beacon.pk, trait.pk),
            authentication='apikey {0}:{1}'.format(
                test_admin_data['username'], self.api_key))
        self.assertHttpOK(resp)

    def test_alternative_beacon_trait_creation(self):
        beacon = Beacon.objects.latest('pk')
        trait = Trait.objects.latest('pk')
        resp = self.api_client.post(
            '/api/v1/beacon/traits/', data={
                'pk': beacon.pk,
                'trait_pk': trait.pk,
            },
            authentication='apikey {0}:{1}'.format(
                test_admin_data['username'], self.api_key))
        self.assertHttpOK(resp)
