#!/usr/bin/python3
# -*- coding: utf-8 -*-
import argparse
import sys
from subprocess import Popen, PIPE
from typing import List, Tuple

emoji_list = """😀 grinning face (face, grin, grinning face)
😃 grinning face with big eyes (face, grinning face with big eyes, mouth, open, smile)
😄 grinning face with smiling eyes (eye, face, grinning face with smiling eyes, mouth, open, smile)
😁 beaming face with smiling eyes (beaming face with smiling eyes, eye, face, grin, smile)
😆 grinning squinting face (face, grinning squinting face, laugh, mouth, satisfied, smile)
😅 grinning face with sweat (cold, face, grinning face with sweat, open, smile, sweat)
🤣 rolling on the floor laughing (face, floor, laugh, rolling, rolling on the floor laughing)
😂 face with tears of joy (face, face with tears of joy, joy, laugh, tear)
🙂 slightly smiling face (face, slightly smiling face, smile)
🙃 upside-down face (face, upside-down)
😉 winking face (face, wink, winking face)
😊 smiling face with smiling eyes (blush, eye, face, smile, smiling face with smiling eyes)
😇 smiling face with halo (angel, face, fantasy, halo, innocent, smiling face with halo)
🥰 smiling face with hearts (adore, crush, hearts, in love, smiling face with hearts)
😍 smiling face with heart-eyes (eye, face, love, smile, smiling face with heart-eyes)
🤩 star-struck (eyes, face, grinning, star, star-struck)
😘 face blowing a kiss (face, face blowing a kiss, kiss)
😗 kissing face (face, kiss, kissing face)
☺ smiling face (face, outlined, relaxed, smile, smiling face)
😚 kissing face with closed eyes (closed, eye, face, kiss, kissing face with closed eyes)
😙 kissing face with smiling eyes (eye, face, kiss, kissing face with smiling eyes, smile)
😋 face savoring food (delicious, face, face savoring food, savouring, smile, yum)
😛 face with tongue (face, face with tongue, tongue)
😜 winking face with tongue (eye, face, joke, tongue, wink, winking face with tongue)
🤪 zany face (eye, goofy, large, small, zany face)
😝 squinting face with tongue (eye, face, horrible, squinting face with tongue, taste, tongue)
🤑 money-mouth face (face, money, money-mouth face, mouth)
🤗 hugging face (face, hug, hugging)
🤭 face with hand over mouth (face with hand over mouth, whoops)
🤫 shushing face (quiet, shush, shushing face)
🤔 thinking face (face, thinking)
🤐 zipper-mouth face (face, mouth, zipper, zipper-mouth face)
🤨 face with raised eyebrow (distrust, face with raised eyebrow, skeptic)
😐 neutral face (deadpan, face, meh, neutral)
😑 expressionless face (expressionless, face, inexpressive, meh, unexpressive)
😶 face without mouth (face, face without mouth, mouth, quiet, silent)
😏 smirking face (face, smirk, smirking face)
😒 unamused face (face, unamused, unhappy)
🙄 face with rolling eyes (eyeroll, eyes, face, face with rolling eyes, rolling)
😬 grimacing face (face, grimace, grimacing face)
🤥 lying face (face, lie, lying face, pinocchio)
😌 relieved face (face, relieved)
😔 pensive face (dejected, face, pensive)
😪 sleepy face (face, sleep, sleepy face)
🤤 drooling face (drooling, face)
😴 sleeping face (face, sleep, sleeping face, zzz)
😷 face with medical mask (cold, doctor, face, face with medical mask, mask, sick)
🤒 face with thermometer (face, face with thermometer, ill, sick, thermometer)
🤕 face with head-bandage (bandage, face, face with head-bandage, hurt, injury)
🤢 nauseated face (face, nauseated, vomit)
🤮 face vomiting (face vomiting, sick, vomit)
🤧 sneezing face (face, gesundheit, sneeze, sneezing face)
🥵 hot face (feverish, heat stroke, hot, hot face, red-faced, sweating)
🥶 cold face (blue-faced, cold, cold face, freezing, frostbite, icicles)
🥴 woozy face (dizzy, intoxicated, tipsy, uneven eyes, wavy mouth, woozy face)
😵 dizzy face (dizzy, face)
🤯 exploding head (exploding head, shocked)
🤠 cowboy hat face (cowboy, cowgirl, face, hat)
🥳 partying face (celebration, hat, horn, party, partying face)
😎 smiling face with sunglasses (bright, cool, face, smiling face with sunglasses, sun, sunglasses)
🤓 nerd face (face, geek, nerd)
🧐 face with monocle (face with monocle, stuffy)
😕 confused face (confused, face, meh)
😟 worried face (face, worried)
🙁 slightly frowning face (face, frown, slightly frowning face)
☹ frowning face (face, frown, frowning face)
😮 face with open mouth (face, face with open mouth, mouth, open, sympathy)
😯 hushed face (face, hushed, stunned, surprised)
😲 astonished face (astonished, face, shocked, totally)
😳 flushed face (dazed, face, flushed)
🥺 pleading face (begging, mercy, pleading face, puppy eyes)
😦 frowning face with open mouth (face, frown, frowning face with open mouth, mouth, open)
😧 anguished face (anguished, face)
😨 fearful face (face, fear, fearful, scared)
😰 anxious face with sweat (anxious face with sweat, blue, cold, face, rushed, sweat)
😥 sad but relieved face (disappointed, face, relieved, sad but relieved face, whew)
😢 crying face (cry, crying face, face, sad, tear)
😭 loudly crying face (cry, face, loudly crying face, sad, sob, tear)
😱 face screaming in fear (face, face screaming in fear, fear, munch, scared, scream)
😖 confounded face (confounded, face)
😣 persevering face (face, persevere, persevering face)
😞 disappointed face (disappointed, face)
😓 downcast face with sweat (cold, downcast face with sweat, face, sweat)
😩 weary face (face, tired, weary)
😫 tired face (face, tired)
🥱 yawning face (bored, tired, yawn, yawning face)
😤 face with steam from nose (face, face with steam from nose, triumph, won)
😡 pouting face (angry, face, mad, pouting, rage, red)
😠 angry face (angry, face, mad)
🤬 face with symbols on mouth (face with symbols on mouth, swearing)
😈 smiling face with horns (face, fairy tale, fantasy, horns, smile, smiling face with horns)
👿 angry face with horns (angry face with horns, demon, devil, face, fantasy, imp)
💀 skull (death, face, fairy tale, monster, skull)
☠ skull and crossbones (crossbones, death, face, monster, skull, skull and crossbones)
💩 pile of poo (dung, face, monster, pile of poo, poo, poop)
🤡 clown face (clown, face)
👹 ogre (creature, face, fairy tale, fantasy, monster, ogre)
👺 goblin (creature, face, fairy tale, fantasy, goblin, monster)
👻 ghost (creature, face, fairy tale, fantasy, ghost, monster)
👽 alien (alien, creature, extraterrestrial, face, fantasy, ufo)
👾 alien monster (alien, creature, extraterrestrial, face, monster, ufo)
🤖 robot (face, monster, robot)
😺 grinning cat (cat, face, grinning, mouth, open, smile)
😸 grinning cat with smiling eyes (cat, eye, face, grin, grinning cat with smiling eyes, smile)
😹 cat with tears of joy (cat, cat with tears of joy, face, joy, tear)
😻 smiling cat with heart-eyes (cat, eye, face, heart, love, smile, smiling cat with heart-eyes)
😼 cat with wry smile (cat, cat with wry smile, face, ironic, smile, wry)
😽 kissing cat (cat, eye, face, kiss, kissing cat)
🙀 weary cat (cat, face, oh, surprised, weary)
😿 crying cat (cat, cry, crying cat, face, sad, tear)
😾 pouting cat (cat, face, pouting)
🙈 see-no-evil monkey (evil, face, forbidden, monkey, see, see-no-evil monkey)
🙉 hear-no-evil monkey (evil, face, forbidden, hear, hear-no-evil monkey, monkey)
🙊 speak-no-evil monkey (evil, face, forbidden, monkey, speak, speak-no-evil monkey)
💋 kiss mark (kiss, kiss mark, lips)
💌 love letter (heart, letter, love, mail)
💘 heart with arrow (arrow, cupid, heart with arrow)
💝 heart with ribbon (heart with ribbon, ribbon, valentine)
💖 sparkling heart (excited, sparkle, sparkling heart)
💗 growing heart (excited, growing, growing heart, nervous, pulse)
💓 beating heart (beating, beating heart, heartbeat, pulsating)
💞 revolving hearts (revolving, revolving hearts)
💕 two hearts (love, two hearts)
💟 heart decoration (heart, heart decoration)
❣ heart exclamation (exclamation, heart exclamation, mark, punctuation)
💔 broken heart (break, broken, broken heart)
❤ red heart (heart, red heart)
🧡 orange heart (orange, orange heart)
💛 yellow heart (yellow, yellow heart)
💚 green heart (green, green heart)
💙 blue heart (blue, blue heart)
💜 purple heart (purple, purple heart)
🤎 brown heart (brown, heart)
🖤 black heart (black, black heart, evil, wicked)
🤍 white heart (heart, white)
💯 hundred points (100, full, hundred, hundred points, score)
💢 anger symbol (anger symbol, angry, comic, mad)
💥 collision (boom, collision, comic)
💫 dizzy (comic, dizzy, star)
💦 sweat droplets (comic, splashing, sweat, sweat droplets)
💨 dashing away (comic, dash, dashing away, running)
🕳 hole (hole)
💣 bomb (bomb, comic)
💬 speech balloon (balloon, bubble, comic, dialog, speech)
👁️‍🗨️ eye in speech bubble
🗨 left speech bubble (dialog, left speech bubble, speech)
🗯 right anger bubble (angry, balloon, bubble, mad, right anger bubble)
💭 thought balloon (balloon, bubble, comic, thought)
💤 zzz (comic, sleep, zzz)
👋 waving hand (hand, wave, waving)
🤚 raised back of hand (backhand, raised, raised back of hand)
🖐 hand with fingers splayed (finger, hand, hand with fingers splayed, splayed)
✋ raised hand (hand, raised hand)
🖖 vulcan salute (finger, hand, spock, vulcan, vulcan salute)
👌 OK hand (hand, OK)
🤏 pinching hand (pinching hand, small amount)
✌ victory hand (hand, v, victory)
🤞 crossed fingers (cross, crossed fingers, finger, hand, luck)
🤟 love-you gesture (hand, ILY, love-you gesture)
🤘 sign of the horns (finger, hand, horns, rock-on, sign of the horns)
🤙 call me hand (call, call me hand, hand)
👈 backhand index pointing left (backhand, backhand index pointing left, finger, hand, index, point)
👉 backhand index pointing right (backhand, backhand index pointing right, finger, hand, index, point)
👆 backhand index pointing up (backhand, backhand index pointing up, finger, hand, point, up)
🖕 middle finger (finger, hand, middle finger)
👇 backhand index pointing down (backhand, backhand index pointing down, down, finger, hand, point)
☝ index pointing up (finger, hand, index, index pointing up, point, up)
👍 thumbs up (+1, hand, thumb, thumbs up, up)
👎 thumbs down (-1, down, hand, thumb, thumbs down)
✊ raised fist (clenched, fist, hand, punch, raised fist)
👊 oncoming fist (clenched, fist, hand, oncoming fist, punch)
🤛 left-facing fist (fist, left-facing fist, leftwards)
🤜 right-facing fist (fist, right-facing fist, rightwards)
👏 clapping hands (clap, clapping hands, hand)
🙌 raising hands (celebration, gesture, hand, hooray, raised, raising hands)
👐 open hands (hand, open, open hands)
🤲 palms up together (palms up together, prayer)
🤝 handshake (agreement, hand, handshake, meeting, shake)
🙏 folded hands (ask, folded hands, hand, please, pray, thanks)
✍ writing hand (hand, write, writing hand)
💅 nail polish (care, cosmetics, manicure, nail, polish)
🤳 selfie (camera, phone, selfie)
💪 flexed biceps (biceps, comic, flex, flexed biceps, muscle)
🦾 mechanical arm (accessibility, mechanical arm, prosthetic)
🦿 mechanical leg (accessibility, mechanical leg, prosthetic)
🦵 leg (kick, leg, limb)
🦶 foot (foot, kick, stomp)
👂 ear (body, ear)
🦻 ear with hearing aid (accessibility, ear with hearing aid, hard of hearing)
👃 nose (body, nose)
🧠 brain (brain, intelligent)
🦷 tooth (dentist, tooth)
🦴 bone (bone, skeleton)
👀 eyes (eye, eyes, face)
👁 eye (body, eye)
👅 tongue (body, tongue)
👄 mouth (lips, mouth)
👶 baby (baby, young)
🧒 child (child, gender-neutral, unspecified gender, young)
👦 boy (boy, young)
👧 girl (girl, Virgo, young, zodiac)
🧑 person (adult, gender-neutral, person, unspecified gender)
👱 person: blond hair (blond, blond-haired person, hair, person: blond hair)
👨 man (adult, man)
🧔 man: beard (beard, man, man: beard, person)
👱‍♂️ man: blond hair
👨‍🦰 man: red hair
👨‍🦱 man: curly hair
👨‍🦳 man: white hair
👨‍🦲 man: bald
👩 woman (adult, woman)
👱‍♀️ woman: blond hair
👩‍🦰 woman: red hair
👩‍🦱 woman: curly hair
👩‍🦳 woman: white hair
👩‍🦲 woman: bald
🧓 older person (adult, gender-neutral, old, older person, unspecified gender)
👴 old man (adult, man, old)
👵 old woman (adult, old, woman)
🙍 person frowning (frown, gesture, person frowning)
🙍‍♂️ man frowning
🙍‍♀️ woman frowning
🙎 person pouting (gesture, person pouting, pouting)
🙎‍♂️ man pouting
🙎‍♀️ woman pouting
🙅 person gesturing NO (forbidden, gesture, hand, person gesturing NO, prohibited)
🙅‍♂️ man gesturing NO
🙅‍♀️ woman gesturing NO
🙆 person gesturing OK (gesture, hand, OK, person gesturing OK)
🙆‍♂️ man gesturing OK
🙆‍♀️ woman gesturing OK
💁 person tipping hand (hand, help, information, person tipping hand, sassy, tipping)
💁‍♂️ man tipping hand
💁‍♀️ woman tipping hand
🙋 person raising hand (gesture, hand, happy, person raising hand, raised)
🙋‍♂️ man raising hand
🙋‍♀️ woman raising hand
🧏 deaf person (accessibility, deaf, deaf person, ear, hear)
🧏‍♂️ deaf man
🧏‍♀️ deaf woman
🙇 person bowing (apology, bow, gesture, person bowing, sorry)
🙇‍♂️ man bowing
🙇‍♀️ woman bowing
🤦 person facepalming (disbelief, exasperation, face, palm, person facepalming)
🤦‍♂️ man facepalming
🤦‍♀️ woman facepalming
🤷 person shrugging (doubt, ignorance, indifference, person shrugging, shrug)
🤷‍♂️ man shrugging
🤷‍♀️ woman shrugging
👨‍⚕️ man health worker
👩‍⚕️ woman health worker
👨‍🎓 man student (graduate, man, student)
👩‍🎓 woman student (graduate, student, woman)
👨‍🏫 man teacher (instructor, man, professor, teacher)
👩‍🏫 woman teacher (instructor, professor, teacher, woman)
👨‍⚖️ man judge
👩‍⚖️ woman judge
👨‍🌾 man farmer (farmer, gardener, man, rancher)
👩‍🌾 woman farmer (farmer, gardener, rancher, woman)
👨‍🍳 man cook (chef, cook, man)
👩‍🍳 woman cook (chef, cook, woman)
👨‍🔧 man mechanic (electrician, man, mechanic, plumber, tradesperson)
👩‍🔧 woman mechanic (electrician, mechanic, plumber, tradesperson, woman)
👨‍🏭 man factory worker (assembly, factory, industrial, man, worker)
👩‍🏭 woman factory worker (assembly, factory, industrial, woman, worker)
👨‍💼 man office worker (architect, business, man, man office worker, manager, white-collar)
👩‍💼 woman office worker (architect, business, manager, white-collar, woman, woman office worker)
👨‍🔬 man scientist (biologist, chemist, engineer, man, physicist, scientist)
👩‍🔬 woman scientist (biologist, chemist, engineer, physicist, scientist, woman)
👨‍💻 man technologist (coder, developer, inventor, man, software, technologist)
👩‍💻 woman technologist (coder, developer, inventor, software, technologist, woman)
👨‍🎤 man singer (actor, entertainer, man, rock, singer, star)
👩‍🎤 woman singer (actor, entertainer, rock, singer, star, woman)
👨‍🎨 man artist (artist, man, palette)
👩‍🎨 woman artist (artist, palette, woman)
👨‍✈️ man pilot
👩‍✈️ woman pilot
👨‍🚀 man astronaut (astronaut, man, rocket)
👩‍🚀 woman astronaut (astronaut, rocket, woman)
👨‍🚒 man firefighter (firefighter, firetruck, man)
👩‍🚒 woman firefighter (firefighter, firetruck, woman)
👮 police officer (cop, officer, police)
👮‍♂️ man police officer
👮‍♀️ woman police officer
🕵 detective (detective, sleuth, spy)
🕵️‍♂️ man detective
🕵️‍♀️ woman detective
💂 guard (guard)
💂‍♂️ man guard
💂‍♀️ woman guard
👷 construction worker (construction, hat, worker)
👷‍♂️ man construction worker
👷‍♀️ woman construction worker
🤴 prince (prince)
👸 princess (fairy tale, fantasy, princess)
👳 person wearing turban (person wearing turban, turban)
👳‍♂️ man wearing turban
👳‍♀️ woman wearing turban
👲 man with Chinese cap (gua pi mao, hat, man, man with Chinese cap)
🧕 woman with headscarf (headscarf, hijab, mantilla, tichel, woman with headscarf)
🤵 man in tuxedo (groom, man, man in tuxedo, tuxedo)
👰 bride with veil (bride, bride with veil, veil, wedding)
🤰 pregnant woman (pregnant, woman)
🤱 breast-feeding (baby, breast, breast-feeding, nursing)
👼 baby angel (angel, baby, face, fairy tale, fantasy)
🎅 Santa Claus (celebration, Christmas, claus, father, santa, Santa Claus)
🤶 Mrs. Claus (celebration, Christmas, claus, mother, Mrs., Mrs. Claus)
🦸 superhero (good, hero, heroine, superhero, superpower)
🦸‍♂️ man superhero
🦸‍♀️ woman superhero
🦹 supervillain (criminal, evil, superpower, supervillain, villain)
🦹‍♂️ man supervillain
🦹‍♀️ woman supervillain
🧙 mage (mage, sorcerer, sorceress, witch, wizard)
🧙‍♂️ man mage
🧙‍♀️ woman mage
🧚 fairy (fairy, Oberon, Puck, Titania)
🧚‍♂️ man fairy
🧚‍♀️ woman fairy
🧛 vampire (Dracula, undead, vampire)
🧛‍♂️ man vampire
🧛‍♀️ woman vampire
🧜 merperson (mermaid, merman, merperson, merwoman)
🧜‍♂️ merman
🧜‍♀️ mermaid
🧝 elf (elf, magical)
🧝‍♂️ man elf
🧝‍♀️ woman elf
🧞 genie (djinn, genie)
🧞‍♂️ man genie
🧞‍♀️ woman genie
🧟 zombie (undead, walking dead, zombie)
🧟‍♂️ man zombie
🧟‍♀️ woman zombie
💆 person getting massage (face, massage, person getting massage, salon)
💆‍♂️ man getting massage
💆‍♀️ woman getting massage
💇 person getting haircut (barber, beauty, haircut, parlor, person getting haircut)
💇‍♂️ man getting haircut
💇‍♀️ woman getting haircut
🚶 person walking (hike, person walking, walk, walking)
🚶‍♂️ man walking
🚶‍♀️ woman walking
🧍 person standing (person standing, stand, standing)
🧍‍♂️ man standing
🧍‍♀️ woman standing
🧎 person kneeling (kneel, kneeling, person kneeling)
🧎‍♂️ man kneeling
🧎‍♀️ woman kneeling
👨‍🦯 man with probing cane (accessibility, blind, man, man with probing cane)
👩‍🦯 woman with probing cane (accessibility, blind, woman, woman with probing cane)
👨‍🦼 man in motorized wheelchair (accessibility, man, man in motorized wheelchair, wheelchair)
👩‍🦼 woman in motorized wheelchair (accessibility, wheelchair, woman, woman in motorized wheelchair)
👨‍🦽 man in manual wheelchair (accessibility, man, man in manual wheelchair, wheelchair)
👩‍🦽 woman in manual wheelchair (accessibility, wheelchair, woman, woman in manual wheelchair)
🏃 person running (marathon, person running, running)
🏃‍♂️ man running
🏃‍♀️ woman running
💃 woman dancing (dancing, woman)
🕺 man dancing (dance, man, man dancing)
🕴 man in suit levitating (business, man, man in suit levitating, suit)
👯 people with bunny ears (bunny ear, dancer, partying, people with bunny ears)
👯‍♂️ men with bunny ears
👯‍♀️ women with bunny ears
🧖 person in steamy room (person in steamy room, sauna, steam room)
🧖‍♂️ man in steamy room
🧖‍♀️ woman in steamy room
🧗 person climbing (climber, person climbing)
🧗‍♂️ man climbing
🧗‍♀️ woman climbing
🤺 person fencing (fencer, fencing, person fencing, sword)
🏇 horse racing (horse, jockey, racehorse, racing)
⛷ skier (ski, skier, snow)
🏂 snowboarder (ski, snow, snowboard, snowboarder)
🏌 person golfing (ball, golf, person golfing)
🏌️‍♂️ man golfing
🏌️‍♀️ woman golfing
🏄 person surfing (person surfing, surfing)
🏄‍♂️ man surfing
🏄‍♀️ woman surfing
🚣 person rowing boat (boat, person rowing boat, rowboat)
🚣‍♂️ man rowing boat
🚣‍♀️ woman rowing boat
🏊 person swimming (person swimming, swim)
🏊‍♂️ man swimming
🏊‍♀️ woman swimming
⛹ person bouncing ball (ball, person bouncing ball)
⛹️‍♂️ man bouncing ball
⛹️‍♀️ woman bouncing ball
🏋 person lifting weights (lifter, person lifting weights, weight)
🏋️‍♂️ man lifting weights
🏋️‍♀️ woman lifting weights
🚴 person biking (bicycle, biking, cyclist, person biking)
🚴‍♂️ man biking
🚴‍♀️ woman biking
🚵 person mountain biking (bicycle, bicyclist, bike, cyclist, mountain, person mountain biking)
🚵‍♂️ man mountain biking
🚵‍♀️ woman mountain biking
🤸 person cartwheeling (cartwheel, gymnastics, person cartwheeling)
🤸‍♂️ man cartwheeling
🤸‍♀️ woman cartwheeling
🤼 people wrestling (people wrestling, wrestle, wrestler)
🤼‍♂️ men wrestling
🤼‍♀️ women wrestling
🤽 person playing water polo (person playing water polo, polo, water)
🤽‍♂️ man playing water polo
🤽‍♀️ woman playing water polo
🤾 person playing handball (ball, handball, person playing handball)
🤾‍♂️ man playing handball
🤾‍♀️ woman playing handball
🤹 person juggling (balance, juggle, multitask, person juggling, skill)
🤹‍♂️ man juggling
🤹‍♀️ woman juggling
🧘 person in lotus position (meditation, person in lotus position, yoga)
🧘‍♂️ man in lotus position
🧘‍♀️ woman in lotus position
🛀 person taking bath (bath, bathtub, person taking bath)
🛌 person in bed (hotel, person in bed, sleep)
🧑‍🤝‍🧑 people holding hands (couple, hand, hold, holding hands, people holding hands, person)
👭 women holding hands (couple, hand, holding hands, women, women holding hands)
👫 woman and man holding hands (couple, hand, hold, holding hands, man, woman, woman and man holding hands)
👬 men holding hands (couple, Gemini, holding hands, man, men, men holding hands, twins, zodiac)
💏 kiss (couple, kiss)
👩‍❤️‍💋‍👨 kiss: woman, man
👨‍❤️‍💋‍👨 kiss: man, man
👩‍❤️‍💋‍👩 kiss: woman, woman
💑 couple with heart (couple, couple with heart, love)
👩‍❤️‍👨 couple with heart: woman, man
👨‍❤️‍👨 couple with heart: man, man
👩‍❤️‍👩 couple with heart: woman, woman
👪 family (family)
👨‍👩‍👦 family: man, woman, boy
👨‍👩‍👧 family: man, woman, girl
👨‍👩‍👧‍👦 family: man, woman, girl, boy
👨‍👩‍👦‍👦 family: man, woman, boy, boy
👨‍👩‍👧‍👧 family: man, woman, girl, girl
👨‍👨‍👦 family: man, man, boy
👨‍👨‍👧 family: man, man, girl
👨‍👨‍👧‍👦 family: man, man, girl, boy
👨‍👨‍👦‍👦 family: man, man, boy, boy
👨‍👨‍👧‍👧 family: man, man, girl, girl
👩‍👩‍👦 family: woman, woman, boy
👩‍👩‍👧 family: woman, woman, girl
👩‍👩‍👧‍👦 family: woman, woman, girl, boy
👩‍👩‍👦‍👦 family: woman, woman, boy, boy
👩‍👩‍👧‍👧 family: woman, woman, girl, girl
👨‍👦 family: man, boy
👨‍👦‍👦 family: man, boy, boy
👨‍👧 family: man, girl
👨‍👧‍👦 family: man, girl, boy
👨‍👧‍👧 family: man, girl, girl
👩‍👦 family: woman, boy
👩‍👦‍👦 family: woman, boy, boy
👩‍👧 family: woman, girl
👩‍👧‍👦 family: woman, girl, boy
👩‍👧‍👧 family: woman, girl, girl
🗣 speaking head (face, head, silhouette, speak, speaking)
👤 bust in silhouette (bust, bust in silhouette, silhouette)
👥 busts in silhouette (bust, busts in silhouette, silhouette)
👣 footprints (clothing, footprint, footprints, print)
🦰 red hair (ginger, red hair, redhead)
🦱 curly hair (afro, curly, curly hair, ringlets)
🦳 white hair (gray, hair, old, white)
🦲 bald (bald, chemotherapy, hairless, no hair, shaven)
🐵 monkey face (face, monkey)
🐒 monkey (monkey)
🦍 gorilla (gorilla)
🦧 orangutan (ape, orangutan)
🐶 dog face (dog, face, pet)
🐕 dog (dog, pet)
🦮 guide dog (accessibility, blind, guide, guide dog)
🐕‍🦺 service dog (accessibility, assistance, dog, service)
🐩 poodle (dog, poodle)
🐺 wolf (face, wolf)
🦊 fox (face, fox)
🦝 raccoon (curious, raccoon, sly)
🐱 cat face (cat, face, pet)
🐈 cat (cat, pet)
🦁 lion (face, Leo, lion, zodiac)
🐯 tiger face (face, tiger)
🐅 tiger (tiger)
🐆 leopard (leopard)
🐴 horse face (face, horse)
🐎 horse (equestrian, horse, racehorse, racing)
🦄 unicorn (face, unicorn)
🦓 zebra (stripe, zebra)
🦌 deer (deer)
🐮 cow face (cow, face)
🐂 ox (bull, ox, Taurus, zodiac)
🐃 water buffalo (buffalo, water)
🐄 cow (cow)
🐷 pig face (face, pig)
🐖 pig (pig, sow)
🐗 boar (boar, pig)
🐽 pig nose (face, nose, pig)
🐏 ram (Aries, male, ram, sheep, zodiac)
🐑 ewe (ewe, female, sheep)
🐐 goat (Capricorn, goat, zodiac)
🐪 camel (camel, dromedary, hump)
🐫 two-hump camel (bactrian, camel, hump, two-hump camel)
🦙 llama (alpaca, guanaco, llama, vicuña, wool)
🦒 giraffe (giraffe, spots)
🐘 elephant (elephant)
🦏 rhinoceros (rhinoceros)
🦛 hippopotamus (hippo, hippopotamus)
🐭 mouse face (face, mouse)
🐁 mouse (mouse)
🐀 rat (rat)
🐹 hamster (face, hamster, pet)
🐰 rabbit face (bunny, face, pet, rabbit)
🐇 rabbit (bunny, pet, rabbit)
🐿 chipmunk (chipmunk, squirrel)
🦔 hedgehog (hedgehog, spiny)
🦇 bat (bat, vampire)
🐻 bear (bear, face)
🐨 koala (bear, koala)
🐼 panda (face, panda)
🦥 sloth (lazy, sloth, slow)
🦦 otter (fishing, otter, playful)
🦨 skunk (skunk, stink)
🦘 kangaroo (Australia, joey, jump, kangaroo, marsupial)
🦡 badger (badger, honey badger, pester)
🐾 paw prints (feet, paw, paw prints, print)
🦃 turkey (bird, turkey)
🐔 chicken (bird, chicken)
🐓 rooster (bird, rooster)
🐣 hatching chick (baby, bird, chick, hatching)
🐤 baby chick (baby, bird, chick)
🐥 front-facing baby chick (baby, bird, chick, front-facing baby chick)
🐦 bird (bird)
🐧 penguin (bird, penguin)
🕊 dove (bird, dove, fly, peace)
🦅 eagle (bird, eagle)
🦆 duck (bird, duck)
🦢 swan (bird, cygnet, swan, ugly duckling)
🦉 owl (bird, owl, wise)
🦩 flamingo (flamboyant, flamingo, tropical)
🦚 peacock (bird, ostentatious, peacock, peahen, proud)
🦜 parrot (bird, parrot, pirate, talk)
🐸 frog (face, frog)
🐊 crocodile (crocodile)
🐢 turtle (terrapin, tortoise, turtle)
🦎 lizard (lizard, reptile)
🐍 snake (bearer, Ophiuchus, serpent, snake, zodiac)
🐲 dragon face (dragon, face, fairy tale)
🐉 dragon (dragon, fairy tale)
🦕 sauropod (brachiosaurus, brontosaurus, diplodocus, sauropod)
🦖 T-Rex (T-Rex, Tyrannosaurus Rex)
🐳 spouting whale (face, spouting, whale)
🐋 whale (whale)
🐬 dolphin (dolphin, flipper)
🐟 fish (fish, Pisces, zodiac)
🐠 tropical fish (fish, tropical)
🐡 blowfish (blowfish, fish)
🦈 shark (fish, shark)
🐙 octopus (octopus)
🐚 spiral shell (shell, spiral)
🐌 snail (snail)
🦋 butterfly (butterfly, insect, pretty)
🐛 bug (bug, insect)
🐜 ant (ant, insect)
🐝 honeybee (bee, honeybee, insect)
🐞 lady beetle (beetle, insect, lady beetle, ladybird, ladybug)
🦗 cricket (cricket, grasshopper)
🕷 spider (insect, spider)
🕸 spider web (spider, web)
🦂 scorpion (scorpio, Scorpio, scorpion, zodiac)
🦟 mosquito (disease, fever, insect, malaria, mosquito, virus)
🦠 microbe (amoeba, bacteria, microbe, virus)
💐 bouquet (bouquet, flower)
🌸 cherry blossom (blossom, cherry, flower)
💮 white flower (flower, white flower)
🏵 rosette (plant, rosette)
🌹 rose (flower, rose)
🥀 wilted flower (flower, wilted)
🌺 hibiscus (flower, hibiscus)
🌻 sunflower (flower, sun, sunflower)
🌼 blossom (blossom, flower)
🌷 tulip (flower, tulip)
🌱 seedling (seedling, young)
🌲 evergreen tree (evergreen tree, tree)
🌳 deciduous tree (deciduous, shedding, tree)
🌴 palm tree (palm, tree)
🌵 cactus (cactus, plant)
🌾 sheaf of rice (ear, grain, rice, sheaf of rice)
🌿 herb (herb, leaf)
☘ shamrock (plant, shamrock)
🍀 four leaf clover (4, clover, four, four-leaf clover, leaf)
🍁 maple leaf (falling, leaf, maple)
🍂 fallen leaf (fallen leaf, falling, leaf)
🍃 leaf fluttering in wind (blow, flutter, leaf, leaf fluttering in wind, wind)
🍇 grapes (fruit, grape, grapes)
🍈 melon (fruit, melon)
🍉 watermelon (fruit, watermelon)
🍊 tangerine (fruit, orange, tangerine)
🍋 lemon (citrus, fruit, lemon)
🍌 banana (banana, fruit)
🍍 pineapple (fruit, pineapple)
🥭 mango (fruit, mango, tropical)
🍎 red apple (apple, fruit, red)
🍏 green apple (apple, fruit, green)
🍐 pear (fruit, pear)
🍑 peach (fruit, peach)
🍒 cherries (berries, cherries, cherry, fruit, red)
🍓 strawberry (berry, fruit, strawberry)
🥝 kiwi fruit (food, fruit, kiwi)
🍅 tomato (fruit, tomato, vegetable)
🥥 coconut (coconut, palm, piña colada)
🥑 avocado (avocado, food, fruit)
🍆 eggplant (aubergine, eggplant, vegetable)
🥔 potato (food, potato, vegetable)
🥕 carrot (carrot, food, vegetable)
🌽 ear of corn (corn, ear, ear of corn, maize, maze)
🌶 hot pepper (hot, pepper)
🥒 cucumber (cucumber, food, pickle, vegetable)
🥬 leafy green (bok choy, cabbage, kale, leafy green, lettuce)
🥦 broccoli (broccoli, wild cabbage)
🧄 garlic (flavoring, garlic)
🧅 onion (flavoring, onion)
🍄 mushroom (mushroom, toadstool)
🥜 peanuts (food, nut, peanut, peanuts, vegetable)
🌰 chestnut (chestnut, plant)
🍞 bread (bread, loaf)
🥐 croissant (bread, crescent roll, croissant, food, french)
🥖 baguette bread (baguette, bread, food, french)
🥨 pretzel (pretzel, twisted)
🥯 bagel (bagel, bakery, schmear)
🥞 pancakes (crêpe, food, hotcake, pancake, pancakes)
🧇 waffle (indecisive, iron, waffle)
🧀 cheese wedge (cheese, cheese wedge)
🍖 meat on bone (bone, meat, meat on bone)
🍗 poultry leg (bone, chicken, drumstick, leg, poultry)
🥩 cut of meat (chop, cut of meat, lambchop, porkchop, steak)
🥓 bacon (bacon, food, meat)
🍔 hamburger (burger, hamburger)
🍟 french fries (french, fries)
🍕 pizza (cheese, pizza, slice)
🌭 hot dog (frankfurter, hot dog, hotdog, sausage)
🥪 sandwich (bread, sandwich)
🌮 taco (mexican, taco)
🌯 burrito (burrito, mexican, wrap)
🥙 stuffed flatbread (falafel, flatbread, food, gyro, kebab, stuffed)
🧆 falafel (chickpea, falafel, meatball)
🥚 egg (egg, food)
🍳 cooking (cooking, egg, frying, pan)
🥘 shallow pan of food (casserole, food, paella, pan, shallow, shallow pan of food)
🍲 pot of food (pot, pot of food, stew)
🥣 bowl with spoon (bowl with spoon, breakfast, cereal, congee)
🥗 green salad (food, green, salad)
🍿 popcorn (popcorn)
🧈 butter (butter, dairy)
🧂 salt (condiment, salt, shaker)
🥫 canned food (can, canned food)
🍱 bento box (bento, box)
🍘 rice cracker (cracker, rice)
🍙 rice ball (ball, Japanese, rice)
🍚 cooked rice (cooked, rice)
🍛 curry rice (curry, rice)
🍜 steaming bowl (bowl, noodle, ramen, steaming)
🍝 spaghetti (pasta, spaghetti)
🍠 roasted sweet potato (potato, roasted, sweet)
🍢 oden (kebab, oden, seafood, skewer, stick)
🍣 sushi (sushi)
🍤 fried shrimp (fried, prawn, shrimp, tempura)
🍥 fish cake with swirl (cake, fish, fish cake with swirl, pastry, swirl)
🥮 moon cake (autumn, festival, moon cake, yuèbǐng)
🍡 dango (dango, dessert, Japanese, skewer, stick, sweet)
🥟 dumpling (dumpling, empanada, gyōza, jiaozi, pierogi, potsticker)
🥠 fortune cookie (fortune cookie, prophecy)
🥡 takeout box (oyster pail, takeout box)
🦀 crab (Cancer, crab, zodiac)
🦞 lobster (bisque, claws, lobster, seafood)
🦐 shrimp (food, shellfish, shrimp, small)
🦑 squid (food, molusc, squid)
🦪 oyster (diving, oyster, pearl)
🍦 soft ice cream (cream, dessert, ice, icecream, soft, sweet)
🍧 shaved ice (dessert, ice, shaved, sweet)
🍨 ice cream (cream, dessert, ice, sweet)
🍩 doughnut (dessert, donut, doughnut, sweet)
🍪 cookie (cookie, dessert, sweet)
🎂 birthday cake (birthday, cake, celebration, dessert, pastry, sweet)
🍰 shortcake (cake, dessert, pastry, shortcake, slice, sweet)
🧁 cupcake (bakery, cupcake, sweet)
🥧 pie (filling, pastry, pie)
🍫 chocolate bar (bar, chocolate, dessert, sweet)
🍬 candy (candy, dessert, sweet)
🍭 lollipop (candy, dessert, lollipop, sweet)
🍮 custard (custard, dessert, pudding, sweet)
🍯 honey pot (honey, honeypot, pot, sweet)
🍼 baby bottle (baby, bottle, drink, milk)
🥛 glass of milk (drink, glass, glass of milk, milk)
☕ hot beverage (beverage, coffee, drink, hot, steaming, tea)
🍵 teacup without handle (beverage, cup, drink, tea, teacup, teacup without handle)
🍶 sake (bar, beverage, bottle, cup, drink, sake)
🍾 bottle with popping cork (bar, bottle, bottle with popping cork, cork, drink, popping)
🍷 wine glass (bar, beverage, drink, glass, wine)
🍸 cocktail glass (bar, cocktail, drink, glass)
🍹 tropical drink (bar, drink, tropical)
🍺 beer mug (bar, beer, drink, mug)
🍻 clinking beer mugs (bar, beer, clink, clinking beer mugs, drink, mug)
🥂 clinking glasses (celebrate, clink, clinking glasses, drink, glass)
🥃 tumbler glass (glass, liquor, shot, tumbler, whisky)
🥤 cup with straw (cup with straw, juice, soda)
🧃 beverage box (beverage box, juice box)
🧉 mate (drink, mate)
🧊 ice (cold, ice, ice cube, iceberg)
🥢 chopsticks (chopsticks, hashi)
🍽 fork and knife with plate (cooking, fork, fork and knife with plate, knife, plate)
🍴 fork and knife (cooking, cutlery, fork, fork and knife, knife)
🥄 spoon (spoon, tableware)
🔪 kitchen knife (cooking, hocho, kitchen knife, knife, tool, weapon)
🏺 amphora (amphora, Aquarius, cooking, drink, jug, zodiac)
🌍 globe showing Europe-Africa (Africa, earth, Europe, globe, globe showing Europe-Africa, world)
🌎 globe showing Americas (Americas, earth, globe, globe showing Americas, world)
🌏 globe showing Asia-Australia (Asia, Australia, earth, globe, globe showing Asia-Australia, world)
🌐 globe with meridians (earth, globe, globe with meridians, meridians, world)
🗺 world map (map, world)
🗾 map of Japan (Japan, map, map of Japan)
🧭 compass (compass, magnetic, navigation, orienteering)
🏔 snow-capped mountain (cold, mountain, snow, snow-capped mountain)
⛰ mountain (mountain)
🌋 volcano (eruption, mountain, volcano)
🗻 mount fuji (fuji, mount fuji, mountain)
🏕 camping (camping)
🏖 beach with umbrella (beach, beach with umbrella, umbrella)
🏜 desert (desert)
🏝 desert island (desert, island)
🏞 national park (national park, park)
🏟 stadium (stadium)
🏛 classical building (classical, classical building)
🏗 building construction (building construction, construction)
🧱 brick (brick, bricks, clay, mortar, wall)
🏘 houses (houses)
🏚 derelict house (derelict, house)
🏠 house (home, house)
🏡 house with garden (garden, home, house, house with garden)
🏢 office building (building, office building)
🏣 Japanese post office (Japanese, Japanese post office, post)
🏤 post office (European, post, post office)
🏥 hospital (doctor, hospital, medicine)
🏦 bank (bank, building)
🏨 hotel (building, hotel)
🏩 love hotel (hotel, love)
🏪 convenience store (convenience, store)
🏫 school (building, school)
🏬 department store (department, store)
🏭 factory (building, factory)
🏯 Japanese castle (castle, Japanese)
🏰 castle (castle, European)
💒 wedding (chapel, romance, wedding)
🗼 Tokyo tower (Tokyo, tower)
🗽 Statue of Liberty (liberty, statue, Statue of Liberty)
⛪ church (Christian, church, cross, religion)
🕌 mosque (islam, mosque, Muslim, religion)
🛕 hindu temple (hindu, temple)
🕍 synagogue (Jew, Jewish, religion, synagogue, temple)
⛩ shinto shrine (religion, shinto, shrine)
🕋 kaaba (islam, kaaba, Muslim, religion)
⛲ fountain (fountain)
⛺ tent (camping, tent)
🌁 foggy (fog, foggy)
🌃 night with stars (night, night with stars, star)
🏙 cityscape (city, cityscape)
🌄 sunrise over mountains (morning, mountain, sun, sunrise, sunrise over mountains)
🌅 sunrise (morning, sun, sunrise)
🌆 cityscape at dusk (city, cityscape at dusk, dusk, evening, landscape, sunset)
🌇 sunset (dusk, sun, sunset)
🌉 bridge at night (bridge, bridge at night, night)
♨ hot springs (hot, hotsprings, springs, steaming)
🎠 carousel horse (carousel, horse)
🎡 ferris wheel (amusement park, ferris, wheel)
🎢 roller coaster (amusement park, coaster, roller)
💈 barber pole (barber, haircut, pole)
🎪 circus tent (circus, tent)
🚂 locomotive (engine, locomotive, railway, steam, train)
🚃 railway car (car, electric, railway, train, tram, trolleybus)
🚄 high-speed train (high-speed train, railway, shinkansen, speed, train)
🚅 bullet train (bullet, railway, shinkansen, speed, train)
🚆 train (railway, train)
🚇 metro (metro, subway)
🚈 light rail (light rail, railway)
🚉 station (railway, station, train)
🚊 tram (tram, trolleybus)
🚝 monorail (monorail, vehicle)
🚞 mountain railway (car, mountain, railway)
🚋 tram car (car, tram, trolleybus)
🚌 bus (bus, vehicle)
🚍 oncoming bus (bus, oncoming)
🚎 trolleybus (bus, tram, trolley, trolleybus)
🚐 minibus (bus, minibus)
🚑 ambulance (ambulance, vehicle)
🚒 fire engine (engine, fire, truck)
🚓 police car (car, patrol, police)
🚔 oncoming police car (car, oncoming, police)
🚕 taxi (taxi, vehicle)
🚖 oncoming taxi (oncoming, taxi)
🚗 automobile (automobile, car)
🚘 oncoming automobile (automobile, car, oncoming)
🚙 sport utility vehicle (recreational, sport utility, sport utility vehicle)
🚚 delivery truck (delivery, truck)
🚛 articulated lorry (articulated lorry, lorry, semi, truck)
🚜 tractor (tractor, vehicle)
🏎 racing car (car, racing)
🏍 motorcycle (motorcycle, racing)
🛵 motor scooter (motor, scooter)
🦽 manual wheelchair (accessibility, manual wheelchair)
🦼 motorized wheelchair (accessibility, motorized wheelchair)
🛺 auto rickshaw (auto rickshaw, tuk tuk)
🚲 bicycle (bicycle, bike)
🛴 kick scooter (kick, scooter)
🛹 skateboard (board, skateboard)
🚏 bus stop (bus, busstop, stop)
🛣 motorway (highway, motorway, road)
🛤 railway track (railway, railway track, train)
🛢 oil drum (drum, oil)
⛽ fuel pump (diesel, fuel, fuelpump, gas, pump, station)
🚨 police car light (beacon, car, light, police, revolving)
🚥 horizontal traffic light (horizontal traffic light, light, signal, traffic)
🚦 vertical traffic light (light, signal, traffic, vertical traffic light)
🛑 stop sign (octagonal, sign, stop)
🚧 construction (barrier, construction)
⚓ anchor (anchor, ship, tool)
⛵ sailboat (boat, resort, sailboat, sea, yacht)
🛶 canoe (boat, canoe)
🚤 speedboat (boat, speedboat)
🛳 passenger ship (passenger, ship)
⛴ ferry (boat, ferry, passenger)
🛥 motor boat (boat, motor boat, motorboat)
🚢 ship (boat, passenger, ship)
✈ airplane (aeroplane, airplane)
🛩 small airplane (aeroplane, airplane, small airplane)
🛫 airplane departure (aeroplane, airplane, check-in, departure, departures)
🛬 airplane arrival (aeroplane, airplane, airplane arrival, arrivals, arriving, landing)
🪂 parachute (hang-glide, parachute, parasail, skydive)
💺 seat (chair, seat)
🚁 helicopter (helicopter, vehicle)
🚟 suspension railway (railway, suspension)
🚠 mountain cableway (cable, gondola, mountain, mountain cableway)
🚡 aerial tramway (aerial, cable, car, gondola, tramway)
🛰 satellite (satellite, space)
🚀 rocket (rocket, space)
🛸 flying saucer (flying saucer, UFO)
🛎 bellhop bell (bell, bellhop, hotel)
🧳 luggage (luggage, packing, travel)
⌛ hourglass done (hourglass done, sand, timer)
⏳ hourglass not done (hourglass, hourglass not done, sand, timer)
⌚ watch (clock, watch)
⏰ alarm clock (alarm, clock)
⏱ stopwatch (clock, stopwatch)
⏲ timer clock (clock, timer)
🕰 mantelpiece clock (clock, mantelpiece clock)
🕛 twelve o’clock (00, 12, 12:00, clock, o’clock, twelve)
🕧 twelve-thirty (12, 12:30, clock, thirty, twelve, twelve-thirty)
🕐 one o’clock (00, 1, 1:00, clock, o’clock, one)
🕜 one-thirty (1, 1:30, clock, one, one-thirty, thirty)
🕑 two o’clock (00, 2, 2:00, clock, o’clock, two)
🕝 two-thirty (2, 2:30, clock, thirty, two, two-thirty)
🕒 three o’clock (00, 3, 3:00, clock, o’clock, three)
🕞 three-thirty (3, 3:30, clock, thirty, three, three-thirty)
🕓 four o’clock (00, 4, 4:00, clock, four, o’clock)
🕟 four-thirty (4, 4:30, clock, four, four-thirty, thirty)
🕔 five o’clock (00, 5, 5:00, clock, five, o’clock)
🕠 five-thirty (5, 5:30, clock, five, five-thirty, thirty)
🕕 six o’clock (00, 6, 6:00, clock, o’clock, six)
🕡 six-thirty (6, 6:30, clock, six, six-thirty, thirty)
🕖 seven o’clock (00, 7, 7:00, clock, o’clock, seven)
🕢 seven-thirty (7, 7:30, clock, seven, seven-thirty, thirty)
🕗 eight o’clock (00, 8, 8:00, clock, eight, o’clock)
🕣 eight-thirty (8, 8:30, clock, eight, eight-thirty, thirty)
🕘 nine o’clock (00, 9, 9:00, clock, nine, o’clock)
🕤 nine-thirty (9, 9:30, clock, nine, nine-thirty, thirty)
🕙 ten o’clock (00, 10, 10:00, clock, o’clock, ten)
🕥 ten-thirty (10, 10:30, clock, ten, ten-thirty, thirty)
🕚 eleven o’clock (00, 11, 11:00, clock, eleven, o’clock)
🕦 eleven-thirty (11, 11:30, clock, eleven, eleven-thirty, thirty)
🌑 new moon (dark, moon, new moon)
🌒 waxing crescent moon (crescent, moon, waxing)
🌓 first quarter moon (first quarter moon, moon, quarter)
🌔 waxing gibbous moon (gibbous, moon, waxing)
🌕 full moon (full, moon)
🌖 waning gibbous moon (gibbous, moon, waning)
🌗 last quarter moon (last quarter moon, moon, quarter)
🌘 waning crescent moon (crescent, moon, waning)
🌙 crescent moon (crescent, moon)
🌚 new moon face (face, moon, new moon face)
🌛 first quarter moon face (face, first quarter moon face, moon, quarter)
🌜 last quarter moon face (face, last quarter moon face, moon, quarter)
🌡 thermometer (thermometer, weather)
☀ sun (bright, rays, sun, sunny)
🌝 full moon face (bright, face, full, moon)
🌞 sun with face (bright, face, sun, sun with face)
🪐 ringed planet (ringed planet, saturn, saturnine)
⭐ star (star)
🌟 glowing star (glittery, glow, glowing star, shining, sparkle, star)
🌠 shooting star (falling, shooting, star)
🌌 milky way (milky way, space)
☁ cloud (cloud, weather)
⛅ sun behind cloud (cloud, sun, sun behind cloud)
⛈ cloud with lightning and rain (cloud, cloud with lightning and rain, rain, thunder)
🌤 sun behind small cloud (cloud, sun, sun behind small cloud)
🌥 sun behind large cloud (cloud, sun, sun behind large cloud)
🌦 sun behind rain cloud (cloud, rain, sun, sun behind rain cloud)
🌧 cloud with rain (cloud, cloud with rain, rain)
🌨 cloud with snow (cloud, cloud with snow, cold, snow)
🌩 cloud with lightning (cloud, cloud with lightning, lightning)
🌪 tornado (cloud, tornado, whirlwind)
🌫 fog (cloud, fog)
🌬 wind face (blow, cloud, face, wind)
🌀 cyclone (cyclone, dizzy, hurricane, twister, typhoon)
🌈 rainbow (rain, rainbow)
🌂 closed umbrella (closed umbrella, clothing, rain, umbrella)
☂ umbrella (clothing, rain, umbrella)
☔ umbrella with rain drops (clothing, drop, rain, umbrella, umbrella with rain drops)
⛱ umbrella on ground (rain, sun, umbrella, umbrella on ground)
⚡ high voltage (danger, electric, high voltage, lightning, voltage, zap)
❄ snowflake (cold, snow, snowflake)
☃ snowman (cold, snow, snowman)
⛄ snowman without snow (cold, snow, snowman, snowman without snow)
☄ comet (comet, space)
🔥 fire (fire, flame, tool)
💧 droplet (cold, comic, drop, droplet, sweat)
🌊 water wave (ocean, water, wave)
🎃 jack-o-lantern (celebration, halloween, jack, jack-o-lantern, lantern)
🎄 Christmas tree (celebration, Christmas, tree)
🎆 fireworks (celebration, fireworks)
🎇 sparkler (celebration, fireworks, sparkle, sparkler)
🧨 firecracker (dynamite, explosive, firecracker, fireworks)
✨ sparkles (*, sparkle, sparkles, star)
🎈 balloon (balloon, celebration)
🎉 party popper (celebration, party, popper, tada)
🎊 confetti ball (ball, celebration, confetti)
🎋 tanabata tree (banner, celebration, Japanese, tanabata tree, tree)
🎍 pine decoration (bamboo, celebration, Japanese, pine, pine decoration)
🎎 Japanese dolls (celebration, doll, festival, Japanese, Japanese dolls)
🎏 carp streamer (carp, celebration, streamer)
🎐 wind chime (bell, celebration, chime, wind)
🎑 moon viewing ceremony (celebration, ceremony, moon, moon viewing ceremony)
🧧 red envelope (gift, good luck, hóngbāo, lai see, money, red envelope)
🎀 ribbon (celebration, ribbon)
🎁 wrapped gift (box, celebration, gift, present, wrapped)
🎗 reminder ribbon (celebration, reminder, ribbon)
🎟 admission tickets (admission, admission tickets, ticket)
🎫 ticket (admission, ticket)
🎖 military medal (celebration, medal, military)
🏆 trophy (prize, trophy)
🏅 sports medal (medal, sports medal)
🥇 1st place medal (1st place medal, first, gold, medal)
🥈 2nd place medal (2nd place medal, medal, second, silver)
🥉 3rd place medal (3rd place medal, bronze, medal, third)
⚽ soccer ball (ball, football, soccer)
⚾ baseball (ball, baseball)
🥎 softball (ball, glove, softball, underarm)
🏀 basketball (ball, basketball, hoop)
🏐 volleyball (ball, game, volleyball)
🏈 american football (american, ball, football)
🏉 rugby football (ball, football, rugby)
🎾 tennis (ball, racquet, tennis)
🥏 flying disc (flying disc, ultimate)
🎳 bowling (ball, bowling, game)
🏏 cricket game (ball, bat, cricket game, game)
🏑 field hockey (ball, field, game, hockey, stick)
🏒 ice hockey (game, hockey, ice, puck, stick)
🥍 lacrosse (ball, goal, lacrosse, stick)
🏓 ping pong (ball, bat, game, paddle, ping pong, table tennis)
🏸 badminton (badminton, birdie, game, racquet, shuttlecock)
🥊 boxing glove (boxing, glove)
🥋 martial arts uniform (judo, karate, martial arts, martial arts uniform, taekwondo, uniform)
🥅 goal net (goal, net)
⛳ flag in hole (flag in hole, golf, hole)
⛸ ice skate (ice, skate)
🎣 fishing pole (fish, fishing pole, pole)
🤿 diving mask (diving, diving mask, scuba, snorkeling)
🎽 running shirt (athletics, running, sash, shirt)
🎿 skis (ski, skis, snow)
🛷 sled (sled, sledge, sleigh)
🥌 curling stone (curling stone, game, rock)
🎯 direct hit (bullseye, dart, direct hit, game, hit, target)
🪀 yo-yo (fluctuate, toy, yo-yo)
🪁 kite (fly, kite, soar)
🎱 pool 8 ball (8, ball, billiard, eight, game, pool 8 ball)
🔮 crystal ball (ball, crystal, fairy tale, fantasy, fortune, tool)
🧿 nazar amulet (bead, charm, evil-eye, nazar, nazar amulet, talisman)
🎮 video game (controller, game, video game)
🕹 joystick (game, joystick, video game)
🎰 slot machine (game, slot, slot machine)
🎲 game die (dice, die, game)
🧩 puzzle piece (clue, interlocking, jigsaw, piece, puzzle)
🧸 teddy bear (plaything, plush, stuffed, teddy bear, toy)
♠ spade suit (card, game, spade suit)
♥ heart suit (card, game, heart suit)
♦ diamond suit (card, diamond suit, game)
♣ club suit (card, club suit, game)
♟ chess pawn (chess, chess pawn, dupe, expendable)
🃏 joker (card, game, joker, wildcard)
🀄 mahjong red dragon (game, mahjong, mahjong red dragon, red)
🎴 flower playing cards (card, flower, flower playing cards, game, Japanese, playing)
🎭 performing arts (art, mask, performing, performing arts, theater, theatre)
🖼 framed picture (art, frame, framed picture, museum, painting, picture)
🎨 artist palette (art, artist palette, museum, painting, palette)
🧵 thread (needle, sewing, spool, string, thread)
🧶 yarn (ball, crochet, knit, yarn)
👓 glasses (clothing, eye, eyeglasses, eyewear, glasses)
🕶 sunglasses (dark, eye, eyewear, glasses, sunglasses)
🥽 goggles (eye protection, goggles, swimming, welding)
🥼 lab coat (doctor, experiment, lab coat, scientist)
🦺 safety vest (emergency, safety, vest)
👔 necktie (clothing, necktie, tie)
👕 t-shirt (clothing, shirt, t-shirt, tshirt)
👖 jeans (clothing, jeans, pants, trousers)
🧣 scarf (neck, scarf)
🧤 gloves (gloves, hand)
🧥 coat (coat, jacket)
🧦 socks (socks, stocking)
👗 dress (clothing, dress)
👘 kimono (clothing, kimono)
🥻 sari (clothing, dress, sari)
🩱 one-piece swimsuit (bathing suit, one-piece swimsuit)
🩲 briefs (bathing suit, briefs, one-piece, swimsuit, underwear)
🩳 shorts (bathing suit, pants, shorts, underwear)
👙 bikini (bikini, clothing, swim)
👚 woman’s clothes (clothing, woman, woman’s clothes)
👛 purse (clothing, coin, purse)
👜 handbag (bag, clothing, handbag, purse)
👝 clutch bag (bag, clothing, clutch bag, pouch)
🛍 shopping bags (bag, hotel, shopping, shopping bags)
🎒 backpack (backpack, bag, rucksack, satchel, school)
👞 man’s shoe (clothing, man, man’s shoe, shoe)
👟 running shoe (athletic, clothing, running shoe, shoe, sneaker)
🥾 hiking boot (backpacking, boot, camping, hiking)
🥿 flat shoe (ballet flat, flat shoe, slip-on, slipper)
👠 high-heeled shoe (clothing, heel, high-heeled shoe, shoe, woman)
👡 woman’s sandal (clothing, sandal, shoe, woman, woman’s sandal)
🩰 ballet shoes (ballet, ballet shoes, dance)
👢 woman’s boot (boot, clothing, shoe, woman, woman’s boot)
👑 crown (clothing, crown, king, queen)
👒 woman’s hat (clothing, hat, woman, woman’s hat)
🎩 top hat (clothing, hat, top, tophat)
🎓 graduation cap (cap, celebration, clothing, graduation, hat)
🧢 billed cap (baseball cap, billed cap)
⛑ rescue worker’s helmet (aid, cross, face, hat, helmet, rescue worker’s helmet)
📿 prayer beads (beads, clothing, necklace, prayer, religion)
💄 lipstick (cosmetics, lipstick, makeup)
💍 ring (diamond, ring)
💎 gem stone (diamond, gem, gem stone, jewel)
🔇 muted speaker (mute, muted speaker, quiet, silent, speaker)
🔈 speaker low volume (soft, speaker low volume)
🔉 speaker medium volume (medium, speaker medium volume)
🔊 speaker high volume (loud, speaker high volume)
📢 loudspeaker (loud, loudspeaker, public address)
📣 megaphone (cheering, megaphone)
📯 postal horn (horn, post, postal)
🔔 bell (bell)
🔕 bell with slash (bell, bell with slash, forbidden, mute, quiet, silent)
🎼 musical score (music, musical score, score)
🎵 musical note (music, musical note, note)
🎶 musical notes (music, musical notes, note, notes)
🎙 studio microphone (mic, microphone, music, studio)
🎚 level slider (level, music, slider)
🎛 control knobs (control, knobs, music)
🎤 microphone (karaoke, mic, microphone)
🎧 headphone (earbud, headphone)
📻 radio (radio, video)
🎷 saxophone (instrument, music, sax, saxophone)
🎸 guitar (guitar, instrument, music)
🎹 musical keyboard (instrument, keyboard, music, musical keyboard, piano)
🎺 trumpet (instrument, music, trumpet)
🎻 violin (instrument, music, violin)
🪕 banjo (banjo, music, stringed)
🥁 drum (drum, drumsticks, music)
📱 mobile phone (cell, mobile, phone, telephone)
📲 mobile phone with arrow (arrow, cell, mobile, mobile phone with arrow, phone, receive)
☎ telephone (phone, telephone)
📞 telephone receiver (phone, receiver, telephone)
📟 pager (pager)
📠 fax machine (fax, fax machine)
🔋 battery (battery)
🔌 electric plug (electric, electricity, plug)
💻 laptop computer (computer, laptop computer, pc, personal)
🖥 desktop computer (computer, desktop)
🖨 printer (computer, printer)
⌨ keyboard (computer, keyboard)
🖱 computer mouse (computer, computer mouse)
🖲 trackball (computer, trackball)
💽 computer disk (computer, disk, minidisk, optical)
💾 floppy disk (computer, disk, floppy)
💿 optical disk (cd, computer, disk, optical)
📀 dvd (blu-ray, computer, disk, dvd, optical)
🧮 abacus (abacus, calculation)
🎥 movie camera (camera, cinema, movie)
🎞 film frames (cinema, film, frames, movie)
📽 film projector (cinema, film, movie, projector, video)
🎬 clapper board (clapper, clapper board, movie)
📺 television (television, tv, video)
📷 camera (camera, video)
📸 camera with flash (camera, camera with flash, flash, video)
📹 video camera (camera, video)
📼 videocassette (tape, vhs, video, videocassette)
🔍 magnifying glass tilted left (glass, magnifying, magnifying glass tilted left, search, tool)
🔎 magnifying glass tilted right (glass, magnifying, magnifying glass tilted right, search, tool)
🕯 candle (candle, light)
💡 light bulb (bulb, comic, electric, idea, light)
🔦 flashlight (electric, flashlight, light, tool, torch)
🏮 red paper lantern (bar, lantern, light, red, red paper lantern)
🪔 diya lamp (diya, lamp, oil)
📔 notebook with decorative cover (book, cover, decorated, notebook, notebook with decorative cover)
📕 closed book (book, closed)
📖 open book (book, open)
📗 green book (book, green)
📘 blue book (blue, book)
📙 orange book (book, orange)
📚 books (book, books)
📓 notebook (notebook)
📒 ledger (ledger, notebook)
📃 page with curl (curl, document, page, page with curl)
📜 scroll (paper, scroll)
📄 page facing up (document, page, page facing up)
📰 newspaper (news, newspaper, paper)
🗞 rolled-up newspaper (news, newspaper, paper, rolled, rolled-up newspaper)
📑 bookmark tabs (bookmark, mark, marker, tabs)
🔖 bookmark (bookmark, mark)
🏷 label (label)
💰 money bag (bag, dollar, money, moneybag)
💴 yen banknote (banknote, bill, currency, money, note, yen)
💵 dollar banknote (banknote, bill, currency, dollar, money, note)
💶 euro banknote (banknote, bill, currency, euro, money, note)
💷 pound banknote (banknote, bill, currency, money, note, pound)
💸 money with wings (banknote, bill, fly, money, money with wings, wings)
💳 credit card (card, credit, money)
🧾 receipt (accounting, bookkeeping, evidence, proof, receipt)
💹 chart increasing with yen (chart, chart increasing with yen, graph, growth, money, yen)
💱 currency exchange (bank, currency, exchange, money)
💲 heavy dollar sign (currency, dollar, heavy dollar sign, money)
✉ envelope (email, envelope, letter)
📧 e-mail (e-mail, email, letter, mail)
📨 incoming envelope (e-mail, email, envelope, incoming, letter, receive)
📩 envelope with arrow (arrow, e-mail, email, envelope, envelope with arrow, outgoing)
📤 outbox tray (box, letter, mail, outbox, sent, tray)
📥 inbox tray (box, inbox, letter, mail, receive, tray)
📦 package (box, package, parcel)
📫 closed mailbox with raised flag (closed, closed mailbox with raised flag, mail, mailbox, postbox)
📪 closed mailbox with lowered flag (closed, closed mailbox with lowered flag, lowered, mail, mailbox, postbox)
📬 open mailbox with raised flag (mail, mailbox, open, open mailbox with raised flag, postbox)
📭 open mailbox with lowered flag (lowered, mail, mailbox, open, open mailbox with lowered flag, postbox)
📮 postbox (mail, mailbox, postbox)
🗳 ballot box with ballot (ballot, ballot box with ballot, box)
✏ pencil (pencil)
✒ black nib (black nib, nib, pen)
🖋 fountain pen (fountain, pen)
🖊 pen (ballpoint, pen)
🖌 paintbrush (paintbrush, painting)
🖍 crayon (crayon)
📝 memo (memo, pencil)
💼 briefcase (briefcase)
📁 file folder (file, folder)
📂 open file folder (file, folder, open)
🗂 card index dividers (card, dividers, index)
📅 calendar (calendar, date)
📆 tear-off calendar (calendar, tear-off calendar)
🗒 spiral notepad (note, pad, spiral, spiral notepad)
🗓 spiral calendar (calendar, pad, spiral)
📇 card index (card, index, rolodex)
📈 chart increasing (chart, chart increasing, graph, growth, trend, upward)
📉 chart decreasing (chart, chart decreasing, down, graph, trend)
📊 bar chart (bar, chart, graph)
📋 clipboard (clipboard)
📌 pushpin (pin, pushpin)
📍 round pushpin (pin, pushpin, round pushpin)
📎 paperclip (paperclip)
🖇 linked paperclips (link, linked paperclips, paperclip)
📏 straight ruler (ruler, straight edge, straight ruler)
📐 triangular ruler (ruler, set, triangle, triangular ruler)
✂ scissors (cutting, scissors, tool)
🗃 card file box (box, card, file)
🗄 file cabinet (cabinet, file, filing)
🗑 wastebasket (wastebasket)
🔒 locked (closed, locked)
🔓 unlocked (lock, open, unlock, unlocked)
🔏 locked with pen (ink, lock, locked with pen, nib, pen, privacy)
🔐 locked with key (closed, key, lock, locked with key, secure)
🔑 key (key, lock, password)
🗝 old key (clue, key, lock, old)
🔨 hammer (hammer, tool)
🪓 axe (axe, chop, hatchet, split, wood)
⛏ pick (mining, pick, tool)
⚒ hammer and pick (hammer, hammer and pick, pick, tool)
🛠 hammer and wrench (hammer, hammer and wrench, spanner, tool, wrench)
🗡 dagger (dagger, knife, weapon)
⚔ crossed swords (crossed, swords, weapon)
🔫 pistol (gun, handgun, pistol, revolver, tool, weapon)
🏹 bow and arrow (archer, arrow, bow, bow and arrow, Sagittarius, zodiac)
🛡 shield (shield, weapon)
🔧 wrench (spanner, tool, wrench)
🔩 nut and bolt (bolt, nut, nut and bolt, tool)
⚙ gear (cog, cogwheel, gear, tool)
🗜 clamp (clamp, compress, tool, vice)
⚖ balance scale (balance, justice, Libra, scale, zodiac)
🦯 probing cane (accessibility, blind, probing cane)
🔗 link (link)
⛓ chains (chain, chains)
🧰 toolbox (chest, mechanic, tool, toolbox)
🧲 magnet (attraction, horseshoe, magnet, magnetic)
⚗ alembic (alembic, chemistry, tool)
🧪 test tube (chemist, chemistry, experiment, lab, science, test tube)
🧫 petri dish (bacteria, biologist, biology, culture, lab, petri dish)
🧬 dna (biologist, dna, evolution, gene, genetics, life)
🔬 microscope (microscope, science, tool)
🔭 telescope (science, telescope, tool)
📡 satellite antenna (antenna, dish, satellite)
💉 syringe (medicine, needle, shot, sick, syringe)
🩸 drop of blood (bleed, blood donation, drop of blood, injury, medicine, menstruation)
💊 pill (doctor, medicine, pill, sick)
🩹 adhesive bandage (adhesive bandage, bandage)
🩺 stethoscope (doctor, heart, medicine, stethoscope)
🚪 door (door)
🛏 bed (bed, hotel, sleep)
🛋 couch and lamp (couch, couch and lamp, hotel, lamp)
🪑 chair (chair, seat, sit)
🚽 toilet (toilet)
🚿 shower (shower, water)
🛁 bathtub (bath, bathtub)
🪒 razor (razor, sharp, shave)
🧴 lotion bottle (lotion, lotion bottle, moisturizer, shampoo, sunscreen)
🧷 safety pin (diaper, punk rock, safety pin)
🧹 broom (broom, cleaning, sweeping, witch)
🧺 basket (basket, farming, laundry, picnic)
🧻 roll of paper (paper towels, roll of paper, toilet paper)
🧼 soap (bar, bathing, cleaning, lather, soap, soapdish)
🧽 sponge (absorbing, cleaning, porous, sponge)
🧯 fire extinguisher (extinguish, fire, fire extinguisher, quench)
🛒 shopping cart (cart, shopping, trolley)
🚬 cigarette (cigarette, smoking)
⚰ coffin (coffin, death)
⚱ funeral urn (ashes, death, funeral, urn)
🗿 moai (face, moai, moyai, statue)
🏧 ATM sign (atm, ATM sign, automated, bank, teller)
🚮 litter in bin sign (litter, litter bin, litter in bin sign)
🚰 potable water (drinking, potable, water)
♿ wheelchair symbol (access, wheelchair symbol)
🚹 men’s room (lavatory, man, men’s room, restroom, wc)
🚺 women’s room (lavatory, restroom, wc, woman, women’s room)
🚻 restroom (lavatory, restroom, WC)
🚼 baby symbol (baby, baby symbol, changing)
🚾 water closet (closet, lavatory, restroom, water, wc)
🛂 passport control (control, passport)
🛃 customs (customs)
🛄 baggage claim (baggage, claim)
🛅 left luggage (baggage, left luggage, locker, luggage)
⚠ warning (warning)
🚸 children crossing (child, children crossing, crossing, pedestrian, traffic)
⛔ no entry (entry, forbidden, no, not, prohibited, traffic)
🚫 prohibited (entry, forbidden, no, not, prohibited)
🚳 no bicycles (bicycle, bike, forbidden, no, no bicycles, prohibited)
🚭 no smoking (forbidden, no, not, prohibited, smoking)
🚯 no littering (forbidden, litter, no, no littering, not, prohibited)
🚱 non-potable water (non-drinking, non-potable, water)
🚷 no pedestrians (forbidden, no, no pedestrians, not, pedestrian, prohibited)
📵 no mobile phones (cell, forbidden, mobile, no, no mobile phones, phone)
🔞 no one under eighteen (18, age restriction, eighteen, no one under eighteen, prohibited, underage)
☢ radioactive (radioactive, sign)
☣ biohazard (biohazard, sign)
⬆ up arrow (arrow, cardinal, direction, north, up arrow)
↗ up-right arrow (arrow, direction, intercardinal, northeast, up-right arrow)
➡ right arrow (arrow, cardinal, direction, east, right arrow)
↘ down-right arrow (arrow, direction, down-right arrow, intercardinal, southeast)
⬇ down arrow (arrow, cardinal, direction, down, south)
↙ down-left arrow (arrow, direction, down-left arrow, intercardinal, southwest)
⬅ left arrow (arrow, cardinal, direction, left arrow, west)
↖ up-left arrow (arrow, direction, intercardinal, northwest, up-left arrow)
↕ up-down arrow (arrow, up-down arrow)
↔ left-right arrow (arrow, left-right arrow)
↩ right arrow curving left (arrow, right arrow curving left)
↪ left arrow curving right (arrow, left arrow curving right)
⤴ right arrow curving up (arrow, right arrow curving up)
⤵ right arrow curving down (arrow, down, right arrow curving down)
🔃 clockwise vertical arrows (arrow, clockwise, clockwise vertical arrows, reload)
🔄 counterclockwise arrows button (anticlockwise, arrow, counterclockwise, counterclockwise arrows button, withershins)
🔙 BACK arrow (arrow, back, BACK arrow)
🔚 END arrow (arrow, end, END arrow)
🔛 ON! arrow (arrow, mark, on, ON! arrow)
🔜 SOON arrow (arrow, soon, SOON arrow)
🔝 TOP arrow (arrow, top, TOP arrow, up)
🛐 place of worship (place of worship, religion, worship)
⚛ atom symbol (atheist, atom, atom symbol)
🕉 om (Hindu, om, religion)
✡ star of David (David, Jew, Jewish, religion, star, star of David)
☸ wheel of dharma (Buddhist, dharma, religion, wheel, wheel of dharma)
☯ yin yang (religion, tao, taoist, yang, yin)
✝ latin cross (Christian, cross, latin cross, religion)
☦ orthodox cross (Christian, cross, orthodox cross, religion)
☪ star and crescent (islam, Muslim, religion, star and crescent)
☮ peace symbol (peace, peace symbol)
🕎 menorah (candelabrum, candlestick, menorah, religion)
🔯 dotted six-pointed star (dotted six-pointed star, fortune, star)
♈ Aries (Aries, ram, zodiac)
♉ Taurus (bull, ox, Taurus, zodiac)
♊ Gemini (Gemini, twins, zodiac)
♋ Cancer (Cancer, crab, zodiac)
♌ Leo (Leo, lion, zodiac)
♍ Virgo (Virgo, zodiac)
♎ Libra (balance, justice, Libra, scales, zodiac)
♏ Scorpio (Scorpio, scorpion, scorpius, zodiac)
♐ Sagittarius (archer, Sagittarius, zodiac)
♑ Capricorn (Capricorn, goat, zodiac)
♒ Aquarius (Aquarius, bearer, water, zodiac)
♓ Pisces (fish, Pisces, zodiac)
⛎ Ophiuchus (bearer, Ophiuchus, serpent, snake, zodiac)
🔀 shuffle tracks button (arrow, crossed, shuffle tracks button)
🔁 repeat button (arrow, clockwise, repeat, repeat button)
🔂 repeat single button (arrow, clockwise, once, repeat single button)
▶ play button (arrow, play, play button, right, triangle)
⏩ fast-forward button (arrow, double, fast, fast-forward button, forward)
⏭ next track button (arrow, next scene, next track, next track button, triangle)
⏯ play or pause button (arrow, pause, play, play or pause button, right, triangle)
◀ reverse button (arrow, left, reverse, reverse button, triangle)
⏪ fast reverse button (arrow, double, fast reverse button, rewind)
⏮ last track button (arrow, last track button, previous scene, previous track, triangle)
🔼 upwards button (arrow, button, red, upwards button)
⏫ fast up button (arrow, double, fast up button)
🔽 downwards button (arrow, button, down, downwards button, red)
⏬ fast down button (arrow, double, down, fast down button)
⏸ pause button (bar, double, pause, pause button, vertical)
⏹ stop button (square, stop, stop button)
⏺ record button (circle, record, record button)
⏏ eject button (eject, eject button)
🎦 cinema (camera, cinema, film, movie)
🔅 dim button (brightness, dim, dim button, low)
🔆 bright button (bright, bright button, brightness)
📶 antenna bars (antenna, antenna bars, bar, cell, mobile, phone)
📳 vibration mode (cell, mobile, mode, phone, telephone, vibration)
📴 mobile phone off (cell, mobile, off, phone, telephone)
♀ female sign (female sign, woman)
♂ male sign (male sign, man)
⚕ medical symbol (aesculapius, medical symbol, medicine, staff)
♾ infinity (forever, infinity, unbounded, universal)
♻ recycling symbol (recycle, recycling symbol)
⚜ fleur-de-lis (fleur-de-lis)
🔱 trident emblem (anchor, emblem, ship, tool, trident)
📛 name badge (badge, name)
🔰 Japanese symbol for beginner (beginner, chevron, Japanese, Japanese symbol for beginner, leaf)
⭕ hollow red circle (circle, hollow red circle, large, o, red)
✅ check mark button (✓, button, check, mark)
☑ check box with check (✓, box, check, check box with check)
✔ check mark (✓, check, mark)
✖ multiplication sign (×, cancel, multiplication, multiply, sign, x)
❌ cross mark (×, cancel, cross, mark, multiplication, multiply, x)
❎ cross mark button (×, cross mark button, mark, square, x)
➕ plus sign (+, math, plus, sign)
➖ minus sign (-, −, math, minus, sign)
➗ division sign (÷, division, math, sign)
➰ curly loop (curl, curly loop, loop)
➿ double curly loop (curl, double, double curly loop, loop)
〽 part alternation mark (mark, part, part alternation mark)
✳ eight-spoked asterisk (*, asterisk, eight-spoked asterisk)
✴ eight-pointed star (*, eight-pointed star, star)
❇ sparkle (*, sparkle)
‼ double exclamation mark (!, !!, bangbang, double exclamation mark, exclamation, mark)
⁉ exclamation question mark (!, !?, ?, exclamation, interrobang, mark, punctuation, question)
❓ question mark (?, mark, punctuation, question)
❔ white question mark (?, mark, outlined, punctuation, question, white question mark)
❕ white exclamation mark (!, exclamation, mark, outlined, punctuation, white exclamation mark)
❗ exclamation mark (!, exclamation, mark, punctuation)
〰 wavy dash (dash, punctuation, wavy)
© copyright (c, copyright)
® registered (r, registered)
™ trade mark (mark, tm, trade mark, trademark)
#️⃣ keycap: #
*️⃣ keycap: *
0️⃣ keycap: 0
1️⃣ keycap: 1
2️⃣ keycap: 2
3️⃣ keycap: 3
4️⃣ keycap: 4
5️⃣ keycap: 5
6️⃣ keycap: 6
7️⃣ keycap: 7
8️⃣ keycap: 8
9️⃣ keycap: 9
🔟 keycap: 10
🔠 input latin uppercase (ABCD, input, latin, letters, uppercase)
🔡 input latin lowercase (abcd, input, latin, letters, lowercase)
🔢 input numbers (1234, input, numbers)
🔣 input symbols (〒♪&%, input, input symbols)
🔤 input latin letters (abc, alphabet, input, latin, letters)
🅰 A button (blood type) (a, A button (blood type), blood type)
🆎 AB button (blood type) (ab, AB button (blood type), blood type)
🅱 B button (blood type) (b, B button (blood type), blood type)
🆑 CL button (cl, CL button)
🆒 COOL button (cool, COOL button)
🆓 FREE button (free, FREE button)
ℹ information (i, information)
🆔 ID button (id, ID button, identity)
Ⓜ circled M (circle, circled M, m)
🆕 NEW button (new, NEW button)
🆖 NG button (ng, NG button)
🅾 O button (blood type) (blood type, o, O button (blood type))
🆗 OK button (OK, OK button)
🅿 P button (P button, parking)
🆘 SOS button (help, sos, SOS button)
🆙 UP! button (mark, up, UP! button)
🆚 VS button (versus, vs, VS button)
🈁 Japanese “here” button (“here”, Japanese, Japanese “here” button, katakana, ココ)
🈂 Japanese “service charge” button (“service charge”, Japanese, Japanese “service charge” button, katakana, サ)
🈷 Japanese “monthly amount” button (“monthly amount”, ideograph, Japanese, Japanese “monthly amount” button, 月)
🈶 Japanese “not free of charge” button (“not free of charge”, ideograph, Japanese, Japanese “not free of charge” button, 有)
🈯 Japanese “reserved” button (“reserved”, ideograph, Japanese, Japanese “reserved” button, 指)
🉐 Japanese “bargain” button (“bargain”, ideograph, Japanese, Japanese “bargain” button, 得)
🈹 Japanese “discount” button (“discount”, ideograph, Japanese, Japanese “discount” button, 割)
🈚 Japanese “free of charge” button (“free of charge”, ideograph, Japanese, Japanese “free of charge” button, 無)
🈲 Japanese “prohibited” button (“prohibited”, ideograph, Japanese, Japanese “prohibited” button, 禁)
🉑 Japanese “acceptable” button (“acceptable”, ideograph, Japanese, Japanese “acceptable” button, 可)
🈸 Japanese “application” button (“application”, ideograph, Japanese, Japanese “application” button, 申)
🈴 Japanese “passing grade” button (“passing grade”, ideograph, Japanese, Japanese “passing grade” button, 合)
🈳 Japanese “vacancy” button (“vacancy”, ideograph, Japanese, Japanese “vacancy” button, 空)
㊗ Japanese “congratulations” button (“congratulations”, ideograph, Japanese, Japanese “congratulations” button, 祝)
㊙ Japanese “secret” button (“secret”, ideograph, Japanese, Japanese “secret” button, 秘)
🈺 Japanese “open for business” button (“open for business”, ideograph, Japanese, Japanese “open for business” button, 営)
🈵 Japanese “no vacancy” button (“no vacancy”, ideograph, Japanese, Japanese “no vacancy” button, 満)
🔴 red circle (circle, geometric, red)
🟠 orange circle (circle, orange)
🟡 yellow circle (circle, yellow)
🟢 green circle (circle, green)
🔵 blue circle (blue, circle, geometric)
🟣 purple circle (circle, purple)
🟤 brown circle (brown, circle)
⚫ black circle (black circle, circle, geometric)
⚪ white circle (circle, geometric, white circle)
🟥 red square (red, square)
🟧 orange square (orange, square)
🟨 yellow square (square, yellow)
🟩 green square (green, square)
🟦 blue square (blue, square)
🟪 purple square (purple, square)
🟫 brown square (brown, square)
⬛ black large square (black large square, geometric, square)
⬜ white large square (geometric, square, white large square)
◼ black medium square (black medium square, geometric, square)
◻ white medium square (geometric, square, white medium square)
◾ black medium-small square (black medium-small square, geometric, square)
◽ white medium-small square (geometric, square, white medium-small square)
▪ black small square (black small square, geometric, square)
▫ white small square (geometric, square, white small square)
🔶 large orange diamond (diamond, geometric, large orange diamond, orange)
🔷 large blue diamond (blue, diamond, geometric, large blue diamond)
🔸 small orange diamond (diamond, geometric, orange, small orange diamond)
🔹 small blue diamond (blue, diamond, geometric, small blue diamond)
🔺 red triangle pointed up (geometric, red, red triangle pointed up)
🔻 red triangle pointed down (down, geometric, red, red triangle pointed down)
💠 diamond with a dot (comic, diamond, diamond with a dot, geometric, inside)
🔘 radio button (button, geometric, radio)
🔳 white square button (button, geometric, outlined, square, white square button)
🔲 black square button (black square button, button, geometric, square)
🏁 chequered flag (checkered, chequered, chequered flag, racing)
🚩 triangular flag (post, triangular flag)
🎌 crossed flags (celebration, cross, crossed, crossed flags, Japanese)
🏴 black flag (black flag, waving)
🏳 white flag (waving, white flag)
🏳️‍🌈 rainbow flag
🏴‍☠️ pirate flag
🇦🇨 flag: Ascension Island
🇦🇩 flag: Andorra
🇦🇪 flag: United Arab Emirates
🇦🇫 flag: Afghanistan
🇦🇬 flag: Antigua & Barbuda
🇦🇮 flag: Anguilla
🇦🇱 flag: Albania
🇦🇲 flag: Armenia
🇦🇴 flag: Angola
🇦🇶 flag: Antarctica
🇦🇷 flag: Argentina
🇦🇸 flag: American Samoa
🇦🇹 flag: Austria
🇦🇺 flag: Australia
🇦🇼 flag: Aruba
🇦🇽 flag: Åland Islands
🇦🇿 flag: Azerbaijan
🇧🇦 flag: Bosnia & Herzegovina
🇧🇧 flag: Barbados
🇧🇩 flag: Bangladesh
🇧🇪 flag: Belgium
🇧🇫 flag: Burkina Faso
🇧🇬 flag: Bulgaria
🇧🇭 flag: Bahrain
🇧🇮 flag: Burundi
🇧🇯 flag: Benin
🇧🇱 flag: St. Barthélemy
🇧🇲 flag: Bermuda
🇧🇳 flag: Brunei
🇧🇴 flag: Bolivia
🇧🇶 flag: Caribbean Netherlands
🇧🇷 flag: Brazil
🇧🇸 flag: Bahamas
🇧🇹 flag: Bhutan
🇧🇻 flag: Bouvet Island
🇧🇼 flag: Botswana
🇧🇾 flag: Belarus
🇧🇿 flag: Belize
🇨🇦 flag: Canada
🇨🇨 flag: Cocos (Keeling) Islands
🇨🇩 flag: Congo - Kinshasa
🇨🇫 flag: Central African Republic
🇨🇬 flag: Congo - Brazzaville
🇨🇭 flag: Switzerland
🇨🇮 flag: Côte d’Ivoire
🇨🇰 flag: Cook Islands
🇨🇱 flag: Chile
🇨🇲 flag: Cameroon
🇨🇳 flag: China
🇨🇴 flag: Colombia
🇨🇵 flag: Clipperton Island
🇨🇷 flag: Costa Rica
🇨🇺 flag: Cuba
🇨🇻 flag: Cape Verde
🇨🇼 flag: Curaçao
🇨🇽 flag: Christmas Island
🇨🇾 flag: Cyprus
🇨🇿 flag: Czechia
🇩🇪 flag: Germany
🇩🇬 flag: Diego Garcia
🇩🇯 flag: Djibouti
🇩🇰 flag: Denmark
🇩🇲 flag: Dominica
🇩🇴 flag: Dominican Republic
🇩🇿 flag: Algeria
🇪🇦 flag: Ceuta & Melilla
🇪🇨 flag: Ecuador
🇪🇪 flag: Estonia
🇪🇬 flag: Egypt
🇪🇭 flag: Western Sahara
🇪🇷 flag: Eritrea
🇪🇸 flag: Spain
🇪🇹 flag: Ethiopia
🇪🇺 flag: European Union
🇫🇮 flag: Finland
🇫🇯 flag: Fiji
🇫🇰 flag: Falkland Islands
🇫🇲 flag: Micronesia
🇫🇴 flag: Faroe Islands
🇫🇷 flag: France
🇬🇦 flag: Gabon
🇬🇧 flag: United Kingdom
🇬🇩 flag: Grenada
🇬🇪 flag: Georgia
🇬🇫 flag: French Guiana
🇬🇬 flag: Guernsey
🇬🇭 flag: Ghana
🇬🇮 flag: Gibraltar
🇬🇱 flag: Greenland
🇬🇲 flag: Gambia
🇬🇳 flag: Guinea
🇬🇵 flag: Guadeloupe
🇬🇶 flag: Equatorial Guinea
🇬🇷 flag: Greece
🇬🇸 flag: South Georgia & South Sandwich Islands
🇬🇹 flag: Guatemala
🇬🇺 flag: Guam
🇬🇼 flag: Guinea-Bissau
🇬🇾 flag: Guyana
🇭🇰 flag: Hong Kong SAR China
🇭🇲 flag: Heard & McDonald Islands
🇭🇳 flag: Honduras
🇭🇷 flag: Croatia
🇭🇹 flag: Haiti
🇭🇺 flag: Hungary
🇮🇨 flag: Canary Islands
🇮🇩 flag: Indonesia
🇮🇪 flag: Ireland
🇮🇱 flag: Israel
🇮🇲 flag: Isle of Man
🇮🇳 flag: India
🇮🇴 flag: British Indian Ocean Territory
🇮🇶 flag: Iraq
🇮🇷 flag: Iran
🇮🇸 flag: Iceland
🇮🇹 flag: Italy
🇯🇪 flag: Jersey
🇯🇲 flag: Jamaica
🇯🇴 flag: Jordan
🇯🇵 flag: Japan
🇰🇪 flag: Kenya
🇰🇬 flag: Kyrgyzstan
🇰🇭 flag: Cambodia
🇰🇮 flag: Kiribati
🇰🇲 flag: Comoros
🇰🇳 flag: St. Kitts & Nevis
🇰🇵 flag: North Korea
🇰🇷 flag: South Korea
🇰🇼 flag: Kuwait
🇰🇾 flag: Cayman Islands
🇰🇿 flag: Kazakhstan
🇱🇦 flag: Laos
🇱🇧 flag: Lebanon
🇱🇨 flag: St. Lucia
🇱🇮 flag: Liechtenstein
🇱🇰 flag: Sri Lanka
🇱🇷 flag: Liberia
🇱🇸 flag: Lesotho
🇱🇹 flag: Lithuania
🇱🇺 flag: Luxembourg
🇱🇻 flag: Latvia
🇱🇾 flag: Libya
🇲🇦 flag: Morocco
🇲🇨 flag: Monaco
🇲🇩 flag: Moldova
🇲🇪 flag: Montenegro
🇲🇫 flag: St. Martin
🇲🇬 flag: Madagascar
🇲🇭 flag: Marshall Islands
🇲🇰 flag: North Macedonia
🇲🇱 flag: Mali
🇲🇲 flag: Myanmar (Burma)
🇲🇳 flag: Mongolia
🇲🇴 flag: Macao SAR China
🇲🇵 flag: Northern Mariana Islands
🇲🇶 flag: Martinique
🇲🇷 flag: Mauritania
🇲🇸 flag: Montserrat
🇲🇹 flag: Malta
🇲🇺 flag: Mauritius
🇲🇻 flag: Maldives
🇲🇼 flag: Malawi
🇲🇽 flag: Mexico
🇲🇾 flag: Malaysia
🇲🇿 flag: Mozambique
🇳🇦 flag: Namibia
🇳🇨 flag: New Caledonia
🇳🇪 flag: Niger
🇳🇫 flag: Norfolk Island
🇳🇬 flag: Nigeria
🇳🇮 flag: Nicaragua
🇳🇱 flag: Netherlands
🇳🇴 flag: Norway
🇳🇵 flag: Nepal
🇳🇷 flag: Nauru
🇳🇺 flag: Niue
🇳🇿 flag: New Zealand
🇴🇲 flag: Oman
🇵🇦 flag: Panama
🇵🇪 flag: Peru
🇵🇫 flag: French Polynesia
🇵🇬 flag: Papua New Guinea
🇵🇭 flag: Philippines
🇵🇰 flag: Pakistan
🇵🇱 flag: Poland
🇵🇲 flag: St. Pierre & Miquelon
🇵🇳 flag: Pitcairn Islands
🇵🇷 flag: Puerto Rico
🇵🇸 flag: Palestinian Territories
🇵🇹 flag: Portugal
🇵🇼 flag: Palau
🇵🇾 flag: Paraguay
🇶🇦 flag: Qatar
🇷🇪 flag: Réunion
🇷🇴 flag: Romania
🇷🇸 flag: Serbia
🇷🇺 flag: Russia
🇷🇼 flag: Rwanda
🇸🇦 flag: Saudi Arabia
🇸🇧 flag: Solomon Islands
🇸🇨 flag: Seychelles
🇸🇩 flag: Sudan
🇸🇪 flag: Sweden
🇸🇬 flag: Singapore
🇸🇭 flag: St. Helena
🇸🇮 flag: Slovenia
🇸🇯 flag: Svalbard & Jan Mayen
🇸🇰 flag: Slovakia
🇸🇱 flag: Sierra Leone
🇸🇲 flag: San Marino
🇸🇳 flag: Senegal
🇸🇴 flag: Somalia
🇸🇷 flag: Suriname
🇸🇸 flag: South Sudan
🇸🇹 flag: São Tomé & Príncipe
🇸🇻 flag: El Salvador
🇸🇽 flag: Sint Maarten
🇸🇾 flag: Syria
🇸🇿 flag: Eswatini
🇹🇦 flag: Tristan da Cunha
🇹🇨 flag: Turks & Caicos Islands
🇹🇩 flag: Chad
🇹🇫 flag: French Southern Territories
🇹🇬 flag: Togo
🇹🇭 flag: Thailand
🇹🇯 flag: Tajikistan
🇹🇰 flag: Tokelau
🇹🇱 flag: Timor-Leste
🇹🇲 flag: Turkmenistan
🇹🇳 flag: Tunisia
🇹🇴 flag: Tonga
🇹🇷 flag: Turkey
🇹🇹 flag: Trinidad & Tobago
🇹🇻 flag: Tuvalu
🇹🇼 flag: Taiwan
🇹🇿 flag: Tanzania
🇺🇦 flag: Ukraine
🇺🇬 flag: Uganda
🇺🇲 flag: U.S. Outlying Islands
🇺🇳 flag: United Nations
🇺🇸 flag: United States
🇺🇾 flag: Uruguay
🇺🇿 flag: Uzbekistan
🇻🇦 flag: Vatican City
🇻🇨 flag: St. Vincent & Grenadines
🇻🇪 flag: Venezuela
🇻🇬 flag: British Virgin Islands
🇻🇮 flag: U.S. Virgin Islands
🇻🇳 flag: Vietnam
🇻🇺 flag: Vanuatu
🇼🇫 flag: Wallis & Futuna
🇼🇸 flag: Samoa
🇽🇰 flag: Kosovo
🇾🇪 flag: Yemen
🇾🇹 flag: Mayotte
🇿🇦 flag: South Africa
🇿🇲 flag: Zambia
🇿🇼 flag: Zimbabwe
🏴󠁧󠁢󠁥󠁮󠁧󠁿 flag: England
🏴󠁧󠁢󠁳󠁣󠁴󠁿 flag: Scotland
🏴󠁧󠁢󠁷󠁬󠁳󠁿 flag: Wales
"""

skin_tone_selectable_emojis = {'☝', '⛹', '✊', '✋', '✌', '✍', '🎅', '🏂', '🏃', '🏄', '🏇', '🏊',
                               '🏋', '🏌', '👂', '👃', '👆', '👇', '👈', '👉', '👊', '👋', '👌',
                               '👍', '👎', '👏', '👐', '👦', '👧', '👨', '👩', '👪', '👫', '👬',
                               '👭', '👮', '👯', '👰', '👱', '👲', '👳', '👴', '👵', '👶', '👷',
                               '👸', '👼', '💁', '💂', '💃', '💅', '💆', '💇', '💏', '💑', '💪',
                               '🕴', '🕵', '🕺', '🖐', '🖕', '🖖', '🙅', '🙆', '🙇', '🙋', '🙌',
                               '🙍', '🙎', '🙏', '🚣', '🚴', '🚵', '🚶', '🛀', '🛌', '🤏', '🤘',
                               '🤙', '🤚', '🤛', '🤜', '🤝', '🤞', '🤟', '🤦', '🤰', '🤱', '🤲',
                               '🤳', '🤴', '🤵', '🤶', '🤷', '🤸', '🤹', '🤼', '🤽', '🤾', '🦵',
                               '🦶', '🦸', '🦹', '🦻', '🧍', '🧎', '🧏', '🧑', '🧒', '🧓', '🧔',
                               '🧕', '🧖', '🧗', '🧘', '🧙', '🧚', '🧛', '🧜', '🧝'}

fitzpatrick_modifiers = {
    '': 'neutral',
    '🏻': 'light skin',
    '🏼': 'medium-light skin',
    '🏽': 'moderate skin',
    '🏾': 'dark brown skin',
    '🏿': 'black skin'
}

fitzpatrick_modifiers_reversed = {" ".join(name.split()[:-1]): modifier for modifier, name in
                                  fitzpatrick_modifiers.items() if name != "neutral"}


def main() -> None:
    args = parse_arguments()
    active_window = get_active_window()

    returncode, stdout = open_main_rofi_window(args)

    if returncode == 1:
        sys.exit()
    else:
        emojis = compile_chosen_emojis(stdout.splitlines(), args.skin_tone, args.rofi_args)

        if returncode == 0:
            insert_emojis(emojis, active_window, args.use_clipboard)
        elif returncode == 10:
            copy_emojis_to_clipboard(emojis)
        elif returncode == 11:
            type_emojis(emojis, active_window)
        elif returncode == 12:
            copy_paste_emojis(emojis, active_window)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Select, insert or copy Unicode emojis using rofi')
    parser.add_argument(
        '--use-clipboard',
        '-c',
        dest='use_clipboard',
        action='store_true',
        help='Do not type the emoji directly, but copy it to the clipboard, insert it from there '
             'and then restore the clipboard\'s original value '
    )
    parser.add_argument(
        '--skin-tone',
        '-s',
        dest='skin_tone',
        action='store',
        choices=['neutral', 'light', 'medium-light', 'moderate', 'dark brown', 'black', 'ask'],
        default='ask',
        help='Decide on a skin-tone for all supported emojis. If not set (or set to "ask"), '
             'you will be asked for each one '
    )
    parser.add_argument(
        '--rofi-args',
        dest='rofi_args',
        action='store',
        default='',
        help='A string of arguments to give to rofi'
    )
    parsed_args = parser.parse_args()
    parsed_args.rofi_args = parsed_args.rofi_args.split()

    return parsed_args


def get_active_window() -> str:
    xdotool = Popen(args=['xdotool', 'getactivewindow'], stdout=PIPE)
    return xdotool.communicate()[0].decode("utf-8")[:-1]


def open_main_rofi_window(args) -> Tuple[int, bytes]:
    rofi = Popen(
        [
            'rofi',
            '-dmenu',
            '-i',
            '-multi-select',
            '-p',
            ' 😀   ',
            '-kb-custom-1',
            'Alt+c',
            '-kb-custom-2',
            'Alt+t',
            '-kb-custom-3',
            'Alt+p',
            *args.rofi_args
        ],
        stdin=PIPE,
        stdout=PIPE
    )
    (stdout, _) = rofi.communicate(input=emoji_list.encode('utf-8'))
    return rofi.returncode, stdout


def compile_chosen_emojis(chosen_emojis: List[bytes], skin_tone: str, rofi_args: List[str]) -> str:
    emojis = ""
    for line in chosen_emojis:
        emoji = line.decode('utf-8').split()[0]

        if emoji in skin_tone_selectable_emojis:
            emoji = select_skin_tone(emoji, skin_tone, rofi_args)

        emojis += emoji

    return emojis


def select_skin_tone(selected_emoji: chr, skin_tone: str, rofi_args: List[str]) -> str:
    if skin_tone == 'neutral':
        return selected_emoji
    elif skin_tone != 'ask':
        return selected_emoji + fitzpatrick_modifiers_reversed[skin_tone]
    else:
        modified_emojis = '\n'.join(map(
            lambda modifier: selected_emoji + modifier + " " + fitzpatrick_modifiers[modifier],
            fitzpatrick_modifiers.keys()
        ))

        rofi_skin = Popen(
            [
                'rofi',
                '-dmenu',
                '-i',
                '-p',
                selected_emoji + '   ',
                *rofi_args
            ],
            stdin=PIPE,
            stdout=PIPE
        )

        (stdout_skin, _) = rofi_skin.communicate(input=modified_emojis.encode('utf-8'))

        if rofi_skin.returncode == 1:
            return ''

        return stdout_skin.split()[0].decode('utf-8')


def insert_emojis(emojis: str, active_window: str, use_clipboard: bool = False) -> None:
    if use_clipboard:
        copy_paste_emojis(emojis, active_window)
    else:
        type_emojis(emojis, active_window)


def copy_paste_emojis(emojis: str, active_window: str) -> None:
    old_clipboard_content = Popen(args=['xsel', '-o', '-b'], stdout=PIPE) \
        .communicate()[0]
    old_primary_content = Popen(args=['xsel', '-o', '-p'], stdout=PIPE) \
        .communicate()[0]

    Popen(args=['xsel', '-i', '-b'], stdin=PIPE) \
        .communicate(input=emojis.encode('utf-8'))
    Popen(args=['xsel', '-i', '-p'], stdin=PIPE) \
        .communicate(input=emojis.encode('utf-8'))

    Popen([
        'xdotool',
        'key',
        '--clearmodifiers',
        '--window',
        active_window,
        'Shift+Insert'
    ]).wait()

    Popen(args=['xsel', '-i', '-b'], stdin=PIPE) \
        .communicate(input=old_clipboard_content)
    Popen(args=['xsel', '-i', '-p'], stdin=PIPE) \
        .communicate(input=old_primary_content)


def type_emojis(emojis: str, active_window: str) -> None:
    Popen([
        'xdotool',
        'type',
        '--clearmodifiers',
        '--window',
        active_window,
        emojis
    ])


def copy_emojis_to_clipboard(emojis: str) -> None:
    xsel = Popen(
        [
            'xsel',
            '-i',
            '-b'
        ],
        stdin=PIPE
    )
    xsel.communicate(input=emojis.encode('utf-8'))


if __name__ == "__main__":
    main()
