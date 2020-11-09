from random import choice


def match_return(to_eq, to_respond):
    return lambda msg: msg == to_eq, lambda msg, *_: to_respond


def short_username(name):
    return name.split('-')[0].strip()


bot_names = ["bevo", "b-evo", "bot", "ess-bot", "bevoo", "bevooo", "essbot", "ess bot"]
greetings = ["hi", "hello", "hey", "helloo", "hellooo", "g morining", "gmorning", "good morning", "morning", "good day", "good afternoon", "good evening", "greetings", "greeting", "good to see you", "its good seeing you", "how are you", "how're you", "how are you doing", "how ya doin'", "how ya doin", "how is everything", "how is everything going", "how's everything going", "how is you", "how's you", "how are things", "how're things", "how is it going", "how's it going", "how's it goin'", "how's it goin", "how is life been treating you", "how's life been treating you", "how have you been", "how've you been", "what is up", "what's up", "what is cracking", "what's cracking", "what is good", "what's good", "what is happening", "what's happening", "what is new", "what's new", "what is neww", "g’day", "howdy", "o/", ":wave:"]
intro_emoji = ["robot", "sunny", "astronaut", "wave", "sunglasses", "zany_face"]

message_handlers = [
    # condition, handler
    match_return("!test", "Beep boop :robot:"),
    match_return("!introduce-yourself",
                 "Hi ESS @here!\n"
                 "My name is B-Evo, and in the future I hope to perform the following tasks for the team:\n"
                 "1) Provide a test-bed for the personal assistant that'll be integrated in the suit. :robot: :astronaut:\n"
                 "2) Execute familiar bot-commands like provide meeting summaries and GDrive upload notifications. :robot: :page_facing_up:\n"
                 "3) Act as a companion in these dark times. :robot: :hugging:\n"
                 "Stay safe all. :robot: :family:"),
    (lambda msg: any(greeting in msg for greeting in greetings) and
                 any(bot_name in msg for bot_name in bot_names),
     lambda msg, display_name: f"Hi {short_username(display_name)}! :{choice(intro_emoji)}:")
]
