def id_to_name(id):
    a = id.split(sep='_')
    b = ''
    if len(a) == 1:
        b = str(a[0])
    else:
        for i in range(len(a) - 1):
            b += a[i] + ' '
        b += a[len(a) - 1]
    return b.capitalize()


class Item:
    """The abstract class for items. Item types will inherit this class' main attributes.
    """
    def __init__(self, id, location, *args):
        self.id = id
        self.name = id_to_name(id)
        self.location = location

    def __str__(self):
        return "{}\nLocated in: {}\n".format(self.name, self.location)


class Stationary(Item):

    def __init__(self, id, location):
        self.name = id_to_name(id)
        super().__init__(id, location)

    def __str__(self):
        return "{}\nLocated in: {}\n".format(self.name, self.location)


class Movable(Item):
    '''Movable items gain pick up and drop methods to move them around'''

    def __init__(self, id, location):
        self.name = id_to_name(id)
        super().__init__(id, location)

    def __str__(self):
        return "{}\nLocated in: {}\n".format(self.name, self.location)

    def PickUp(self):
        if self.location.lower() == CurrentLocation.lower():
            self.location = 'inventory'
        else:
            print('There is no such item here!')

    def Drop(self):
        if self.location.lower() == 'inventory':
            self.location = CurrentLocation
        else:
            print('You are not carrying this item')


class Usable(Item):
    '''Usable Items will get a method that will print a custom piece of text when used. '''

    def __init__(self, id, location, use, text):
        self.use = use
        self.reads = id_to_name(text)
        self.name = id_to_name(id)
        super().__init__(id, location)

    def __str__(self):
        return "{}\nLocated in: {}\nUse Command: \'{}\'".format(self.name, self.location, self.use)


class Door:
    '''The door class includes the rooms the doors connect as well as the door status and door commands. '''

    def __init__(self, dir1, dir2, room1, room2, status):
        self.dir1 = dir1
        self.dir2 = dir2
        self.room1 = room1
        self.room2 = room2
        self.status = status

    def __str__(self):
        return "An {} door connects the {}'s {} side with the {}'s {} side.".format(self.status, self.room1, self.dir1,
                                                                                    self.room2, self.dir2)

    def OpenDoor(self):
        if self.status == 'closed':
            self.status = 'open'
            print('You have opened the door.')
        elif self.status == 'open':
            print('The door is already open')
        else:
            print('You cannot open this door.')

    def UnlockDoor(self):
        fl = False
        for i in range(len(items)):
            if (items[i].name.lower() == 'key') and (items[i].location.lower() == 'inventory'):
                fl = True
        if fl == False:
            print('You do not have a key.')
        if fl == True:
            if self.status == 'locked':
                self.status = 'closed'
                print('You have unlocked the door.')
            else:
                print('The door is already unlocked.')

    def LockDoor(self):
        fl = False
        for i in range(len(items)):
            if (items[i].name.lower() == 'key') and (items[i].location.lower() == 'inventory'):
                fl = True
        if fl == False:
            print('You do not have a key.')
        if fl == True:
            if self.status == 'locked':
                print('The door is already locked')
            else:
                self.status = 'locked'
                print('You lock the door')

    def CloseDoor(self):
        if self.status == 'open':
            self.status = 'closed'
            print('You have closed the door.')
        else:
            print('The door is already closed')


def PickUp(item):
    if item.location.lower() == CurrentLocation.lower():
        item.location = 'inventory'
        print('You picked the {} up.'.format(item.name))
    else:
        print('There is no such item here!')


def Drop(item):
    if item.location.lower() == 'inventory':
        item.location = CurrentLocation
        print('You left the {} on the floor.'.format(item.name))
    else:
        print('You are not carrying such an item')


def UseItem(item):
    print(item.reads)


def StartUp():
    global doors
    global items
    global rooms
    global StartLocation
    global CurrentLocation
    global UseCommands
    global ItemClassID
    doors = []
    items = []
    rooms = []
    ItemClassID = []

    buffer = open('houseconfig.txt').read().split(sep='\n')
    for a in buffer:
        if a.startswith('room'):
            rooms.append(a.split()[1])
        if a.startswith('door'):
            doors.append(
                Door(a.split()[1].split(sep='-')[0], a.split()[1].split(sep='-')[1], a.split()[3], a.split()[4],
                     a.split()[2]))
        if a.startswith('item'):
            if a.split()[3].lower() == 'stationary':
                items.append(Stationary(a.split()[1], a.split()[2]))
                ItemClassID.append(0)
            if a.split()[3].lower() == 'movable':
                items.append(Movable(a.split()[1], a.split()[2]))
                ItemClassID.append(1)
            if a.split()[3].lower() == 'usable':
                items.append(Usable(a.split()[1], a.split()[2], a.split()[4], a.split(maxsplit=5)[5]))
                ItemClassID.append(
                    2)
        if a.startswith('start'):
            StartLocation = a.split()[1]
            CurrentLocation = StartLocation


def LookAround():
    print('You are now in the {}.\n'.format(CurrentLocation.capitalize()))
    flag = False
    for i in range(len(items)):
        if items[i].location.lower() == CurrentLocation.lower():
            flag = True
    if flag == True:
        print('You can see the following item(s) in the room:', end='\n')
        for i in range(len(items)):
            if items[i].location.lower() == CurrentLocation.lower():
                print(items[i])

    for i in range(len(doors)):
        if doors[i].room1.lower() == CurrentLocation.lower():
            print('There is a(n) {} door on the {} of the room that leads to the {}.'.format(doors[i].status,
                                                                                             doors[i].dir1,
                                                                                             doors[i].room2))
        if doors[i].room2.lower() == CurrentLocation.lower():
            print('There is a(n) {} door on the {} of the room that leads to the {}.'.format(doors[i].status,
                                                                                             doors[i].dir2,
                                                                                             doors[i].room1))


def ViewInventory():
    flag1 = False
    for i in range(len(items)):
        if items[i].location.lower() == 'inventory':
            flag1 = True
    if flag1 == False:
        print('You are carrying nothing')
    else:
        print('You are carrying the following item(s)')
        for i in range(len(items)):
            if items[i].location.lower() == 'inventory':
                print(items[i])


def Move(To):
    global CurrentLocation
    valid = False
    for i in range(len(doors)):
        if (CurrentLocation.lower() == doors[i].room1.lower()) and (To.lower() == doors[i].dir1.lower()) and (
                doors[i].status.lower() == 'open'):
            CurrentLocation = doors[i].room2
            valid = True
            print('You are now in the {}.'.format(CurrentLocation))
            break
        if (CurrentLocation.lower() == doors[i].room2.lower()) and (To.lower() == doors[i].dir2.lower()) and (
                doors[i].status.lower() == 'open'):
            CurrentLocation = doors[i].room1
            valid = True
            print('You are now in the {}.'.format(CurrentLocation))
            break
    if valid == False:
        print('Invalid Move. Either there is no door there or the door is closed')


def ShowCommands():
    print("""Commands:
      'move d': moves you to an adjacent room if the door leading there is open
      'open d': opens a closed door in the direction d
      'close d': closes an open door in the direction d
      'lock d': locks an unlocked door in the direction d
      'unlock d': unlocks a locked door in the direction d
      'pick up x': picks an item up
      'drop x': drops an item on the ground
      'look around': tells you about your surroundings
      'inventory': Gives you info on items you are carrying(including special uses)
      'commands':Brings up this reminder
      'quit': Quits the game!
      *Directions are: N,S,E,W""")


def PlayerInput():
    global CurrentLocation
    plinput = input('What would you like to do next?\n').lower()
    listofmoves = []
    listofdirections = ['n', 's', 'e', 'w']
    movableitems = []
    usableitems = []
    Usecommands = []
    for i in range(len(items)):
        if ItemClassID[i] > 0:
            movableitems.append(items[i].name.lower())
        if ItemClassID[i] == 2:
            usableitems.append(items[i].name.lower())
            Usecommands.append(items[i].use.lower() + ' ' + items[i].name.lower())
    for i in range(len(doors)):
        listofmoves.append(doors[i].room1.lower() + ' ' + doors[i].dir1.lower())
        listofmoves.append(doors[i].room2.lower() + ' ' + doors[i].dir2.lower())
    if plinput.lower().startswith('move'):
        if (CurrentLocation.lower() + ' ' + plinput.lower().split()[1]) in listofmoves:
            Move(plinput.lower().split()[1])
            return 0
        else:
            print('That is not a valid move')
    elif plinput.startswith('open'):
        if plinput.split()[1] in listofdirections:
            for i in range(len(doors)):
                if plinput.split()[1].lower() == doors[i].dir1.lower() and CurrentLocation.lower() == doors[
                    i].room1.lower():
                    doors[i].OpenDoor()
                    return 0
                if plinput.split()[1].lower() == doors[i].dir2.lower() and CurrentLocation.lower() == doors[
                    i].room2.lower():
                    doors[i].OpenDoor()
                    return 0
    elif plinput.startswith('close'):
        if plinput.split()[1] in listofdirections:
            for i in range(len(doors)):
                if plinput.split()[1].lower() == doors[i].dir1.lower() and CurrentLocation.lower() == doors[
                    i].room1.lower():
                    doors[i].CloseDoor()
                    return 0
                if plinput.split()[1].lower() == doors[i].dir2.lower() and CurrentLocation.lower() == doors[
                    i].room2.lower():
                    doors[i].CloseDoor()
                    return 0
    elif plinput.startswith('lock'):
        if plinput.split()[1] in listofdirections:
            for i in range(len(doors)):
                if plinput.split()[1].lower() == doors[i].dir1.lower() and CurrentLocation.lower() == doors[
                    i].room1.lower():
                    doors[i].LockDoor()
                    return 0
                if plinput.split()[1].lower() == doors[i].dir2.lower() and CurrentLocation.lower() == doors[
                    i].room2.lower():
                    doors[i].LockDoor()
                    return 0
    elif plinput.startswith('unlock'):
        if plinput.split()[1] in listofdirections:
            for i in range(len(doors)):
                if plinput.split()[1].lower() == doors[i].dir1.lower() and CurrentLocation.lower() == doors[
                    i].room1.lower():
                    doors[i].UnlockDoor()
                    return 0
                if plinput.split()[1].lower() == doors[i].dir2.lower() and CurrentLocation.lower() == doors[
                    i].room2.lower():
                    doors[i].UnlockDoor()
                    return 0
    elif plinput.lower() == 'look around':
        LookAround()
        return 0
    elif plinput.lower() == 'quit':
        quit()
    elif plinput.lower() == 'commands':
        ShowCommands()
        return 0
    elif plinput.lower() == 'inventory':
        ViewInventory()
        return 0
    elif plinput.startswith('pick up') and (((' '.join(plinput.split()[2:])).lower()) in movableitems):
        for i in range(len(items)):
            if (' '.join(plinput.split()[2:])).lower() == items[i].name.lower():
                PickUp(items[i])
                return 0
    elif plinput.startswith('drop') and plinput.split()[1] in movableitems:
        for i in range(len(items)):
            if (' '.join(plinput.split()[1:])).lower() == items[i].name.lower():
                Drop(items[i])
                return 0
    elif (plinput.startswith('use') or (plinput.lower() in Usecommands)) and ' '.join(plinput.split()[1:]) in movableitems:
        try:
            for i in range(len(items)):
                if (' '.join(plinput.split()[1:])).lower() == items[i].name.lower() and ((items[i].location.lower()=='inventory') or (items[i].location.lower()==CurrentLocation.lower())):
                    UseItem(items[i])
                    return 0
        except:
            for i in range(len(Usecommands)):
                if plinput.lower() == Usecommands[i] and ((items[i].location.lower()=='inventory') or (items[i].location.lower()==CurrentLocation.lower())):
                    index = i
                    UseItem(items[index].name)
                    return 0
    return 1


StartUp()
ShowCommands()
LookAround()

playing = True
while playing == True:
    p_input = PlayerInput()
    if p_input != 0:
        print('Invalid command.')
