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
        'Oof, **?k?/?d?/?a?** by ?s?.',
        'What a game by ?s?! **?k? kills and ?d? deaths!**',
        'Yikes, **?d? deaths** and only ?k? kills for ?s? that last match.',
        'Disappointing match, ?s?.  Just bad.  Like, really? **?k?/?d?/?a?**?',
        'All around terrible performance this past match by ?s? with **?d? deaths.**',
        'Just a little bit of limit testing by ?s?, resulting in **?d? deaths.**',
        'You gotta admit, that was a pretty lousy performance by ?s?...  **?d? deaths...**'
    ],
    'heavy': [ # 10-14
        '**NEWS FLASH:** ?S? DROPS A **?d? DEATH** GAME',
        'Damn, ?s? really died **?d? times** in one game.',
        'WOW!  **?d? deaths** by ?s? in this int-heavy game!',
        'Holy moly - **?d? DEATHS** BY ?S?!!',
        '**THIS JUST IN:** ?S? JUST died **?d?** TIMES',
        'Solid **?d? bomb** by ?s?.',
        'Mr. Inty Pants ?s? just inted **?d? times!**'
    ],
    'turbo': [ # 15-19
        'Get **pooped** on ?s?! That was a terrible game! **?d?**',
        '**BREAKING NEWS:** ?S? INTS ANOTHER GAME WITH **?d? DEATHS**',
        '**HOLY SMOKES!** ?s? just gifted us **?d? deaths!**',
        'It\'s a bird!  It\'s a plane!  Wait, no!  It\'s just ?s?\'s **?d? deaths** flying through the air!',
        'Someone\'s gotta report ?s? to the International Next-level Throwing Society (I.N.T.S.) for those **?d? deaths!**',
        'New feature on the **?S? INT SHOW!**  This episode, ?s? dies **?d? times!**'
    ],
    'turbo-mega': [ # 20+
        'Incredible.  A once in a blue moon performance.  We are all honored, ?s?, to witness your **?d? death** game.',
        '**HOLY INT!**  How does someone even die **?d? times** in one game??  Unbelievable!'
    ]
}
