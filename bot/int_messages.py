# int_message.py

# Customize your int-messages below, following the key provided.

# ?s? = Summoner name
# ?S? = All caps Summoner name
# ?d? = # of deaths
# ?k? = # of kills
# ?a? = # of assists
int_messages = {
    'standard': [ # 0-10
        '?s? just died **?d? times!** Wow!',
        '**?k?/?d?/?a?** game coming from ?s?.  Nice.',
        'Oof, **?k?/?d?/?a?** by ?s?. What OP score would that even be??',
        'What a game by ?s?! **?d? deaths and ?k? kills!**',
        'Yikes, **?d? deaths** and only ?k? kills for ?s? that last match.'
    ],
    'heavy': [ # 10-14
        '**NEWS FLASH:** ?S? DROPS A **?d? DEATH** GAME',
        'Damn, ?s? really died **?d? times** in one game.',
        'WOW!  **?d? deaths** by ?s? in this int-heavy game!',
        'Holy moly - **?d? DEATHS** BY ?S?!!'
    ],
    'turbo': [ # 15-19
        'Get **pooped** on ?s?! That was a terrible game! **?d?**',
        '**BREAKING NEWS:** ?S? INTS ANOTHER GAME WITH **?d? DEATHS**',
        '**HOLY SMOKES!** ?s? just gifted us **?d? deaths!**'
    ],
    'turbo-mega': [ # 20+
        'Incredible.  Once in a blue moon.  A **?d? death** game by ?s?.  We are all honored, ?s?.'
    ]
}
