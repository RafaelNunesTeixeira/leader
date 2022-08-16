from otree.api import *

doc = """
Big Five 10-item inventory
Rammstedt, B., & John, O. P. (2007). Measuring personality in one minute or less: A 10-item short version of the 
Big Five Inventory in English and German. Journal of research in Personality, 41(1), 203-212.
https://www.westmont.edu/_academics/departments/psychology/documents/rammstedt_and_john.pdf

Global preferences survey
Falk, A., Becker, A., Dohmen, T., Enke, B., Huffman, D., & Sunde, U. (2018). 
Global evidence on economic preferences. The Quarterly Journal of Economics, 133(4), 1645-1692.
https://www.briq-institute.org/global-preferences/home

Rule following
Kimbrough, Erik O., and Alexander Vostroknutov.
"A portable method of eliciting respect for social norms." Economics Letters 168 (2018): 147-150.

CRT

Frederick, S. (2005). 
Cognitive reflection and decision making. Journal of Economic Perspectives, 19(4), 25-42. doi: 10.1257/089533005775196732

"""


class Constants(BaseConstants):
    name_in_url = 'survey'
    players_per_group = None
    num_rounds = 1
    contact = 'survey/contact.html'
    papercups_template = __name__ + '/papercups.html'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


def make_q(label):
    return models.IntegerField(label=label, choices=[1, 2, 3, 4, 5], widget=widgets.RadioSelect)


class Player(BasePlayer):
    """RCT"""
    crt1 = models.IntegerField(label='A bat and a ball cost $1.10 in total. The bat costs $1.00 more than the ball.How much does the ball cost? (in cents)')
    crt2 = models.IntegerField(label='If it takes 5 machines 5 minutes to make 5 widgets, how long would it take 100 machines to make 100 widgets? (in minutes)')
    crt3 = models.IntegerField(label='In a lake, there is a patch of lily pads. Every day, the patch doubles in size. If it takes 48 days for the patch to cover the entire lake, how long would it take for the patch to cover half of the lake? (in days)')
    crt = models.FloatField(initial=0)

    """big five"""
    extraversion = models.FloatField()
    agreeableness = models.FloatField()
    conscientiousness = models.FloatField()
    neuroticism = models.FloatField()
    openness = models.FloatField()

    """falk"""
    alt = models.FloatField()
    pr = models.FloatField()
    nr = models.FloatField()
    tr = models.FloatField()

    """"reactance"""


    """""Big five"""
    bf1 = make_q('is reserved')
    bf2 = make_q('is generally trusting')
    bf3 = make_q('tends to be lazy')
    bf4 = make_q('is relaxed, handles stress well')
    bf5 = make_q('has few artistic interests')
    bf6 = make_q('is outgoing, sociable')
    bf7 = make_q('tends to find fault with others')
    bf8 = make_q('does a thorough job')
    bf9 = make_q('gets nervous easily')
    bf10 = make_q('has an active imagination')


    """falk"""

    """type1 - same scale"""
    al1 = make_q('is willing to give to good causes without expecting anything in return')
    pr1 = make_q('is willing to return a favor someone helped me')
    nr1 = make_q('will take revenge at the first occasion, if I am treated very unjustly, even if there is a cost to do so')
    nr2 = make_q('is willing to punish someone who treats me unfairly, even if there may be costs for me')
    nr3 = make_q('is willing to punish someone who treats others unfairly, even if there may be costs for me')
    tr1 = make_q('assumes that people have only the best intentions')

    """"type 2"""

    pr2 = models.IntegerField(
        choices=[[1, 'No present'], [2, 'The present worth 5 euros'], [3, 'The present worth 10 euros'],
                 [4, 'The present worth 15 euros'], [5, 'The present worth 20 euros'],
                 [6, 'The present worth 25 euros'], [7, 'The present worth 30 euros']],
        label='Situation 2: You are in an area you are not familiar with, and you realize you lost your way. You ask a stranger for directions. The stranger offers to take you to your destination. Helping you costs the stranger about 20 Euros in total. However, the stranger says he or she does not want any money from you. You have six presents with you. The cheapest present costs 5 Euros, the most  expensive one costs 30 Euros. Do you give one of the presents to the stranger as a “thank-you”- gift? If so, which present do you give to the stranger?',
        widget=widgets.RadioSelect)
    al2 = models.IntegerField(
        label='Situation 1: Today you unexpectedly received 1,000 Euros. How much of this amount would you donate to a good cause? (Values between 0 and 1000 are allowed.)',
        min=0, max=1000)



    """reactance"""

    com1 = make_q('becomes angry when my freedom of choice is restricted')
    com2 = make_q('is disappointed to see others submitting to standards and rules')
    com3 = make_q('feels like doing the opposite when someone forces me to do something')
    com4 = make_q('becomes frustrated when I am unable to make free and independent decisions')
    com5 = make_q('finds contradicting others stimulating')

    com = models.FloatField()
    che = models.FloatField()

    rul= models.FloatField()

def combine_score(positive, negative):
    return 3 + (positive - negative) / 2



##PAGES

class survey(Page):
    pass

class crt(Page):
    form_model = 'player'
    form_fields = ['crt1', 'crt2', 'crt3',]

    def before_next_page(player: Player, timeout_happened):
        if player.crt1!=5:
            player.crt = player.crt+1
        if player.crt2!=5:
            player.crt = player.crt+1
        if player.crt3!=47:
            player.crt = player.crt+1





class bigfive(Page):
    form_model = 'player'
    form_fields = ['bf1', 'bf2', 'bf3', 'bf4', 'bf5', 'bf6', 'bf7', 'bf8', 'bf9', 'bf10']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.extraversion = combine_score(player.bf6, player.bf1)
        player.agreeableness = combine_score(player.bf2, player.bf7)
        player.conscientiousness = combine_score(player.bf8, player.bf3)
        player.neuroticism = combine_score(player.bf9, player.bf4)
        player.openness = combine_score(player.bf10, player.bf5)

class falksc2(Page):
    form_model = 'player'
    form_fields = ['al2', 'pr2']


class falksc(Page):
    form_model = 'player'
    form_fields = ['pr1', 'nr1', 'nr2', 'nr3', 'al1', 'tr1']


    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.pr = (player.pr1+(player.pr2)*(5/7))/2
        player.nr = (player.nr1+player.nr2+player.nr3)/3
        player.tr = player.tr1
        player.alt = (player.al1 + player.al2 / 200) / 2

class reactance(Page):
    form_model = 'player'
    form_fields = ['com1', 'com2', 'com3', 'com4', 'com5']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.com= (player.com1 + player.com2 + player.com3 + player.com4 + player.com5)/5

class rule(Page):
    form_model = 'player'
    form_fields = ['rul','che']

    def error_message(self, values):
        if int(values['che']) < 50:
            return 'Please, allocate the 50 ball.'

    def before_next_page(player: Player, timeout_happened):
        player.participant.rule=(player.rul) *1 + 0.5*(50- (player.rul))
page_sequence = [rule]

""""""
