from discord import FFmpegPCMAudio
from collections import namedtuple
from random import choice
import utils


songs_path = "songs/"


def match_return(to_eq, to_respond):
    return lambda msg: msg == to_eq, lambda msg, *_: to_respond


def side_effect_send(*possible_texts):
    async def send(client, message):
        await message.channel.send(choice(possible_texts))
    return send


def play_song_from(song_list):
    async def play(client, message):
        audio_object = get_audio_from_file(choice(song_list))
        if audio_object is None:
            return
        invitation = await client.play_in_channel("General", audio_object, send_invitation=True)
        await message.channel.send(invitation)
    return play


def format_quote(author, quote):
    return f"Here's a quote from {author} :smiley:\n" \
           f"```{quote}```"


def get_audio_from_file(song_name):
    try:
        *_, file_name, start_on = next(utils.search(songs, _0=song_name))
    except StopIteration:
        return None
    else:
        return FFmpegPCMAudio(songs_path + file_name, options='-ss ' + start_on)


bot_names = ["bevo", "b-evo", "bot", "ess-bot", "bevoo", "bevooo", "essbot", "ess bot"]
greetings = ["hi", "hello", "hey", "helloo", "hellooo", "good morning", "good day", "good afternoon", "good evening", "greetings", "greeting", "good to see you", "its good seeing you", "how are you", "how're you", "how are you doing", "how ya doin'", "how ya doin", "how is everything", "how is everything going", "how's everything going", "how are things", "how're things", "how is it going", "how's it going", "how's it goin'", "how's it goin", "how is life been treating you", "how's life been treating you", "how have you been", "how've you been", "what is up", "what's up", "what is cracking", "what's cracking", "what is good", "what's good", "what is happening", "what's happening", "what is new", "what's new", "g’day", "howdy", "o/", "👋"]
intro_emoji = ["robot", "sunny", "astronaut", "wave", "sunglasses", "zany_face"]

mars_quotes = [
    # author, quote
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

songs = [
    # title, artist, url, file_name, start_on
    ("starboy", "the weeknd", "https://www.youtube.com/watch?v=34Na4j8AVgA", "The Weeknd - Starboy ft. Daft Punk (Official Video)-34Na4j8AVgA.webm", "0"),
    ("warriors", "imagine dragons", "https://youtu.be/fmI_Ndrxy14", "Warriors (ft. Imagine Dragons) _ Worlds 2014 - League of Legends-fmI_Ndrxy14.webm", "1:23"),
    ("we are the champions", "queen", "https://www.youtube.com/watch?v=04854XqcfCY", "Queen - We Are The Champions (Official Video)-04854XqcfCY.webm", "39"),
    ("don't stop the party", "pitbull", "https://www.youtube.com/watch?v=i0vFid2tKbI", "Pitbull - Don't Stop The Party ft. TJR-i0vFid2tKbI.m4a", "19"),
    ("the best", "tina turner", 'https://www.youtube.com/watch?v=GC5E8ie2pdM', "Tina Turner - The Best (Official Music Video) [HD REMASTERED]-GC5E8ie2pdM.webm", "1:02"),
    ("eye of the tiger", "survivor", 'https://www.youtube.com/watch?v=btPJPFnesV4', "Survivor - Eye Of The Tiger (Official HD Video)-btPJPFnesV4.webm", "9"),
    ("party rock", "lmfao", "https://www.youtube.com/watch?v=Coq-OlEdZQ8", "Party Rock Anthem - LMFAO Lyrics-Coq-OlEdZQ8.webm", "1:59"),
    ("can't hold us", "macklemore", "https://www.youtube.com/watch?v=89AnqCZ8JtA", "Can t Hold Us Lyrics Macklemore and Ryan Lewis Low)-89AnqCZ8JtA.webm", "0"),
    ("i got you", "james brown", "https://www.youtube.com/watch?v=iSLwVaebsJg", "I Got You (I Feel Good)-iSLwVaebsJg.webm", "0"),
    ("can't stop the feeling", "justin timberlake", "https://www.youtube.com/watch?v=VUdeIFQtDYU", "CAN'T STOP THE FEELING! - Justin Timberlake (Lyrics) 🎵-VUdeIFQtDYU.m4a", "1:00"),
    ("i gotta feeling", "black eyed peas", "https://www.youtube.com/watch?v=CwdrtwZiQ9E", "Black Eyed Peas - I Gotta Feeling (Audio)-CwdrtwZiQ9E.webm", "0"),
    ("we will rock you", "queen", "https://www.youtube.com/watch?v=-tJYN-eG1zk", "Queen - We Will Rock You (Official Video)--tJYN-eG1zk.webm", "5"),
    ("ain't no stoppin' us now", "mcfadden and whitehead", "https://www.youtube.com/watch?v=DY0tsKCB4lc", "Aint No Stopping Us Now Mcfadden and Whitehead-DY0tsKCB4lc.webm", "33"),
    ("i will survive", "gloria gaynor", "https://www.youtube.com/watch?v=ARt9HV9T0w8", "Gloria Gaynor - I Will Survive [Official Video] 1978 [Audio iTunes Plus AAC M4A]-ARt9HV9T0w8.webm", "1"),
    ("another one bites the dust", "queen", "https://www.youtube.com/watch?v=cGJ_IyFwieY", "Queen   Another One Bites The Dust Lyrics-cGJ_IyFwieY.webm", "0"),
    ("beat it", "michael jackson", "https://www.youtube.com/watch?v=T2PAkPp0_bY", "Michael Jackson-Beat it (Lyrics)-T2PAkPp0_bY.webm", "23"),
    ("don't stop me now", "queen", "https://www.youtube.com/watch?v=HgzGwKwLmgM", "Queen - Don't Stop Me Now (Official Video)-HgzGwKwLmgM.webm", "1:10"),
    ("what doesn't kill you makes you stronger", "kelly clarkson", "https://www.youtube.com/watch?v=Xn676-fLq7I", "Kelly Clarkson - Stronger (What Doesn't Kill You) [Official Video]-Xn676-fLq7I.webm", "41"),
    ("the final countdown", "europe", "https://www.youtube.com/watch?v=NNiTxUEnmKI", "The Final Countdown-NNiTxUEnmKI.webm", "1:56"),
    ("chariots of fire", "vangelis", "https://www.youtube.com/watch?v=8a-HfNE3EIo", "Vangelis - Chariots Of Fire-8a-HfNE3EIo.webm", "40"),
    ("almost there", "anika noni rose", "https://www.youtube.com/watch?v=ThMwHKfzz1I", "Anika Noni Rose - Almost There (From 'The Princess and the Frog')-ThMwHKfzz1I.webm", "30"),
    ("happy birthday", "Westminster Choir College", "https://www.youtube.com/watch?v=t_DDFjXUm00", "Happy Birthday from Westminster Choir College-t_DDFjXUm00.m4a", "6"),
]

stop_message = "Type !stop to stop the music :robot:"

champagne_songs = ["we are the champions", "warriors", "the best", "ain't no stoppin' us now", "don't stop me now"]
celebration_songs = ["don't stop the party", "party rock", "can't hold us", "i got you", "can't stop the feeling", "i gotta feeling", "don't stop me now"]
motivation_songs = ["eye of the tiger", "we will rock you", "i will survive", "another one bites the dust", "beat it", "don't stop me now", "what doesn't kill you makes you stronger"]
almost_there_songs = ["the final countdown", "chariots of fire", "almost there"]
birthday_songs = ["happy birthday"]


async def birthday_handler(client, message):
    await message.channel.send(f"Happy birthday {message.mentions[0].mention if message.mentions else 'good friend'}! Enjoy your day!")
    await message.channel.send(":partying_face: :birthday: :balloon:")
    await message.channel.send("Join the voice-channel for the birthday singing :cake:")
    await play_song_from(birthday_songs)(client, message)
    await message.channel.send("(To stop me from singing, type !stop)")


async def stop_handler(client, message):
    voice_client = message.guild.voice_client
    if not voice_client:
        return

    if voice_client.is_playing():
        voice_client.stop()
        await message.channel.send(f"Oh okay :{'slight_smile' if 'please' in message.content else 'disappointed'}:")

    await voice_client.disconnect()


message_handlers = [
    # condition, handler, *side_effects
    match_return("!test", "Beep boop :robot:"),
    match_return("!introduce-yourself",
                 "Hi ESS @here!\n"
                 "My name is B-Evo, and in the future I hope to perform the following tasks for the team:\n"
                 "1) Provide a test-bed for the personal assistant that'll be integrated in the suit. :robot: :astronaut:\n"
                 "2) Execute familiar bot-commands like provide meeting summaries and GDrive upload notifications. :robot: :page_facing_up:\n"
                 "3) Act as a companion in these dark times. :robot: :hugging:\n"
                 "Stay safe all. :robot: :family:"),
    (lambda msg: msg.startswith("!stop"), None, stop_handler),
    (lambda msg: utils.sentence_contains(msg, "happy birthday"), None, birthday_handler),
    (lambda msg: utils.sentence_contains(msg, "pop the champagne"), None,
     side_effect_send(":champagne:"), side_effect_send("Join the voice-channel for a piece of victory music :champagne_glass:"),
     play_song_from(champagne_songs), side_effect_send(stop_message)),
    (lambda msg: utils.sentence_contains(msg, "let's celebrate"), None,
     side_effect_send(":balloon: :partying_face: :confetti_ball:"), side_effect_send("Join the voice-channel for a piece of celebration music :champagne_glass:"),
     play_song_from(celebration_songs), side_effect_send(stop_message)),
    (lambda msg: utils.sentence_contains(msg, "motivation"), None,
     side_effect_send(":muscle:"), side_effect_send("YES YOU CAN!", "I believe in you guys", "YOU ROCK!"), side_effect_send("Join the voice-channel for some motivational music"),
     play_song_from(motivation_songs), side_effect_send(stop_message)),
    (lambda msg: utils.sentence_contains(msg, "almost there"), None,
     side_effect_send(":muscle:"), side_effect_send("The final steps...", "You're almost there..."), side_effect_send("Join the voice-channel for some music"),
     play_song_from(almost_there_songs), side_effect_send(stop_message)),
    (lambda msg: msg.startswith("!quote"),
     lambda msg, *_: format_quote(*choice(mars_quotes))),
    (lambda msg: any(utils.sentence_contains(msg, greeting) for greeting in greetings) and
                 any(utils.sentence_contains(msg, bot_name) for bot_name in bot_names),
     lambda msg, display_name: f"Hi {utils.short_username(display_name)}! :{choice(intro_emoji)}:"),
    (lambda msg: msg.startswith("!calc") and utils.safe_to_evaluate(msg[6:]),
     lambda msg, *_: utils.silent_eval(msg[6:]))
    # TODO add time-zone converter
]
