from otree.api import *


c = Currency  # old name for currency; you can delete this.

doc = """
experiment
"""


class Constants(BaseConstants):
    name_in_url = 'task1'
    players_per_group = 3
    num_rounds = 10
    instructions_template = 'leader1/instructions.html'
    # """Amount allocated to each player"""
    endowment = float(20)
    punish = 10
    punmulti = 2
    multiplier = 1.5
    rounds = 10
    contact = 'leader1/contact.html'
    papercups_template = __name__ + '/papercups.html'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_contribution = models.FloatField()
    individual_share = models.FloatField()
    final = models.FloatField()


class Player(BasePlayer):
    treat = models.IntegerField()
    rol =  models.StringField()
    galera = models.StringField()
    contribution = models.IntegerField(
        min=0,
        max=Constants.endowment,
        doc="""The amount contributed by the Group Member""",
        widget=(),
        label="How much will you contribute to the project (from 0 to 20)?",
    )
    s1= models.FloatField()


# FUNCTIONS

def vars_for_admin_report(subsession: Subsession):
    contributions = [p.contribution for p in subsession.get_players() if p.contribution != None]
    if contributions:
        return dict(
            avg_contribution=sum(contributions) / len(contributions),
            min_contribution=min(contributions),
            max_contribution=max(contributions),
        )
    else:
        return dict(
            avg_contribution='(no data)',
            min_contribution='(no data)',
            max_contribution='(no data)',
        )


def set_payoffs(group: Group):
    group.total_contribution = sum([p.contribution for p in group.get_players()])
    group.final = group.total_contribution * Constants.multiplier
    group.individual_share = (
            group.total_contribution * Constants.multiplier / Constants.players_per_group
    )

    for p in group.get_players():
        p.payoff = ((Constants.endowment - p.contribution) + group.individual_share)
        p.s1 = float((Constants.endowment - p.contribution) + group.individual_share)

# PAGES


class Role(Page):
    def vars_for_template(player: Player):
        if player.id_in_group == 1:
            role = 'Group Member 1'
        if player.id_in_group == 2:
            role = 'Group Member 2'
        if player.id_in_group == 3:
            role = 'Group Leader'

        return dict(role=role)

    def before_next_page(player: Player, timeout_happened):
            player.treat = 1
            if player.treat == 1:
                player.galera = "Group Member 1 and Group Member 2, and a Group Leader"
                player.participant.gal = "Group Member 1, Group Member 2, and a Group Leader"
            if player.treat == 0:
                player.galera = "Group Member 1, Group Member 2, and Group Member 3"
                player.participant.gal = "Group Member 1, Group Member 2, and Group Member 3"
            if player.id_in_group == 1:
                player.participant.rol = 'Group Member 1'
            if player.id_in_group == 2:
                player.rol = 'Group Member 2'
                player.participant.rol = 'Group Member 2'
            if player.id_in_group == 3:
                if player.treat == 1:
                    player.rol = 'Group Leader'
                    player.participant.rol = 'Group Leader'
                if player.treat == 0:
                    player.rol = 'Group Member 3'
                    player.participant.rol = 'Group Member 3'

    def is_displayed(self):
        return self.subsession.round_number == 1




class instructions(Page):
    def vars_for_template(player: Player):
        return dict(galera=player.galera,
                    role=player.role)


class formation(WaitPage):
    title_text = "Your group is being formed."
    body_text = "Waiting for the other participants to join the experiment "
    group_by_arrival_time = True
    def is_displayed(self):
        return self.subsession.round_number == 1




class Contribute(Page):
    """Player: Choose how much to contribute"""

    form_model = 'player'
    form_fields = ['contribution']

class Contributewaitpage(WaitPage):
    after_all_players_arrive = set_payoffs
    body_text = "Waiting for other participants to contribute."




class Results(Page):

    def vars_for_template(player: Player):
        group = player.group
        others = player.get_others_in_group()
        contribution = player.contribution

        return dict(total_earnings=group.total_contribution * Constants.multiplier,
                    rol=player.role,
                    contribution=contribution,
                    endkept=Constants.endowment - contribution,
                    s1=player.s1,

                    )


page_sequence = [formation, Role, Contribute, Contributewaitpage, Results]