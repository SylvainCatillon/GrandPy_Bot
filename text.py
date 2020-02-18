FR_TEXT = dict(
    # Your sentences must contains {name} at the place wich you want to display
    # the name of the place, and {address} at the place wich you want
    # to display its address
    address=[
        "Comment?! {name}? Ahhhh, oui, je me souviens de cette adresse! " \
        "C'est: {address}",
        "{name} tu dis? Bien sûr mon p'tit: {address}"
    ],

    # Your sentence must contains {story} and {story_title}
    story=[
        "Mais t'ai-je déjà raconté l'histoire de ce quartier qui " \
        "m'a vu en culottes courtes ? {story_title}: {story}",
        "J'adore cet endroit! Je connais les environs comme " \
        "ma poche! Par exemple, {story_title}: {story}",
        "C'est l'un de nos endroits préférés avec GrandMa Bot!!! " \
        "Je pourrais en parler pendant des heures: {story_title}. {story}"
    ],

    story_link="En savoir plus sur Wikipedia",

    address_not_found="Désolé mon p'tit, je me souviens plus où c'est...",

    form_label="Tu cherches une adresse? Demande moi!",
    form_placeholder="Salut GrandPy ! Est-ce que tu connais l'adresse " \
        "d'OpenClassrooms ?",

    # Sentence to be displayed on computers.
    # Please include "GrandPy Bot" in it
    long_header="Bonjour mon p'tit! Je suis GrandPy Bot! " \
        "Tu cherches ton chemin?",
    # Sentence to be displayed on smartphones and tablets.
    # Please include "GrandPy Bot" in it
    short_header="GrandPy Bot",

    # Sentence to be displayed if the request to /get_response fail
    get_response_error="Houla, je crois que ma connexion ne marche pas " \
        "bien.. Ca doit etre l'age!!"
)
