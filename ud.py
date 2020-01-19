import random
import threading
import datetime
import collections
import itertools

from utils import synchronized, PlayerStack

class Event:
    def __init__(self, source, target):
        self.source = source
        self.target = target
        
    def affected(self, player):
        return (self.is_global and player != self.source) or player == self.target

    @property
    def is_global(self):
        return False
    
    def format(self, player):
        pass
    
    def format_spectactor(self):
    	pass

class FAKEvent(Event):
    def __init__(self, source, target, amount, health, infected):
        Event.__init__(self, source, target)
        self.amount = amount
        self.infected = infected
        self.health = health

    def affected(self, player):
        return player == self.target and player != self.source

    def format(self, player):
        result = []
        if player == self.target:
            result.append("{} healed you for {} HP.".format(self.source.name, self.amount))
            if self.infected:
                result.append(" You are no longer infected.")
    
    def format_spectator(self):
        result = []
        target_name = self.target.name if self.target is not self.source else "themself"
        result.append("{} healed {} for {} HP. Taking them to {}. ".format(self.source.name, target_name, self.amount, self.health))
        if self.infected:
                result.append(" They cured an infection.")
        
        return "".join(result)

class AttackEvent(Event):
    def __init__(self, source, target):
        Event.__init__(self, source, target)
        self.target_hp = target.health

    @property
    def is_global(self):
        return self.target_hp == 0
		    
class ZombieAttackEvent(AttackEvent):
    def __init__(self, source, target, damage, verb, grasped, infected, gain):
        AttackEvent.__init__(self, source, target)
        self.source = source
        self.target = target
        self.damage = damage        
        self.verb = verb
        self.grasped = grasped
        self.infected = infected
        self.gain = gain
                
    def format(self, player):
        if self.target == player:
            return self._format_target(player)
        elif self.is_global:
            return "{} killed {}.".format(self.source.display_name(A, UPPER), self.target.display_name(A, LOWER))
        else:
            raise Exception("This event is not meant to be consumed by {}".format(player.name))
    
    def format_source(self):
        event = []
        event.append("You {} {} for {} damage".format(self.verb[0], self.target.display_name(A, LOWER), self.damage))
                
        if self.target_hp == 0:
           event.append(". They die")
        else:
            if self.grasped:
                event.append(" and grab hold of their blue jacket")
            
            if self.infected:
                event.append(". They become infected")
        
            event.append(". They drop to {} HP".format(self.target_hp))
            
        if self.gain != 0:
            event.append(". You gain {}".format(self.gain))
            
        event.append(".")
        
        return "".join(event)

    def format_spectator(self):
        event = []
        event.append("{} {} {} for {} damage.".format(self.source.name, self.verb[1], self.target.name, self.damage))

        if self.infected:
                event.append(" The bite was infected.")
        
        if self.grasped:
            event.append(" The zombie grabbed hold of them!")
            
        if self.target_hp == 0:
            event.append(" They were killed by the zombie.")
        else:
            event.append(" They drop to {} HP.".format(self.target_hp))
    	  	
        return "".join(event)
    	        
    def _format_target(self, player):
        event = []
        event.append("A zombie {} you for {} damage.".format(self.verb[1], self.damage))
        
        if self.infected:
            event.append("The zombie's bite was infected.")
        
        if self.grasped:
            event.append("The zombie grabbed hold of you!")
            
        if self.target_hp == 0:
            event.append("You were killed by the zombie.")
        
        return " ".join(event)
    
class ZombieGripLostEvent(Event):
    def affected(self, player):
        return self.target == player
    
    def format(self, player):
        assert self.target == player, "This event is meant only for target player"
        return "The zombie lost its grip."
    
    def format_spectator(self):
    	return "{} lost its grip on {}".format(self.source.name, self.target.name)
        
class HumanAttackEvent(AttackEvent):
    def __init__(self, source, target, weapon, damage):
        AttackEvent.__init__(self, source, target)
        self.weapon = weapon
        self.target = target
        self.damage = damage
    
    def format(self, player):
        if self.target == player:
            return self._format_target(player)
        elif self.is_global:
            return "{} killed {}.".format(self.source.display_name(A, UPPER), self.target.display_name(A, LOWER))
        else:
            raise Exception("This event is not meant to be consumed by {}".format(player.name))

    def format_source(self):
        event = []
        event.append("You {} {} for {} damage".format(self.weapon.source_text, self.target.display_name(THE, LOWER), self.damage))
                
        if self.target_hp == 0:
           event.append(". They die")
        else:
            event.append(". They drop to {} HP".format(self.target_hp))
            
        event.append(".")        
        return "".join(event)

    def format_spectator(self):
        event = []
        attack_text = self.weapon.spectator_text.format(self.target.name)
        event.append("{} {} for {} damage.".format(self.source.name, attack_text, self.damage))
        
        if self.target_hp == 0:
            event.append(" They were killed.")
        else:
            event.append(" They drop to {} HP.".format(self.target_hp))
            
        return " ".join(event)
    	    
    def _format_target(self, player):
        event = []
        event.append("{} {} for {} damage.".format(self.source.name, self.weapon.target_text, self.damage))
        
        if self.target_hp == 0:
            event.append("You were killed by {}.".format(self.source.name))
            
        return " ".join(event)
    
class SpectatorEvent(Event):
    def __init__(self, source, target):
        Event.__init__(self, source, target)

    def affected(self, player):
        return False

    def format(self, player):
        raise NotImplementedError("This event is meant to be consumed only by spectators")

    def format_spectator(self):
        pass

class ZombieMissEvent(SpectatorEvent):
    def __init__(self, source, target, verb):
        SpectatorEvent.__init__(self, source, target)
        self.verb = verb

    def format_spectator(self):
        return "{} tries to {} {} and misses.".format(self.source.name, self.verb, self.target.name)

class HumanMissEvent(SpectatorEvent):
    def __init__(self, source, target, weapon_name):
        SpectatorEvent.__init__(self, source, target)
        self.weapon_name = weapon_name
    
    def format_spectator(self):
        return "{} attacks {} with {} and misses.".format(self.source.name, self.target.name, self.weapon_name)

class ReloadEvent(SpectatorEvent):
    def __init__(self, source, weapon_name):
        SpectatorEvent.__init__(self, source, source)
        self.weapon_name = weapon_name

    def format_spectator(self):
        return "{} reloads their {}".format(self.source.name, self.weapon_name)

class InfectionEvent(SpectatorEvent):
	def __init__(self, target):
		SpectatorEvent.__init__(self, target, target)
		self.target_hp = target.health
		
	def format_spectator(self):
		return "{} lost 1 HP due to infection. They dropped to {}.".format(self.target.name, self.target_hp)

class EventCollection:
    def __init__(self):
        self.collection = []
    
    def __iter__(self):
    	return iter(self.collection)
    	
    def __len__(self):
        return len(self.collection)
        
    def add(self, event):
        self.collection.append(event)
        
    def affected(self, start, player):
        for event in self.collection[start:]:
            if event.affected(player):
                yield event
    
Attack = collections.namedtuple("Attack", ["name", "action", "chance", "damage"])

A = 0
THE = 1
LOWER = 0
UPPER = 1

class Player:
    def __init__(self, id, name, team, events):
        self.id = id
        self.health = 60
        self.ap = 50
        self.events = events
        self.last_event = 0
        self.infected = False
        self.grasp = None
        self.name = name
        self.team = team
        self.ready = False

        self.last_weapon = None
        self.last_target = None
    
    def display_name(self, article, case):
        return self.name

    @property
    def available_attacks(self):
        raise NotImplementedError()

    def attack(self, action, target):
        raise NotImplementedError()

    def harm(self, amount):
        self.health = max(0, self.health - amount)
        return amount
    
    def add_event(self, event):
        self.events.add(event)
        
    @property
    def dead(self):
        return self.health == 0
    
    def get_new_events(self):
        result = [e.format(self) for e in self.events.affected(self.last_event, self)]
        self.last_event = len(self.events)
        return result

class Zombie(Player):
    _article = ("a", "the")

    def __init__(self, id, name, team, events):
        Player.__init__(self, id, name, team, events)
        self.grasping = None

    def display_name(self, article, case):
        article_str = Zombie._article[article]
        if case == UPPER:
            article_str = article_str.capitalize()
        
        return  "{} zombie".format(article_str)
        
    def _attack(self, target, damage, chance, can_infect, can_grasp, can_heal, verb):
        if target.health == 0:
            return "Your target is no longer here."
        
        self.ap -= 1
        
        if target.grasp == self:
            chance += 0.1
        
        if random.random() <= chance:            
            damage = target.harm(damage)                        
            grasped = False
            infected = False
            gain = 0
            
            if not target.dead:                                
                if can_grasp and self._try_grasp(target):
                    grasped = True
                if can_infect and not target.infected:
                    target.infected = True
                    infected = True                                                                
            
            if can_heal:
                gain = damage if self.health + damage <= 60 else 60 - self.health
                self.health += gain                
            
            event = ZombieAttackEvent(self, target, damage, verb, grasped, infected, gain)
            self.add_event(event)
            return event.format_source()
            
        else:
            message = "You attack {} and miss.".format(target.display_name(THE, LOWER), damage)
            self.add_event(ZombieMissEvent(self, target, verb[0]))
            if target.grasp == self and random.random() <= 0.5:
                message += " You loose your grasp."
                self._release_grasp()
                self.add_event(ZombieGripLostEvent(self, target))
            return message
        
    @property
    def available_attacks(self):
        return [ Attack("hands", "maul", 50, 3), Attack("teeth", "teeth", 30, 4)]

    def attack(self, action, target):
        if action == "maul":
            return self.hands(target)
        elif action == "teeth":
            return self.bite(target)

    def hands(self, target):
        return self._attack(target, 3, 0.5, False, True, False, ("maul", "clawed at"))

    def bite(self, target):
        return self._attack(target, 4, 0.3, True, False, True, ("bite", "bit into"))

    def _try_grasp(self, target):
        if target.grasp != self:
                if target.grasp is not None:
                    return False #if someone else is grasping the player, grasp fails, UD might handle this diferently
                if self.grasping != None:
                    self.grasping.grasp = None
                    self.grasping = None
                    
                target.grasp = self
                self.grasping = target
                return True
                
        return False
    
    def _release_grasp(self):
        self.grasping.grasp = None
        self.grasping = None

class Item:
    action_map = {}
    def __init__(self, name = None, action="", target=False):
        self.name = name
        self.action = action
        self.target = target

        if action not in Item.action_map:
            Item.action_map[action] = name
        
    def use(self, owner, target):
        return (False, None)
    
class FirstAidKit(Item):
    def __init__(self):
        Item.__init__(self, "first-aid kit", "use-h", True)
    
    def use(self, owner, target):
        assert target.health <= 60
        
        if target.health == 60:
            return (False, "{} is already at full health".format(target.display_name(THE, UPPER)))
        
        amount = 10 if target.health + 10 <= 60 else 60 - target.health
        target.health += amount

        infected = target.infected
        if infected:
            target.infected = False

        target.add_event(FAKEvent(owner, target, amount, target.health, infected))

        message = []
        if target == owner:
            message.append("You heal yourself for {} HP.".format(amount))
            if infected:
                message.append(" You cure your infection.")
        else:
            message.append("You heal {} for {} HP.".format(target.display_name(THE, LOWER), amount))
            if infected:
                message.append(" You cure their infection.")

        return (True, "".join(message))
    
class Weapon(Item):
    def __init__(self, name, action, chance, damage, source_text, target_text, spectator_text):
        Item.__init__(self, name, action)
        self.chance = chance
        self.damage = damage
        self.source_text = source_text
        self.target_text = target_text
        self.spectator_text = spectator_text
    
    @property
    def has_ammo(self):
        return True
    
    def spend(self):
        pass

class Ammo(Item):
    def __init__(self, name, action, weapon, amount, max_amount):
        Item.__init__(self, name, action)
        
        self.weapon = weapon
        self.amount = amount
        self.max_amount = max_amount
    
    def use(self, owner, target):
        if target != owner:
            return (False, "This item can't be used on someone else.")
        
        weapons = owner.get_item(self.weapon)
        
        if len(weapons) == 0:
            return (False, "You don't have a {}".format(self.weapon))
        

        weapon = min(weapons, key=lambda x: x.shots)
        
        if weapon.shots == self.max_amount:
            return (False,"You dont have any {}s that need reloading.".format(self.weapon))
                
        weapon.shots = min(self.max_amount, weapon.shots + self.amount)
        owner.add_event(ReloadEvent(owner, weapon.name))
        return (True, "You reload your {}.".format(self.weapon))
        

class Firearm(Weapon):
    def __init__(self, name, action, chance, damage, shots, source_text, target_text, spectator_text):
        Weapon.__init__(self, name, action, chance, damage, source_text, target_text, spectator_text)
        self.shots = shots
    
    @property
    def has_ammo(self):
        return self.shots > 0
        
    def spend(self):
        if self.has_ammo:
            self.shots -= 1

fak = FirstAidKit()

knife = Weapon("knife", "knife", 0.5, 2, "stab", "stabbed you", "stabbed {}")
axe = Weapon("fire axe", "axe", 0.4, 3, "attack", "attacked you with an axe", "attacked {} with an axe")

clip = Ammo("pistol clip", "use-k", "pistol", 6, 6)
shell = Ammo("shotgun shell", "use-r", "shotgun", 1, 2)

def pistol(shots=6): return Firearm("pistol", "pistol", 0.65, 5, shots, "fire your pistol at", "shot you with a pistol", "shot {} with a pistol")
def shotgun(shots=2): return Firearm("shotgun", "shotgun", 0.65, 10, shots, "fire your shotgun at", "shot you with a shotgun", "shot {} with a shotgun")

def apply_infection(func):
    def wrapper(self, *args, **kwargs):
        old = self.ap
        result = func(self, *args, **kwargs)
        if self.infected and self.ap != old:
            self.harm(1)
            self.add_event(InfectionEvent(self))
            if result is None:
                result = ""
            else:
                result += " "
            
            result += "You loose 1 hp due to your infection."
        return result

    return wrapper

punch = Weapon("punch", "punch", 0.25, 1, "attack", "punched you", "punched {}")
class Human(Player):
    def __init__(self, id, name, team, events):
        Player.__init__(self, id, name, team, events)
        self._inventory = {}
        
    @property
    def available_attacks(self):        
        weapons = itertools.chain((punch,), 
            (items[0] for items in self._inventory.values() if len(items) > 0 and isinstance(items[0], Weapon))
        )

        return [Attack(weapon.name, weapon.action, int(weapon.chance * 100), weapon.damage) for weapon in weapons]

    @apply_infection
    def attack(self, action, target):
        if action == "punch":
            return self._punch(target)
        else:
            if action not in Item.action_map:
                raise ValueError("Unknown weapon")

            return self._attack_from_inventory(Item.action_map[action], target)

    @property
    def inventory(self):
        for item_collection in self._inventory.values():
            for item in item_collection:
                yield item

    def add_item(self, item):
        if item.name not in self._inventory:
            self._inventory[item.name] = []
        
        self._inventory[item.name].append(item)

    def _punch(self, target):
        return self._attack_weapon(punch, target)

    def _attack_from_inventory(self, weapon_name, target):
        weapons = self.get_item(weapon_name)
        if len(weapons) == 0:
            return "You don't have {}.".format(weapon_name)
                
        for weapon in weapons:
            if weapon.has_ammo:
                break
        else:
            return "Your {} is empty".format(weapon.name)

        return self._attack_weapon(weapon, target)
            
    def _attack_weapon(self, weapon, target):
        if not isinstance(weapon, Weapon):
            raise Exception("{} not a weapon".format(weapon.name))
        
        if target.health == 0:
            return "Your target is no longer here."
                
        self.ap -= 1                
        weapon.spend()
        
        if random.random() <= weapon.chance:
            damage = target.harm(weapon.damage)            
            event = HumanAttackEvent(self, target, weapon, damage)
            self.add_event(event)
            return event.format_source()
        else:
            self.add_event(HumanMissEvent(self, target, weapon.name))
            return "You attack with your {} and miss.".format(weapon.name)


    @apply_infection
    def use(self, item_name, target):
        if item_name in Item.action_map:
            item_name = Item.action_map[item_name]

        items = self.get_item(item_name)
        if len(items) == 0:
            return "You don't have {}.".format(item_name)
        
        item = items[-1]
        result, message = item.use(self, target)        
        
        if result:
            self.ap -= 1
            items.pop()

        return message
    
    def get_item(self, name):
        if name not in self._inventory:
            return []
        return self._inventory[name]
    
WAITING = 0
READY = 1
STARTED = 2
FINISHED = 3

VICTORY = 1
DRAW = 0

USE = 0
ATTACK = 1

Action = collections.namedtuple("Action", ["type", "item"])
DoResult = collections.namedtuple("DoResult", ["finished", "template_dict"])
VictoryStatus = collections.namedtuple("VictoryStatus", ["result", "team"])

class Game:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.events = EventCollection()
        self.players = {}
        self.humans = PlayerStack()
        self.zombies = PlayerStack()
        self.host = None
        self.lock = threading.RLock()
               
        self.ready = 0
        self.start_time = None
        self.finished = False
        self.victory_status = None
        self.lobby_version = 0

    @property
    def teams(self):
        return ("A", "B")

    @property
    @synchronized
    def state(self):
        if self.start_time is None:
            return WAITING
        elif datetime.datetime.utcnow() < self.start_time:
            return READY
        elif not self.finished:
            return STARTED
        else:
            return FINISHED

    @property
    def state_str(self):
        state = self.state
        if state == WAITING:
            return "WAITING"
        elif state == READY:
            return "READY"
        elif state == STARTED:
            return "STARTED"
        elif state == FINISHED:
            return "FINISHED"

        raise ValueError("Unknown state")

    @property
    @synchronized
    def status(self):
        return (self.state_str, self.lobby_version)

    @synchronized
    def do(self, session, action=None, target=None):
        if session not in self.players:
            raise ValueError("You have not joined this game.")

        if self.state == WAITING:
            raise ValueError("Game has not yet started")

        if self.state == FINISHED:
            return DoResult(True, None)
            
        player = self.players[session]
        result = {"name":player.name}

        is_zombie = isinstance(player, Zombie)

        message = None
        
        if target is not None:
            player.last_target = target

        if player.last_target is not None:
            result["last_target"] = player.last_target

        target, message, action = self._resolve_target(target, message, action, player)
                
        old_ap = player.ap
        (someone_died, (message, target)) = self._check_killed(
            [x for x in (player, target) if x is not None],
            lambda: self._perform_action(action, player, target),
            self._remove_from_stack
        )

        ap_spent = player.ap == 0 and old_ap != 0

        if player.last_weapon is not None:
            result["last_weapon"] = player.last_weapon

        if someone_died or ap_spent:
            self._check_if_finished()        

        if message is not None:
            result["message"] = message

        result["since_last_turn"] = player.get_new_events()
        
        if hasattr(player, "inventory"):
            result["inventory"] = list(player.inventory)
        
        result["health"] = player.health
        result["ap"] = player.ap
        result["team"] = player.team

        result["humans"] = [other for other in self.humans if other is not player]
        (result["zombies"], result["same_team_zombies"]) = self._get_zombies(player)

        result["dead"] = player.dead or is_zombie
        result["attacks"] = player.available_attacks

        result["is_zombie"] = is_zombie
        result["player_id"] = player.id        

        return DoResult(self.state == FINISHED, result)

    def _remove_from_stack(self, player):
        if isinstance(player, Zombie):
            self.zombies.remove(player)
        else:
            self.humans.remove(player)
        

    def _update_stack(self, player):
        if isinstance(player, Zombie):
            self.zombies.update(player)
        else:
            self.humans.update(player)

    def _get_zombies(self, player):
        same_team_zombies = 0
        zombies = []

        for z in self.zombies:
            if z is not player:
                if z.team == player.team:
                    same_team_zombies += 1
                zombies.append(z)

        return (zombies, same_team_zombies)
            
    def _check_if_finished(self):
        assert self.state == STARTED

        surviving_teams = set(player.team for player in self.players.values() if not player.dead)

        if len(surviving_teams) == 1:
            self.finished = True
            self.victory_status = VictoryStatus(VICTORY, next(iter(surviving_teams)))
        elif len(surviving_teams) == 0 or all(player.ap == 0 for player in self.players.values() if not player.dead):
            self.finished = True
            self.victory_status = VictoryStatus(DRAW, None)
        

    def _check_killed(self, players, action, on_killed):        
        before_action = [x.dead for x in players]
        action_result = action()

        result = False
        for player, old in zip(players, before_action):
            if old != player.dead:
                assert player.dead, "returning to life is not expected"
                result = True
                on_killed(player)

        return (result, action_result)

    def _perform_action(self, action, player, target):
        message = None
        if action is not None:
            if self.state == READY:
                message = "The game has not yet started, try again in a few seconds"
            elif player.ap == 0:
                message = "You have run out of Action Points."
            elif player.health == 0:
                message = "You can't do that, you are dead."
            elif action.type == USE:
                if isinstance(player, Human):                                    
                    if target is None:
                        target = player
                    message = player.use(action.item, target)
                    self._update_stack(player)
                else:
                    message = "You can't use items, you are dead."
            elif action.type == ATTACK:
                if target == None:
                    raise ValueError("Invalid target, attack must specify a target")
                message = player.attack(action.item, target)
                self._update_stack(player)
                player.last_weapon = action.item

        return (message, target)


    def _resolve_target(self, target, message, action, current_player):
        if target is None or target == "":
            return (None, message, action)

        if target is not None:
            if target == "z":                
                for player in self.zombies:
                    if player != current_player:
                        return (player, message, action)
                else:
                    return (None, None, "There are no zombies here.")
            else:
                target = int(target)
                if target not in self.players:
                    raise ValueError("Unknown player {}".format(target))
                return (self.players[target], message, action)


    @synchronized
    def create_player(self, name, cls, id, team):
        if name == "":
            raise ValueError("Player name cannot be empty")
        if cls not in ["Human", "Zombie"]:
            raise ValueError("Invalid class")

        player = None
        if cls == "Human":
            player = Human(id, name, team, self.events)
            player.add_item(knife)
            player.add_item(axe)
            player.add_item(pistol())
            player.add_item(shotgun(1))
            player.add_item(FirstAidKit())
            player.add_item(clip)
            player.add_item(clip)
            player.add_item(shell)
            player.add_item(shell)
            self.humans.update(player)
        else:
            assert cls == "Zombie"
            player = Zombie(id, name, team, self.events)
            self.zombies.update(player)

        self.players[id] = player
        self.lobby_version += 1
        return player

    @synchronized
    def player_ready(self, id):
        if self.state == WAITING and len(self.players) > 1:
            player = self.try_get(id)

            if player is None:
                raise ValueError("Invalid id")

            for team in self.teams:
                if len(self.team(team)) == 0:
                    raise ValueError("Team {} is empty".format(team))

            if not player.ready:
                player.ready = True                
                self.lobby_version += 1
                self.ready += 1

                if self.ready == len(self.players):
                    self.start_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=2)

    @synchronized
    def player_kick(self, host_id, player_id):
        host_id = int(host_id)
        player_id = int(player_id)

        host = self.try_get(host_id)
        if host is None or host is not self.host:
            raise ValueError("Invalid host_id")

        player = self.try_get(player_id)
        
        if player is None:
            raise ValueError("Invalid player_id")

        if player is host:
            raise ValueError("You can't kick yourself")

        self._remove_from_stack(self.players[player.id])
        del self.players[player.id]
        self.lobby_version += 1

        if isinstance(player, Zombie):
            self.zombies -= 1

    @synchronized
    def player_switch(self, player_id):
        player_id = int(player_id)
        player = self.try_get(player_id)

        if player is None:
            raise ValueError("Invalid player_id")

        team = player.team
        player.team = self.teams[(self.teams.index(team)+1)%len(self.teams)]
        self.lobby_version += 1

    @synchronized
    def team(self, team_name):
        return [player for player in self.players.values() if player.team == team_name]

    @synchronized
    def __contains__(self, id):
        return self.players[id]

    @synchronized
    def try_get(self, id):
        if id in self.players:
            return self.players[id]
        else:
            return None
    
    @property
    def done(self):
        return False

class GameCollection:
    def __init__(self, max_games=256):
        self.games = {}
        self.ordered_games = []
        self.lock = threading.RLock()
        self.max_games = max_games
        self.games_created = 0

    @synchronized
    def __contains__(self, id):
        return id in self.games

    @synchronized
    def try_get(self, id):
        if id in self.games:
            return self.games[id]
        else:
            return None

    @synchronized
    def create_game(self, name, host_name, host_cls, host_id):
        id = self._get_id()
        game = Game(name, id)
        host = game.create_player(host_name, host_cls, host_id, "A")
        game.host = host

        self.games[id] = game
        self.ordered_games.append(game)

        if len(self.ordered_games) > self.max_games:
            self._cleanup()

        self.games_created += 1
        return game

    def _get_id(self):
        while True:
            id = random.randrange(0, 2**32)
            if id not in self.games:
                return id

    def _cleanup(self):
        to_remove = []
        for i, game in enumerate(self.ordered_games):
            if game.done:
                to_remove.append(i)

            if len(self.ordered_games) - len(to_remove) <= self.max_games:
                break

        for index in to_remove:
            game = self.ordered_games[index]
            del self.ordered_games[index]
            del self.games[game.id]
