FR_TEXT = dict(
    # Your sentences must contain {name} at the place wich you want to display
    # the name of the place, and {address} at the place wich you want
    # to display its address
    address=[
        "Comment?! {name}? Ahhhh, oui, je me souviens de cette adresse! " \
        "C'est: {address}",
        "{name} tu dis? Bien sûr mon p'tit: {address}"
    ],

    # Your sentences must contain {story} and {story_title}
    story=[
        "Mais t'ai-je déjà raconté l'histoire de ce quartier qui " \
        "m'a vu en culottes courtes ? {story_title}: {story}",
        "J'adore cet endroit! Je connais les environs comme " \
        "ma poche! Par exemple, {story_title}: {story}",
        "C'est l'un de nos endroits préférés avec GrandMa Bot!!! " \
        "Je pourrais en parler pendant des heures: {story_title}. {story}"
    ],

    #  Text displayed if the address isn't found
    address_not_found="Désolé mon p'tit, je me souviens plus où c'est...",

    #  Text displayed if the address is found but not the story
    failed_story="Saperlipopette, de quoi est-ce que je parlais déja?",

    #  Text of the link to the Wikipedia page
    story_link="En savoir plus sur Wikipedia",

    #  Label and placeholder of the form where the user ask its question
    form_label="Tu cherches une adresse? Demande moi!",
    form_placeholder="Salut GrandPy! Dis, est-ce que tu connais "\
        "l'adresse de la Tour Eiffel?",

    # Header text to be displayed on computers.
    # Please include "GrandPy Bot" in it
    long_header="Bonjour mon p'tit! Je suis GrandPy Bot! " \
        "Tu cherches ton chemin?",
    # Header text to be displayed on smartphones and tablets.
    # Please include "GrandPy Bot" in it
    short_header="GrandPy Bot",
)
