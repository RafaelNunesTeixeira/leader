from os import environ

environ['OTREE_PRODUCTION'] = "1"

SESSION_CONFIGS = [
    dict(
        name='introleader1',
        app_sequence=['introleader1'],
        num_demo_participants=4,
    ),
    dict(
        name='final1',
        app_sequence=['leader1', 'survey', 'svo', 'end'],
        num_demo_participants=3,
    ),
    dict(
        name='introleader2',
        app_sequence=['introleader2'],
        num_demo_participants=3,
    ),
    dict(
        name='final2',
        app_sequence=['leader2', 'survey', 'svo', 'end'],
        num_demo_participants=3,
    ),
    dict(
        name='svo',
        app_sequence=['svo'],
        num_demo_participants=3,
    ),
    dict(
        name='survey',
        app_sequence=['survey'],
        num_demo_participants=1,
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True


ROOMS = [
    dict(
        name='ExperimentG1',
        display_name='Experiment - ABS1',
    ),

    dict(
        name='ExperimentG2',
        display_name='Experiment - ABS2',
        participant_label_file='_rooms/ABS.txt',
    ),

    dict(
        name='ExperimentG3',
        display_name='Experiment - ABS3',
    ),
    dict(
        name='ExperimentG4',
        display_name='Experiment - ABS4',
        participant_label_file='_rooms/ABS.txt',
    ),
]

AUTH_LEVEL = environ.get('OTREE_AUTH_LEVEL')



ADMIN_USERNAME = 'bu'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = 'bu'


DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""


SECRET_KEY = '3844923960320'

INSTALLED_APPS = ['otree']



PARTICIPANT_FIELDS = ['rule','gal','rol','treat','attention',]