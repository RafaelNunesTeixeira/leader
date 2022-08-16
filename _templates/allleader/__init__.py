from otree.api import *


c = Currency  # old name for currency; you can delete this.

doc = """
experiment
"""


class Constants(BaseConstants):
    name_in_url = 'allleader'
    players_per_group = 3
    num_rounds = 10
    instructions_template = 'allleader/instructions.html'
    # """Amount allocated to each player"""
    endowment = float(20)
    punish = 10
    punmulti = 2
    multiplier = 1.5
    rounds = 10
    contact = 'allleader/contact.html'

class Subsession(BaseSubsession):
    pass


def creating_session(subsession):
    pass


class Group(BaseGroup):
    total_contribution = models.FloatField()
    individual_share = models.FloatField()


class Player(BasePlayer):
    """controling"""
    treat = models.IntegerField()
    galera = models.StringField()
    rol = models.StringField()

    """data"""
    contribution = models.IntegerField(
        min=0,
        max=Constants.endowment,
        doc="""The amount contributed by the Group Member""",
        widget=(),
        label="How much will you contribute to the project (from 0 to 20)?",
    )
    pun1, pun2, pun3 = [models.IntegerField(blank=True, initial=0) for i in range(3)]
    s1= models.FloatField()
    s2 = models.FloatField()

    """questions"""

class formation(WaitPage):
    title_text = "Your group is being formed."
    body_text = "We require groups of 3 participants in order to start the experiment. We are waiting for the other participants to complete the group. " \
                "Any problems or questions, please enter in the following zoom link: " \
                "https://uva-live.zoom.us/j/2531047886"
    group_by_arrival_time = True

    def is_displayed(self):
        return self.subsession.round_number == 1


class groups(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.subsession.round_number == 1

    def before_next_page(player: Player, timeout_happened):
        if (player.group.id_in_subsession % 2) == 0:
            player.treat = 1
            player.galera = "Group Member 1 and Group Member 2, and a Group Leader"
        else:
            player.treat = 0
            player.gal = "Group Member 1, Group Member 2, and Group Member 3"
        if player.id_in_group == 1:
            player.rol = 'Group Member 1'
        if player.id_in_group == 2:
            player.rol = 'Group Member 2'
        if player.id_in_group == 3:
            if player.treat == 1:
                player.rol = 'Group Leader'
            if player.treat == 0:
                player.rol = 'Group Member 3'


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
    group.individual_share = (
            group.total_contribution * Constants.multiplier / Constants.players_per_group
    )

    for p in group.get_players():
        p.payoff = (Constants.endowment - p.contribution) + group.individual_share
        p.s1 = float((Constants.endowment - p.contribution) + group.individual_share)


def set_payoffs2(group: Group):
    group.total_contribution = sum([p.contribution for p in group.get_players()])
    group.individual_share = (
            group.total_contribution * Constants.multiplier / Constants.players_per_group
    )

    for p in group.get_players():
        if p.id_in_group == 1:
            punishment = [j.pun1 for j in p.get_others_in_group() if j.pun1 is not None]
            give = sum(filter(None, [p.pun2, p.pun3]))
        if p.id_in_group == 2:
            punishment = [j.pun2 for j in p.get_others_in_group() if j.pun2 is not None]
            give = sum(filter(None, [p.pun1, p.pun3]))
        if p.id_in_group == 3:
            punishment = [j.pun3 for j in p.get_others_in_group() if j.pun3 is not None]
            give = sum(filter(None, [p.pun1, p.pun2]))
        total_punishment = sum(punishment)
        p.payoff = max(0, (Constants.endowment - p.contribution) + group.individual_share - give - 2 * total_punishment)
        p.s2 = float(max(0, (Constants.endowment - p.contribution) + group.individual_share - give - 2 * total_punishment))


# PAGES

class Contribute(Page):
    """Player: Choose how much to contribute"""

    form_model = 'player'
    form_fields = ['contribution']



class instructions(Page):
    def vars_for_template(player: Player):
        return dict(galera=player.galera,
                    role=player.role)



class Contributewaitpage(WaitPage):
    after_all_players_arrive = set_payoffs
    body_text = "Waiting for other participants to contribute."



class Deduction(Page):
    """Players payoff: How much each has earned"""
    form_model = 'player'
    form_fields = ['pun1', 'pun2', 'pun3']



    def vars_for_template(player: Player):
        group = player.group
        others = player.get_others_in_group()
        if player.id_in_group == 1:
            form = ['pun2', 'pun3']
        if player.id_in_group == 2:
            form = ['pun1', 'pun3']
        if player.id_in_group == 3:
            form = ['pun1', 'pun2']
        data = zip(others, form)
        contribution = player.contribution


        return dict(total_earnings=group.total_contribution * Constants.multiplier,
                    endkept= Constants.endowment-contribution,
                    rol=player.role,
                    data=data,
                    contribution=contribution,
                    s1=player.s1,
                    )

    def error_message(player, values):
        if player.id_in_group ==1:
            if int(values['pun2']) + int(values['pun3']) > 10:
                return 'You can allocate up to 10 points in punishment.'
        if player.id_in_group == 2:
            if int(values['pun1']) + int(values['pun3']) > 10:
                return 'You can allocate up to 10 points in punishment.'
        if player.id_in_group == 3:
            if int(values['pun1']) + int(values['pun2']) > 10:
                return 'You can allocate up to 10 points in punishment.'

    @staticmethod
    def js_vars(player: Player):
        return {
            'bRequireFS': Constants.bRequireFS,
            'bCheckFocus': Constants.bCheckFocus,
        }


class PunishmentWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs2
    body_text = "Waiting for other participants to contribute."

class Results(Page):
    @staticmethod
    def js_vars(player: Player):
        return {
            'bRequireFS': Constants.bRequireFS,
            'bCheckFocus': Constants.bCheckFocus,
        }

    def vars_for_template(player: Player):
        group = player.group
        others = player.get_others_in_group()
        if player.id_in_group == 1:
            form = [player.pun2, player.pun3]
            form2 = [(g.pun1) * 2 for g in others]
        if player.id_in_group == 2:
            form = [player.pun1, player.pun3]
            form2 = [(g.pun2)*2 for g in others]
        if player.id_in_group == 3:
            form = [player.pun1, player.pun2]
            form2 = [(g.pun3)*2 for g in others]


        data = zip(others, form)
        data2= zip(others, form2)
        contribution = player.contribution
        pung=sum(form)
        punr=sum(form2)
        punishment=pung+punr


        return dict(total_earnings=group.total_contribution * Constants.multiplier,
                    punishment=punishment,
                    rol=player.role,
                    data=data,
                    data2=data2,
                    pung=pung,
                    punr=punr,
                    contribution=contribution,
                    endkept=Constants.endowment - contribution,
                    s1=player.s1,

                    )


page_sequence = [formation, groups, Contribute, Contributewaitpage, Deduction, PunishmentWaitPage, Results]