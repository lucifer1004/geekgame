import os
import signal
# import verify
# import comm
import functools
print = functools.partial(print, flush=True)
TIMEOUT = 600000
PLAYER_INIT_MONEY = 500
SALER_INIT_MONEY = 10000
DISCOUNT = 0.9
MAX_LINES = 100


class Commodity:

    def __init__(self, name, desc, price, num):
        self.name = name
        self.desc = desc
        self.price = price
        self.num = num


class Merchant:

    def __init__(self, money):
        self.money = money
        self.possession = dict()

    def gain_commodity(self, commodity, num):
        self.possession[commodity] = self.possession.get(commodity, 0) + num

    def gain_money(self, money):
        self.money += money

    def take_commodity(self, commodity, num):
        new_num = self.possession.get(commodity, 0) - num
        if new_num < 0:
            raise ValueError('no enough commodity')
        self.possession[commodity] = new_num
        if new_num == 0:
            del self.possession[commodity]

    def take_money(self, money):
        if self.money < money:
            raise ValueError('no enough money')
        self.money -= money


def load_commodities():
    global commodities
    commodities = []
    for name, data in [('citrine', {'desc': 'C', 'price': 250}), ('jade', {'desc': 'J', 'price': 375}), ('onyx', {'desc': 'O', 'price': 500}), ('emerald', {'desc': 'E', 'price': 750}), ('sapphire', {'desc': 'S', 'price': 1000}), ('ruby', {'desc': 'R', 'price': 1250}), ('flag', {'desc': 'F', 'price': 100000})]:
        commodities.append(Commodity(name, data['desc'], data['price'], 1))
    else:
        commodities.sort(key=(lambda c: c.price))


def find_commodity(name):
    for c in commodities:
        if c.name == name:
            return c


def build_saler():
    saler = Merchant(SALER_INIT_MONEY)
    for c in commodities:
        num = 1 if c.name == 'flag' else 10
        saler.gain_commodity(c.name, num)
    else:
        return saler


def build_player():
    player = Merchant(PLAYER_INIT_MONEY)
    player.gain_commodity(commodities[0].name, 1)
    return player


def _check_transaction(filename):
    global player
    global saler
    transaction = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            if line.startswith('#'):
                pass
            else:
                try:
                    line = line.split()
                    name, num = line[0], int(line[1])
                    c = find_commodity(name)
                    if c is None:
                        raise ValueError('%s: invalid name' % name)
                    money = c.price * num
                    if num > 0:
                        if name not in saler.possession:
                            raise ValueError('%s: not available' % name)
                        else:
                            if name == 'flag':
                                raise ValueError('%s: not for sale' % name)
                            if saler.possession[name] < num:
                                raise ValueError('%s: too much to buy' % name)
                            if player.money < money:
                                raise ValueError('%s: too expensive' % name)
                            transaction.append('buy %d %s ($%d)' %
                                               (num, name, money))
                    else:
                        money = int(-money * DISCOUNT)
                        print(player.possession)
                        if name not in player.possession:
                            raise ValueError('%s: not available' % name)
                        if player.possession[name] < -num:
                            raise ValueError('%s: too much to sale' % name)
                        if saler.money < money:
                            raise ValueError('%s: too expensive' % name)
                        transaction.append('sale %d %s ($%d)' %
                                           (-num, name, money))
                except Exception as e:
                    raise e

    return transaction


def _perform_transaction(filename):
    with open(filename, 'r') as f:
        for line in f.readlines():
            if line.startswith('#'):
                continue
            else:
                try:
                    line = line.split()
                    name, num = line[0], int(line[1])
                    c = find_commodity(name)
                    money = c.price * num
                    if num > 0:
                        player.take_money(money)
                        player.gain_commodity(name, num)
                        saler.gain_money(money)
                        saler.take_commodity(name, num)
                    else:
                        money = int(-money * DISCOUNT)
                        player.gain_money(money)
                        player.take_commodity(name, -num)
                        saler.take_money(money)
                        saler.gain_commodity(name, -num)
                except ValueError as e:
                    print(e)
                    return False
                except Exception as e:
                    print(e)
                    return False
        return True


def check_transaction(filename):
    try:
        transaction = _check_transaction(filename)
        print('You are going to:')
        print('\n'.join(transaction))
        print('Type \'y\' to confirm: ')
        if input() == 'y':
            print('confirmed')
            return True
        else:
            print('cancelled')
            return False
    except ValueError as e:
        print(e)
        return False
    except Exception as e:
        print(e)
        return False


def perform_transaction(filename):
    return _perform_transaction(filename)


def banner():
    print('Welcome to the store.')
    print('What do you want to do?')
    print("Type 'help' for help.")


if __name__ == '__main__':
    signal.alarm(TIMEOUT)
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    token = input('token: ')
    # if verify.validate(token) is None:
    #     print('wrong token')
    #     exit()
    # comm.set_token(token)
    load_commodities()
    saler = build_saler()
    player = build_player()
    banner()
    while True:
        while True:
            try:
                cmd = input('\n> ')
            except EOFError:
                print('bye')
                exit(0)
            if cmd == 'help':
                print('help: show help message')
                print('inspect: show your possessions')
                print('list: show commodities in the store')
                print('trade: start a transaction')
                print()
                print('an example for trade:')
                print('jade 1 (buy 1 jade)')
                print('citrine -1 (sale 1 citrine)')
                print('END (trade ends)')

            elif cmd == 'inspect':
                print('You have $%d, and' % player.money)
                if len(player.possession) == 0:
                    print('nothing')
                else:
                    for name, num in player.possession.items():
                        c = find_commodity(name)
                        print('%s ($%d * %d): %s' %
                              (name, c.price, num, c.desc))

            elif cmd == 'list':
                print('Saler have $%d, and' % saler.money)
                for name, num in saler.possession.items():
                    c = find_commodity(name)
                    print('%s ($%d * %d)' % (name, c.price, num))

            elif cmd == 'trade':
                filename = os.path.join(
                    '.', token[:5] + token[-5:] + '.txt')
                f = open(filename, 'w')
                for _ in range(MAX_LINES):
                    line = input()
                    if line == 'END':
                        f.close()
                        break
                    else:
                        f.write(line + '\n')

                if not check_transaction(filename):
                    pass
                elif perform_transaction(filename):
                    print('transaction completed')
                else:
                    print('transaction failed')

            else:
                print('command error')
                exit()
