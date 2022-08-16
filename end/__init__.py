from otree.api import *


c = Currency  # old name for currency; you can delete this.

doc = """
experiment
"""


class Constants(BaseConstants):
    name_in_url = 'end'
    players_per_group = None
    num_rounds = 1
    contact = 'end/contact.html'
    zoom = 'end/contact.html'
    papercups_template = __name__ + '/papercups.html'

class Subsession(BaseSubsession):
    pass


def creating_session(subsession):
    pass



class Group(BaseGroup):
    pass

class Player(BasePlayer):
    info=models.StringField()
    pay=models.FloatField()
    points=models.FloatField()

    gender = models.StringField(
        choices=['Male', 'Female',
                 'Other', 'I do not want to inform'],
        label='What is your Gender?',
        widget=widgets.RadioSelect,
    )
    age=models.IntegerField(label='How old are you?')
    exp = models.StringField(
        choices=['Yes', 'No',
                 'I don`t remember'],
        label='Have you ever participated in an experiment with a similar task?',
        widget=widgets.RadioSelect,
    )
    strategy = models.StringField(

        label='How did you decide on the amount you contributed to the project?',
    )




class end2(Page):
    form_model = 'player'
    form_fields = ['gender','age', 'exp', 'strategy']

    def before_next_page(player: Player, timeout_happened):
        rule = max(0, float(player.participant.rule))
        player.points= round((float(player.participant.payoff)))
        player.pay = round((float(player.participant.payoff)) * 0.02,2)-0.7
        player.info = player.participant.label
        player.participant.payoff = player.pay




class end(Page):
    form_model = 'player'

    def vars_for_template(self):
        rule = max(0,float(self.participant.rule))
        rot = self.participant.label
        points= self.points
        pay = self.pay
        return dict(pay=pay,
                    rule=rule,
                    points=points,
                    fim=str(
                        "https://lab-abs.sona-systems.com/webstudy_credit.aspx?experiment_id=123&credit_token=526e094c9e804152b37d462f0aa8b7cb&survey_code=") + str(
                        rot),)

page_sequence = [end2, end]
