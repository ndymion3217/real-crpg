import random as rd
import datetime as dt
import pickle
import resource
import inventory as inven
import status
import monster as mob
import item
import action
from dice import rollDice


class Character:
    def __init__(self, name, cls, race, stat, value, description):  # 기본적인 캐릭터의 정보생성자입니다.
        self.status = status.Status(name, cls, race, stat[0], stat[1], stat[2],stat[3], stat[4], stat[5], value, description)
        self.inventory = inven.Inventory()
        self.action = action.Action()

    def show_info(self):  # /캐릭터확인 명령어를위한 함수입니다.
        self.status.show_status(self.inventory)
        self.status.show_equip_status()

    def meleeattack(self, op):  # 근접공격 명령어를위한 함수입니다.
        self.action.meleeAttack(op, self)

    def check_body(self, monster):  # 몬스터 루팅을위한 함수
        self.action.check_body(self.inventory, monster)

    def equip(self, item):  # 무기장비를 위한함수입니다.
        if item.type == 'weapon':
            temp = self.status.weapon_unequip()
            if temp == None:
                pass
            else:
                self.inventory.item_setter(temp)
        elif item.type == 'armor':
            temp = self.status.armor_unequip()
            if temp == None:
                pass
            else:
                self.inventory.item_setter(self.status.armor_unequip())
        else:
            temp = self.status.shield_unequip()
            if temp == None:
                pass
            else:
                self.inventory.item_setter(self.status.shield_unequip())
        self.status.equip(self.inventory.item_getter(item.name))


class Place:
    pass


class Log:
    def __init__(self, string):
        self.timestamp = dt.datetime.now()
       # self.type = type  # 문장의 타입을 담는 합수 / 예: 전투, 대화, 상황묘사
        self.sentence = string

    def get_log(self):
        return str(self.timestamp) + ') ' + self.sentence


def show_and_select(list):  # 보기를 나열하고 선택해서 반환하는 함수
    while True:
        for i, j in enumerate(list):
            print('{}. {}'.format(i + 1, j))
        choose = int(input('위의 보기중에 골라주세요. : '))
        result = list[choose - 1]
        choose1 = int(input('\n{} 이(가) 맞습니까?\n1.예 2.아니오 : '.format(result)))
        if choose1 == 1:
            return result
        else: pass


def random_sentence_printer(list):  # 묘사를 랜덤으로 출력해주는 함수입니다.
    print(rd.choice(list))


def script_reader(list):  # 스크립트를 출력해주는 함수입니다.
    for i in list:
        print(i)
        input()


class Session:  # 세션을 담습니다.
    def __init__(self, name):  # 리소스에 미리 설정된 데이터를 이름으로 검색해, 속성에 담습니다.
        for i in resource.session:
            if i[0] == name:
                self.session = i
                break
        self.name = name
        self.monster = []
        for i in range(self.session[2]):
            self.monster.append(Monster(self.session[1]))
        script_reader(self.session[3])


class Master:
    def __init__(self):  # 마스터의 생성자로, 플레이어 캐릭터와, 세션, 장소들을 담고있습니다.
        self.player = []
        self.cur_session = ''#Session('튜토리얼')
        self.cur_monster = []
        self.place = []
        self.log = []
        self.battle_status = False

    def make_new_character(self):  # 새로운 플레이어 추가 함수
        input('캐릭터를 생성합니다.')
        print()
        print('직업을 골라주세요.')
        cls = show_and_select(resource.classes)
        print('종족을 골라주세요.')
        race = show_and_select(resource.races)
        print('이름을 골라주세요.')
        name = show_and_select(resource.worrior_names)
        print('외모를 골라주세요.')
        outlook1 = show_and_select(resource.worrior_outlooking1)
        outlook2 = show_and_select(resource.worrior_outlooking2)
        outlook3 = show_and_select(resource.worrior_outlooking3)
        script_reader(resource.status_select)
        answer = int(input('어느 방법으로 하시겠습니까?\n1.3d6  2.직접배분 : '))
        if answer == 1:
            num = []
            for i in range(6):
                num.append(rollDice(3, 6, 0))
            while True:
                stat = ['근력', '민첩', '체력', '지능', '지혜', '매력']
                nums = []
                for i in num:
                    nums.append(i)
                result = []
                print('그럼, 능력치를 선택할 차례입니다.')
                for i in stat:
                    for j, k in enumerate(nums):
                        print('{}.{}'.format(j + 1, k))
                    choose = int(input('{}에 몇점을 배치할까요? : '.format(i)))
                    result.append(nums.pop(choose - 1))
                for i in range(0, 6):
                    if result[i] > 15:
                        add = '(+2)'
                    elif result[i] > 12:
                        add = '(+1)'
                    elif result[i] > 8:
                        add = ''
                    elif result[i] == 8:
                        add = '(-1)'
                    print('{} : {}{}'.format(stat[i], result[i], add))
                choose = int(input('맞습니까?\n1.예 2.아니오 : '))
                if choose == 1:
                    choose = int(input('직업은 바꾸시겠습니까?\n1.네 2.아니오 : '))
                    if choose == 2:
                        break
                    else:
                        print('직업을 골라주세요.')
                        cls = show_and_select(resource.classes)
                else:
                    pass
        else:
            while True:
                stat = ['근력', '민첩', '체력', '지능', '지혜', '매력']
                nums = [16, 15, 13, 12, 9, 8]
                result = []
                print('그럼, 능력치를 선택할 차례입니다.')
                for i in stat:
                    for j, k in enumerate(nums):
                        print('{}.{}'.format(j + 1, k))
                    choose = int(input('{}에 몇점을 배치할까요? : '.format(i)))
                    result.append(nums.pop(choose - 1))
                for i in range(0, 6):
                    if result[i] > 15:
                        add = '(+2)'
                    elif result[i] > 12:
                        add = '(+1)'
                    elif result[i] > 8:
                        add = ''
                    elif result[i] == 8:
                        add = '(-1)'
                    print('{} : {}{}'.format(stat[i], result[i], add))
                choose = int(input('맞습니까?\n1.예 2.아니오 : '))
                if choose == 1:
                    break
                else:
                    pass
        print('가치관을 골라주세요.')
        value = show_and_select(resource.values)
        description = '{}과 {}, 그리고 {}을 가진 {}은...'.format(outlook1, outlook2, outlook3, name)
        description += input('마지막으로 모험을 떠나기 전,\n어떤 생활을 해왔는지'
                             '간략하게 작성해 주세요.')
        self.player.append(Character(name, cls, race, result, value, description))
        self.player[0].equip(item.Item('주먹'))

    def what_now(self):  # 마스터의 물음입니다.
        if len(self.cur_monster) > 0:
            if len(self.cur_monster) == 1:
                monsters = '{} 상태인 {}가 앞에 있습니다.'.format(self.cur_monster[0].get_cur_hp(), self.cur_monster[0].name)
            else:
                monsters = ''
                for monster in cur_monster:
                    monsters += '{} 상태인 {}, '.format(monster.get_cur_hp(), monster.name)
                monsters = monsters[:-2] + ' 가 앞에 있습니다.'
            print(monsters)
        string = input("이제 어떻게 하시겠습니까?? : ")  # 질문을 한뒤, '/'를 포함하는 명령어가 아니라면 전부 로그로 들어갑니다.
        if '/' in string:
            if string == '/게임종료':
                choose = int(input("정말 종료하시겠습니까?\n부가 자네를 그리워할걸세.\n1.예 2.아니오 : "))
                if choose == 1:
                    return 'end game'
            elif string == '/시스템명령어':
                for i in resource.command_list:
                    print(i)
            elif string == '/로그보기':
                for i in self.log:
                    print(i.get_log())
            elif string == '/직전취소':
                print('미구현')
            elif string == '/캐릭터확인':
                self.player[0].show_info()
            elif string == '/일반명령어':
                script_reader(resource.command_help1)
                for i in self.player[0].action.have:
                    print(i)
                print('이상입니다.')
            elif string == '/가방확인':
                self.player[0].inventory.show_inventory()

        else:
            if '근접공격' in string:
                for monster in self.cur_monster:
                    if monster.name in string:
                        self.player[0].meleeattack(monster)
            elif '소지품확인' in string:
                if self.battle_status:
                    print('전투중엔 불가능합니다...')
                    return
                for i in self.cur_monster:
                    if i.name in string and i.dead:
                        self.player[0].check_body(i)
                        self.monster_remover(i)
                    else:
                        print('주변에 죽어있지 않은듯합니다.')
            elif '착용' in string:
                if self.battle_status:
                    print('전투중엔 불가능합니다...')
                    return
                else:
                    for item in self.player[0].inventory.space:
                        if item.name in string:
                            print('{} 을(를) 착용합니다.'.format(item.name))
                            self.player[0].equip(item)
                            break
            self.alive_monster_checker()
            self.log.append(Log(string))

    def monster_setter(self, name):  # 전투상황에 돌입하게 몬스터를 추가하는 함수입니다.
        self.cur_monster.append(mob.Monster(name))
        if self.battle_status:
            pass
        else:
            self.battle_status_changer()

    def monster_remover(self, monster):  # 루팅이후 몬스터를 제거하는 함수입니다.
        self.cur_monster.remove(monster)

    def alive_monster_checker(self):  # 전투후, 살아남은 몬스터를 확인하는 함수입니다.
        result = [monster.dead for monster in self.cur_monster]
        if all(result):
            self.battle_status = False

    def battle_status_changer(self):  # 전투상황으로 돌입하는 함수입니다.
        if self.battle_status:
            self.battle_status = False
        else:
            self.battle_status = True

    def session_setter(self, name):  # 세션을 추가합니다.
        self.cur_session = Session(name)


DM = Master()
DM.player.append(Character('테스트', '전사', '엘프', [16, 15, 13, 12, 9, 8], '선', '메롱'))
DM.monster_setter('고블린')

if __name__ == '__main__':
    while True:
        answer = DM.what_now()
        if answer == 'end game':
            break