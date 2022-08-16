from otree.api import *


c = Currency  # old name for currency; you can delete this.

doc = """
experiment
"""


class Constants(BaseConstants):
    name_in_url = 'intro2'
    players_per_group = None
    num_rounds = 1
    instructions_template = 'introleader1/instructions.html'
    # """Amount allocated to each player"""
    endowment = float(20)
    punish = 10
    punmulti = 2
    multiplier = 1.5
    rounds = 10
    contact = 'introleader1/contact.html'
    papercups_template = __name__ + '/papercups.html'
    pfee = 2.10

class Subsession(BaseSubsession):
    pass

def creating_session(subsession):

    for player in subsession.get_players():
        player.treat = 0

        player.tamanho = len(player.subsession.get_players())
        if player.treat==1:
            player.galera = "Group Member 1 and Group Member 2, and a Group Leader"
            player.participant.gal = "Group Member 1, Group Member 2, and a Group Leader"
        if player.treat == 0:
            player.galera = "Group Member 1, Group Member 2, and Group Member 3"
            player.participant.gal = "Group Member 1, Group Member 2, and Group Member 3"

class Group(BaseGroup):
    top_bid = models.CurrencyField(initial=0)



class Player(BasePlayer):
    active = models.BooleanField(initial=True)
    tamanho = models.IntegerField()
    confirm =models.BooleanField()
    treat = models.IntegerField()
    galera = models.StringField()
    rol = models.StringField()
    testloko = models.IntegerField(initial=0)



    ##check-up
    q1 = models.IntegerField(
        choices=[60, 48, 40, 28, 37, 52],
        widget=widgets.RadioSelect,
    )

    q2 = models.IntegerField(
        choices=[60, 10, 30, 40, 20, 15],
        widget=widgets.RadioSelect,
    )
    q3 = models.IntegerField(
        choices=[60, 48, 40, 28, 37, 52],
        widget=widgets.RadioSelect,
    )
    q4 = models.IntegerField(
        choices=[1, 2, 10, 20, 100, 200],
        widget=widgets.RadioSelect,
    )

    q5= models.IntegerField(
        choices=[11, 42, 21, 88, 77, 33],
        widget=widgets.RadioSelect,
    )
    q6= models.IntegerField(
        choices=[[1,'Yes'], [2,'No']],
        widget=widgets.RadioSelect,
    )
    q7= models.IntegerField(
        choices=[5, 8, 10, 15, 20, 30],
        widget=widgets.RadioSelect,
    )





def get_state(player: Player):
    return dict(
        top_bid=player.group.top_bid,
        bid = player.testloko
    )


class Introduction(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1


class test2(Page):
    pass


class begin(Page):
    form_model = 'player'
    form_fields = ['confirm']
    def is_displayed(self):
        return self.subsession.round_number == 1
    def error_message(self, values):
        if values['confirm']==False:
            return 'You cannot continue if you can`t finish the experiment in this moment. Please, join another session later.'



class test(Page):
    @staticmethod
    def js_vars(player: Player):
        return dict(my_id=player.id_in_group, tamanho=player.tamanho)

    @staticmethod
    def live_method(player: Player, bid):
        group = player.group
        testloko = player.testloko
        my_id = player.id_in_group

        if bid:
            player.testloko = bid

            sum = 0

            for p in group.get_players():
                sum += max(int(p.testloko-1),0)

            group.top_bid = sum
            tamanho = len(group.get_players())
            return {0: dict(get_state(player))}
        else:
            return {my_id: get_state(player)}







class questions(Page):
    form_model = 'player'
    form_fields = ['q1','q2','q3','q4','q5','q6','q7']

    def error_message(self, values):
        if int(values['q1']) != 60:
            return 'Question 1 is wrong. Please, read again the instructions below and give the correct answer.'
        if int(values['q2']) != 20:
            return 'Question 2 is wrong. Please, read again the instructions below and give the correct answer.'
        if int(values['q3']) != 28:
            return 'Question 3 is wrong. Please, read again the instructions below and give the correct answer.'
        if int(values['q4']) != 2:
            return 'Question 4 is wrong. Please, read again the instructions below and give the correct answer.'
        if int(values['q6']) != 1:
            return 'Question 6 is wrong. Please, read again the instructions below and give the correct answer.'
        if int(values['q7']) != 10:
            return 'Question 7 is wrong. Please, read again the instructions below and give the correct answer.'


    def is_displayed(self):
        return self.subsession.round_number == 1


page_sequence = [begin, Introduction,questions,test]
