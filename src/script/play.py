import random
import jk


# 게임 클래스
class Game:
    def __init__(self, player):
        self.original_card = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S08", "S09", "S10", "S11", "S12", "S13",
                              "D01", "D02", "D03", "D04", "D05", "D06", "D07", "D08", "D09", "D10", "D11", "D12", "D13",
                              "H01", "H02", "H03", "H04", "H05", "H06", "H07", "H08", "H09", "H10", "H11", "H12", "H13",
                              "C01", "C02", "C03", "C04", "C05", "C06", "C07", "C08", "C09", "C10", "C11", "C12", "C13"]
        self.hand = [['0' for _ in range(7)] for _ in range(4)]
        self.player = player

    # 게임 시작
    def game_start(self):
        self.playing_deck = self.original_card  # 덱 복사
        random.shuffle(self.playing_deck)  # 덱 섞기

    # 순서 결정
    def ordering(self, a, b):
        score_check = [jk.Check(i[a:b]) for i in self.hand]
        print(score_check)
        scores = ([i.get_score() for i in score_check])
        print(scores)
        print()
        return scores.index(max(scores))  # 높은 패가 누구인지

    # 카드 분배
    def distribute(self, order):  # order : 분배 순서
        for hand in self.hand[order:] + self.hand[:order]:
            hand[hand.index('0')] = self.playing_deck[0]
            del self.playing_deck[0]

    # 오픈할 카드 선택
    def open(self, index, number):  # index : 몇 번째 플레이어, number : 오픈할 카드
        self.hand[index][2], self.hand[index][number] = self.hand[index][number], self.hand[index][2]

    # fold
    def fold(self, who):  # who : 몇 번째 플레이어
        del self.player[self.player.index(who)]  # player 리스트에서 제거


# 배팅 클래스
class Betting:
    def __init__(self, parent, have_money):  # 게임 시작할 때 각 플레이어 객체 생성 / have_money[index] : 보유금
        self.parent = parent
        self.have_money = have_money  # 보유금
        self.play = [1 for _ in range(4)]  # 추가 플레이 가능(올인이면 불가능)
        self.accumulate_money = [0, 0, 0, 0]  # 각 턴 배팅금
        self.betting_money = 0  # 내야할 돈
        self.before_money = 0  # 이전 순서가 낸 돈
        self.table_money = 10000  # 테이블 머니
        self.call_count = 0  # 콜 개수

    # 레이즈
    def raise_(self, index, times):  # 레이즈 / times : 몇 배 레이즈인지
        self.betting_money = int(self.table_money * (times - 1))  # 내야할 돈은 판돈 * (배수 - 1)
        if self.have_money[index] < (self.betting_money - self.accumulate_money[index]):  # 낼 돈이 없으면
            self.betting_money = self.have_money[index]  # 올인
            self.have_money[index] = 0  # 올인
            self.play[index] = 0  # 추가 플레이 불가능
        else:  # 낼 돈이 있으면
            self.have_money[index] -= (self.betting_money - self.accumulate_money[index])  # 더 내야할 돈만 내기 (이번 턴에 낸 돈 누적을 빼줌)
            self.accumulate_money[index] += self.betting_money  # 이번 턴 돈 누적
        self.before_money = self.betting_money  # 다음 사람이 낼 금액
        self.table_money += self.betting_money  # 테이블 머니에 낸 돈 추가
        self.call_count = 0  # 콜 개수 초기화
        self.parent.is_turn_start = False  # 턴 시작이 아님

    # 콜
    def call(self, index):
        self.betting_money = self.before_money  # 내야할 돈은 전 사람이 낸 금액
        if self.have_money[index] < (self.betting_money - self.accumulate_money[index]):  # 낼 돈이 없으면
            self.betting_money = self.have_money[index]  # 가진 돈 전부 배팅
            self.have_money[index] = 0  # 올인
            self.play[index] = 0  # 추가 플레이 불가능
        else:  # 낼 돈이 있으면
            self.have_money[index] -= (self.betting_money - self.accumulate_money[index])  # 더 내야할 돈만 내기 (이번 턴에 낸 돈 누적을 빼줌)
            self.accumulate_money[index] += self.betting_money  # 이번 턴 돈 누적
        self.table_money += self.betting_money  # 테이블 머니에 낸 돈 추가
        self.call_count += 1  # 콜 개수 추가
        self.parent.is_turn_start = False  # 턴 시작이 아님

    # 다음 턴 시작
    def next_turn(self):
        self.accumulate_money = [0, 0, 0, 0]  # 각 턴 배팅금 초기화
        self.before_money = 0  # 이전 사람이 낸 돈 초기화
        self.call_count = 0  # 콜 개수 초기화
