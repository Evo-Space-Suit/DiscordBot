from random import choice
import ast
import math
import re
import string


def match_return(to_eq, to_respond):
    return lambda msg: msg == to_eq, lambda msg, *_: to_respond


def short_username(name):
    return re.match(r"^([a-zA-Z ])+", name).group().strip()


def raw_words(msg):
    exclude = set(string.punctuation)
    return ''.join(ch for ch in msg if ch not in exclude).split(' ')


def safe_to_evaluate(string):
    if len(string) > 300:
        return False
    try:
        tree = ast.parse(string)
    except SyntaxError:
        return False

    available_names = set(dir(math))
    allowed_node_types = [ast.Module, ast.Expr,
                          ast.BinOp, ast.Constant, ast.keyword,  # ast.Attribute
                          ast.Load, ast.Call,
                          ast.Div, ast.Mult, ast.Add, ast.Sub, ast.Pow]

    def inclusion_criteria(node):
        if isinstance(node, ast.Name):
            return node.id in available_names
        return any(isinstance(node, node_type) for node_type in allowed_node_types)
    return all(map(inclusion_criteria, ast.walk(tree)))


def silent_eval(expression):
    try:
        return f"Result: {eval(expression, {}, vars(math))}"
    except Exception as e:
        print(e, repr(expression))
        return f"Error: {e}"


def format_quote(author, quote):
    return f"Here's a quote from {author} :smiley:\n" \
           f"```{quote}```"


bot_names = ["bevo", "b-evo", "bot", "ess-bot", "bevoo", "bevooo", "essbot", "ess bot"]
greetings = ["hi", "hello", "hey", "helloo", "hellooo", "good morning", "good day", "good afternoon", "good evening", "greetings", "greeting", "good to see you", "its good seeing you", "how are you", "how're you", "how are you doing", "how ya doin'", "how ya doin", "how is everything", "how is everything going", "how's everything going", "how are things", "how're things", "how is it going", "how's it going", "how's it goin'", "how's it goin", "how is life been treating you", "how's life been treating you", "how have you been", "how've you been", "what is up", "what's up", "what is cracking", "what's cracking", "what is good", "what's good", "what is happening", "what's happening", "what is new", "what's new", "g’day", "howdy", "o/", ":wave:"]
intro_emoji = ["robot", "sunny", "astronaut", "wave", "sunglasses", "zany_face"]
mars_quotes = [
    ('Buzz Aldrin', 'Mars is there, waiting to be reached.'),
    ('Ray Bradbury', 'Science is no more than an investigation of a miracle we can never explain, and art is an interpretation of that miracle.'),
    ('Gene Roddenberry', "It isn't all over; everything has not been invented; the human adventure is just beginning."),
    ('HAL 9000', 'I am putting myself to the fullest possible use, which is all I think that any conscious entity can ever hope to do.'),
    ('Arthur C. Clarke', 'Two possibilities exist: either we are alone in the Universe or we are not. Both are equally terrifying.'),
    ('Isaac Asimov', 'The saddest aspect of life right now is that science fiction gathers knowledge faster than society gathers wisdom.'),
    ('Ray Bradbury', 'We are all children of this universe. Not just Earth, or Mars, or this system, but the whole grand fireworks. And if we are interested in Mars at all, it is only because we wonder over our past and worry terribly about our possible future.'),
    ('Ray Bradbury', 'What’s the use of looking at Mars through a telescope, sitting on panels, writing books, if it isn’t to guarantee, not just the survival of mankind, but mankind surviving forever!'),
    ('Buzz Aldrin', 'The first human beings to land on Mars should not come back to Earth. They should be the beginning of a build-up of a colony/settlement, I call it a ‘permanence’.'),
    ('Harrison Schmitt', 'It might be helpful to realize, that very probably the parents of the first native born Martians are alive today.'),
    ('John Noble Wilford', 'Mars tugs at the human imagination like no other planet. With a force mightier than gravity, it attracts the eye to the shimmering red presence in the clear night sky.'),
    ('Buzz Aldrin', 'I think humans will reach Mars, and I would like to see it happen in my lifetime.'),
    ('Paul Davies', 'A permanent base on Mars would have a number of advantages beyond being a bonanza for planetary science and geology. If, as some evidence suggests, exotic micro-organisms have arisen independently of terrestrial life, studying them could revolutionise biology, medicine and biotechnology.'),
    ('Andy Weir', "The planet's famous red colour is from iron oxide coating everything. So it's not just a desert. It's a desert so old it's literally rusting."),
    ('John Updike', 'Mars has long exerted a pull on the human imagination. The erratically moving red star in the sky was seen as sinister or violent by the ancients: The Greeks identified it with Ares, the god of war; the Babylonians named it after Nergal, god of the underworld. To the ancient Chinese, it was Ying-huo, the fire planet.'),
    ('Elon Musk', "Mars is the only place in the solar system where it's possible for life to become multi-planetarian."),
    ('Steven Squyres', 'The thing that sets Mars apart is that it is the one planet that is enough like Earth that you can imagine life possibly once having taken hold there.'),
    ('Buzz Aldrin', 'Mars has been flown by, orbited, smacked into, radar inspected, and rocketed onto, as well as bounced upon, rolled over, shoveled, drilled into, baked, and even laser blasted.'),
]


message_handlers = [
    # condition, handler
    match_return("!test", "Beep boop :robot:"),
    # TODO show available commands
    match_return("!introduce-yourself",
                 "Hi ESS @here!\n"
                 "My name is B-Evo, and in the future I hope to perform the following tasks for the team:\n"
                 "1) Provide a test-bed for the personal assistant that'll be integrated in the suit. :robot: :astronaut:\n"
                 "2) Execute familiar bot-commands like provide meeting summaries and GDrive upload notifications. :robot: :page_facing_up:\n"
                 "3) Act as a companion in these dark times. :robot: :hugging:\n"
                 "Stay safe all. :robot: :family:"),
    (lambda msg: msg.startswith("!quote"),
     lambda msg, *_: format_quote(*choice(mars_quotes))),
    (lambda msg: any(greeting in msg for greeting in greetings) and  # TODO improve search in msg
                 any(bot_name in msg for bot_name in bot_names),
     lambda msg, display_name: f"Hi {short_username(display_name)}! :{choice(intro_emoji)}:"),
    (lambda msg: msg.startswith("!calc") and safe_to_evaluate(msg[6:]),
     lambda msg, *_: silent_eval(msg[6:]))
    # TODO add time-zone converter
]
