#!/usr/bin/python3
# -*- coding: utf-8 -*-
import argparse
import sys
from subprocess import Popen, PIPE
from typing import List, Tuple, Union

emoji_list = """😀 grinning face <small>(face, grin, grinning face)</small>
😃 grinning face with big eyes <small>(face, grinning face with big eyes, mouth, open, smile)</small>
😄 grinning face with smiling eyes <small>(eye, face, grinning face with smiling eyes, mouth, open, smile)</small>
😁 beaming face with smiling eyes <small>(beaming face with smiling eyes, eye, face, grin, smile)</small>
😆 grinning squinting face <small>(face, grinning squinting face, laugh, mouth, satisfied, smile)</small>
😅 grinning face with sweat <small>(cold, face, grinning face with sweat, open, smile, sweat)</small>
🤣 rolling on the floor laughing <small>(face, floor, laugh, rolling, rolling on the floor laughing)</small>
😂 face with tears of joy <small>(face, face with tears of joy, joy, laugh, tear)</small>
🙂 slightly smiling face <small>(face, slightly smiling face, smile)</small>
🙃 upside-down face <small>(face, upside-down)</small>
😉 winking face <small>(face, wink, winking face)</small>
😊 smiling face with smiling eyes <small>(blush, eye, face, smile, smiling face with smiling eyes)</small>
😇 smiling face with halo <small>(angel, face, fantasy, halo, innocent, smiling face with halo)</small>
🥰 smiling face with hearts <small>(adore, crush, hearts, in love, smiling face with hearts)</small>
😍 smiling face with heart-eyes <small>(eye, face, love, smile, smiling face with heart-eyes)</small>
🤩 star-struck <small>(eyes, face, grinning, star, star-struck)</small>
😘 face blowing a kiss <small>(face, face blowing a kiss, kiss)</small>
😗 kissing face <small>(face, kiss, kissing face)</small>
☺ smiling face <small>(face, outlined, relaxed, smile, smiling face)</small>
😚 kissing face with closed eyes <small>(closed, eye, face, kiss, kissing face with closed eyes)</small>
😙 kissing face with smiling eyes <small>(eye, face, kiss, kissing face with smiling eyes, smile)</small>
😋 face savoring food <small>(delicious, face, face savoring food, savouring, smile, yum)</small>
😛 face with tongue <small>(face, face with tongue, tongue)</small>
😜 winking face with tongue <small>(eye, face, joke, tongue, wink, winking face with tongue)</small>
🤪 zany face <small>(eye, goofy, large, small, zany face)</small>
😝 squinting face with tongue <small>(eye, face, horrible, squinting face with tongue, taste, tongue)</small>
🤑 money-mouth face <small>(face, money, money-mouth face, mouth)</small>
🤗 hugging face <small>(face, hug, hugging)</small>
🤭 face with hand over mouth <small>(face with hand over mouth, whoops)</small>
🤫 shushing face <small>(quiet, shush, shushing face)</small>
🤔 thinking face <small>(face, thinking)</small>
🤐 zipper-mouth face <small>(face, mouth, zipper, zipper-mouth face)</small>
🤨 face with raised eyebrow <small>(distrust, face with raised eyebrow, skeptic)</small>
😐 neutral face <small>(deadpan, face, meh, neutral)</small>
😑 expressionless face <small>(expressionless, face, inexpressive, meh, unexpressive)</small>
😶 face without mouth <small>(face, face without mouth, mouth, quiet, silent)</small>
😏 smirking face <small>(face, smirk, smirking face)</small>
😒 unamused face <small>(face, unamused, unhappy)</small>
🙄 face with rolling eyes <small>(eyeroll, eyes, face, face with rolling eyes, rolling)</small>
😬 grimacing face <small>(face, grimace, grimacing face)</small>
🤥 lying face <small>(face, lie, lying face, pinocchio)</small>
😌 relieved face <small>(face, relieved)</small>
😔 pensive face <small>(dejected, face, pensive)</small>
😪 sleepy face <small>(face, sleep, sleepy face)</small>
🤤 drooling face <small>(drooling, face)</small>
😴 sleeping face <small>(face, sleep, sleeping face, zzz)</small>
😷 face with medical mask <small>(cold, doctor, face, face with medical mask, mask, sick)</small>
🤒 face with thermometer <small>(face, face with thermometer, ill, sick, thermometer)</small>
🤕 face with head-bandage <small>(bandage, face, face with head-bandage, hurt, injury)</small>
🤢 nauseated face <small>(face, nauseated, vomit)</small>
🤮 face vomiting <small>(face vomiting, sick, vomit)</small>
🤧 sneezing face <small>(face, gesundheit, sneeze, sneezing face)</small>
🥵 hot face <small>(feverish, heat stroke, hot, hot face, red-faced, sweating)</small>
🥶 cold face <small>(blue-faced, cold, cold face, freezing, frostbite, icicles)</small>
🥴 woozy face <small>(dizzy, intoxicated, tipsy, uneven eyes, wavy mouth, woozy face)</small>
😵 dizzy face <small>(dizzy, face)</small>
🤯 exploding head <small>(exploding head, shocked)</small>
🤠 cowboy hat face <small>(cowboy, cowgirl, face, hat)</small>
🥳 partying face <small>(celebration, hat, horn, party, partying face)</small>
😎 smiling face with sunglasses <small>(bright, cool, face, smiling face with sunglasses, sun, sunglasses)</small>
🤓 nerd face <small>(face, geek, nerd)</small>
🧐 face with monocle <small>(face with monocle, stuffy)</small>
😕 confused face <small>(confused, face, meh)</small>
😟 worried face <small>(face, worried)</small>
🙁 slightly frowning face <small>(face, frown, slightly frowning face)</small>
☹ frowning face <small>(face, frown, frowning face)</small>
😮 face with open mouth <small>(face, face with open mouth, mouth, open, sympathy)</small>
😯 hushed face <small>(face, hushed, stunned, surprised)</small>
😲 astonished face <small>(astonished, face, shocked, totally)</small>
😳 flushed face <small>(dazed, face, flushed)</small>
🥺 pleading face <small>(begging, mercy, pleading face, puppy eyes)</small>
😦 frowning face with open mouth <small>(face, frown, frowning face with open mouth, mouth, open)</small>
😧 anguished face <small>(anguished, face)</small>
😨 fearful face <small>(face, fear, fearful, scared)</small>
😰 anxious face with sweat <small>(anxious face with sweat, blue, cold, face, rushed, sweat)</small>
😥 sad but relieved face <small>(disappointed, face, relieved, sad but relieved face, whew)</small>
😢 crying face <small>(cry, crying face, face, sad, tear)</small>
😭 loudly crying face <small>(cry, face, loudly crying face, sad, sob, tear)</small>
😱 face screaming in fear <small>(face, face screaming in fear, fear, munch, scared, scream)</small>
😖 confounded face <small>(confounded, face)</small>
😣 persevering face <small>(face, persevere, persevering face)</small>
😞 disappointed face <small>(disappointed, face)</small>
😓 downcast face with sweat <small>(cold, downcast face with sweat, face, sweat)</small>
😩 weary face <small>(face, tired, weary)</small>
😫 tired face <small>(face, tired)</small>
🥱 yawning face <small>(bored, tired, yawn, yawning face)</small>
😤 face with steam from nose <small>(face, face with steam from nose, triumph, won)</small>
😡 pouting face <small>(angry, face, mad, pouting, rage, red)</small>
😠 angry face <small>(angry, face, mad)</small>
🤬 face with symbols on mouth <small>(face with symbols on mouth, swearing)</small>
😈 smiling face with horns <small>(face, fairy tale, fantasy, horns, smile, smiling face with horns)</small>
👿 angry face with horns <small>(angry face with horns, demon, devil, face, fantasy, imp)</small>
💀 skull <small>(death, face, fairy tale, monster, skull)</small>
☠ skull and crossbones <small>(crossbones, death, face, monster, skull, skull and crossbones)</small>
💩 pile of poo <small>(dung, face, monster, pile of poo, poo, poop)</small>
🤡 clown face <small>(clown, face)</small>
👹 ogre <small>(creature, face, fairy tale, fantasy, monster, ogre)</small>
👺 goblin <small>(creature, face, fairy tale, fantasy, goblin, monster)</small>
👻 ghost <small>(creature, face, fairy tale, fantasy, ghost, monster)</small>
👽 alien <small>(alien, creature, extraterrestrial, face, fantasy, ufo)</small>
👾 alien monster <small>(alien, creature, extraterrestrial, face, monster, ufo)</small>
🤖 robot <small>(face, monster, robot)</small>
😺 grinning cat <small>(cat, face, grinning, mouth, open, smile)</small>
😸 grinning cat with smiling eyes <small>(cat, eye, face, grin, grinning cat with smiling eyes, smile)</small>
😹 cat with tears of joy <small>(cat, cat with tears of joy, face, joy, tear)</small>
😻 smiling cat with heart-eyes <small>(cat, eye, face, heart, love, smile, smiling cat with heart-eyes)</small>
😼 cat with wry smile <small>(cat, cat with wry smile, face, ironic, smile, wry)</small>
😽 kissing cat <small>(cat, eye, face, kiss, kissing cat)</small>
🙀 weary cat <small>(cat, face, oh, surprised, weary)</small>
😿 crying cat <small>(cat, cry, crying cat, face, sad, tear)</small>
😾 pouting cat <small>(cat, face, pouting)</small>
🙈 see-no-evil monkey <small>(evil, face, forbidden, monkey, see, see-no-evil monkey)</small>
🙉 hear-no-evil monkey <small>(evil, face, forbidden, hear, hear-no-evil monkey, monkey)</small>
🙊 speak-no-evil monkey <small>(evil, face, forbidden, monkey, speak, speak-no-evil monkey)</small>
💋 kiss mark <small>(kiss, kiss mark, lips)</small>
💌 love letter <small>(heart, letter, love, mail)</small>
💘 heart with arrow <small>(arrow, cupid, heart with arrow)</small>
💝 heart with ribbon <small>(heart with ribbon, ribbon, valentine)</small>
💖 sparkling heart <small>(excited, sparkle, sparkling heart)</small>
💗 growing heart <small>(excited, growing, growing heart, nervous, pulse)</small>
💓 beating heart <small>(beating, beating heart, heartbeat, pulsating)</small>
💞 revolving hearts <small>(revolving, revolving hearts)</small>
💕 two hearts <small>(love, two hearts)</small>
💟 heart decoration <small>(heart, heart decoration)</small>
❣ heart exclamation <small>(exclamation, heart exclamation, mark, punctuation)</small>
💔 broken heart <small>(break, broken, broken heart)</small>
❤ red heart <small>(heart, red heart)</small>
🧡 orange heart <small>(orange, orange heart)</small>
💛 yellow heart <small>(yellow, yellow heart)</small>
💚 green heart <small>(green, green heart)</small>
💙 blue heart <small>(blue, blue heart)</small>
💜 purple heart <small>(purple, purple heart)</small>
🤎 brown heart <small>(brown, heart)</small>
🖤 black heart <small>(black, black heart, evil, wicked)</small>
🤍 white heart <small>(heart, white)</small>
💯 hundred points <small>(100, full, hundred, hundred points, score)</small>
💢 anger symbol <small>(anger symbol, angry, comic, mad)</small>
💥 collision <small>(boom, collision, comic)</small>
💫 dizzy <small>(comic, dizzy, star)</small>
💦 sweat droplets <small>(comic, splashing, sweat, sweat droplets)</small>
💨 dashing away <small>(comic, dash, dashing away, running)</small>
🕳 hole <small>(hole)</small>
💣 bomb <small>(bomb, comic)</small>
💬 speech balloon <small>(balloon, bubble, comic, dialog, speech)</small>
👁️‍🗨️ eye in speech bubble
🗨 left speech bubble <small>(dialog, left speech bubble, speech)</small>
🗯 right anger bubble <small>(angry, balloon, bubble, mad, right anger bubble)</small>
💭 thought balloon <small>(balloon, bubble, comic, thought)</small>
💤 zzz <small>(comic, sleep, zzz)</small>
👋 waving hand <small>(hand, wave, waving)</small>
🤚 raised back of hand <small>(backhand, raised, raised back of hand)</small>
🖐 hand with fingers splayed <small>(finger, hand, hand with fingers splayed, splayed)</small>
✋ raised hand <small>(hand, raised hand)</small>
🖖 vulcan salute <small>(finger, hand, spock, vulcan, vulcan salute)</small>
👌 OK hand <small>(hand, OK)</small>
🤏 pinching hand <small>(pinching hand, small amount)</small>
✌ victory hand <small>(hand, v, victory)</small>
🤞 crossed fingers <small>(cross, crossed fingers, finger, hand, luck)</small>
🤟 love-you gesture <small>(hand, ILY, love-you gesture)</small>
🤘 sign of the horns <small>(finger, hand, horns, rock-on, sign of the horns)</small>
🤙 call me hand <small>(call, call me hand, hand)</small>
👈 backhand index pointing left <small>(backhand, backhand index pointing left, finger, hand, index, point)</small>
👉 backhand index pointing right <small>(backhand, backhand index pointing right, finger, hand, index, point)</small>
👆 backhand index pointing up <small>(backhand, backhand index pointing up, finger, hand, point, up)</small>
🖕 middle finger <small>(finger, hand, middle finger)</small>
👇 backhand index pointing down <small>(backhand, backhand index pointing down, down, finger, hand, point)</small>
☝ index pointing up <small>(finger, hand, index, index pointing up, point, up)</small>
👍 thumbs up <small>(+1, hand, thumb, thumbs up, up)</small>
👎 thumbs down <small>(-1, down, hand, thumb, thumbs down)</small>
✊ raised fist <small>(clenched, fist, hand, punch, raised fist)</small>
👊 oncoming fist <small>(clenched, fist, hand, oncoming fist, punch)</small>
🤛 left-facing fist <small>(fist, left-facing fist, leftwards)</small>
🤜 right-facing fist <small>(fist, right-facing fist, rightwards)</small>
👏 clapping hands <small>(clap, clapping hands, hand)</small>
🙌 raising hands <small>(celebration, gesture, hand, hooray, raised, raising hands)</small>
👐 open hands <small>(hand, open, open hands)</small>
🤲 palms up together <small>(palms up together, prayer)</small>
🤝 handshake <small>(agreement, hand, handshake, meeting, shake)</small>
🙏 folded hands <small>(ask, folded hands, hand, please, pray, thanks)</small>
✍ writing hand <small>(hand, write, writing hand)</small>
💅 nail polish <small>(care, cosmetics, manicure, nail, polish)</small>
🤳 selfie <small>(camera, phone, selfie)</small>
💪 flexed biceps <small>(biceps, comic, flex, flexed biceps, muscle)</small>
🦾 mechanical arm <small>(accessibility, mechanical arm, prosthetic)</small>
🦿 mechanical leg <small>(accessibility, mechanical leg, prosthetic)</small>
🦵 leg <small>(kick, leg, limb)</small>
🦶 foot <small>(foot, kick, stomp)</small>
👂 ear <small>(body, ear)</small>
🦻 ear with hearing aid <small>(accessibility, ear with hearing aid, hard of hearing)</small>
👃 nose <small>(body, nose)</small>
🧠 brain <small>(brain, intelligent)</small>
🦷 tooth <small>(dentist, tooth)</small>
🦴 bone <small>(bone, skeleton)</small>
👀 eyes <small>(eye, eyes, face)</small>
👁 eye <small>(body, eye)</small>
👅 tongue <small>(body, tongue)</small>
👄 mouth <small>(lips, mouth)</small>
👶 baby <small>(baby, young)</small>
🧒 child <small>(child, gender-neutral, unspecified gender, young)</small>
👦 boy <small>(boy, young)</small>
👧 girl <small>(girl, Virgo, young, zodiac)</small>
🧑 person <small>(adult, gender-neutral, person, unspecified gender)</small>
👱 person: blond hair <small>(blond, blond-haired person, hair, person: blond hair)</small>
👨 man <small>(adult, man)</small>
🧔 man: beard <small>(beard, man, man: beard, person)</small>
👱‍♂️ man: blond hair
👨‍🦰 man: red hair
👨‍🦱 man: curly hair
👨‍🦳 man: white hair
👨‍🦲 man: bald
👩 woman <small>(adult, woman)</small>
👱‍♀️ woman: blond hair
👩‍🦰 woman: red hair
👩‍🦱 woman: curly hair
👩‍🦳 woman: white hair
👩‍🦲 woman: bald
🧓 older person <small>(adult, gender-neutral, old, older person, unspecified gender)</small>
👴 old man <small>(adult, man, old)</small>
👵 old woman <small>(adult, old, woman)</small>
🙍 person frowning <small>(frown, gesture, person frowning)</small>
🙍‍♂️ man frowning
🙍‍♀️ woman frowning
🙎 person pouting <small>(gesture, person pouting, pouting)</small>
🙎‍♂️ man pouting
🙎‍♀️ woman pouting
🙅 person gesturing NO <small>(forbidden, gesture, hand, person gesturing NO, prohibited)</small>
🙅‍♂️ man gesturing NO
🙅‍♀️ woman gesturing NO
🙆 person gesturing OK <small>(gesture, hand, OK, person gesturing OK)</small>
🙆‍♂️ man gesturing OK
🙆‍♀️ woman gesturing OK
💁 person tipping hand <small>(hand, help, information, person tipping hand, sassy, tipping)</small>
💁‍♂️ man tipping hand
💁‍♀️ woman tipping hand
🙋 person raising hand <small>(gesture, hand, happy, person raising hand, raised)</small>
🙋‍♂️ man raising hand
🙋‍♀️ woman raising hand
🧏 deaf person <small>(accessibility, deaf, deaf person, ear, hear)</small>
🧏‍♂️ deaf man
🧏‍♀️ deaf woman
🙇 person bowing <small>(apology, bow, gesture, person bowing, sorry)</small>
🙇‍♂️ man bowing
🙇‍♀️ woman bowing
🤦 person facepalming <small>(disbelief, exasperation, face, palm, person facepalming)</small>
🤦‍♂️ man facepalming
🤦‍♀️ woman facepalming
🤷 person shrugging <small>(doubt, ignorance, indifference, person shrugging, shrug)</small>
🤷‍♂️ man shrugging
🤷‍♀️ woman shrugging
👨‍⚕️ man health worker
👩‍⚕️ woman health worker
👨‍🎓 man student <small>(graduate, man, student)</small>
👩‍🎓 woman student <small>(graduate, student, woman)</small>
👨‍🏫 man teacher <small>(instructor, man, professor, teacher)</small>
👩‍🏫 woman teacher <small>(instructor, professor, teacher, woman)</small>
👨‍⚖️ man judge
👩‍⚖️ woman judge
👨‍🌾 man farmer <small>(farmer, gardener, man, rancher)</small>
👩‍🌾 woman farmer <small>(farmer, gardener, rancher, woman)</small>
👨‍🍳 man cook <small>(chef, cook, man)</small>
👩‍🍳 woman cook <small>(chef, cook, woman)</small>
👨‍🔧 man mechanic <small>(electrician, man, mechanic, plumber, tradesperson)</small>
👩‍🔧 woman mechanic <small>(electrician, mechanic, plumber, tradesperson, woman)</small>
👨‍🏭 man factory worker <small>(assembly, factory, industrial, man, worker)</small>
👩‍🏭 woman factory worker <small>(assembly, factory, industrial, woman, worker)</small>
👨‍💼 man office worker <small>(architect, business, man, man office worker, manager, white-collar)</small>
👩‍💼 woman office worker <small>(architect, business, manager, white-collar, woman, woman office worker)</small>
👨‍🔬 man scientist <small>(biologist, chemist, engineer, man, physicist, scientist)</small>
👩‍🔬 woman scientist <small>(biologist, chemist, engineer, physicist, scientist, woman)</small>
👨‍💻 man technologist <small>(coder, developer, inventor, man, software, technologist)</small>
👩‍💻 woman technologist <small>(coder, developer, inventor, software, technologist, woman)</small>
👨‍🎤 man singer <small>(actor, entertainer, man, rock, singer, star)</small>
👩‍🎤 woman singer <small>(actor, entertainer, rock, singer, star, woman)</small>
👨‍🎨 man artist <small>(artist, man, palette)</small>
👩‍🎨 woman artist <small>(artist, palette, woman)</small>
👨‍✈️ man pilot
👩‍✈️ woman pilot
👨‍🚀 man astronaut <small>(astronaut, man, rocket)</small>
👩‍🚀 woman astronaut <small>(astronaut, rocket, woman)</small>
👨‍🚒 man firefighter <small>(firefighter, firetruck, man)</small>
👩‍🚒 woman firefighter <small>(firefighter, firetruck, woman)</small>
👮 police officer <small>(cop, officer, police)</small>
👮‍♂️ man police officer
👮‍♀️ woman police officer
🕵 detective <small>(detective, sleuth, spy)</small>
🕵️‍♂️ man detective
🕵️‍♀️ woman detective
💂 guard <small>(guard)</small>
💂‍♂️ man guard
💂‍♀️ woman guard
👷 construction worker <small>(construction, hat, worker)</small>
👷‍♂️ man construction worker
👷‍♀️ woman construction worker
🤴 prince <small>(prince)</small>
👸 princess <small>(fairy tale, fantasy, princess)</small>
👳 person wearing turban <small>(person wearing turban, turban)</small>
👳‍♂️ man wearing turban
👳‍♀️ woman wearing turban
👲 man with Chinese cap <small>(gua pi mao, hat, man, man with Chinese cap)</small>
🧕 woman with headscarf <small>(headscarf, hijab, mantilla, tichel, woman with headscarf)</small>
🤵 man in tuxedo <small>(groom, man, man in tuxedo, tuxedo)</small>
👰 bride with veil <small>(bride, bride with veil, veil, wedding)</small>
🤰 pregnant woman <small>(pregnant, woman)</small>
🤱 breast-feeding <small>(baby, breast, breast-feeding, nursing)</small>
👼 baby angel <small>(angel, baby, face, fairy tale, fantasy)</small>
🎅 Santa Claus <small>(celebration, Christmas, claus, father, santa, Santa Claus)</small>
🤶 Mrs. Claus <small>(celebration, Christmas, claus, mother, Mrs., Mrs. Claus)</small>
🦸 superhero <small>(good, hero, heroine, superhero, superpower)</small>
🦸‍♂️ man superhero
🦸‍♀️ woman superhero
🦹 supervillain <small>(criminal, evil, superpower, supervillain, villain)</small>
🦹‍♂️ man supervillain
🦹‍♀️ woman supervillain
🧙 mage <small>(mage, sorcerer, sorceress, witch, wizard)</small>
🧙‍♂️ man mage
🧙‍♀️ woman mage
🧚 fairy <small>(fairy, Oberon, Puck, Titania)</small>
🧚‍♂️ man fairy
🧚‍♀️ woman fairy
🧛 vampire <small>(Dracula, undead, vampire)</small>
🧛‍♂️ man vampire
🧛‍♀️ woman vampire
🧜 merperson <small>(mermaid, merman, merperson, merwoman)</small>
🧜‍♂️ merman
🧜‍♀️ mermaid
🧝 elf <small>(elf, magical)</small>
🧝‍♂️ man elf
🧝‍♀️ woman elf
🧞 genie <small>(djinn, genie)</small>
🧞‍♂️ man genie
🧞‍♀️ woman genie
🧟 zombie <small>(undead, walking dead, zombie)</small>
🧟‍♂️ man zombie
🧟‍♀️ woman zombie
💆 person getting massage <small>(face, massage, person getting massage, salon)</small>
💆‍♂️ man getting massage
💆‍♀️ woman getting massage
💇 person getting haircut <small>(barber, beauty, haircut, parlor, person getting haircut)</small>
💇‍♂️ man getting haircut
💇‍♀️ woman getting haircut
🚶 person walking <small>(hike, person walking, walk, walking)</small>
🚶‍♂️ man walking
🚶‍♀️ woman walking
🧍 person standing <small>(person standing, stand, standing)</small>
🧍‍♂️ man standing
🧍‍♀️ woman standing
🧎 person kneeling <small>(kneel, kneeling, person kneeling)</small>
🧎‍♂️ man kneeling
🧎‍♀️ woman kneeling
👨‍🦯 man with probing cane <small>(accessibility, blind, man, man with probing cane)</small>
👩‍🦯 woman with probing cane <small>(accessibility, blind, woman, woman with probing cane)</small>
👨‍🦼 man in motorized wheelchair <small>(accessibility, man, man in motorized wheelchair, wheelchair)</small>
👩‍🦼 woman in motorized wheelchair <small>(accessibility, wheelchair, woman, woman in motorized wheelchair)</small>
👨‍🦽 man in manual wheelchair <small>(accessibility, man, man in manual wheelchair, wheelchair)</small>
👩‍🦽 woman in manual wheelchair <small>(accessibility, wheelchair, woman, woman in manual wheelchair)</small>
🏃 person running <small>(marathon, person running, running)</small>
🏃‍♂️ man running
🏃‍♀️ woman running
💃 woman dancing <small>(dancing, woman)</small>
🕺 man dancing <small>(dance, man, man dancing)</small>
🕴 man in suit levitating <small>(business, man, man in suit levitating, suit)</small>
👯 people with bunny ears <small>(bunny ear, dancer, partying, people with bunny ears)</small>
👯‍♂️ men with bunny ears
👯‍♀️ women with bunny ears
🧖 person in steamy room <small>(person in steamy room, sauna, steam room)</small>
🧖‍♂️ man in steamy room
🧖‍♀️ woman in steamy room
🧗 person climbing <small>(climber, person climbing)</small>
🧗‍♂️ man climbing
🧗‍♀️ woman climbing
🤺 person fencing <small>(fencer, fencing, person fencing, sword)</small>
🏇 horse racing <small>(horse, jockey, racehorse, racing)</small>
⛷ skier <small>(ski, skier, snow)</small>
🏂 snowboarder <small>(ski, snow, snowboard, snowboarder)</small>
🏌 person golfing <small>(ball, golf, person golfing)</small>
🏌️‍♂️ man golfing
🏌️‍♀️ woman golfing
🏄 person surfing <small>(person surfing, surfing)</small>
🏄‍♂️ man surfing
🏄‍♀️ woman surfing
🚣 person rowing boat <small>(boat, person rowing boat, rowboat)</small>
🚣‍♂️ man rowing boat
🚣‍♀️ woman rowing boat
🏊 person swimming <small>(person swimming, swim)</small>
🏊‍♂️ man swimming
🏊‍♀️ woman swimming
⛹ person bouncing ball <small>(ball, person bouncing ball)</small>
⛹️‍♂️ man bouncing ball
⛹️‍♀️ woman bouncing ball
🏋 person lifting weights <small>(lifter, person lifting weights, weight)</small>
🏋️‍♂️ man lifting weights
🏋️‍♀️ woman lifting weights
🚴 person biking <small>(bicycle, biking, cyclist, person biking)</small>
🚴‍♂️ man biking
🚴‍♀️ woman biking
🚵 person mountain biking <small>(bicycle, bicyclist, bike, cyclist, mountain, person mountain biking)</small>
🚵‍♂️ man mountain biking
🚵‍♀️ woman mountain biking
🤸 person cartwheeling <small>(cartwheel, gymnastics, person cartwheeling)</small>
🤸‍♂️ man cartwheeling
🤸‍♀️ woman cartwheeling
🤼 people wrestling <small>(people wrestling, wrestle, wrestler)</small>
🤼‍♂️ men wrestling
🤼‍♀️ women wrestling
🤽 person playing water polo <small>(person playing water polo, polo, water)</small>
🤽‍♂️ man playing water polo
🤽‍♀️ woman playing water polo
🤾 person playing handball <small>(ball, handball, person playing handball)</small>
🤾‍♂️ man playing handball
🤾‍♀️ woman playing handball
🤹 person juggling <small>(balance, juggle, multitask, person juggling, skill)</small>
🤹‍♂️ man juggling
🤹‍♀️ woman juggling
🧘 person in lotus position <small>(meditation, person in lotus position, yoga)</small>
🧘‍♂️ man in lotus position
🧘‍♀️ woman in lotus position
🛀 person taking bath <small>(bath, bathtub, person taking bath)</small>
🛌 person in bed <small>(hotel, person in bed, sleep)</small>
🧑‍🤝‍🧑 people holding hands <small>(couple, hand, hold, holding hands, people holding hands, person)</small>
👭 women holding hands <small>(couple, hand, holding hands, women, women holding hands)</small>
👫 woman and man holding hands <small>(couple, hand, hold, holding hands, man, woman, woman and man holding hands)</small>
👬 men holding hands <small>(couple, Gemini, holding hands, man, men, men holding hands, twins, zodiac)</small>
💏 kiss <small>(couple, kiss)</small>
👩‍❤️‍💋‍👨 kiss: woman, man
👨‍❤️‍💋‍👨 kiss: man, man
👩‍❤️‍💋‍👩 kiss: woman, woman
💑 couple with heart <small>(couple, couple with heart, love)</small>
👩‍❤️‍👨 couple with heart: woman, man
👨‍❤️‍👨 couple with heart: man, man
👩‍❤️‍👩 couple with heart: woman, woman
👪 family <small>(family)</small>
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
🗣 speaking head <small>(face, head, silhouette, speak, speaking)</small>
👤 bust in silhouette <small>(bust, bust in silhouette, silhouette)</small>
👥 busts in silhouette <small>(bust, busts in silhouette, silhouette)</small>
👣 footprints <small>(clothing, footprint, footprints, print)</small>
🦰 red hair <small>(ginger, red hair, redhead)</small>
🦱 curly hair <small>(afro, curly, curly hair, ringlets)</small>
🦳 white hair <small>(gray, hair, old, white)</small>
🦲 bald <small>(bald, chemotherapy, hairless, no hair, shaven)</small>
🐵 monkey face <small>(face, monkey)</small>
🐒 monkey <small>(monkey)</small>
🦍 gorilla <small>(gorilla)</small>
🦧 orangutan <small>(ape, orangutan)</small>
🐶 dog face <small>(dog, face, pet)</small>
🐕 dog <small>(dog, pet)</small>
🦮 guide dog <small>(accessibility, blind, guide, guide dog)</small>
🐕‍🦺 service dog <small>(accessibility, assistance, dog, service)</small>
🐩 poodle <small>(dog, poodle)</small>
🐺 wolf <small>(face, wolf)</small>
🦊 fox <small>(face, fox)</small>
🦝 raccoon <small>(curious, raccoon, sly)</small>
🐱 cat face <small>(cat, face, pet)</small>
🐈 cat <small>(cat, pet)</small>
🦁 lion <small>(face, Leo, lion, zodiac)</small>
🐯 tiger face <small>(face, tiger)</small>
🐅 tiger <small>(tiger)</small>
🐆 leopard <small>(leopard)</small>
🐴 horse face <small>(face, horse)</small>
🐎 horse <small>(equestrian, horse, racehorse, racing)</small>
🦄 unicorn <small>(face, unicorn)</small>
🦓 zebra <small>(stripe, zebra)</small>
🦌 deer <small>(deer)</small>
🐮 cow face <small>(cow, face)</small>
🐂 ox <small>(bull, ox, Taurus, zodiac)</small>
🐃 water buffalo <small>(buffalo, water)</small>
🐄 cow <small>(cow)</small>
🐷 pig face <small>(face, pig)</small>
🐖 pig <small>(pig, sow)</small>
🐗 boar <small>(boar, pig)</small>
🐽 pig nose <small>(face, nose, pig)</small>
🐏 ram <small>(Aries, male, ram, sheep, zodiac)</small>
🐑 ewe <small>(ewe, female, sheep)</small>
🐐 goat <small>(Capricorn, goat, zodiac)</small>
🐪 camel <small>(camel, dromedary, hump)</small>
🐫 two-hump camel <small>(bactrian, camel, hump, two-hump camel)</small>
🦙 llama <small>(alpaca, guanaco, llama, vicuña, wool)</small>
🦒 giraffe <small>(giraffe, spots)</small>
🐘 elephant <small>(elephant)</small>
🦏 rhinoceros <small>(rhinoceros)</small>
🦛 hippopotamus <small>(hippo, hippopotamus)</small>
🐭 mouse face <small>(face, mouse)</small>
🐁 mouse <small>(mouse)</small>
🐀 rat <small>(rat)</small>
🐹 hamster <small>(face, hamster, pet)</small>
🐰 rabbit face <small>(bunny, face, pet, rabbit)</small>
🐇 rabbit <small>(bunny, pet, rabbit)</small>
🐿 chipmunk <small>(chipmunk, squirrel)</small>
🦔 hedgehog <small>(hedgehog, spiny)</small>
🦇 bat <small>(bat, vampire)</small>
🐻 bear <small>(bear, face)</small>
🐨 koala <small>(bear, koala)</small>
🐼 panda <small>(face, panda)</small>
🦥 sloth <small>(lazy, sloth, slow)</small>
🦦 otter <small>(fishing, otter, playful)</small>
🦨 skunk <small>(skunk, stink)</small>
🦘 kangaroo <small>(Australia, joey, jump, kangaroo, marsupial)</small>
🦡 badger <small>(badger, honey badger, pester)</small>
🐾 paw prints <small>(feet, paw, paw prints, print)</small>
🦃 turkey <small>(bird, turkey)</small>
🐔 chicken <small>(bird, chicken)</small>
🐓 rooster <small>(bird, rooster)</small>
🐣 hatching chick <small>(baby, bird, chick, hatching)</small>
🐤 baby chick <small>(baby, bird, chick)</small>
🐥 front-facing baby chick <small>(baby, bird, chick, front-facing baby chick)</small>
🐦 bird <small>(bird)</small>
🐧 penguin <small>(bird, penguin)</small>
🕊 dove <small>(bird, dove, fly, peace)</small>
🦅 eagle <small>(bird, eagle)</small>
🦆 duck <small>(bird, duck)</small>
🦢 swan <small>(bird, cygnet, swan, ugly duckling)</small>
🦉 owl <small>(bird, owl, wise)</small>
🦩 flamingo <small>(flamboyant, flamingo, tropical)</small>
🦚 peacock <small>(bird, ostentatious, peacock, peahen, proud)</small>
🦜 parrot <small>(bird, parrot, pirate, talk)</small>
🐸 frog <small>(face, frog)</small>
🐊 crocodile <small>(crocodile)</small>
🐢 turtle <small>(terrapin, tortoise, turtle)</small>
🦎 lizard <small>(lizard, reptile)</small>
🐍 snake <small>(bearer, Ophiuchus, serpent, snake, zodiac)</small>
🐲 dragon face <small>(dragon, face, fairy tale)</small>
🐉 dragon <small>(dragon, fairy tale)</small>
🦕 sauropod <small>(brachiosaurus, brontosaurus, diplodocus, sauropod)</small>
🦖 T-Rex <small>(T-Rex, Tyrannosaurus Rex)</small>
🐳 spouting whale <small>(face, spouting, whale)</small>
🐋 whale <small>(whale)</small>
🐬 dolphin <small>(dolphin, flipper)</small>
🐟 fish <small>(fish, Pisces, zodiac)</small>
🐠 tropical fish <small>(fish, tropical)</small>
🐡 blowfish <small>(blowfish, fish)</small>
🦈 shark <small>(fish, shark)</small>
🐙 octopus <small>(octopus)</small>
🐚 spiral shell <small>(shell, spiral)</small>
🐌 snail <small>(snail)</small>
🦋 butterfly <small>(butterfly, insect, pretty)</small>
🐛 bug <small>(bug, insect)</small>
🐜 ant <small>(ant, insect)</small>
🐝 honeybee <small>(bee, honeybee, insect)</small>
🐞 lady beetle <small>(beetle, insect, lady beetle, ladybird, ladybug)</small>
🦗 cricket <small>(cricket, grasshopper)</small>
🕷 spider <small>(insect, spider)</small>
🕸 spider web <small>(spider, web)</small>
🦂 scorpion <small>(scorpio, Scorpio, scorpion, zodiac)</small>
🦟 mosquito <small>(disease, fever, insect, malaria, mosquito, virus)</small>
🦠 microbe <small>(amoeba, bacteria, microbe, virus)</small>
💐 bouquet <small>(bouquet, flower)</small>
🌸 cherry blossom <small>(blossom, cherry, flower)</small>
💮 white flower <small>(flower, white flower)</small>
🏵 rosette <small>(plant, rosette)</small>
🌹 rose <small>(flower, rose)</small>
🥀 wilted flower <small>(flower, wilted)</small>
🌺 hibiscus <small>(flower, hibiscus)</small>
🌻 sunflower <small>(flower, sun, sunflower)</small>
🌼 blossom <small>(blossom, flower)</small>
🌷 tulip <small>(flower, tulip)</small>
🌱 seedling <small>(seedling, young)</small>
🌲 evergreen tree <small>(evergreen tree, tree)</small>
🌳 deciduous tree <small>(deciduous, shedding, tree)</small>
🌴 palm tree <small>(palm, tree)</small>
🌵 cactus <small>(cactus, plant)</small>
🌾 sheaf of rice <small>(ear, grain, rice, sheaf of rice)</small>
🌿 herb <small>(herb, leaf)</small>
☘ shamrock <small>(plant, shamrock)</small>
🍀 four leaf clover <small>(4, clover, four, four-leaf clover, leaf)</small>
🍁 maple leaf <small>(falling, leaf, maple)</small>
🍂 fallen leaf <small>(fallen leaf, falling, leaf)</small>
🍃 leaf fluttering in wind <small>(blow, flutter, leaf, leaf fluttering in wind, wind)</small>
🍇 grapes <small>(fruit, grape, grapes)</small>
🍈 melon <small>(fruit, melon)</small>
🍉 watermelon <small>(fruit, watermelon)</small>
🍊 tangerine <small>(fruit, orange, tangerine)</small>
🍋 lemon <small>(citrus, fruit, lemon)</small>
🍌 banana <small>(banana, fruit)</small>
🍍 pineapple <small>(fruit, pineapple)</small>
🥭 mango <small>(fruit, mango, tropical)</small>
🍎 red apple <small>(apple, fruit, red)</small>
🍏 green apple <small>(apple, fruit, green)</small>
🍐 pear <small>(fruit, pear)</small>
🍑 peach <small>(fruit, peach)</small>
🍒 cherries <small>(berries, cherries, cherry, fruit, red)</small>
🍓 strawberry <small>(berry, fruit, strawberry)</small>
🥝 kiwi fruit <small>(food, fruit, kiwi)</small>
🍅 tomato <small>(fruit, tomato, vegetable)</small>
🥥 coconut <small>(coconut, palm, piña colada)</small>
🥑 avocado <small>(avocado, food, fruit)</small>
🍆 eggplant <small>(aubergine, eggplant, vegetable)</small>
🥔 potato <small>(food, potato, vegetable)</small>
🥕 carrot <small>(carrot, food, vegetable)</small>
🌽 ear of corn <small>(corn, ear, ear of corn, maize, maze)</small>
🌶 hot pepper <small>(hot, pepper)</small>
🥒 cucumber <small>(cucumber, food, pickle, vegetable)</small>
🥬 leafy green <small>(bok choy, cabbage, kale, leafy green, lettuce)</small>
🥦 broccoli <small>(broccoli, wild cabbage)</small>
🧄 garlic <small>(flavoring, garlic)</small>
🧅 onion <small>(flavoring, onion)</small>
🍄 mushroom <small>(mushroom, toadstool)</small>
🥜 peanuts <small>(food, nut, peanut, peanuts, vegetable)</small>
🌰 chestnut <small>(chestnut, plant)</small>
🍞 bread <small>(bread, loaf)</small>
🥐 croissant <small>(bread, crescent roll, croissant, food, french)</small>
🥖 baguette bread <small>(baguette, bread, food, french)</small>
🥨 pretzel <small>(pretzel, twisted)</small>
🥯 bagel <small>(bagel, bakery, schmear)</small>
🥞 pancakes <small>(crêpe, food, hotcake, pancake, pancakes)</small>
🧇 waffle <small>(indecisive, iron, waffle)</small>
🧀 cheese wedge <small>(cheese, cheese wedge)</small>
🍖 meat on bone <small>(bone, meat, meat on bone)</small>
🍗 poultry leg <small>(bone, chicken, drumstick, leg, poultry)</small>
🥩 cut of meat <small>(chop, cut of meat, lambchop, porkchop, steak)</small>
🥓 bacon <small>(bacon, food, meat)</small>
🍔 hamburger <small>(burger, hamburger)</small>
🍟 french fries <small>(french, fries)</small>
🍕 pizza <small>(cheese, pizza, slice)</small>
🌭 hot dog <small>(frankfurter, hot dog, hotdog, sausage)</small>
🥪 sandwich <small>(bread, sandwich)</small>
🌮 taco <small>(mexican, taco)</small>
🌯 burrito <small>(burrito, mexican, wrap)</small>
🥙 stuffed flatbread <small>(falafel, flatbread, food, gyro, kebab, stuffed)</small>
🧆 falafel <small>(chickpea, falafel, meatball)</small>
🥚 egg <small>(egg, food)</small>
🍳 cooking <small>(cooking, egg, frying, pan)</small>
🥘 shallow pan of food <small>(casserole, food, paella, pan, shallow, shallow pan of food)</small>
🍲 pot of food <small>(pot, pot of food, stew)</small>
🥣 bowl with spoon <small>(bowl with spoon, breakfast, cereal, congee)</small>
🥗 green salad <small>(food, green, salad)</small>
🍿 popcorn <small>(popcorn)</small>
🧈 butter <small>(butter, dairy)</small>
🧂 salt <small>(condiment, salt, shaker)</small>
🥫 canned food <small>(can, canned food)</small>
🍱 bento box <small>(bento, box)</small>
🍘 rice cracker <small>(cracker, rice)</small>
🍙 rice ball <small>(ball, Japanese, rice)</small>
🍚 cooked rice <small>(cooked, rice)</small>
🍛 curry rice <small>(curry, rice)</small>
🍜 steaming bowl <small>(bowl, noodle, ramen, steaming)</small>
🍝 spaghetti <small>(pasta, spaghetti)</small>
🍠 roasted sweet potato <small>(potato, roasted, sweet)</small>
🍢 oden <small>(kebab, oden, seafood, skewer, stick)</small>
🍣 sushi <small>(sushi)</small>
🍤 fried shrimp <small>(fried, prawn, shrimp, tempura)</small>
🍥 fish cake with swirl <small>(cake, fish, fish cake with swirl, pastry, swirl)</small>
🥮 moon cake <small>(autumn, festival, moon cake, yuèbǐng)</small>
🍡 dango <small>(dango, dessert, Japanese, skewer, stick, sweet)</small>
🥟 dumpling <small>(dumpling, empanada, gyōza, jiaozi, pierogi, potsticker)</small>
🥠 fortune cookie <small>(fortune cookie, prophecy)</small>
🥡 takeout box <small>(oyster pail, takeout box)</small>
🦀 crab <small>(Cancer, crab, zodiac)</small>
🦞 lobster <small>(bisque, claws, lobster, seafood)</small>
🦐 shrimp <small>(food, shellfish, shrimp, small)</small>
🦑 squid <small>(food, molusc, squid)</small>
🦪 oyster <small>(diving, oyster, pearl)</small>
🍦 soft ice cream <small>(cream, dessert, ice, icecream, soft, sweet)</small>
🍧 shaved ice <small>(dessert, ice, shaved, sweet)</small>
🍨 ice cream <small>(cream, dessert, ice, sweet)</small>
🍩 doughnut <small>(dessert, donut, doughnut, sweet)</small>
🍪 cookie <small>(cookie, dessert, sweet)</small>
🎂 birthday cake <small>(birthday, cake, celebration, dessert, pastry, sweet)</small>
🍰 shortcake <small>(cake, dessert, pastry, shortcake, slice, sweet)</small>
🧁 cupcake <small>(bakery, cupcake, sweet)</small>
🥧 pie <small>(filling, pastry, pie)</small>
🍫 chocolate bar <small>(bar, chocolate, dessert, sweet)</small>
🍬 candy <small>(candy, dessert, sweet)</small>
🍭 lollipop <small>(candy, dessert, lollipop, sweet)</small>
🍮 custard <small>(custard, dessert, pudding, sweet)</small>
🍯 honey pot <small>(honey, honeypot, pot, sweet)</small>
🍼 baby bottle <small>(baby, bottle, drink, milk)</small>
🥛 glass of milk <small>(drink, glass, glass of milk, milk)</small>
☕ hot beverage <small>(beverage, coffee, drink, hot, steaming, tea)</small>
🍵 teacup without handle <small>(beverage, cup, drink, tea, teacup, teacup without handle)</small>
🍶 sake <small>(bar, beverage, bottle, cup, drink, sake)</small>
🍾 bottle with popping cork <small>(bar, bottle, bottle with popping cork, cork, drink, popping)</small>
🍷 wine glass <small>(bar, beverage, drink, glass, wine)</small>
🍸 cocktail glass <small>(bar, cocktail, drink, glass)</small>
🍹 tropical drink <small>(bar, drink, tropical)</small>
🍺 beer mug <small>(bar, beer, drink, mug)</small>
🍻 clinking beer mugs <small>(bar, beer, clink, clinking beer mugs, drink, mug)</small>
🥂 clinking glasses <small>(celebrate, clink, clinking glasses, drink, glass)</small>
🥃 tumbler glass <small>(glass, liquor, shot, tumbler, whisky)</small>
🥤 cup with straw <small>(cup with straw, juice, soda)</small>
🧃 beverage box <small>(beverage box, juice box)</small>
🧉 mate <small>(drink, mate)</small>
🧊 ice <small>(cold, ice, ice cube, iceberg)</small>
🥢 chopsticks <small>(chopsticks, hashi)</small>
🍽 fork and knife with plate <small>(cooking, fork, fork and knife with plate, knife, plate)</small>
🍴 fork and knife <small>(cooking, cutlery, fork, fork and knife, knife)</small>
🥄 spoon <small>(spoon, tableware)</small>
🔪 kitchen knife <small>(cooking, hocho, kitchen knife, knife, tool, weapon)</small>
🏺 amphora <small>(amphora, Aquarius, cooking, drink, jug, zodiac)</small>
🌍 globe showing Europe-Africa <small>(Africa, earth, Europe, globe, globe showing Europe-Africa, world)</small>
🌎 globe showing Americas <small>(Americas, earth, globe, globe showing Americas, world)</small>
🌏 globe showing Asia-Australia <small>(Asia, Australia, earth, globe, globe showing Asia-Australia, world)</small>
🌐 globe with meridians <small>(earth, globe, globe with meridians, meridians, world)</small>
🗺 world map <small>(map, world)</small>
🗾 map of Japan <small>(Japan, map, map of Japan)</small>
🧭 compass <small>(compass, magnetic, navigation, orienteering)</small>
🏔 snow-capped mountain <small>(cold, mountain, snow, snow-capped mountain)</small>
⛰ mountain <small>(mountain)</small>
🌋 volcano <small>(eruption, mountain, volcano)</small>
🗻 mount fuji <small>(fuji, mount fuji, mountain)</small>
🏕 camping <small>(camping)</small>
🏖 beach with umbrella <small>(beach, beach with umbrella, umbrella)</small>
🏜 desert <small>(desert)</small>
🏝 desert island <small>(desert, island)</small>
🏞 national park <small>(national park, park)</small>
🏟 stadium <small>(stadium)</small>
🏛 classical building <small>(classical, classical building)</small>
🏗 building construction <small>(building construction, construction)</small>
🧱 brick <small>(brick, bricks, clay, mortar, wall)</small>
🏘 houses <small>(houses)</small>
🏚 derelict house <small>(derelict, house)</small>
🏠 house <small>(home, house)</small>
🏡 house with garden <small>(garden, home, house, house with garden)</small>
🏢 office building <small>(building, office building)</small>
🏣 Japanese post office <small>(Japanese, Japanese post office, post)</small>
🏤 post office <small>(European, post, post office)</small>
🏥 hospital <small>(doctor, hospital, medicine)</small>
🏦 bank <small>(bank, building)</small>
🏨 hotel <small>(building, hotel)</small>
🏩 love hotel <small>(hotel, love)</small>
🏪 convenience store <small>(convenience, store)</small>
🏫 school <small>(building, school)</small>
🏬 department store <small>(department, store)</small>
🏭 factory <small>(building, factory)</small>
🏯 Japanese castle <small>(castle, Japanese)</small>
🏰 castle <small>(castle, European)</small>
💒 wedding <small>(chapel, romance, wedding)</small>
🗼 Tokyo tower <small>(Tokyo, tower)</small>
🗽 Statue of Liberty <small>(liberty, statue, Statue of Liberty)</small>
⛪ church <small>(Christian, church, cross, religion)</small>
🕌 mosque <small>(islam, mosque, Muslim, religion)</small>
🛕 hindu temple <small>(hindu, temple)</small>
🕍 synagogue <small>(Jew, Jewish, religion, synagogue, temple)</small>
⛩ shinto shrine <small>(religion, shinto, shrine)</small>
🕋 kaaba <small>(islam, kaaba, Muslim, religion)</small>
⛲ fountain <small>(fountain)</small>
⛺ tent <small>(camping, tent)</small>
🌁 foggy <small>(fog, foggy)</small>
🌃 night with stars <small>(night, night with stars, star)</small>
🏙 cityscape <small>(city, cityscape)</small>
🌄 sunrise over mountains <small>(morning, mountain, sun, sunrise, sunrise over mountains)</small>
🌅 sunrise <small>(morning, sun, sunrise)</small>
🌆 cityscape at dusk <small>(city, cityscape at dusk, dusk, evening, landscape, sunset)</small>
🌇 sunset <small>(dusk, sun, sunset)</small>
🌉 bridge at night <small>(bridge, bridge at night, night)</small>
♨ hot springs <small>(hot, hotsprings, springs, steaming)</small>
🎠 carousel horse <small>(carousel, horse)</small>
🎡 ferris wheel <small>(amusement park, ferris, wheel)</small>
🎢 roller coaster <small>(amusement park, coaster, roller)</small>
💈 barber pole <small>(barber, haircut, pole)</small>
🎪 circus tent <small>(circus, tent)</small>
🚂 locomotive <small>(engine, locomotive, railway, steam, train)</small>
🚃 railway car <small>(car, electric, railway, train, tram, trolleybus)</small>
🚄 high-speed train <small>(high-speed train, railway, shinkansen, speed, train)</small>
🚅 bullet train <small>(bullet, railway, shinkansen, speed, train)</small>
🚆 train <small>(railway, train)</small>
🚇 metro <small>(metro, subway)</small>
🚈 light rail <small>(light rail, railway)</small>
🚉 station <small>(railway, station, train)</small>
🚊 tram <small>(tram, trolleybus)</small>
🚝 monorail <small>(monorail, vehicle)</small>
🚞 mountain railway <small>(car, mountain, railway)</small>
🚋 tram car <small>(car, tram, trolleybus)</small>
🚌 bus <small>(bus, vehicle)</small>
🚍 oncoming bus <small>(bus, oncoming)</small>
🚎 trolleybus <small>(bus, tram, trolley, trolleybus)</small>
🚐 minibus <small>(bus, minibus)</small>
🚑 ambulance <small>(ambulance, vehicle)</small>
🚒 fire engine <small>(engine, fire, truck)</small>
🚓 police car <small>(car, patrol, police)</small>
🚔 oncoming police car <small>(car, oncoming, police)</small>
🚕 taxi <small>(taxi, vehicle)</small>
🚖 oncoming taxi <small>(oncoming, taxi)</small>
🚗 automobile <small>(automobile, car)</small>
🚘 oncoming automobile <small>(automobile, car, oncoming)</small>
🚙 sport utility vehicle <small>(recreational, sport utility, sport utility vehicle)</small>
🚚 delivery truck <small>(delivery, truck)</small>
🚛 articulated lorry <small>(articulated lorry, lorry, semi, truck)</small>
🚜 tractor <small>(tractor, vehicle)</small>
🏎 racing car <small>(car, racing)</small>
🏍 motorcycle <small>(motorcycle, racing)</small>
🛵 motor scooter <small>(motor, scooter)</small>
🦽 manual wheelchair <small>(accessibility, manual wheelchair)</small>
🦼 motorized wheelchair <small>(accessibility, motorized wheelchair)</small>
🛺 auto rickshaw <small>(auto rickshaw, tuk tuk)</small>
🚲 bicycle <small>(bicycle, bike)</small>
🛴 kick scooter <small>(kick, scooter)</small>
🛹 skateboard <small>(board, skateboard)</small>
🚏 bus stop <small>(bus, busstop, stop)</small>
🛣 motorway <small>(highway, motorway, road)</small>
🛤 railway track <small>(railway, railway track, train)</small>
🛢 oil drum <small>(drum, oil)</small>
⛽ fuel pump <small>(diesel, fuel, fuelpump, gas, pump, station)</small>
🚨 police car light <small>(beacon, car, light, police, revolving)</small>
🚥 horizontal traffic light <small>(horizontal traffic light, light, signal, traffic)</small>
🚦 vertical traffic light <small>(light, signal, traffic, vertical traffic light)</small>
🛑 stop sign <small>(octagonal, sign, stop)</small>
🚧 construction <small>(barrier, construction)</small>
⚓ anchor <small>(anchor, ship, tool)</small>
⛵ sailboat <small>(boat, resort, sailboat, sea, yacht)</small>
🛶 canoe <small>(boat, canoe)</small>
🚤 speedboat <small>(boat, speedboat)</small>
🛳 passenger ship <small>(passenger, ship)</small>
⛴ ferry <small>(boat, ferry, passenger)</small>
🛥 motor boat <small>(boat, motor boat, motorboat)</small>
🚢 ship <small>(boat, passenger, ship)</small>
✈ airplane <small>(aeroplane, airplane)</small>
🛩 small airplane <small>(aeroplane, airplane, small airplane)</small>
🛫 airplane departure <small>(aeroplane, airplane, check-in, departure, departures)</small>
🛬 airplane arrival <small>(aeroplane, airplane, airplane arrival, arrivals, arriving, landing)</small>
🪂 parachute <small>(hang-glide, parachute, parasail, skydive)</small>
💺 seat <small>(chair, seat)</small>
🚁 helicopter <small>(helicopter, vehicle)</small>
🚟 suspension railway <small>(railway, suspension)</small>
🚠 mountain cableway <small>(cable, gondola, mountain, mountain cableway)</small>
🚡 aerial tramway <small>(aerial, cable, car, gondola, tramway)</small>
🛰 satellite <small>(satellite, space)</small>
🚀 rocket <small>(rocket, space)</small>
🛸 flying saucer <small>(flying saucer, UFO)</small>
🛎 bellhop bell <small>(bell, bellhop, hotel)</small>
🧳 luggage <small>(luggage, packing, travel)</small>
⌛ hourglass done <small>(hourglass done, sand, timer)</small>
⏳ hourglass not done <small>(hourglass, hourglass not done, sand, timer)</small>
⌚ watch <small>(clock, watch)</small>
⏰ alarm clock <small>(alarm, clock)</small>
⏱ stopwatch <small>(clock, stopwatch)</small>
⏲ timer clock <small>(clock, timer)</small>
🕰 mantelpiece clock <small>(clock, mantelpiece clock)</small>
🕛 twelve o’clock <small>(00, 12, 12:00, clock, o’clock, twelve)</small>
🕧 twelve-thirty <small>(12, 12:30, clock, thirty, twelve, twelve-thirty)</small>
🕐 one o’clock <small>(00, 1, 1:00, clock, o’clock, one)</small>
🕜 one-thirty <small>(1, 1:30, clock, one, one-thirty, thirty)</small>
🕑 two o’clock <small>(00, 2, 2:00, clock, o’clock, two)</small>
🕝 two-thirty <small>(2, 2:30, clock, thirty, two, two-thirty)</small>
🕒 three o’clock <small>(00, 3, 3:00, clock, o’clock, three)</small>
🕞 three-thirty <small>(3, 3:30, clock, thirty, three, three-thirty)</small>
🕓 four o’clock <small>(00, 4, 4:00, clock, four, o’clock)</small>
🕟 four-thirty <small>(4, 4:30, clock, four, four-thirty, thirty)</small>
🕔 five o’clock <small>(00, 5, 5:00, clock, five, o’clock)</small>
🕠 five-thirty <small>(5, 5:30, clock, five, five-thirty, thirty)</small>
🕕 six o’clock <small>(00, 6, 6:00, clock, o’clock, six)</small>
🕡 six-thirty <small>(6, 6:30, clock, six, six-thirty, thirty)</small>
🕖 seven o’clock <small>(00, 7, 7:00, clock, o’clock, seven)</small>
🕢 seven-thirty <small>(7, 7:30, clock, seven, seven-thirty, thirty)</small>
🕗 eight o’clock <small>(00, 8, 8:00, clock, eight, o’clock)</small>
🕣 eight-thirty <small>(8, 8:30, clock, eight, eight-thirty, thirty)</small>
🕘 nine o’clock <small>(00, 9, 9:00, clock, nine, o’clock)</small>
🕤 nine-thirty <small>(9, 9:30, clock, nine, nine-thirty, thirty)</small>
🕙 ten o’clock <small>(00, 10, 10:00, clock, o’clock, ten)</small>
🕥 ten-thirty <small>(10, 10:30, clock, ten, ten-thirty, thirty)</small>
🕚 eleven o’clock <small>(00, 11, 11:00, clock, eleven, o’clock)</small>
🕦 eleven-thirty <small>(11, 11:30, clock, eleven, eleven-thirty, thirty)</small>
🌑 new moon <small>(dark, moon, new moon)</small>
🌒 waxing crescent moon <small>(crescent, moon, waxing)</small>
🌓 first quarter moon <small>(first quarter moon, moon, quarter)</small>
🌔 waxing gibbous moon <small>(gibbous, moon, waxing)</small>
🌕 full moon <small>(full, moon)</small>
🌖 waning gibbous moon <small>(gibbous, moon, waning)</small>
🌗 last quarter moon <small>(last quarter moon, moon, quarter)</small>
🌘 waning crescent moon <small>(crescent, moon, waning)</small>
🌙 crescent moon <small>(crescent, moon)</small>
🌚 new moon face <small>(face, moon, new moon face)</small>
🌛 first quarter moon face <small>(face, first quarter moon face, moon, quarter)</small>
🌜 last quarter moon face <small>(face, last quarter moon face, moon, quarter)</small>
🌡 thermometer <small>(thermometer, weather)</small>
☀ sun <small>(bright, rays, sun, sunny)</small>
🌝 full moon face <small>(bright, face, full, moon)</small>
🌞 sun with face <small>(bright, face, sun, sun with face)</small>
🪐 ringed planet <small>(ringed planet, saturn, saturnine)</small>
⭐ star <small>(star)</small>
🌟 glowing star <small>(glittery, glow, glowing star, shining, sparkle, star)</small>
🌠 shooting star <small>(falling, shooting, star)</small>
🌌 milky way <small>(milky way, space)</small>
☁ cloud <small>(cloud, weather)</small>
⛅ sun behind cloud <small>(cloud, sun, sun behind cloud)</small>
⛈ cloud with lightning and rain <small>(cloud, cloud with lightning and rain, rain, thunder)</small>
🌤 sun behind small cloud <small>(cloud, sun, sun behind small cloud)</small>
🌥 sun behind large cloud <small>(cloud, sun, sun behind large cloud)</small>
🌦 sun behind rain cloud <small>(cloud, rain, sun, sun behind rain cloud)</small>
🌧 cloud with rain <small>(cloud, cloud with rain, rain)</small>
🌨 cloud with snow <small>(cloud, cloud with snow, cold, snow)</small>
🌩 cloud with lightning <small>(cloud, cloud with lightning, lightning)</small>
🌪 tornado <small>(cloud, tornado, whirlwind)</small>
🌫 fog <small>(cloud, fog)</small>
🌬 wind face <small>(blow, cloud, face, wind)</small>
🌀 cyclone <small>(cyclone, dizzy, hurricane, twister, typhoon)</small>
🌈 rainbow <small>(rain, rainbow)</small>
🌂 closed umbrella <small>(closed umbrella, clothing, rain, umbrella)</small>
☂ umbrella <small>(clothing, rain, umbrella)</small>
☔ umbrella with rain drops <small>(clothing, drop, rain, umbrella, umbrella with rain drops)</small>
⛱ umbrella on ground <small>(rain, sun, umbrella, umbrella on ground)</small>
⚡ high voltage <small>(danger, electric, high voltage, lightning, voltage, zap)</small>
❄ snowflake <small>(cold, snow, snowflake)</small>
☃ snowman <small>(cold, snow, snowman)</small>
⛄ snowman without snow <small>(cold, snow, snowman, snowman without snow)</small>
☄ comet <small>(comet, space)</small>
🔥 fire <small>(fire, flame, tool)</small>
💧 droplet <small>(cold, comic, drop, droplet, sweat)</small>
🌊 water wave <small>(ocean, water, wave)</small>
🎃 jack-o-lantern <small>(celebration, halloween, jack, jack-o-lantern, lantern)</small>
🎄 Christmas tree <small>(celebration, Christmas, tree)</small>
🎆 fireworks <small>(celebration, fireworks)</small>
🎇 sparkler <small>(celebration, fireworks, sparkle, sparkler)</small>
🧨 firecracker <small>(dynamite, explosive, firecracker, fireworks)</small>
✨ sparkles <small>(*, sparkle, sparkles, star)</small>
🎈 balloon <small>(balloon, celebration)</small>
🎉 party popper <small>(celebration, party, popper, tada)</small>
🎊 confetti ball <small>(ball, celebration, confetti)</small>
🎋 tanabata tree <small>(banner, celebration, Japanese, tanabata tree, tree)</small>
🎍 pine decoration <small>(bamboo, celebration, Japanese, pine, pine decoration)</small>
🎎 Japanese dolls <small>(celebration, doll, festival, Japanese, Japanese dolls)</small>
🎏 carp streamer <small>(carp, celebration, streamer)</small>
🎐 wind chime <small>(bell, celebration, chime, wind)</small>
🎑 moon viewing ceremony <small>(celebration, ceremony, moon, moon viewing ceremony)</small>
🧧 red envelope <small>(gift, good luck, hóngbāo, lai see, money, red envelope)</small>
🎀 ribbon <small>(celebration, ribbon)</small>
🎁 wrapped gift <small>(box, celebration, gift, present, wrapped)</small>
🎗 reminder ribbon <small>(celebration, reminder, ribbon)</small>
🎟 admission tickets <small>(admission, admission tickets, ticket)</small>
🎫 ticket <small>(admission, ticket)</small>
🎖 military medal <small>(celebration, medal, military)</small>
🏆 trophy <small>(prize, trophy)</small>
🏅 sports medal <small>(medal, sports medal)</small>
🥇 1st place medal <small>(1st place medal, first, gold, medal)</small>
🥈 2nd place medal <small>(2nd place medal, medal, second, silver)</small>
🥉 3rd place medal <small>(3rd place medal, bronze, medal, third)</small>
⚽ soccer ball <small>(ball, football, soccer)</small>
⚾ baseball <small>(ball, baseball)</small>
🥎 softball <small>(ball, glove, softball, underarm)</small>
🏀 basketball <small>(ball, basketball, hoop)</small>
🏐 volleyball <small>(ball, game, volleyball)</small>
🏈 american football <small>(american, ball, football)</small>
🏉 rugby football <small>(ball, football, rugby)</small>
🎾 tennis <small>(ball, racquet, tennis)</small>
🥏 flying disc <small>(flying disc, ultimate)</small>
🎳 bowling <small>(ball, bowling, game)</small>
🏏 cricket game <small>(ball, bat, cricket game, game)</small>
🏑 field hockey <small>(ball, field, game, hockey, stick)</small>
🏒 ice hockey <small>(game, hockey, ice, puck, stick)</small>
🥍 lacrosse <small>(ball, goal, lacrosse, stick)</small>
🏓 ping pong <small>(ball, bat, game, paddle, ping pong, table tennis)</small>
🏸 badminton <small>(badminton, birdie, game, racquet, shuttlecock)</small>
🥊 boxing glove <small>(boxing, glove)</small>
🥋 martial arts uniform <small>(judo, karate, martial arts, martial arts uniform, taekwondo, uniform)</small>
🥅 goal net <small>(goal, net)</small>
⛳ flag in hole <small>(flag in hole, golf, hole)</small>
⛸ ice skate <small>(ice, skate)</small>
🎣 fishing pole <small>(fish, fishing pole, pole)</small>
🤿 diving mask <small>(diving, diving mask, scuba, snorkeling)</small>
🎽 running shirt <small>(athletics, running, sash, shirt)</small>
🎿 skis <small>(ski, skis, snow)</small>
🛷 sled <small>(sled, sledge, sleigh)</small>
🥌 curling stone <small>(curling stone, game, rock)</small>
🎯 direct hit <small>(bullseye, dart, direct hit, game, hit, target)</small>
🪀 yo-yo <small>(fluctuate, toy, yo-yo)</small>
🪁 kite <small>(fly, kite, soar)</small>
🎱 pool 8 ball <small>(8, ball, billiard, eight, game, pool 8 ball)</small>
🔮 crystal ball <small>(ball, crystal, fairy tale, fantasy, fortune, tool)</small>
🧿 nazar amulet <small>(bead, charm, evil-eye, nazar, nazar amulet, talisman)</small>
🎮 video game <small>(controller, game, video game)</small>
🕹 joystick <small>(game, joystick, video game)</small>
🎰 slot machine <small>(game, slot, slot machine)</small>
🎲 game die <small>(dice, die, game)</small>
🧩 puzzle piece <small>(clue, interlocking, jigsaw, piece, puzzle)</small>
🧸 teddy bear <small>(plaything, plush, stuffed, teddy bear, toy)</small>
♠ spade suit <small>(card, game, spade suit)</small>
♥ heart suit <small>(card, game, heart suit)</small>
♦ diamond suit <small>(card, diamond suit, game)</small>
♣ club suit <small>(card, club suit, game)</small>
♟ chess pawn <small>(chess, chess pawn, dupe, expendable)</small>
🃏 joker <small>(card, game, joker, wildcard)</small>
🀄 mahjong red dragon <small>(game, mahjong, mahjong red dragon, red)</small>
🎴 flower playing cards <small>(card, flower, flower playing cards, game, Japanese, playing)</small>
🎭 performing arts <small>(art, mask, performing, performing arts, theater, theatre)</small>
🖼 framed picture <small>(art, frame, framed picture, museum, painting, picture)</small>
🎨 artist palette <small>(art, artist palette, museum, painting, palette)</small>
🧵 thread <small>(needle, sewing, spool, string, thread)</small>
🧶 yarn <small>(ball, crochet, knit, yarn)</small>
👓 glasses <small>(clothing, eye, eyeglasses, eyewear, glasses)</small>
🕶 sunglasses <small>(dark, eye, eyewear, glasses, sunglasses)</small>
🥽 goggles <small>(eye protection, goggles, swimming, welding)</small>
🥼 lab coat <small>(doctor, experiment, lab coat, scientist)</small>
🦺 safety vest <small>(emergency, safety, vest)</small>
👔 necktie <small>(clothing, necktie, tie)</small>
👕 t-shirt <small>(clothing, shirt, t-shirt, tshirt)</small>
👖 jeans <small>(clothing, jeans, pants, trousers)</small>
🧣 scarf <small>(neck, scarf)</small>
🧤 gloves <small>(gloves, hand)</small>
🧥 coat <small>(coat, jacket)</small>
🧦 socks <small>(socks, stocking)</small>
👗 dress <small>(clothing, dress)</small>
👘 kimono <small>(clothing, kimono)</small>
🥻 sari <small>(clothing, dress, sari)</small>
🩱 one-piece swimsuit <small>(bathing suit, one-piece swimsuit)</small>
🩲 briefs <small>(bathing suit, briefs, one-piece, swimsuit, underwear)</small>
🩳 shorts <small>(bathing suit, pants, shorts, underwear)</small>
👙 bikini <small>(bikini, clothing, swim)</small>
👚 woman’s clothes <small>(clothing, woman, woman’s clothes)</small>
👛 purse <small>(clothing, coin, purse)</small>
👜 handbag <small>(bag, clothing, handbag, purse)</small>
👝 clutch bag <small>(bag, clothing, clutch bag, pouch)</small>
🛍 shopping bags <small>(bag, hotel, shopping, shopping bags)</small>
🎒 backpack <small>(backpack, bag, rucksack, satchel, school)</small>
👞 man’s shoe <small>(clothing, man, man’s shoe, shoe)</small>
👟 running shoe <small>(athletic, clothing, running shoe, shoe, sneaker)</small>
🥾 hiking boot <small>(backpacking, boot, camping, hiking)</small>
🥿 flat shoe <small>(ballet flat, flat shoe, slip-on, slipper)</small>
👠 high-heeled shoe <small>(clothing, heel, high-heeled shoe, shoe, woman)</small>
👡 woman’s sandal <small>(clothing, sandal, shoe, woman, woman’s sandal)</small>
🩰 ballet shoes <small>(ballet, ballet shoes, dance)</small>
👢 woman’s boot <small>(boot, clothing, shoe, woman, woman’s boot)</small>
👑 crown <small>(clothing, crown, king, queen)</small>
👒 woman’s hat <small>(clothing, hat, woman, woman’s hat)</small>
🎩 top hat <small>(clothing, hat, top, tophat)</small>
🎓 graduation cap <small>(cap, celebration, clothing, graduation, hat)</small>
🧢 billed cap <small>(baseball cap, billed cap)</small>
⛑ rescue worker’s helmet <small>(aid, cross, face, hat, helmet, rescue worker’s helmet)</small>
📿 prayer beads <small>(beads, clothing, necklace, prayer, religion)</small>
💄 lipstick <small>(cosmetics, lipstick, makeup)</small>
💍 ring <small>(diamond, ring)</small>
💎 gem stone <small>(diamond, gem, gem stone, jewel)</small>
🔇 muted speaker <small>(mute, muted speaker, quiet, silent, speaker)</small>
🔈 speaker low volume <small>(soft, speaker low volume)</small>
🔉 speaker medium volume <small>(medium, speaker medium volume)</small>
🔊 speaker high volume <small>(loud, speaker high volume)</small>
📢 loudspeaker <small>(loud, loudspeaker, public address)</small>
📣 megaphone <small>(cheering, megaphone)</small>
📯 postal horn <small>(horn, post, postal)</small>
🔔 bell <small>(bell)</small>
🔕 bell with slash <small>(bell, bell with slash, forbidden, mute, quiet, silent)</small>
🎼 musical score <small>(music, musical score, score)</small>
🎵 musical note <small>(music, musical note, note)</small>
🎶 musical notes <small>(music, musical notes, note, notes)</small>
🎙 studio microphone <small>(mic, microphone, music, studio)</small>
🎚 level slider <small>(level, music, slider)</small>
🎛 control knobs <small>(control, knobs, music)</small>
🎤 microphone <small>(karaoke, mic, microphone)</small>
🎧 headphone <small>(earbud, headphone)</small>
📻 radio <small>(radio, video)</small>
🎷 saxophone <small>(instrument, music, sax, saxophone)</small>
🎸 guitar <small>(guitar, instrument, music)</small>
🎹 musical keyboard <small>(instrument, keyboard, music, musical keyboard, piano)</small>
🎺 trumpet <small>(instrument, music, trumpet)</small>
🎻 violin <small>(instrument, music, violin)</small>
🪕 banjo <small>(banjo, music, stringed)</small>
🥁 drum <small>(drum, drumsticks, music)</small>
📱 mobile phone <small>(cell, mobile, phone, telephone)</small>
📲 mobile phone with arrow <small>(arrow, cell, mobile, mobile phone with arrow, phone, receive)</small>
☎ telephone <small>(phone, telephone)</small>
📞 telephone receiver <small>(phone, receiver, telephone)</small>
📟 pager <small>(pager)</small>
📠 fax machine <small>(fax, fax machine)</small>
🔋 battery <small>(battery)</small>
🔌 electric plug <small>(electric, electricity, plug)</small>
💻 laptop <small>(computer, laptop computer, pc, personal)</small>
🖥 desktop computer <small>(computer, desktop)</small>
🖨 printer <small>(computer, printer)</small>
⌨ keyboard <small>(computer, keyboard)</small>
🖱 computer mouse <small>(computer, computer mouse)</small>
🖲 trackball <small>(computer, trackball)</small>
💽 computer disk <small>(computer, disk, minidisk, optical)</small>
💾 floppy disk <small>(computer, disk, floppy)</small>
💿 optical disk <small>(cd, computer, disk, optical)</small>
📀 dvd <small>(blu-ray, computer, disk, dvd, optical)</small>
🧮 abacus <small>(abacus, calculation)</small>
🎥 movie camera <small>(camera, cinema, movie)</small>
🎞 film frames <small>(cinema, film, frames, movie)</small>
📽 film projector <small>(cinema, film, movie, projector, video)</small>
🎬 clapper board <small>(clapper, clapper board, movie)</small>
📺 television <small>(television, tv, video)</small>
📷 camera <small>(camera, video)</small>
📸 camera with flash <small>(camera, camera with flash, flash, video)</small>
📹 video camera <small>(camera, video)</small>
📼 videocassette <small>(tape, vhs, video, videocassette)</small>
🔍 magnifying glass tilted left <small>(glass, magnifying, magnifying glass tilted left, search, tool)</small>
🔎 magnifying glass tilted right <small>(glass, magnifying, magnifying glass tilted right, search, tool)</small>
🕯 candle <small>(candle, light)</small>
💡 light bulb <small>(bulb, comic, electric, idea, light)</small>
🔦 flashlight <small>(electric, flashlight, light, tool, torch)</small>
🏮 red paper lantern <small>(bar, lantern, light, red, red paper lantern)</small>
🪔 diya lamp <small>(diya, lamp, oil)</small>
📔 notebook with decorative cover <small>(book, cover, decorated, notebook, notebook with decorative cover)</small>
📕 closed book <small>(book, closed)</small>
📖 open book <small>(book, open)</small>
📗 green book <small>(book, green)</small>
📘 blue book <small>(blue, book)</small>
📙 orange book <small>(book, orange)</small>
📚 books <small>(book, books)</small>
📓 notebook <small>(notebook)</small>
📒 ledger <small>(ledger, notebook)</small>
📃 page with curl <small>(curl, document, page, page with curl)</small>
📜 scroll <small>(paper, scroll)</small>
📄 page facing up <small>(document, page, page facing up)</small>
📰 newspaper <small>(news, newspaper, paper)</small>
🗞 rolled-up newspaper <small>(news, newspaper, paper, rolled, rolled-up newspaper)</small>
📑 bookmark tabs <small>(bookmark, mark, marker, tabs)</small>
🔖 bookmark <small>(bookmark, mark)</small>
🏷 label <small>(label)</small>
💰 money bag <small>(bag, dollar, money, moneybag)</small>
💴 yen banknote <small>(banknote, bill, currency, money, note, yen)</small>
💵 dollar banknote <small>(banknote, bill, currency, dollar, money, note)</small>
💶 euro banknote <small>(banknote, bill, currency, euro, money, note)</small>
💷 pound banknote <small>(banknote, bill, currency, money, note, pound)</small>
💸 money with wings <small>(banknote, bill, fly, money, money with wings, wings)</small>
💳 credit card <small>(card, credit, money)</small>
🧾 receipt <small>(accounting, bookkeeping, evidence, proof, receipt)</small>
💹 chart increasing with yen <small>(chart, chart increasing with yen, graph, growth, money, yen)</small>
💱 currency exchange <small>(bank, currency, exchange, money)</small>
💲 heavy dollar sign <small>(currency, dollar, heavy dollar sign, money)</small>
✉ envelope <small>(email, envelope, letter)</small>
📧 e-mail <small>(e-mail, email, letter, mail)</small>
📨 incoming envelope <small>(e-mail, email, envelope, incoming, letter, receive)</small>
📩 envelope with arrow <small>(arrow, e-mail, email, envelope, envelope with arrow, outgoing)</small>
📤 outbox tray <small>(box, letter, mail, outbox, sent, tray)</small>
📥 inbox tray <small>(box, inbox, letter, mail, receive, tray)</small>
📦 package <small>(box, package, parcel)</small>
📫 closed mailbox with raised flag <small>(closed, closed mailbox with raised flag, mail, mailbox, postbox)</small>
📪 closed mailbox with lowered flag <small>(closed, closed mailbox with lowered flag, lowered, mail, mailbox, postbox)</small>
📬 open mailbox with raised flag <small>(mail, mailbox, open, open mailbox with raised flag, postbox)</small>
📭 open mailbox with lowered flag <small>(lowered, mail, mailbox, open, open mailbox with lowered flag, postbox)</small>
📮 postbox <small>(mail, mailbox, postbox)</small>
🗳 ballot box with ballot <small>(ballot, ballot box with ballot, box)</small>
✏ pencil <small>(pencil)</small>
✒ black nib <small>(black nib, nib, pen)</small>
🖋 fountain pen <small>(fountain, pen)</small>
🖊 pen <small>(ballpoint, pen)</small>
🖌 paintbrush <small>(paintbrush, painting)</small>
🖍 crayon <small>(crayon)</small>
📝 memo <small>(memo, pencil)</small>
💼 briefcase <small>(briefcase)</small>
📁 file folder <small>(file, folder)</small>
📂 open file folder <small>(file, folder, open)</small>
🗂 card index dividers <small>(card, dividers, index)</small>
📅 calendar <small>(calendar, date)</small>
📆 tear-off calendar <small>(calendar, tear-off calendar)</small>
🗒 spiral notepad <small>(note, pad, spiral, spiral notepad)</small>
🗓 spiral calendar <small>(calendar, pad, spiral)</small>
📇 card index <small>(card, index, rolodex)</small>
📈 chart increasing <small>(chart, chart increasing, graph, growth, trend, upward)</small>
📉 chart decreasing <small>(chart, chart decreasing, down, graph, trend)</small>
📊 bar chart <small>(bar, chart, graph)</small>
📋 clipboard <small>(clipboard)</small>
📌 pushpin <small>(pin, pushpin)</small>
📍 round pushpin <small>(pin, pushpin, round pushpin)</small>
📎 paperclip <small>(paperclip)</small>
🖇 linked paperclips <small>(link, linked paperclips, paperclip)</small>
📏 straight ruler <small>(ruler, straight edge, straight ruler)</small>
📐 triangular ruler <small>(ruler, set, triangle, triangular ruler)</small>
✂ scissors <small>(cutting, scissors, tool)</small>
🗃 card file box <small>(box, card, file)</small>
🗄 file cabinet <small>(cabinet, file, filing)</small>
🗑 wastebasket <small>(wastebasket)</small>
🔒 locked <small>(closed, locked)</small>
🔓 unlocked <small>(lock, open, unlock, unlocked)</small>
🔏 locked with pen <small>(ink, lock, locked with pen, nib, pen, privacy)</small>
🔐 locked with key <small>(closed, key, lock, locked with key, secure)</small>
🔑 key <small>(key, lock, password)</small>
🗝 old key <small>(clue, key, lock, old)</small>
🔨 hammer <small>(hammer, tool)</small>
🪓 axe <small>(axe, chop, hatchet, split, wood)</small>
⛏ pick <small>(mining, pick, tool)</small>
⚒ hammer and pick <small>(hammer, hammer and pick, pick, tool)</small>
🛠 hammer and wrench <small>(hammer, hammer and wrench, spanner, tool, wrench)</small>
🗡 dagger <small>(dagger, knife, weapon)</small>
⚔ crossed swords <small>(crossed, swords, weapon)</small>
🔫 pistol <small>(gun, handgun, pistol, revolver, tool, weapon)</small>
🏹 bow and arrow <small>(archer, arrow, bow, bow and arrow, Sagittarius, zodiac)</small>
🛡 shield <small>(shield, weapon)</small>
🔧 wrench <small>(spanner, tool, wrench)</small>
🔩 nut and bolt <small>(bolt, nut, nut and bolt, tool)</small>
⚙ gear <small>(cog, cogwheel, gear, tool)</small>
🗜 clamp <small>(clamp, compress, tool, vice)</small>
⚖ balance scale <small>(balance, justice, Libra, scale, zodiac)</small>
🦯 probing cane <small>(accessibility, blind, probing cane)</small>
🔗 link <small>(link)</small>
⛓ chains <small>(chain, chains)</small>
🧰 toolbox <small>(chest, mechanic, tool, toolbox)</small>
🧲 magnet <small>(attraction, horseshoe, magnet, magnetic)</small>
⚗ alembic <small>(alembic, chemistry, tool)</small>
🧪 test tube <small>(chemist, chemistry, experiment, lab, science, test tube)</small>
🧫 petri dish <small>(bacteria, biologist, biology, culture, lab, petri dish)</small>
🧬 dna <small>(biologist, dna, evolution, gene, genetics, life)</small>
🔬 microscope <small>(microscope, science, tool)</small>
🔭 telescope <small>(science, telescope, tool)</small>
📡 satellite antenna <small>(antenna, dish, satellite)</small>
💉 syringe <small>(medicine, needle, shot, sick, syringe)</small>
🩸 drop of blood <small>(bleed, blood donation, drop of blood, injury, medicine, menstruation)</small>
💊 pill <small>(doctor, medicine, pill, sick)</small>
🩹 adhesive bandage <small>(adhesive bandage, bandage)</small>
🩺 stethoscope <small>(doctor, heart, medicine, stethoscope)</small>
🚪 door <small>(door)</small>
🛏 bed <small>(bed, hotel, sleep)</small>
🛋 couch and lamp <small>(couch, couch and lamp, hotel, lamp)</small>
🪑 chair <small>(chair, seat, sit)</small>
🚽 toilet <small>(toilet)</small>
🚿 shower <small>(shower, water)</small>
🛁 bathtub <small>(bath, bathtub)</small>
🪒 razor <small>(razor, sharp, shave)</small>
🧴 lotion bottle <small>(lotion, lotion bottle, moisturizer, shampoo, sunscreen)</small>
🧷 safety pin <small>(diaper, punk rock, safety pin)</small>
🧹 broom <small>(broom, cleaning, sweeping, witch)</small>
🧺 basket <small>(basket, farming, laundry, picnic)</small>
🧻 roll of paper <small>(paper towels, roll of paper, toilet paper)</small>
🧼 soap <small>(bar, bathing, cleaning, lather, soap, soapdish)</small>
🧽 sponge <small>(absorbing, cleaning, porous, sponge)</small>
🧯 fire extinguisher <small>(extinguish, fire, fire extinguisher, quench)</small>
🛒 shopping cart <small>(cart, shopping, trolley)</small>
🚬 cigarette <small>(cigarette, smoking)</small>
⚰ coffin <small>(coffin, death)</small>
⚱ funeral urn <small>(ashes, death, funeral, urn)</small>
🗿 moai <small>(face, moai, moyai, statue)</small>
🏧 ATM sign <small>(atm, ATM sign, automated, bank, teller)</small>
🚮 litter in bin sign <small>(litter, litter bin, litter in bin sign)</small>
🚰 potable water <small>(drinking, potable, water)</small>
♿ wheelchair symbol <small>(access, wheelchair symbol)</small>
🚹 men’s room <small>(lavatory, man, men’s room, restroom, wc)</small>
🚺 women’s room <small>(lavatory, restroom, wc, woman, women’s room)</small>
🚻 restroom <small>(lavatory, restroom, WC)</small>
🚼 baby symbol <small>(baby, baby symbol, changing)</small>
🚾 water closet <small>(closet, lavatory, restroom, water, wc)</small>
🛂 passport control <small>(control, passport)</small>
🛃 customs <small>(customs)</small>
🛄 baggage claim <small>(baggage, claim)</small>
🛅 left luggage <small>(baggage, left luggage, locker, luggage)</small>
⚠ warning <small>(warning)</small>
🚸 children crossing <small>(child, children crossing, crossing, pedestrian, traffic)</small>
⛔ no entry <small>(entry, forbidden, no, not, prohibited, traffic)</small>
🚫 prohibited <small>(entry, forbidden, no, not, prohibited)</small>
🚳 no bicycles <small>(bicycle, bike, forbidden, no, no bicycles, prohibited)</small>
🚭 no smoking <small>(forbidden, no, not, prohibited, smoking)</small>
🚯 no littering <small>(forbidden, litter, no, no littering, not, prohibited)</small>
🚱 non-potable water <small>(non-drinking, non-potable, water)</small>
🚷 no pedestrians <small>(forbidden, no, no pedestrians, not, pedestrian, prohibited)</small>
📵 no mobile phones <small>(cell, forbidden, mobile, no, no mobile phones, phone)</small>
🔞 no one under eighteen <small>(18, age restriction, eighteen, no one under eighteen, prohibited, underage)</small>
☢ radioactive <small>(radioactive, sign)</small>
☣ biohazard <small>(biohazard, sign)</small>
⬆ up arrow <small>(arrow, cardinal, direction, north, up arrow)</small>
↗ up-right arrow <small>(arrow, direction, intercardinal, northeast, up-right arrow)</small>
➡ right arrow <small>(arrow, cardinal, direction, east, right arrow)</small>
↘ down-right arrow <small>(arrow, direction, down-right arrow, intercardinal, southeast)</small>
⬇ down arrow <small>(arrow, cardinal, direction, down, south)</small>
↙ down-left arrow <small>(arrow, direction, down-left arrow, intercardinal, southwest)</small>
⬅ left arrow <small>(arrow, cardinal, direction, left arrow, west)</small>
↖ up-left arrow <small>(arrow, direction, intercardinal, northwest, up-left arrow)</small>
↕ up-down arrow <small>(arrow, up-down arrow)</small>
↔ left-right arrow <small>(arrow, left-right arrow)</small>
↩ right arrow curving left <small>(arrow, right arrow curving left)</small>
↪ left arrow curving right <small>(arrow, left arrow curving right)</small>
⤴ right arrow curving up <small>(arrow, right arrow curving up)</small>
⤵ right arrow curving down <small>(arrow, down, right arrow curving down)</small>
🔃 clockwise vertical arrows <small>(arrow, clockwise, clockwise vertical arrows, reload)</small>
🔄 counterclockwise arrows button <small>(anticlockwise, arrow, counterclockwise, counterclockwise arrows button, withershins)</small>
🔙 BACK arrow <small>(arrow, back, BACK arrow)</small>
🔚 END arrow <small>(arrow, end, END arrow)</small>
🔛 ON! arrow <small>(arrow, mark, on, ON! arrow)</small>
🔜 SOON arrow <small>(arrow, soon, SOON arrow)</small>
🔝 TOP arrow <small>(arrow, top, TOP arrow, up)</small>
🛐 place of worship <small>(place of worship, religion, worship)</small>
⚛ atom symbol <small>(atheist, atom, atom symbol)</small>
🕉 om <small>(Hindu, om, religion)</small>
✡ star of David <small>(David, Jew, Jewish, religion, star, star of David)</small>
☸ wheel of dharma <small>(Buddhist, dharma, religion, wheel, wheel of dharma)</small>
☯ yin yang <small>(religion, tao, taoist, yang, yin)</small>
✝ latin cross <small>(Christian, cross, latin cross, religion)</small>
☦ orthodox cross <small>(Christian, cross, orthodox cross, religion)</small>
☪ star and crescent <small>(islam, Muslim, religion, star and crescent)</small>
☮ peace symbol <small>(peace, peace symbol)</small>
🕎 menorah <small>(candelabrum, candlestick, menorah, religion)</small>
🔯 dotted six-pointed star <small>(dotted six-pointed star, fortune, star)</small>
♈ Aries <small>(Aries, ram, zodiac)</small>
♉ Taurus <small>(bull, ox, Taurus, zodiac)</small>
♊ Gemini <small>(Gemini, twins, zodiac)</small>
♋ Cancer <small>(Cancer, crab, zodiac)</small>
♌ Leo <small>(Leo, lion, zodiac)</small>
♍ Virgo <small>(Virgo, zodiac)</small>
♎ Libra <small>(balance, justice, Libra, scales, zodiac)</small>
♏ Scorpio <small>(Scorpio, scorpion, scorpius, zodiac)</small>
♐ Sagittarius <small>(archer, Sagittarius, zodiac)</small>
♑ Capricorn <small>(Capricorn, goat, zodiac)</small>
♒ Aquarius <small>(Aquarius, bearer, water, zodiac)</small>
♓ Pisces <small>(fish, Pisces, zodiac)</small>
⛎ Ophiuchus <small>(bearer, Ophiuchus, serpent, snake, zodiac)</small>
🔀 shuffle tracks button <small>(arrow, crossed, shuffle tracks button)</small>
🔁 repeat button <small>(arrow, clockwise, repeat, repeat button)</small>
🔂 repeat single button <small>(arrow, clockwise, once, repeat single button)</small>
▶ play button <small>(arrow, play, play button, right, triangle)</small>
⏩ fast-forward button <small>(arrow, double, fast, fast-forward button, forward)</small>
⏭ next track button <small>(arrow, next scene, next track, next track button, triangle)</small>
⏯ play or pause button <small>(arrow, pause, play, play or pause button, right, triangle)</small>
◀ reverse button <small>(arrow, left, reverse, reverse button, triangle)</small>
⏪ fast reverse button <small>(arrow, double, fast reverse button, rewind)</small>
⏮ last track button <small>(arrow, last track button, previous scene, previous track, triangle)</small>
🔼 upwards button <small>(arrow, button, red, upwards button)</small>
⏫ fast up button <small>(arrow, double, fast up button)</small>
🔽 downwards button <small>(arrow, button, down, downwards button, red)</small>
⏬ fast down button <small>(arrow, double, down, fast down button)</small>
⏸ pause button <small>(bar, double, pause, pause button, vertical)</small>
⏹ stop button <small>(square, stop, stop button)</small>
⏺ record button <small>(circle, record, record button)</small>
⏏ eject button <small>(eject, eject button)</small>
🎦 cinema <small>(camera, cinema, film, movie)</small>
🔅 dim button <small>(brightness, dim, dim button, low)</small>
🔆 bright button <small>(bright, bright button, brightness)</small>
📶 antenna bars <small>(antenna, antenna bars, bar, cell, mobile, phone)</small>
📳 vibration mode <small>(cell, mobile, mode, phone, telephone, vibration)</small>
📴 mobile phone off <small>(cell, mobile, off, phone, telephone)</small>
♀ female sign <small>(female sign, woman)</small>
♂ male sign <small>(male sign, man)</small>
⚕ medical symbol <small>(aesculapius, medical symbol, medicine, staff)</small>
♾ infinity <small>(forever, infinity, unbounded, universal)</small>
♻ recycling symbol <small>(recycle, recycling symbol)</small>
⚜ fleur-de-lis <small>(fleur-de-lis)</small>
🔱 trident emblem <small>(anchor, emblem, ship, tool, trident)</small>
📛 name badge <small>(badge, name)</small>
🔰 Japanese symbol for beginner <small>(beginner, chevron, Japanese, Japanese symbol for beginner, leaf)</small>
⭕ hollow red circle <small>(circle, hollow red circle, large, o, red)</small>
✅ check mark button <small>(✓, button, check, mark)</small>
☑ check box with check <small>(✓, box, check, check box with check)</small>
✔ check mark <small>(✓, check, mark)</small>
✖ multiplication sign <small>(×, cancel, multiplication, multiply, sign, x)</small>
❌ cross mark <small>(×, cancel, cross, mark, multiplication, multiply, x)</small>
❎ cross mark button <small>(×, cross mark button, mark, square, x)</small>
➕ plus sign <small>(+, math, plus, sign)</small>
➖ minus sign <small>(-, −, math, minus, sign)</small>
➗ division sign <small>(÷, division, math, sign)</small>
➰ curly loop <small>(curl, curly loop, loop)</small>
➿ double curly loop <small>(curl, double, double curly loop, loop)</small>
〽 part alternation mark <small>(mark, part, part alternation mark)</small>
✳ eight-spoked asterisk <small>(*, asterisk, eight-spoked asterisk)</small>
✴ eight-pointed star <small>(*, eight-pointed star, star)</small>
❇ sparkle <small>(*, sparkle)</small>
‼ double exclamation mark <small>(!, !!, bangbang, double exclamation mark, exclamation, mark)</small>
⁉ exclamation question mark <small>(!, !?, ?, exclamation, interrobang, mark, punctuation, question)</small>
❓ question mark <small>(?, mark, punctuation, question)</small>
❔ white question mark <small>(?, mark, outlined, punctuation, question, white question mark)</small>
❕ white exclamation mark <small>(!, exclamation, mark, outlined, punctuation, white exclamation mark)</small>
❗ exclamation mark <small>(!, exclamation, mark, punctuation)</small>
〰 wavy dash <small>(dash, punctuation, wavy)</small>
© copyright <small>(c, copyright)</small>
® registered <small>(r, registered)</small>
™ trade mark <small>(mark, tm, trade mark, trademark)</small>
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
🔠 input latin uppercase <small>(ABCD, input, latin, letters, uppercase)</small>
🔡 input latin lowercase <small>(abcd, input, latin, letters, lowercase)</small>
🔢 input numbers <small>(1234, input, numbers)</small>
🔣 input symbols <small>(〒♪&%, input, input symbols)</small>
🔤 input latin letters <small>(abc, alphabet, input, latin, letters)</small>
🅰 A button (blood type) <small>(a, A button (blood type), blood type)</small>
🆎 AB button (blood type) <small>(ab, AB button (blood type), blood type)</small>
🅱 B button (blood type) <small>(b, B button (blood type), blood type)</small>
🆑 CL button <small>(cl, CL button)</small>
🆒 COOL button <small>(cool, COOL button)</small>
🆓 FREE button <small>(free, FREE button)</small>
ℹ information <small>(i, information)</small>
🆔 ID button <small>(id, ID button, identity)</small>
Ⓜ circled M <small>(circle, circled M, m)</small>
🆕 NEW button <small>(new, NEW button)</small>
🆖 NG button <small>(ng, NG button)</small>
🅾 O button (blood type) <small>(blood type, o, O button (blood type))</small>
🆗 OK button <small>(OK, OK button)</small>
🅿 P button <small>(P button, parking)</small>
🆘 SOS button <small>(help, sos, SOS button)</small>
🆙 UP! button <small>(mark, up, UP! button)</small>
🆚 VS button <small>(versus, vs, VS button)</small>
🈁 Japanese “here” button <small>(“here”, Japanese, Japanese “here” button, katakana, ココ)</small>
🈂 Japanese “service charge” button <small>(“service charge”, Japanese, Japanese “service charge” button, katakana, サ)</small>
🈷 Japanese “monthly amount” button <small>(“monthly amount”, ideograph, Japanese, Japanese “monthly amount” button, 月)</small>
🈶 Japanese “not free of charge” button <small>(“not free of charge”, ideograph, Japanese, Japanese “not free of charge” button, 有)</small>
🈯 Japanese “reserved” button <small>(“reserved”, ideograph, Japanese, Japanese “reserved” button, 指)</small>
🉐 Japanese “bargain” button <small>(“bargain”, ideograph, Japanese, Japanese “bargain” button, 得)</small>
🈹 Japanese “discount” button <small>(“discount”, ideograph, Japanese, Japanese “discount” button, 割)</small>
🈚 Japanese “free of charge” button <small>(“free of charge”, ideograph, Japanese, Japanese “free of charge” button, 無)</small>
🈲 Japanese “prohibited” button <small>(“prohibited”, ideograph, Japanese, Japanese “prohibited” button, 禁)</small>
🉑 Japanese “acceptable” button <small>(“acceptable”, ideograph, Japanese, Japanese “acceptable” button, 可)</small>
🈸 Japanese “application” button <small>(“application”, ideograph, Japanese, Japanese “application” button, 申)</small>
🈴 Japanese “passing grade” button <small>(“passing grade”, ideograph, Japanese, Japanese “passing grade” button, 合)</small>
🈳 Japanese “vacancy” button <small>(“vacancy”, ideograph, Japanese, Japanese “vacancy” button, 空)</small>
㊗ Japanese “congratulations” button <small>(“congratulations”, ideograph, Japanese, Japanese “congratulations” button, 祝)</small>
㊙ Japanese “secret” button <small>(“secret”, ideograph, Japanese, Japanese “secret” button, 秘)</small>
🈺 Japanese “open for business” button <small>(“open for business”, ideograph, Japanese, Japanese “open for business” button, 営)</small>
🈵 Japanese “no vacancy” button <small>(“no vacancy”, ideograph, Japanese, Japanese “no vacancy” button, 満)</small>
🔴 red circle <small>(circle, geometric, red)</small>
🟠 orange circle <small>(circle, orange)</small>
🟡 yellow circle <small>(circle, yellow)</small>
🟢 green circle <small>(circle, green)</small>
🔵 blue circle <small>(blue, circle, geometric)</small>
🟣 purple circle <small>(circle, purple)</small>
🟤 brown circle <small>(brown, circle)</small>
⚫ black circle <small>(black circle, circle, geometric)</small>
⚪ white circle <small>(circle, geometric, white circle)</small>
🟥 red square <small>(red, square)</small>
🟧 orange square <small>(orange, square)</small>
🟨 yellow square <small>(square, yellow)</small>
🟩 green square <small>(green, square)</small>
🟦 blue square <small>(blue, square)</small>
🟪 purple square <small>(purple, square)</small>
🟫 brown square <small>(brown, square)</small>
⬛ black large square <small>(black large square, geometric, square)</small>
⬜ white large square <small>(geometric, square, white large square)</small>
◼ black medium square <small>(black medium square, geometric, square)</small>
◻ white medium square <small>(geometric, square, white medium square)</small>
◾ black medium-small square <small>(black medium-small square, geometric, square)</small>
◽ white medium-small square <small>(geometric, square, white medium-small square)</small>
▪ black small square <small>(black small square, geometric, square)</small>
▫ white small square <small>(geometric, square, white small square)</small>
🔶 large orange diamond <small>(diamond, geometric, large orange diamond, orange)</small>
🔷 large blue diamond <small>(blue, diamond, geometric, large blue diamond)</small>
🔸 small orange diamond <small>(diamond, geometric, orange, small orange diamond)</small>
🔹 small blue diamond <small>(blue, diamond, geometric, small blue diamond)</small>
🔺 red triangle pointed up <small>(geometric, red, red triangle pointed up)</small>
🔻 red triangle pointed down <small>(down, geometric, red, red triangle pointed down)</small>
💠 diamond with a dot <small>(comic, diamond, diamond with a dot, geometric, inside)</small>
🔘 radio button <small>(button, geometric, radio)</small>
🔳 white square button <small>(button, geometric, outlined, square, white square button)</small>
🔲 black square button <small>(black square button, button, geometric, square)</small>
🏁 chequered flag <small>(checkered, chequered, chequered flag, racing)</small>
🚩 triangular flag <small>(post, triangular flag)</small>
🎌 crossed flags <small>(celebration, cross, crossed, crossed flags, Japanese)</small>
🏴 black flag <small>(black flag, waving)</small>
🏳 white flag <small>(waving, white flag)</small>
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
  space
! exclamation mark
! exclamation mark
# number sign
$ dollar sign
% percent sign
& ampersand
( left parenthesis
) right parenthesis
* asterisk
+ plus sign
, comma
- hyphen-minus
. full stop
/ solidus
0 digit zero
1 digit one
2 digit two
3 digit three
4 digit four
5 digit five
6 digit six
7 digit seven
8 digit eight
9 digit nine
: colon
; semicolon
< less-than sign
= equals sign
> greater-than sign
? question mark
@ commercial at
A latin capital letter a
B latin capital letter b
C latin capital letter c
D latin capital letter d
E latin capital letter e
F latin capital letter f
G latin capital letter g
H latin capital letter h
I latin capital letter i
J latin capital letter j
K latin capital letter k
L latin capital letter l
M latin capital letter m
N latin capital letter n
O latin capital letter o
P latin capital letter p
Q latin capital letter q
R latin capital letter r
S latin capital letter s
T latin capital letter t
U latin capital letter u
V latin capital letter v
W latin capital letter w
X latin capital letter x
Y latin capital letter y
Z latin capital letter z
[ left square bracket
\ reverse solidus
] right square bracket
^ circumflex accent
_ low line
` grave accent
a latin small letter a
b latin small letter b
c latin small letter c
d latin small letter d
e latin small letter e
f latin small letter f
g latin small letter g
h latin small letter h
i latin small letter i
j latin small letter j
k latin small letter k
l latin small letter l
m latin small letter m
n latin small letter n
o latin small letter o
p latin small letter p
q latin small letter q
r latin small letter r
s latin small letter s
t latin small letter t
u latin small letter u
v latin small letter v
w latin small letter w
x latin small letter x
y latin small letter y
z latin small letter z
{ left curly bracket
| vertical line
} right curly bracket
~ tilde
  no-break space
¡ inverted exclamation mark
¢ cent sign
£ pound sign
¤ currency sign
¥ yen sign
¦ broken bar
§ section sign
¨ diaeresis
¬ not sign
¯ macron
° degree sign
± plus-minus sign
² superscript two
³ superscript three
´ acute accent
µ micro sign
¶ pilcrow sign
· middle dot
¹ superscript one
¼ vulgar fraction one quarter
½ vulgar fraction one half
¾ vulgar fraction three quarters
¿ inverted question mark
× multiplication sign
÷ division sign
ı latin small letter dotless i
ȷ latin small letter dotless j
ˆ modifier letter circumflex accent
ˇ caron
˘ breve
˙ dot above
˚ ring above
˜ small tilde
̀ combining grave accent
́ combining acute accent
̂ combining circumflex accent
̃ combining tilde
̄ combining macron
̅ combining overline
̆ combining breve
̇ combining dot above
̈ combining diaeresis
̊ combining ring above
̌ combining caron
̑ combining inverted breve
̣ combining dot below
̬ combining caron below
̭ combining circumflex accent below
̮ combining breve below
̯ combining inverted breve below
̰ combining tilde below
̱ combining macron below
̲ combining low line
̳ combining double low line
̸ combining long solidus overlay
̺ combining inverted bridge below
̿ combining double overline
͆ combining bridge above
Α greek capital letter alpha
Β greek capital letter beta
Γ greek capital letter gamma
Δ greek capital letter delta
Ε greek capital letter epsilon
Ζ greek capital letter zeta
Η greek capital letter eta
Θ greek capital letter theta
Ι greek capital letter iota
Κ greek capital letter kappa
Λ greek capital letter lamda
Μ greek capital letter mu
Ν greek capital letter nu
Ξ greek capital letter xi
Ο greek capital letter omicron
Π greek capital letter pi
Ρ greek capital letter rho
Σ greek capital letter sigma
Τ greek capital letter tau
Φ greek capital letter phi
Χ greek capital letter chi
Ψ greek capital letter psi
Ω greek capital letter omega
α greek small letter alpha
β greek small letter beta
γ greek small letter gamma
δ greek small letter delta
ε greek small letter epsilon
ζ greek small letter zeta
η greek small letter eta
θ greek small letter theta
ι greek small letter iota
κ greek small letter kappa
λ greek small letter lamda
μ greek small letter mu
ν greek small letter nu
ξ greek small letter xi
ο greek small letter omicron
π greek small letter pi
ρ greek small letter rho
σ greek small letter sigma
τ greek small letter tau
υ greek small letter upsilon
φ greek small letter phi
χ greek small letter chi
ψ greek small letter psi
ω greek small letter omega
ϐ greek beta symbol
ϑ greek theta symbol
ϒ greek upsilon with hook symbol
ϕ greek phi symbol
ϖ greek pi symbol
Ϙ greek letter archaic koppa
ϙ greek small letter archaic koppa
Ϛ greek letter stigma
ϛ greek small letter stigma
Ϝ greek letter digamma
ϝ greek small letter digamma
Ϡ greek letter sampi
ϡ greek small letter sampi
ϰ greek kappa symbol
ϱ greek rho symbol
ϴ greek capital theta symbol
ϵ greek lunate epsilon symbol
϶ greek reversed lunate epsilon symbol
Ш cyrillic capital letter sha
؆ arabic-indic cube root
؇ arabic-indic fourth root
؈ arabic ray
  en quad
  em quad
  en space
  em space
  three-per-em space
  four-per-em space
  six-per-em space
  figure space
  thin space
  hair space
​ zero width space
‐ hyphen
‒ figure dash
– en dash
— em dash
‖ double vertical line
† dagger
‡ double dagger
• bullet
… horizontal ellipsis
′ prime
″ double prime
‴ triple prime
‵ reversed prime
‶ reversed double prime
‷ reversed triple prime
※ reference mark
‼ double exclamation mark <small>(!, !!, bangbang, double exclamation mark, exclamation, mark)</small>
⁀ character tie
⁄ fraction slash
⁎ low asterisk
⁏ reversed semicolon
⁐ close up
⁑ two asterisks aligned vertically
⁒ commercial minus sign
⁗ quadruple prime
  medium mathematical space
⁡ function application
⁢ invisible times
⁣ invisible separator
⁤ invisible plus
⁺ superscript plus sign
⁻ superscript minus
⁼ superscript equals sign
⁽ superscript left parenthesis
⁾ superscript right parenthesis
₊ subscript plus sign
₋ subscript minus
₌ subscript equals sign
₍ subscript left parenthesis
₎ subscript right parenthesis
⃐ combining left harpoon above
⃑ combining right harpoon above
⃒ combining long vertical line overlay
⃓ combining short vertical line overlay
⃔ combining anticlockwise arrow above
⃕ combining clockwise arrow above
⃖ combining left arrow above
⃗ combining right arrow above
⃘ combining ring overlay
⃙ combining clockwise ring overlay
⃚ combining anticlockwise ring overlay
⃛ combining three dots above
⃜ combining four dots above
⃝ combining enclosing circle
⃞ combining enclosing square
⃟ combining enclosing diamond
⃡ combining left right arrow above
⃤ combining enclosing upward pointing triangle
⃥ combining reverse solidus overlay
⃦ combining double vertical stroke overlay
⃧ combining annuity symbol
⃨ combining triple underdot
⃩ combining wide bridge above
⃪ combining leftwards arrow overlay
⃫ combining long double solidus overlay
⃬ combining rightwards harpoon with barb downwards
⃭ combining leftwards harpoon with barb downwards
⃮ combining left arrow below
⃯ combining right arrow below
ℂ double-struck capital c
ℇ euler constant
ℊ script small g
ℋ script capital h
ℌ black-letter capital h
ℍ double-struck capital h
ℎ planck constant
ℏ planck constant over two pi
ℐ script capital i
ℑ black-letter capital i
ℒ script capital l
ℓ script small l
ℕ double-struck capital n
℘ script capital p
ℙ double-struck capital p
ℚ double-struck capital q
ℛ script capital r
ℜ black-letter capital r
ℝ double-struck capital r
ℤ double-struck capital z
Ω ohm sign
℧ inverted ohm sign
ℨ black-letter capital z
℩ turned greek small letter iota
Å angstrom sign
ℬ script capital b
ℭ black-letter capital c
ℯ script small e
ℰ script capital e
ℱ script capital f
Ⅎ turned capital f
ℳ script capital m
ℴ script small o
ℵ alef symbol
ℶ bet symbol
ℷ gimel symbol
ℸ dalet symbol
ℼ double-struck small pi
ℽ double-struck small gamma
ℾ double-struck capital gamma
ℿ double-struck capital pi
⅀ double-struck n-ary summation
⅁ turned sans-serif capital g
⅂ turned sans-serif capital l
⅃ reversed sans-serif capital l
⅄ turned sans-serif capital y
ⅅ double-struck italic capital d
ⅆ double-struck italic small d
ⅇ double-struck italic small e
ⅈ double-struck italic small i
ⅉ double-struck italic small j
⅋ turned ampersand
← leftwards arrow
↑ upwards arrow
→ rightwards arrow
↓ downwards arrow
↔ left right arrow <small>(arrow, left-right arrow)</small>
↕ up down arrow <small>(arrow, up-down arrow)</small>
↖ north west arrow <small>(arrow, direction, intercardinal, northwest, up-left arrow)</small>
↗ north east arrow <small>(arrow, direction, intercardinal, northeast, up-right arrow)</small>
↘ south east arrow <small>(arrow, direction, down-right arrow, intercardinal, southeast)</small>
↙ south west arrow <small>(arrow, direction, down-left arrow, intercardinal, southwest)</small>
↚ leftwards arrow with stroke
↛ rightwards arrow with stroke
↜ leftwards wave arrow
↝ rightwards wave arrow
↞ leftwards two headed arrow
↟ upwards two headed arrow
↠ rightwards two headed arrow
↡ downwards two headed arrow
↢ leftwards arrow with tail
↣ rightwards arrow with tail
↤ leftwards arrow from bar
↥ upwards arrow from bar
↦ rightwards arrow from bar
↧ downwards arrow from bar
↨ up down arrow with base
↩ leftwards arrow with hook <small>(arrow, right arrow curving left)</small>
↪ rightwards arrow with hook <small>(arrow, left arrow curving right)</small>
↫ leftwards arrow with loop
↬ rightwards arrow with loop
↭ left right wave arrow
↮ left right arrow with stroke
↯ downwards zigzag arrow
↰ upwards arrow with tip leftwards
↱ upwards arrow with tip rightwards
↲ downwards arrow with tip leftwards
↳ downwards arrow with tip rightwards
↶ anticlockwise top semicircle arrow
↷ clockwise top semicircle arrow
↺ anticlockwise open circle arrow
↻ clockwise open circle arrow
↼ leftwards harpoon with barb upwards
↽ leftwards harpoon with barb downwards
↾ upwards harpoon with barb rightwards
↿ upwards harpoon with barb leftwards
⇀ rightwards harpoon with barb upwards
⇁ rightwards harpoon with barb downwards
⇂ downwards harpoon with barb rightwards
⇃ downwards harpoon with barb leftwards
⇄ rightwards arrow over leftwards arrow
⇅ upwards arrow leftwards of downwards arrow
⇆ leftwards arrow over rightwards arrow
⇇ leftwards paired arrows
⇈ upwards paired arrows
⇉ rightwards paired arrows
⇊ downwards paired arrows
⇋ leftwards harpoon over rightwards harpoon
⇌ rightwards harpoon over leftwards harpoon
⇍ leftwards double arrow with stroke
⇎ left right double arrow with stroke
⇏ rightwards double arrow with stroke
⇐ leftwards double arrow
⇑ upwards double arrow
⇒ rightwards double arrow
⇓ downwards double arrow
⇔ left right double arrow
⇕ up down double arrow
⇖ north west double arrow
⇗ north east double arrow
⇘ south east double arrow
⇙ south west double arrow
⇚ leftwards triple arrow
⇛ rightwards triple arrow
⇜ leftwards squiggle arrow
⇝ rightwards squiggle arrow
⇞ upwards arrow with double stroke
⇟ downwards arrow with double stroke
⇠ leftwards dashed arrow
⇡ upwards dashed arrow
⇢ rightwards dashed arrow
⇣ downwards dashed arrow
⇤ leftwards arrow to bar
⇥ rightwards arrow to bar
⇦ leftwards white arrow
⇧ upwards white arrow
⇨ rightwards white arrow
⇩ downwards white arrow
⇪ upwards white arrow from bar
⇫ upwards white arrow on pedestal
⇬ upwards white arrow on pedestal with horizontal bar
⇭ upwards white arrow on pedestal with vertical bar
⇮ upwards white double arrow
⇯ upwards white double arrow on pedestal
⇰ rightwards white arrow from wall
⇱ north west arrow to corner
⇲ south east arrow to corner
⇳ up down white arrow
⇴ right arrow with small circle
⇵ downwards arrow leftwards of upwards arrow
⇶ three rightwards arrows
⇷ leftwards arrow with vertical stroke
⇸ rightwards arrow with vertical stroke
⇹ left right arrow with vertical stroke
⇺ leftwards arrow with double vertical stroke
⇻ rightwards arrow with double vertical stroke
⇼ left right arrow with double vertical stroke
⇽ leftwards open-headed arrow
⇾ rightwards open-headed arrow
⇿ left right open-headed arrow
∀ for all
∁ complement
∂ partial differential
∃ there exists
∄ there does not exist
∅ empty set
∆ increment
∇ nabla
∈ element of
∉ not an element of
∊ small element of
∋ contains as member
∌ does not contain as member
∍ small contains as member
∎ end of proof
∏ n-ary product
∐ n-ary coproduct
∑ n-ary summation
− minus sign
∓ minus-or-plus sign
∔ dot plus
∕ division slash
∖ set minus
∗ asterisk operator
∘ ring operator
∙ bullet operator
√ square root
∛ cube root
∜ fourth root
∝ proportional to
∞ infinity
∟ right angle
∠ angle
∡ measured angle
∢ spherical angle
∣ divides
∤ does not divide
∥ parallel to
∦ not parallel to
∧ logical and
∨ logical or
∩ intersection
∪ union
∫ integral
∬ double integral
∭ triple integral
∮ contour integral
∯ surface integral
∰ volume integral
∱ clockwise integral
∲ clockwise contour integral
∳ anticlockwise contour integral
∴ therefore
∵ because
∶ ratio
∷ proportion
∸ dot minus
∹ excess
∺ geometric proportion
∻ homothetic
∼ tilde operator
∽ reversed tilde
∾ inverted lazy s
∿ sine wave
≀ wreath product
≁ not tilde
≂ minus tilde
≃ asymptotically equal to
≄ not asymptotically equal to
≅ approximately equal to
≆ approximately but not actually equal to
≇ neither approximately nor actually equal to
≈ almost equal to
≉ not almost equal to
≊ almost equal or equal to
≋ triple tilde
≌ all equal to
≍ equivalent to
≎ geometrically equivalent to
≏ difference between
≐ approaches the limit
≑ geometrically equal to
≒ approximately equal to or the image of
≓ image of or approximately equal to
≔ colon equals
≕ equals colon
≖ ring in equal to
≗ ring equal to
≘ corresponds to
≙ estimates
≚ equiangular to
≛ star equals
≜ delta equal to
≝ equal to by definition
≞ measured by
≟ questioned equal to
≠ not equal to
≡ identical to
≢ not identical to
≣ strictly equivalent to
≤ less-than or equal to
≥ greater-than or equal to
≦ less-than over equal to
≧ greater-than over equal to
≨ less-than but not equal to
≩ greater-than but not equal to
≪ much less-than
≫ much greater-than
≬ between
≭ not equivalent to
≮ not less-than
≯ not greater-than
≰ neither less-than nor equal to
≱ neither greater-than nor equal to
≲ less-than or equivalent to
≳ greater-than or equivalent to
≴ neither less-than nor equivalent to
≵ neither greater-than nor equivalent to
≶ less-than or greater-than
≷ greater-than or less-than
≸ neither less-than nor greater-than
≹ neither greater-than nor less-than
≺ precedes
≻ succeeds
≼ precedes or equal to
≽ succeeds or equal to
≾ precedes or equivalent to
≿ succeeds or equivalent to
⊀ does not precede
⊁ does not succeed
⊂ subset of
⊃ superset of
⊄ not a subset of
⊅ not a superset of
⊆ subset of or equal to
⊇ superset of or equal to
⊈ neither a subset of nor equal to
⊉ neither a superset of nor equal to
⊊ subset of with not equal to
⊋ superset of with not equal to
⊌ multiset
⊍ multiset multiplication
⊎ multiset union
⊏ square image of
⊐ square original of
⊑ square image of or equal to
⊒ square original of or equal to
⊓ square cap
⊔ square cup
⊕ circled plus
⊖ circled minus
⊗ circled times
⊘ circled division slash
⊙ circled dot operator
⊚ circled ring operator
⊛ circled asterisk operator
⊜ circled equals
⊝ circled dash
⊞ squared plus
⊟ squared minus
⊠ squared times
⊡ squared dot operator
⊢ right tack
⊣ left tack
⊤ down tack
⊥ up tack
⊦ assertion
⊧ models
⊨ true
⊩ forces
⊪ triple vertical bar right turnstile
⊫ double vertical bar double right turnstile
⊬ does not prove
⊭ not true
⊮ does not force
⊯ negated double vertical bar double right turnstile
⊰ precedes under relation
⊱ succeeds under relation
⊲ normal subgroup of
⊳ contains as normal subgroup
⊴ normal subgroup of or equal to
⊵ contains as normal subgroup or equal to
⊶ original of
⊷ image of
⊸ multimap
⊹ hermitian conjugate matrix
⊺ intercalate
⊻ xor
⊼ nand
⊽ nor
⊾ right angle with arc
⊿ right triangle
⋀ n-ary logical and
⋁ n-ary logical or
⋂ n-ary intersection
⋃ n-ary union
⋄ diamond operator
⋅ dot operator
⋆ star operator
⋇ division times
⋈ bowtie
⋉ left normal factor semidirect product
⋊ right normal factor semidirect product
⋋ left semidirect product
⋌ right semidirect product
⋍ reversed tilde equals
⋎ curly logical or
⋏ curly logical and
⋐ double subset
⋑ double superset
⋒ double intersection
⋓ double union
⋔ pitchfork
⋕ equal and parallel to
⋖ less-than with dot
⋗ greater-than with dot
⋘ very much less-than
⋙ very much greater-than
⋚ less-than equal to or greater-than
⋛ greater-than equal to or less-than
⋜ equal to or less-than
⋝ equal to or greater-than
⋞ equal to or precedes
⋟ equal to or succeeds
⋠ does not precede or equal
⋡ does not succeed or equal
⋢ not square image of or equal to
⋣ not square original of or equal to
⋤ square image of or not equal to
⋥ square original of or not equal to
⋦ less-than but not equivalent to
⋧ greater-than but not equivalent to
⋨ precedes but not equivalent to
⋩ succeeds but not equivalent to
⋪ not normal subgroup of
⋫ does not contain as normal subgroup
⋬ not normal subgroup of or equal to
⋭ does not contain as normal subgroup or equal
⋮ vertical ellipsis
⋯ midline horizontal ellipsis
⋰ up right diagonal ellipsis
⋱ down right diagonal ellipsis
⋲ element of with long horizontal stroke
⋳ element of with vertical bar at end of horizontal stroke
⋴ small element of with vertical bar at end of horizontal stroke
⋵ element of with dot above
⋶ element of with overbar
⋷ small element of with overbar
⋸ element of with underbar
⋹ element of with two horizontal strokes
⋺ contains with long horizontal stroke
⋻ contains with vertical bar at end of horizontal stroke
⋼ small contains with vertical bar at end of horizontal stroke
⋽ contains with overbar
⋾ small contains with overbar
⋿ z notation bag membership
⌀ diameter sign
⌂ house
⌅ projective
⌆ perspective
⌈ left ceiling
⌉ right ceiling
⌊ left floor
⌋ right floor
⌐ reversed not sign
⌑ square lozenge
⌙ turned not sign
⌜ top left corner
⌝ top right corner
⌞ bottom left corner
⌟ bottom right corner
⌠ top half integral
⌡ bottom half integral
⌢ frown
⌣ smile
⌶ apl functional symbol i-beam
⌽ apl functional symbol circle stile
⌿ apl functional symbol slash bar
⍼ right angle with downwards zigzag arrow
⎔ software-function symbol
⎛ left parenthesis upper hook
⎜ left parenthesis extension
⎝ left parenthesis lower hook
⎞ right parenthesis upper hook
⎟ right parenthesis extension
⎠ right parenthesis lower hook
⎡ left square bracket upper corner
⎢ left square bracket extension
⎣ left square bracket lower corner
⎤ right square bracket upper corner
⎥ right square bracket extension
⎦ right square bracket lower corner
⎧ left curly bracket upper hook
⎨ left curly bracket middle piece
⎩ left curly bracket lower hook
⎪ curly bracket extension
⎫ right curly bracket upper hook
⎬ right curly bracket middle piece
⎭ right curly bracket lower hook
⎮ integral extension
⎯ horizontal line extension
⎰ upper left or lower right curly bracket section
⎱ upper right or lower left curly bracket section
⎲ summation top
⎳ summation bottom
⎴ top square bracket
⎵ bottom square bracket
⎶ bottom square bracket over top square bracket
⎷ radical symbol bottom
⏐ vertical line extension
⏜ top parenthesis
⏝ bottom parenthesis
⏞ top curly bracket
⏟ bottom curly bracket
⏠ top tortoise shell bracket
⏡ bottom tortoise shell bracket
⏢ white trapezium
⏣ benzene ring with circle
⏤ straightness
⏥ flatness
⏦ ac current
⏧ electrical intersection
Ⓢ circled latin capital letter s
■ black square
□ white square
▪ black small square <small>(black small square, geometric, square)</small>
▫ white small square <small>(geometric, square, white small square)</small>
▭ white rectangle
▮ black vertical rectangle
▯ white vertical rectangle
▰ black parallelogram
▱ white parallelogram
▲ black up-pointing triangle
△ white up-pointing triangle
▴ black up-pointing small triangle
▵ white up-pointing small triangle
▶ black right-pointing triangle <small>(arrow, play, play button, right, triangle)</small>
▷ white right-pointing triangle
▸ black right-pointing small triangle
▹ white right-pointing small triangle
▼ black down-pointing triangle
▽ white down-pointing triangle
▾ black down-pointing small triangle
▿ white down-pointing small triangle
◀ black left-pointing triangle <small>(arrow, left, reverse, reverse button, triangle)</small>
◁ white left-pointing triangle
◂ black left-pointing small triangle
◃ white left-pointing small triangle
◄ black left-pointing pointer
◅ white left-pointing pointer
◆ black diamond
◇ white diamond
◈ white diamond containing black small diamond
◉ fisheye
◊ lozenge
○ white circle
◎ bullseye
● black circle
◐ circle with left half black
◑ circle with right half black
◒ circle with lower half black
◓ circle with upper half black
◖ left half black circle
◗ right half black circle
◢ black lower right triangle
◣ black lower left triangle
◤ black upper left triangle
◥ black upper right triangle
◦ white bullet
◧ square with left half black
◨ square with right half black
◩ square with upper left diagonal half black
◪ square with lower right diagonal half black
◫ white square with vertical bisecting line
◬ white up-pointing triangle with dot
◯ large circle
◸ upper left triangle
◹ upper right triangle
◺ lower left triangle
◻ white medium square <small>(geometric, square, white medium square)</small>
◼ black medium square <small>(black medium square, geometric, square)</small>
◽ white medium small square <small>(geometric, square, white medium-small square)</small>
◾ black medium small square <small>(black medium-small square, geometric, square)</small>
◿ lower right triangle
★ black star
☆ white star
☉ sun
☌ conjunction
☽ first quarter moon
☾ last quarter moon
☿ mercury
♀ female sign <small>(female sign, woman)</small>
♁ earth
♂ male sign <small>(male sign, man)</small>
♃ jupiter
♄ saturn
♆ neptune
♇ pluto
♈ aries <small>(Aries, ram, zodiac)</small>
♉ taurus <small>(bull, ox, Taurus, zodiac)</small>
♠ black spade suit <small>(card, game, spade suit)</small>
♡ white heart suit
♢ white diamond suit
♣ black club suit <small>(card, club suit, game)</small>
♤ white spade suit
♥ black heart suit <small>(card, game, heart suit)</small>
♦ black diamond suit <small>(card, diamond suit, game)</small>
♧ white club suit
♩ quarter note
♭ music flat sign
♮ music natural sign
♯ music sharp sign
⚀ die face-1
⚁ die face-2
⚂ die face-3
⚃ die face-4
⚄ die face-5
⚅ die face-6
⚆ white circle with dot right
⚇ white circle with two dots
⚈ black circle with white dot right
⚉ black circle with two white dots
⚪ medium white circle <small>(circle, geometric, white circle)</small>
⚫ medium black circle <small>(black circle, circle, geometric)</small>
⚬ medium small white circle
⚲ neuter
✓ check mark
✗ ballot x
✠ maltese cross
✪ circled white star
✶ six pointed black star
❲ light left tortoise shell bracket ornament
❳ light right tortoise shell bracket ornament
⟀ three dimensional angle
⟁ white triangle containing small white triangle
⟂ perpendicular
⟃ open subset
⟄ open superset
⟅ left s-shaped bag delimiter
⟆ right s-shaped bag delimiter
⟇ or with dot inside
⟈ reverse solidus preceding subset
⟉ superset preceding solidus
⟊ vertical bar with horizontal stroke
⟋ mathematical rising diagonal
⟌ long division
⟍ mathematical falling diagonal
⟎ squared logical and
⟏ squared logical or
⟐ white diamond with centred dot
⟑ and with dot
⟒ element of opening upwards
⟓ lower right corner with dot
⟔ upper left corner with dot
⟕ left outer join
⟖ right outer join
⟗ full outer join
⟘ large up tack
⟙ large down tack
⟚ left and right double turnstile
⟛ left and right tack
⟜ left multimap
⟝ long right tack
⟞ long left tack
⟟ up tack with circle above
⟠ lozenge divided by horizontal rule
⟡ white concave-sided diamond
⟢ white concave-sided diamond with leftwards tick
⟣ white concave-sided diamond with rightwards tick
⟤ white square with leftwards tick
⟥ white square with rightwards tick
⟦ mathematical left white square bracket
⟧ mathematical right white square bracket
⟨ mathematical left angle bracket
⟩ mathematical right angle bracket
⟪ mathematical left double angle bracket
⟫ mathematical right double angle bracket
⟬ mathematical left white tortoise shell bracket
⟭ mathematical right white tortoise shell bracket
⟮ mathematical left flattened parenthesis
⟯ mathematical right flattened parenthesis
⟰ upwards quadruple arrow
⟱ downwards quadruple arrow
⟲ anticlockwise gapped circle arrow
⟳ clockwise gapped circle arrow
⟴ right arrow with circled plus
⟵ long leftwards arrow
⟶ long rightwards arrow
⟷ long left right arrow
⟸ long leftwards double arrow
⟹ long rightwards double arrow
⟺ long left right double arrow
⟻ long leftwards arrow from bar
⟼ long rightwards arrow from bar
⟽ long leftwards double arrow from bar
⟾ long rightwards double arrow from bar
⟿ long rightwards squiggle arrow
⤀ rightwards two-headed arrow with vertical stroke
⤁ rightwards two-headed arrow with double vertical stroke
⤂ leftwards double arrow with vertical stroke
⤃ rightwards double arrow with vertical stroke
⤄ left right double arrow with vertical stroke
⤅ rightwards two-headed arrow from bar
⤆ leftwards double arrow from bar
⤇ rightwards double arrow from bar
⤈ downwards arrow with horizontal stroke
⤉ upwards arrow with horizontal stroke
⤊ upwards triple arrow
⤋ downwards triple arrow
⤌ leftwards double dash arrow
⤍ rightwards double dash arrow
⤎ leftwards triple dash arrow
⤏ rightwards triple dash arrow
⤐ rightwards two-headed triple dash arrow
⤑ rightwards arrow with dotted stem
⤒ upwards arrow to bar
⤓ downwards arrow to bar
⤔ rightwards arrow with tail with vertical stroke
⤕ rightwards arrow with tail with double vertical stroke
⤖ rightwards two-headed arrow with tail
⤗ rightwards two-headed arrow with tail with vertical stroke
⤘ rightwards two-headed arrow with tail with double vertical stroke
⤙ leftwards arrow-tail
⤚ rightwards arrow-tail
⤛ leftwards double arrow-tail
⤜ rightwards double arrow-tail
⤝ leftwards arrow to black diamond
⤞ rightwards arrow to black diamond
⤟ leftwards arrow from bar to black diamond
⤠ rightwards arrow from bar to black diamond
⤡ north west and south east arrow
⤢ north east and south west arrow
⤣ north west arrow with hook
⤤ north east arrow with hook
⤥ south east arrow with hook
⤦ south west arrow with hook
⤧ north west arrow and north east arrow
⤨ north east arrow and south east arrow
⤩ south east arrow and south west arrow
⤪ south west arrow and north west arrow
⤫ rising diagonal crossing falling diagonal
⤬ falling diagonal crossing rising diagonal
⤭ south east arrow crossing north east arrow
⤮ north east arrow crossing south east arrow
⤯ falling diagonal crossing north east arrow
⤰ rising diagonal crossing south east arrow
⤱ north east arrow crossing north west arrow
⤲ north west arrow crossing north east arrow
⤳ wave arrow pointing directly right
⤴ arrow pointing rightwards then curving upwards <small>(arrow, right arrow curving up)</small>
⤵ arrow pointing rightwards then curving downwards <small>(arrow, down, right arrow curving down)</small>
⤶ arrow pointing downwards then curving leftwards
⤷ arrow pointing downwards then curving rightwards
⤸ right-side arc clockwise arrow
⤹ left-side arc anticlockwise arrow
⤺ top arc anticlockwise arrow
⤻ bottom arc anticlockwise arrow
⤼ top arc clockwise arrow with minus
⤽ top arc anticlockwise arrow with plus
⤾ lower right semicircular clockwise arrow
⤿ lower left semicircular anticlockwise arrow
⥀ anticlockwise closed circle arrow
⥁ clockwise closed circle arrow
⥂ rightwards arrow above short leftwards arrow
⥃ leftwards arrow above short rightwards arrow
⥄ short rightwards arrow above leftwards arrow
⥅ rightwards arrow with plus below
⥆ leftwards arrow with plus below
⥇ rightwards arrow through x
⥈ left right arrow through small circle
⥉ upwards two-headed arrow from small circle
⥊ left barb up right barb down harpoon
⥋ left barb down right barb up harpoon
⥌ up barb right down barb left harpoon
⥍ up barb left down barb right harpoon
⥎ left barb up right barb up harpoon
⥏ up barb right down barb right harpoon
⥐ left barb down right barb down harpoon
⥑ up barb left down barb left harpoon
⥒ leftwards harpoon with barb up to bar
⥓ rightwards harpoon with barb up to bar
⥔ upwards harpoon with barb right to bar
⥕ downwards harpoon with barb right to bar
⥖ leftwards harpoon with barb down to bar
⥗ rightwards harpoon with barb down to bar
⥘ upwards harpoon with barb left to bar
⥙ downwards harpoon with barb left to bar
⥚ leftwards harpoon with barb up from bar
⥛ rightwards harpoon with barb up from bar
⥜ upwards harpoon with barb right from bar
⥝ downwards harpoon with barb right from bar
⥞ leftwards harpoon with barb down from bar
⥟ rightwards harpoon with barb down from bar
⥠ upwards harpoon with barb left from bar
⥡ downwards harpoon with barb left from bar
⥢ leftwards harpoon with barb up above leftwards harpoon with barb down
⥣ upwards harpoon with barb left beside upwards harpoon with barb right
⥤ rightwards harpoon with barb up above rightwards harpoon with barb down
⥥ downwards harpoon with barb left beside downwards harpoon with barb right
⥦ leftwards harpoon with barb up above rightwards harpoon with barb up
⥧ leftwards harpoon with barb down above rightwards harpoon with barb down
⥨ rightwards harpoon with barb up above leftwards harpoon with barb up
⥩ rightwards harpoon with barb down above leftwards harpoon with barb down
⥪ leftwards harpoon with barb up above long dash
⥫ leftwards harpoon with barb down below long dash
⥬ rightwards harpoon with barb up above long dash
⥭ rightwards harpoon with barb down below long dash
⥮ upwards harpoon with barb left beside downwards harpoon with barb right
⥯ downwards harpoon with barb left beside upwards harpoon with barb right
⥰ right double arrow with rounded head
⥱ equals sign above rightwards arrow
⥲ tilde operator above rightwards arrow
⥳ leftwards arrow above tilde operator
⥴ rightwards arrow above tilde operator
⥵ rightwards arrow above almost equal to
⥶ less-than above leftwards arrow
⥷ leftwards arrow through less-than
⥸ greater-than above rightwards arrow
⥹ subset above rightwards arrow
⥺ leftwards arrow through subset
⥻ superset above leftwards arrow
⥼ left fish tail
⥽ right fish tail
⥾ up fish tail
⥿ down fish tail
⦀ triple vertical bar delimiter
⦁ z notation spot
⦂ z notation type colon
⦃ left white curly bracket
⦄ right white curly bracket
⦅ left white parenthesis
⦆ right white parenthesis
⦇ z notation left image bracket
⦈ z notation right image bracket
⦉ z notation left binding bracket
⦊ z notation right binding bracket
⦋ left square bracket with underbar
⦌ right square bracket with underbar
⦍ left square bracket with tick in top corner
⦎ right square bracket with tick in bottom corner
⦏ left square bracket with tick in bottom corner
⦐ right square bracket with tick in top corner
⦑ left angle bracket with dot
⦒ right angle bracket with dot
⦓ left arc less-than bracket
⦔ right arc greater-than bracket
⦕ double left arc greater-than bracket
⦖ double right arc less-than bracket
⦗ left black tortoise shell bracket
⦘ right black tortoise shell bracket
⦙ dotted fence
⦚ vertical zigzag line
⦛ measured angle opening left
⦜ right angle variant with square
⦝ measured right angle with dot
⦞ angle with s inside
⦟ acute angle
⦠ spherical angle opening left
⦡ spherical angle opening up
⦢ turned angle
⦣ reversed angle
⦤ angle with underbar
⦥ reversed angle with underbar
⦦ oblique angle opening up
⦧ oblique angle opening down
⦨ measured angle with open arm ending in arrow pointing up and right
⦩ measured angle with open arm ending in arrow pointing up and left
⦪ measured angle with open arm ending in arrow pointing down and right
⦫ measured angle with open arm ending in arrow pointing down and left
⦬ measured angle with open arm ending in arrow pointing right and up
⦭ measured angle with open arm ending in arrow pointing left and up
⦮ measured angle with open arm ending in arrow pointing right and down
⦯ measured angle with open arm ending in arrow pointing left and down
⦰ reversed empty set
⦱ empty set with overbar
⦲ empty set with small circle above
⦳ empty set with right arrow above
⦴ empty set with left arrow above
⦵ circle with horizontal bar
⦶ circled vertical bar
⦷ circled parallel
⦸ circled reverse solidus
⦹ circled perpendicular
⦺ circle divided by horizontal bar and top half divided by vertical bar
⦻ circle with superimposed x
⦼ circled anticlockwise-rotated division sign
⦽ up arrow through circle
⦾ circled white bullet
⦿ circled bullet
⧀ circled less-than
⧁ circled greater-than
⧂ circle with small circle to the right
⧃ circle with two horizontal strokes to the right
⧄ squared rising diagonal slash
⧅ squared falling diagonal slash
⧆ squared asterisk
⧇ squared small circle
⧈ squared square
⧉ two joined squares
⧊ triangle with dot above
⧋ triangle with underbar
⧌ s in triangle
⧍ triangle with serifs at bottom
⧎ right triangle above left triangle
⧏ left triangle beside vertical bar
⧐ vertical bar beside right triangle
⧑ bowtie with left half black
⧒ bowtie with right half black
⧓ black bowtie
⧔ times with left half black
⧕ times with right half black
⧖ white hourglass
⧗ black hourglass
⧘ left wiggly fence
⧙ right wiggly fence
⧚ left double wiggly fence
⧛ right double wiggly fence
⧜ incomplete infinity
⧝ tie over infinity
⧞ infinity negated with vertical bar
⧟ double-ended multimap
⧠ square with contoured outline
⧡ increases as
⧢ shuffle product
⧣ equals sign and slanted parallel
⧤ equals sign and slanted parallel with tilde above
⧥ identical to and slanted parallel
⧦ gleich stark
⧧ thermodynamic
⧨ down-pointing triangle with left half black
⧩ down-pointing triangle with right half black
⧪ black diamond with down arrow
⧫ black lozenge
⧬ white circle with down arrow
⧭ black circle with down arrow
⧮ error-barred white square
⧯ error-barred black square
⧰ error-barred white diamond
⧱ error-barred black diamond
⧲ error-barred white circle
⧳ error-barred black circle
⧴ rule-delayed
⧵ reverse solidus operator
⧶ solidus with overbar
⧷ reverse solidus with horizontal stroke
⧸ big solidus
⧹ big reverse solidus
⧺ double plus
⧻ triple plus
⧼ left-pointing curved angle bracket
⧽ right-pointing curved angle bracket
⧾ tiny
⧿ miny
⨀ n-ary circled dot operator
⨁ n-ary circled plus operator
⨂ n-ary circled times operator
⨃ n-ary union operator with dot
⨄ n-ary union operator with plus
⨅ n-ary square intersection operator
⨆ n-ary square union operator
⨇ two logical and operator
⨈ two logical or operator
⨉ n-ary times operator
⨊ modulo two sum
⨋ summation with integral
⨌ quadruple integral operator
⨍ finite part integral
⨎ integral with double stroke
⨏ integral average with slash
⨐ circulation function
⨑ anticlockwise integration
⨒ line integration with rectangular path around pole
⨓ line integration with semicircular path around pole
⨔ line integration not including the pole
⨕ integral around a point operator
⨖ quaternion integral operator
⨗ integral with leftwards arrow with hook
⨘ integral with times sign
⨙ integral with intersection
⨚ integral with union
⨛ integral with overbar
⨜ integral with underbar
⨝ join
⨞ large left triangle operator
⨟ z notation schema composition
⨠ z notation schema piping
⨡ z notation schema projection
⨢ plus sign with small circle above
⨣ plus sign with circumflex accent above
⨤ plus sign with tilde above
⨥ plus sign with dot below
⨦ plus sign with tilde below
⨧ plus sign with subscript two
⨨ plus sign with black triangle
⨩ minus sign with comma above
⨪ minus sign with dot below
⨫ minus sign with falling dots
⨬ minus sign with rising dots
⨭ plus sign in left half circle
⨮ plus sign in right half circle
⨯ vector or cross product
⨰ multiplication sign with dot above
⨱ multiplication sign with underbar
⨲ semidirect product with bottom closed
⨳ smash product
⨴ multiplication sign in left half circle
⨵ multiplication sign in right half circle
⨶ circled multiplication sign with circumflex accent
⨷ multiplication sign in double circle
⨸ circled division sign
⨹ plus sign in triangle
⨺ minus sign in triangle
⨻ multiplication sign in triangle
⨼ interior product
⨽ righthand interior product
⨾ z notation relational composition
⨿ amalgamation or coproduct
⩀ intersection with dot
⩁ union with minus sign
⩂ union with overbar
⩃ intersection with overbar
⩄ intersection with logical and
⩅ union with logical or
⩆ union above intersection
⩇ intersection above union
⩈ union above bar above intersection
⩉ intersection above bar above union
⩊ union beside and joined with union
⩋ intersection beside and joined with intersection
⩌ closed union with serifs
⩍ closed intersection with serifs
⩎ double square intersection
⩏ double square union
⩐ closed union with serifs and smash product
⩑ logical and with dot above
⩒ logical or with dot above
⩓ double logical and
⩔ double logical or
⩕ two intersecting logical and
⩖ two intersecting logical or
⩗ sloping large or
⩘ sloping large and
⩙ logical or overlapping logical and
⩚ logical and with middle stem
⩛ logical or with middle stem
⩜ logical and with horizontal dash
⩝ logical or with horizontal dash
⩞ logical and with double overbar
⩟ logical and with underbar
⩠ logical and with double underbar
⩡ small vee with underbar
⩢ logical or with double overbar
⩣ logical or with double underbar
⩤ z notation domain antirestriction
⩥ z notation range antirestriction
⩦ equals sign with dot below
⩧ identical with dot above
⩨ triple horizontal bar with double vertical stroke
⩩ triple horizontal bar with triple vertical stroke
⩪ tilde operator with dot above
⩫ tilde operator with rising dots
⩬ similar minus similar
⩭ congruent with dot above
⩮ equals with asterisk
⩯ almost equal to with circumflex accent
⩰ approximately equal or equal to
⩱ equals sign above plus sign
⩲ plus sign above equals sign
⩳ equals sign above tilde operator
⩴ double colon equal
⩵ two consecutive equals signs
⩶ three consecutive equals signs
⩷ equals sign with two dots above and two dots below
⩸ equivalent with four dots above
⩹ less-than with circle inside
⩺ greater-than with circle inside
⩻ less-than with question mark above
⩼ greater-than with question mark above
⩽ less-than or slanted equal to
⩾ greater-than or slanted equal to
⩿ less-than or slanted equal to with dot inside
⪀ greater-than or slanted equal to with dot inside
⪁ less-than or slanted equal to with dot above
⪂ greater-than or slanted equal to with dot above
⪃ less-than or slanted equal to with dot above right
⪄ greater-than or slanted equal to with dot above left
⪅ less-than or approximate
⪆ greater-than or approximate
⪇ less-than and single-line not equal to
⪈ greater-than and single-line not equal to
⪉ less-than and not approximate
⪊ greater-than and not approximate
⪋ less-than above double-line equal above greater-than
⪌ greater-than above double-line equal above less-than
⪍ less-than above similar or equal
⪎ greater-than above similar or equal
⪏ less-than above similar above greater-than
⪐ greater-than above similar above less-than
⪑ less-than above greater-than above double-line equal
⪒ greater-than above less-than above double-line equal
⪓ less-than above slanted equal above greater-than above slanted equal
⪔ greater-than above slanted equal above less-than above slanted equal
⪕ slanted equal to or less-than
⪖ slanted equal to or greater-than
⪗ slanted equal to or less-than with dot inside
⪘ slanted equal to or greater-than with dot inside
⪙ double-line equal to or less-than
⪚ double-line equal to or greater-than
⪛ double-line slanted equal to or less-than
⪜ double-line slanted equal to or greater-than
⪝ similar or less-than
⪞ similar or greater-than
⪟ similar above less-than above equals sign
⪠ similar above greater-than above equals sign
⪡ double nested less-than
⪢ double nested greater-than
⪣ double nested less-than with underbar
⪤ greater-than overlapping less-than
⪥ greater-than beside less-than
⪦ less-than closed by curve
⪧ greater-than closed by curve
⪨ less-than closed by curve above slanted equal
⪩ greater-than closed by curve above slanted equal
⪪ smaller than
⪫ larger than
⪬ smaller than or equal to
⪭ larger than or equal to
⪮ equals sign with bumpy above
⪯ precedes above single-line equals sign
⪰ succeeds above single-line equals sign
⪱ precedes above single-line not equal to
⪲ succeeds above single-line not equal to
⪳ precedes above equals sign
⪴ succeeds above equals sign
⪵ precedes above not equal to
⪶ succeeds above not equal to
⪷ precedes above almost equal to
⪸ succeeds above almost equal to
⪹ precedes above not almost equal to
⪺ succeeds above not almost equal to
⪻ double precedes
⪼ double succeeds
⪽ subset with dot
⪾ superset with dot
⪿ subset with plus sign below
⫀ superset with plus sign below
⫁ subset with multiplication sign below
⫂ superset with multiplication sign below
⫃ subset of or equal to with dot above
⫄ superset of or equal to with dot above
⫅ subset of above equals sign
⫆ superset of above equals sign
⫇ subset of above tilde operator
⫈ superset of above tilde operator
⫉ subset of above almost equal to
⫊ superset of above almost equal to
⫋ subset of above not equal to
⫌ superset of above not equal to
⫍ square left open box operator
⫎ square right open box operator
⫏ closed subset
⫐ closed superset
⫑ closed subset or equal to
⫒ closed superset or equal to
⫓ subset above superset
⫔ superset above subset
⫕ subset above subset
⫖ superset above superset
⫗ superset beside subset
⫘ superset beside and joined by dash with subset
⫙ element of opening downwards
⫚ pitchfork with tee top
⫛ transversal intersection
⫝̸ forking
⫝ nonforking
⫞ short left tack
⫟ short down tack
⫠ short up tack
⫡ perpendicular with s
⫢ vertical bar triple right turnstile
⫣ double vertical bar left turnstile
⫤ vertical bar double left turnstile
⫥ double vertical bar double left turnstile
⫦ long dash from left member of double vertical
⫧ short down tack with overbar
⫨ short up tack with underbar
⫩ short up tack above short down tack
⫪ double down tack
⫫ double up tack
⫬ double stroke not sign
⫭ reversed double stroke not sign
⫮ does not divide with reversed negation slash
⫯ vertical line with circle above
⫰ vertical line with circle below
⫱ down tack with circle below
⫲ parallel with horizontal stroke
⫳ parallel with tilde operator
⫴ triple vertical bar binary relation
⫵ triple vertical bar with horizontal stroke
⫶ triple colon operator
⫷ triple nested less-than
⫸ triple nested greater-than
⫹ double-line slanted less-than or equal to
⫺ double-line slanted greater-than or equal to
⫻ triple solidus binary relation
⫼ large triple vertical bar operator
⫽ double solidus operator
⫾ white vertical bar
⫿ n-ary white vertical bar
⬀ north east white arrow
⬁ north west white arrow
⬂ south east white arrow
⬃ south west white arrow
⬄ left right white arrow
⬅ leftwards black arrow <small>(arrow, cardinal, direction, left arrow, west)</small>
⬆ upwards black arrow <small>(arrow, cardinal, direction, north, up arrow)</small>
⬇ downwards black arrow <small>(arrow, cardinal, direction, down, south)</small>
⬈ north east black arrow
⬉ north west black arrow
⬊ south east black arrow
⬋ south west black arrow
⬌ left right black arrow
⬍ up down black arrow
⬎ rightwards arrow with tip downwards
⬏ rightwards arrow with tip upwards
⬐ leftwards arrow with tip downwards
⬑ leftwards arrow with tip upwards
⬒ square with top half black
⬓ square with bottom half black
⬔ square with upper right diagonal half black
⬕ square with lower left diagonal half black
⬖ diamond with left half black
⬗ diamond with right half black
⬘ diamond with top half black
⬙ diamond with bottom half black
⬛ black large square <small>(black large square, geometric, square)</small>
⬜ white large square <small>(geometric, square, white large square)</small>
⬝ black very small square
⬞ white very small square
⬟ black pentagon
⬠ white pentagon
⬡ white hexagon
⬢ black hexagon
⬣ horizontal black hexagon
⬤ black large circle
⬥ black medium diamond
⬦ white medium diamond
⬧ black medium lozenge
⬨ white medium lozenge
⬩ black small diamond
⬪ black small lozenge
⬫ white small lozenge
⬬ black horizontal ellipse
⬭ white horizontal ellipse
⬮ black vertical ellipse
⬯ white vertical ellipse
⬰ left arrow with small circle
⬱ three leftwards arrows
⬲ left arrow with circled plus
⬳ long leftwards squiggle arrow
⬴ leftwards two-headed arrow with vertical stroke
⬵ leftwards two-headed arrow with double vertical stroke
⬶ leftwards two-headed arrow from bar
⬷ leftwards two-headed triple dash arrow
⬸ leftwards arrow with dotted stem
⬹ leftwards arrow with tail with vertical stroke
⬺ leftwards arrow with tail with double vertical stroke
⬻ leftwards two-headed arrow with tail
⬼ leftwards two-headed arrow with tail with vertical stroke
⬽ leftwards two-headed arrow with tail with double vertical stroke
⬾ leftwards arrow through x
⬿ wave arrow pointing directly left
⭀ equals sign above leftwards arrow
⭁ reverse tilde operator above leftwards arrow
⭂ leftwards arrow above reverse almost equal to
⭃ rightwards arrow through greater-than
⭄ rightwards arrow through superset
⭅ leftwards quadruple arrow
⭆ rightwards quadruple arrow
⭇ reverse tilde operator above rightwards arrow
⭈ rightwards arrow above reverse almost equal to
⭉ tilde operator above leftwards arrow
⭊ leftwards arrow above almost equal to
⭋ leftwards arrow above reverse tilde operator
⭌ rightwards arrow above reverse tilde operator
⭐ white medium star <small>(star)</small>
⭑ black small star
⭒ white small star
⭓ black right-pointing pentagon
⭔ white right-pointing pentagon
⮕ rightwards black arrow
⯂ turned black pentagon
⯃ horizontal black octagon
⯄ black octagon
⯅ black medium up-pointing triangle centred
⯆ black medium down-pointing triangle centred
⯇ black medium left-pointing triangle centred
⯈ black medium right-pointing triangle centred
⯊ top half black circle
⯋ bottom half black circle
〈 left angle bracket
〉 right angle bracket
〚 left white square bracket
〛 right white square bracket
の hiragana letter no
﬩ hebrew letter alternative plus sign
︀ variation selector-1
﹡ small asterisk
﹢ small plus sign
﹣ small hyphen-minus
﹤ small less-than sign
﹥ small greater-than sign
﹦ small equals sign
﹨ small reverse solidus
＋ fullwidth plus sign
＜ fullwidth less-than sign
＝ fullwidth equals sign
＞ fullwidth greater-than sign
＼ fullwidth reverse solidus
＾ fullwidth circumflex accent
｜ fullwidth vertical line
～ fullwidth tilde
￢ fullwidth not sign
￩ halfwidth leftwards arrow
￪ halfwidth upwards arrow
￫ halfwidth rightwards arrow
￬ halfwidth downwards arrow
𝐀 mathematical bold capital a
𝐁 mathematical bold capital b
𝐂 mathematical bold capital c
𝐃 mathematical bold capital d
𝐄 mathematical bold capital e
𝐅 mathematical bold capital f
𝐆 mathematical bold capital g
𝐇 mathematical bold capital h
𝐈 mathematical bold capital i
𝐉 mathematical bold capital j
𝐊 mathematical bold capital k
𝐋 mathematical bold capital l
𝐌 mathematical bold capital m
𝐍 mathematical bold capital n
𝐎 mathematical bold capital o
𝐏 mathematical bold capital p
𝐐 mathematical bold capital q
𝐑 mathematical bold capital r
𝐒 mathematical bold capital s
𝐓 mathematical bold capital t
𝐔 mathematical bold capital u
𝐕 mathematical bold capital v
𝐖 mathematical bold capital w
𝐗 mathematical bold capital x
𝐘 mathematical bold capital y
𝐙 mathematical bold capital z
𝐚 mathematical bold small a
𝐛 mathematical bold small b
𝐜 mathematical bold small c
𝐝 mathematical bold small d
𝐞 mathematical bold small e
𝐟 mathematical bold small f
𝐠 mathematical bold small g
𝐡 mathematical bold small h
𝐢 mathematical bold small i
𝐣 mathematical bold small j
𝐤 mathematical bold small k
𝐥 mathematical bold small l
𝐦 mathematical bold small m
𝐧 mathematical bold small n
𝐨 mathematical bold small o
𝐩 mathematical bold small p
𝐪 mathematical bold small q
𝐫 mathematical bold small r
𝐬 mathematical bold small s
𝐭 mathematical bold small t
𝐮 mathematical bold small u
𝐯 mathematical bold small v
𝐰 mathematical bold small w
𝐱 mathematical bold small x
𝐲 mathematical bold small y
𝐳 mathematical bold small z
𝐴 mathematical italic capital a
𝐵 mathematical italic capital b
𝐶 mathematical italic capital c
𝐷 mathematical italic capital d
𝐸 mathematical italic capital e
𝐹 mathematical italic capital f
𝐺 mathematical italic capital g
𝐻 mathematical italic capital h
𝐼 mathematical italic capital i
𝐽 mathematical italic capital j
𝐾 mathematical italic capital k
𝐿 mathematical italic capital l
𝑀 mathematical italic capital m
𝑁 mathematical italic capital n
𝑂 mathematical italic capital o
𝑃 mathematical italic capital p
𝑄 mathematical italic capital q
𝑅 mathematical italic capital r
𝑆 mathematical italic capital s
𝑇 mathematical italic capital t
𝑈 mathematical italic capital u
𝑉 mathematical italic capital v
𝑊 mathematical italic capital w
𝑋 mathematical italic capital x
𝑌 mathematical italic capital y
𝑍 mathematical italic capital z
𝑎 mathematical italic small a
𝑏 mathematical italic small b
𝑐 mathematical italic small c
𝑑 mathematical italic small d
𝑒 mathematical italic small e
𝑓 mathematical italic small f
𝑔 mathematical italic small g
𝑖 mathematical italic small i
𝑗 mathematical italic small j
𝑘 mathematical italic small k
𝑙 mathematical italic small l
𝑚 mathematical italic small m
𝑛 mathematical italic small n
𝑜 mathematical italic small o
𝑝 mathematical italic small p
𝑞 mathematical italic small q
𝑟 mathematical italic small r
𝑠 mathematical italic small s
𝑡 mathematical italic small t
𝑢 mathematical italic small u
𝑣 mathematical italic small v
𝑤 mathematical italic small w
𝑥 mathematical italic small x
𝑦 mathematical italic small y
𝑧 mathematical italic small z
𝑨 mathematical bold italic capital a
𝑩 mathematical bold italic capital b
𝑪 mathematical bold italic capital c
𝑫 mathematical bold italic capital d
𝑬 mathematical bold italic capital e
𝑭 mathematical bold italic capital f
𝑮 mathematical bold italic capital g
𝑯 mathematical bold italic capital h
𝑰 mathematical bold italic capital i
𝑱 mathematical bold italic capital j
𝑲 mathematical bold italic capital k
𝑳 mathematical bold italic capital l
𝑴 mathematical bold italic capital m
𝑵 mathematical bold italic capital n
𝑶 mathematical bold italic capital o
𝑷 mathematical bold italic capital p
𝑸 mathematical bold italic capital q
𝑹 mathematical bold italic capital r
𝑺 mathematical bold italic capital s
𝑻 mathematical bold italic capital t
𝑼 mathematical bold italic capital u
𝑽 mathematical bold italic capital v
𝑾 mathematical bold italic capital w
𝑿 mathematical bold italic capital x
𝒀 mathematical bold italic capital y
𝒁 mathematical bold italic capital z
𝒂 mathematical bold italic small a
𝒃 mathematical bold italic small b
𝒄 mathematical bold italic small c
𝒅 mathematical bold italic small d
𝒆 mathematical bold italic small e
𝒇 mathematical bold italic small f
𝒈 mathematical bold italic small g
𝒉 mathematical bold italic small h
𝒊 mathematical bold italic small i
𝒋 mathematical bold italic small j
𝒌 mathematical bold italic small k
𝒍 mathematical bold italic small l
𝒎 mathematical bold italic small m
𝒏 mathematical bold italic small n
𝒐 mathematical bold italic small o
𝒑 mathematical bold italic small p
𝒒 mathematical bold italic small q
𝒓 mathematical bold italic small r
𝒔 mathematical bold italic small s
𝒕 mathematical bold italic small t
𝒖 mathematical bold italic small u
𝒗 mathematical bold italic small v
𝒘 mathematical bold italic small w
𝒙 mathematical bold italic small x
𝒚 mathematical bold italic small y
𝒛 mathematical bold italic small z
𝒜 mathematical script capital a
𝒞 mathematical script capital c
𝒟 mathematical script capital d
𝒢 mathematical script capital g
𝒥 mathematical script capital j
𝒦 mathematical script capital k
𝒩 mathematical script capital n
𝒪 mathematical script capital o
𝒫 mathematical script capital p
𝒬 mathematical script capital q
𝒮 mathematical script capital s
𝒯 mathematical script capital t
𝒰 mathematical script capital u
𝒱 mathematical script capital v
𝒲 mathematical script capital w
𝒳 mathematical script capital x
𝒴 mathematical script capital y
𝒵 mathematical script capital z
𝒶 mathematical script small a
𝒷 mathematical script small b
𝒸 mathematical script small c
𝒹 mathematical script small d
𝒻 mathematical script small f
𝒽 mathematical script small h
𝒾 mathematical script small i
𝒿 mathematical script small j
𝓀 mathematical script small k
𝓁 mathematical script small l
𝓂 mathematical script small m
𝓃 mathematical script small n
𝓅 mathematical script small p
𝓆 mathematical script small q
𝓇 mathematical script small r
𝓈 mathematical script small s
𝓉 mathematical script small t
𝓊 mathematical script small u
𝓋 mathematical script small v
𝓌 mathematical script small w
𝓍 mathematical script small x
𝓎 mathematical script small y
𝓏 mathematical script small z
𝓐 mathematical bold script capital a
𝓑 mathematical bold script capital b
𝓒 mathematical bold script capital c
𝓓 mathematical bold script capital d
𝓔 mathematical bold script capital e
𝓕 mathematical bold script capital f
𝓖 mathematical bold script capital g
𝓗 mathematical bold script capital h
𝓘 mathematical bold script capital i
𝓙 mathematical bold script capital j
𝓚 mathematical bold script capital k
𝓛 mathematical bold script capital l
𝓜 mathematical bold script capital m
𝓝 mathematical bold script capital n
𝓞 mathematical bold script capital o
𝓟 mathematical bold script capital p
𝓠 mathematical bold script capital q
𝓡 mathematical bold script capital r
𝓢 mathematical bold script capital s
𝓣 mathematical bold script capital t
𝓤 mathematical bold script capital u
𝓥 mathematical bold script capital v
𝓦 mathematical bold script capital w
𝓧 mathematical bold script capital x
𝓨 mathematical bold script capital y
𝓩 mathematical bold script capital z
𝓪 mathematical bold script small a
𝓫 mathematical bold script small b
𝓬 mathematical bold script small c
𝓭 mathematical bold script small d
𝓮 mathematical bold script small e
𝓯 mathematical bold script small f
𝓰 mathematical bold script small g
𝓱 mathematical bold script small h
𝓲 mathematical bold script small i
𝓳 mathematical bold script small j
𝓴 mathematical bold script small k
𝓵 mathematical bold script small l
𝓶 mathematical bold script small m
𝓷 mathematical bold script small n
𝓸 mathematical bold script small o
𝓹 mathematical bold script small p
𝓺 mathematical bold script small q
𝓻 mathematical bold script small r
𝓼 mathematical bold script small s
𝓽 mathematical bold script small t
𝓾 mathematical bold script small u
𝓿 mathematical bold script small v
𝔀 mathematical bold script small w
𝔁 mathematical bold script small x
𝔂 mathematical bold script small y
𝔃 mathematical bold script small z
𝔄 mathematical fraktur capital a
𝔅 mathematical fraktur capital b
𝔇 mathematical fraktur capital d
𝔈 mathematical fraktur capital e
𝔉 mathematical fraktur capital f
𝔊 mathematical fraktur capital g
𝔍 mathematical fraktur capital j
𝔎 mathematical fraktur capital k
𝔏 mathematical fraktur capital l
𝔐 mathematical fraktur capital m
𝔑 mathematical fraktur capital n
𝔒 mathematical fraktur capital o
𝔓 mathematical fraktur capital p
𝔔 mathematical fraktur capital q
𝔖 mathematical fraktur capital s
𝔗 mathematical fraktur capital t
𝔘 mathematical fraktur capital u
𝔙 mathematical fraktur capital v
𝔚 mathematical fraktur capital w
𝔛 mathematical fraktur capital x
𝔜 mathematical fraktur capital y
𝔞 mathematical fraktur small a
𝔟 mathematical fraktur small b
𝔠 mathematical fraktur small c
𝔡 mathematical fraktur small d
𝔢 mathematical fraktur small e
𝔣 mathematical fraktur small f
𝔤 mathematical fraktur small g
𝔥 mathematical fraktur small h
𝔦 mathematical fraktur small i
𝔧 mathematical fraktur small j
𝔨 mathematical fraktur small k
𝔩 mathematical fraktur small l
𝔪 mathematical fraktur small m
𝔫 mathematical fraktur small n
𝔬 mathematical fraktur small o
𝔭 mathematical fraktur small p
𝔮 mathematical fraktur small q
𝔯 mathematical fraktur small r
𝔰 mathematical fraktur small s
𝔱 mathematical fraktur small t
𝔲 mathematical fraktur small u
𝔳 mathematical fraktur small v
𝔴 mathematical fraktur small w
𝔵 mathematical fraktur small x
𝔶 mathematical fraktur small y
𝔷 mathematical fraktur small z
𝔸 mathematical double-struck capital a
𝔹 mathematical double-struck capital b
𝔻 mathematical double-struck capital d
𝔼 mathematical double-struck capital e
𝔽 mathematical double-struck capital f
𝔾 mathematical double-struck capital g
𝕀 mathematical double-struck capital i
𝕁 mathematical double-struck capital j
𝕂 mathematical double-struck capital k
𝕃 mathematical double-struck capital l
𝕄 mathematical double-struck capital m
𝕆 mathematical double-struck capital o
𝕊 mathematical double-struck capital s
𝕋 mathematical double-struck capital t
𝕌 mathematical double-struck capital u
𝕍 mathematical double-struck capital v
𝕎 mathematical double-struck capital w
𝕏 mathematical double-struck capital x
𝕐 mathematical double-struck capital y
𝕒 mathematical double-struck small a
𝕓 mathematical double-struck small b
𝕔 mathematical double-struck small c
𝕕 mathematical double-struck small d
𝕖 mathematical double-struck small e
𝕗 mathematical double-struck small f
𝕘 mathematical double-struck small g
𝕙 mathematical double-struck small h
𝕚 mathematical double-struck small i
𝕛 mathematical double-struck small j
𝕜 mathematical double-struck small k
𝕝 mathematical double-struck small l
𝕞 mathematical double-struck small m
𝕟 mathematical double-struck small n
𝕠 mathematical double-struck small o
𝕡 mathematical double-struck small p
𝕢 mathematical double-struck small q
𝕣 mathematical double-struck small r
𝕤 mathematical double-struck small s
𝕥 mathematical double-struck small t
𝕦 mathematical double-struck small u
𝕧 mathematical double-struck small v
𝕨 mathematical double-struck small w
𝕩 mathematical double-struck small x
𝕪 mathematical double-struck small y
𝕫 mathematical double-struck small z
𝕬 mathematical bold fraktur capital a
𝕭 mathematical bold fraktur capital b
𝕮 mathematical bold fraktur capital c
𝕯 mathematical bold fraktur capital d
𝕰 mathematical bold fraktur capital e
𝕱 mathematical bold fraktur capital f
𝕲 mathematical bold fraktur capital g
𝕳 mathematical bold fraktur capital h
𝕴 mathematical bold fraktur capital i
𝕵 mathematical bold fraktur capital j
𝕶 mathematical bold fraktur capital k
𝕷 mathematical bold fraktur capital l
𝕸 mathematical bold fraktur capital m
𝕹 mathematical bold fraktur capital n
𝕺 mathematical bold fraktur capital o
𝕻 mathematical bold fraktur capital p
𝕼 mathematical bold fraktur capital q
𝕽 mathematical bold fraktur capital r
𝕾 mathematical bold fraktur capital s
𝕿 mathematical bold fraktur capital t
𝖀 mathematical bold fraktur capital u
𝖁 mathematical bold fraktur capital v
𝖂 mathematical bold fraktur capital w
𝖃 mathematical bold fraktur capital x
𝖄 mathematical bold fraktur capital y
𝖅 mathematical bold fraktur capital z
𝖆 mathematical bold fraktur small a
𝖇 mathematical bold fraktur small b
𝖈 mathematical bold fraktur small c
𝖉 mathematical bold fraktur small d
𝖊 mathematical bold fraktur small e
𝖋 mathematical bold fraktur small f
𝖌 mathematical bold fraktur small g
𝖍 mathematical bold fraktur small h
𝖎 mathematical bold fraktur small i
𝖏 mathematical bold fraktur small j
𝖐 mathematical bold fraktur small k
𝖑 mathematical bold fraktur small l
𝖒 mathematical bold fraktur small m
𝖓 mathematical bold fraktur small n
𝖔 mathematical bold fraktur small o
𝖕 mathematical bold fraktur small p
𝖖 mathematical bold fraktur small q
𝖗 mathematical bold fraktur small r
𝖘 mathematical bold fraktur small s
𝖙 mathematical bold fraktur small t
𝖚 mathematical bold fraktur small u
𝖛 mathematical bold fraktur small v
𝖜 mathematical bold fraktur small w
𝖝 mathematical bold fraktur small x
𝖞 mathematical bold fraktur small y
𝖟 mathematical bold fraktur small z
𝖠 mathematical sans-serif capital a
𝖡 mathematical sans-serif capital b
𝖢 mathematical sans-serif capital c
𝖣 mathematical sans-serif capital d
𝖤 mathematical sans-serif capital e
𝖥 mathematical sans-serif capital f
𝖦 mathematical sans-serif capital g
𝖧 mathematical sans-serif capital h
𝖨 mathematical sans-serif capital i
𝖩 mathematical sans-serif capital j
𝖪 mathematical sans-serif capital k
𝖫 mathematical sans-serif capital l
𝖬 mathematical sans-serif capital m
𝖭 mathematical sans-serif capital n
𝖮 mathematical sans-serif capital o
𝖯 mathematical sans-serif capital p
𝖰 mathematical sans-serif capital q
𝖱 mathematical sans-serif capital r
𝖲 mathematical sans-serif capital s
𝖳 mathematical sans-serif capital t
𝖴 mathematical sans-serif capital u
𝖵 mathematical sans-serif capital v
𝖶 mathematical sans-serif capital w
𝖷 mathematical sans-serif capital x
𝖸 mathematical sans-serif capital y
𝖹 mathematical sans-serif capital z
𝖺 mathematical sans-serif small a
𝖻 mathematical sans-serif small b
𝖼 mathematical sans-serif small c
𝖽 mathematical sans-serif small d
𝖾 mathematical sans-serif small e
𝖿 mathematical sans-serif small f
𝗀 mathematical sans-serif small g
𝗁 mathematical sans-serif small h
𝗂 mathematical sans-serif small i
𝗃 mathematical sans-serif small j
𝗄 mathematical sans-serif small k
𝗅 mathematical sans-serif small l
𝗆 mathematical sans-serif small m
𝗇 mathematical sans-serif small n
𝗈 mathematical sans-serif small o
𝗉 mathematical sans-serif small p
𝗊 mathematical sans-serif small q
𝗋 mathematical sans-serif small r
𝗌 mathematical sans-serif small s
𝗍 mathematical sans-serif small t
𝗎 mathematical sans-serif small u
𝗏 mathematical sans-serif small v
𝗐 mathematical sans-serif small w
𝗑 mathematical sans-serif small x
𝗒 mathematical sans-serif small y
𝗓 mathematical sans-serif small z
𝗔 mathematical sans-serif bold capital a
𝗕 mathematical sans-serif bold capital b
𝗖 mathematical sans-serif bold capital c
𝗗 mathematical sans-serif bold capital d
𝗘 mathematical sans-serif bold capital e
𝗙 mathematical sans-serif bold capital f
𝗚 mathematical sans-serif bold capital g
𝗛 mathematical sans-serif bold capital h
𝗜 mathematical sans-serif bold capital i
𝗝 mathematical sans-serif bold capital j
𝗞 mathematical sans-serif bold capital k
𝗟 mathematical sans-serif bold capital l
𝗠 mathematical sans-serif bold capital m
𝗡 mathematical sans-serif bold capital n
𝗢 mathematical sans-serif bold capital o
𝗣 mathematical sans-serif bold capital p
𝗤 mathematical sans-serif bold capital q
𝗥 mathematical sans-serif bold capital r
𝗦 mathematical sans-serif bold capital s
𝗧 mathematical sans-serif bold capital t
𝗨 mathematical sans-serif bold capital u
𝗩 mathematical sans-serif bold capital v
𝗪 mathematical sans-serif bold capital w
𝗫 mathematical sans-serif bold capital x
𝗬 mathematical sans-serif bold capital y
𝗭 mathematical sans-serif bold capital z
𝗮 mathematical sans-serif bold small a
𝗯 mathematical sans-serif bold small b
𝗰 mathematical sans-serif bold small c
𝗱 mathematical sans-serif bold small d
𝗲 mathematical sans-serif bold small e
𝗳 mathematical sans-serif bold small f
𝗴 mathematical sans-serif bold small g
𝗵 mathematical sans-serif bold small h
𝗶 mathematical sans-serif bold small i
𝗷 mathematical sans-serif bold small j
𝗸 mathematical sans-serif bold small k
𝗹 mathematical sans-serif bold small l
𝗺 mathematical sans-serif bold small m
𝗻 mathematical sans-serif bold small n
𝗼 mathematical sans-serif bold small o
𝗽 mathematical sans-serif bold small p
𝗾 mathematical sans-serif bold small q
𝗿 mathematical sans-serif bold small r
𝘀 mathematical sans-serif bold small s
𝘁 mathematical sans-serif bold small t
𝘂 mathematical sans-serif bold small u
𝘃 mathematical sans-serif bold small v
𝘄 mathematical sans-serif bold small w
𝘅 mathematical sans-serif bold small x
𝘆 mathematical sans-serif bold small y
𝘇 mathematical sans-serif bold small z
𝘈 mathematical sans-serif italic capital a
𝘉 mathematical sans-serif italic capital b
𝘊 mathematical sans-serif italic capital c
𝘋 mathematical sans-serif italic capital d
𝘌 mathematical sans-serif italic capital e
𝘍 mathematical sans-serif italic capital f
𝘎 mathematical sans-serif italic capital g
𝘏 mathematical sans-serif italic capital h
𝘐 mathematical sans-serif italic capital i
𝘑 mathematical sans-serif italic capital j
𝘒 mathematical sans-serif italic capital k
𝘓 mathematical sans-serif italic capital l
𝘔 mathematical sans-serif italic capital m
𝘕 mathematical sans-serif italic capital n
𝘖 mathematical sans-serif italic capital o
𝘗 mathematical sans-serif italic capital p
𝘘 mathematical sans-serif italic capital q
𝘙 mathematical sans-serif italic capital r
𝘚 mathematical sans-serif italic capital s
𝘛 mathematical sans-serif italic capital t
𝘜 mathematical sans-serif italic capital u
𝘝 mathematical sans-serif italic capital v
𝘞 mathematical sans-serif italic capital w
𝘟 mathematical sans-serif italic capital x
𝘠 mathematical sans-serif italic capital y
𝘡 mathematical sans-serif italic capital z
𝘢 mathematical sans-serif italic small a
𝘣 mathematical sans-serif italic small b
𝘤 mathematical sans-serif italic small c
𝘥 mathematical sans-serif italic small d
𝘦 mathematical sans-serif italic small e
𝘧 mathematical sans-serif italic small f
𝘨 mathematical sans-serif italic small g
𝘩 mathematical sans-serif italic small h
𝘪 mathematical sans-serif italic small i
𝘫 mathematical sans-serif italic small j
𝘬 mathematical sans-serif italic small k
𝘭 mathematical sans-serif italic small l
𝘮 mathematical sans-serif italic small m
𝘯 mathematical sans-serif italic small n
𝘰 mathematical sans-serif italic small o
𝘱 mathematical sans-serif italic small p
𝘲 mathematical sans-serif italic small q
𝘳 mathematical sans-serif italic small r
𝘴 mathematical sans-serif italic small s
𝘵 mathematical sans-serif italic small t
𝘶 mathematical sans-serif italic small u
𝘷 mathematical sans-serif italic small v
𝘸 mathematical sans-serif italic small w
𝘹 mathematical sans-serif italic small x
𝘺 mathematical sans-serif italic small y
𝘻 mathematical sans-serif italic small z
𝘼 mathematical sans-serif bold italic capital a
𝘽 mathematical sans-serif bold italic capital b
𝘾 mathematical sans-serif bold italic capital c
𝘿 mathematical sans-serif bold italic capital d
𝙀 mathematical sans-serif bold italic capital e
𝙁 mathematical sans-serif bold italic capital f
𝙂 mathematical sans-serif bold italic capital g
𝙃 mathematical sans-serif bold italic capital h
𝙄 mathematical sans-serif bold italic capital i
𝙅 mathematical sans-serif bold italic capital j
𝙆 mathematical sans-serif bold italic capital k
𝙇 mathematical sans-serif bold italic capital l
𝙈 mathematical sans-serif bold italic capital m
𝙉 mathematical sans-serif bold italic capital n
𝙊 mathematical sans-serif bold italic capital o
𝙋 mathematical sans-serif bold italic capital p
𝙌 mathematical sans-serif bold italic capital q
𝙍 mathematical sans-serif bold italic capital r
𝙎 mathematical sans-serif bold italic capital s
𝙏 mathematical sans-serif bold italic capital t
𝙐 mathematical sans-serif bold italic capital u
𝙑 mathematical sans-serif bold italic capital v
𝙒 mathematical sans-serif bold italic capital w
𝙓 mathematical sans-serif bold italic capital x
𝙔 mathematical sans-serif bold italic capital y
𝙕 mathematical sans-serif bold italic capital z
𝙖 mathematical sans-serif bold italic small a
𝙗 mathematical sans-serif bold italic small b
𝙘 mathematical sans-serif bold italic small c
𝙙 mathematical sans-serif bold italic small d
𝙚 mathematical sans-serif bold italic small e
𝙛 mathematical sans-serif bold italic small f
𝙜 mathematical sans-serif bold italic small g
𝙝 mathematical sans-serif bold italic small h
𝙞 mathematical sans-serif bold italic small i
𝙟 mathematical sans-serif bold italic small j
𝙠 mathematical sans-serif bold italic small k
𝙡 mathematical sans-serif bold italic small l
𝙢 mathematical sans-serif bold italic small m
𝙣 mathematical sans-serif bold italic small n
𝙤 mathematical sans-serif bold italic small o
𝙥 mathematical sans-serif bold italic small p
𝙦 mathematical sans-serif bold italic small q
𝙧 mathematical sans-serif bold italic small r
𝙨 mathematical sans-serif bold italic small s
𝙩 mathematical sans-serif bold italic small t
𝙪 mathematical sans-serif bold italic small u
𝙫 mathematical sans-serif bold italic small v
𝙬 mathematical sans-serif bold italic small w
𝙭 mathematical sans-serif bold italic small x
𝙮 mathematical sans-serif bold italic small y
𝙯 mathematical sans-serif bold italic small z
𝙰 mathematical monospace capital a
𝙱 mathematical monospace capital b
𝙲 mathematical monospace capital c
𝙳 mathematical monospace capital d
𝙴 mathematical monospace capital e
𝙵 mathematical monospace capital f
𝙶 mathematical monospace capital g
𝙷 mathematical monospace capital h
𝙸 mathematical monospace capital i
𝙹 mathematical monospace capital j
𝙺 mathematical monospace capital k
𝙻 mathematical monospace capital l
𝙼 mathematical monospace capital m
𝙽 mathematical monospace capital n
𝙾 mathematical monospace capital o
𝙿 mathematical monospace capital p
𝚀 mathematical monospace capital q
𝚁 mathematical monospace capital r
𝚂 mathematical monospace capital s
𝚃 mathematical monospace capital t
𝚄 mathematical monospace capital u
𝚅 mathematical monospace capital v
𝚆 mathematical monospace capital w
𝚇 mathematical monospace capital x
𝚈 mathematical monospace capital y
𝚉 mathematical monospace capital z
𝚊 mathematical monospace small a
𝚋 mathematical monospace small b
𝚌 mathematical monospace small c
𝚍 mathematical monospace small d
𝚎 mathematical monospace small e
𝚏 mathematical monospace small f
𝚐 mathematical monospace small g
𝚑 mathematical monospace small h
𝚒 mathematical monospace small i
𝚓 mathematical monospace small j
𝚔 mathematical monospace small k
𝚕 mathematical monospace small l
𝚖 mathematical monospace small m
𝚗 mathematical monospace small n
𝚘 mathematical monospace small o
𝚙 mathematical monospace small p
𝚚 mathematical monospace small q
𝚛 mathematical monospace small r
𝚜 mathematical monospace small s
𝚝 mathematical monospace small t
𝚞 mathematical monospace small u
𝚟 mathematical monospace small v
𝚠 mathematical monospace small w
𝚡 mathematical monospace small x
𝚢 mathematical monospace small y
𝚣 mathematical monospace small z
𝚤 mathematical italic small dotless i
𝚥 mathematical italic small dotless j
𝚨 mathematical bold capital alpha
𝚩 mathematical bold capital beta
𝚪 mathematical bold capital gamma
𝚫 mathematical bold capital delta
𝚬 mathematical bold capital epsilon
𝚭 mathematical bold capital zeta
𝚮 mathematical bold capital eta
𝚯 mathematical bold capital theta
𝚰 mathematical bold capital iota
𝚱 mathematical bold capital kappa
𝚲 mathematical bold capital lamda
𝚳 mathematical bold capital mu
𝚴 mathematical bold capital nu
𝚵 mathematical bold capital xi
𝚶 mathematical bold capital omicron
𝚷 mathematical bold capital pi
𝚸 mathematical bold capital rho
𝚹 mathematical bold capital theta symbol
𝚺 mathematical bold capital sigma
𝚻 mathematical bold capital tau
𝚼 mathematical bold capital upsilon
𝚽 mathematical bold capital phi
𝚾 mathematical bold capital chi
𝚿 mathematical bold capital psi
𝛀 mathematical bold capital omega
𝛁 mathematical bold nabla
𝛂 mathematical bold small alpha
𝛃 mathematical bold small beta
𝛄 mathematical bold small gamma
𝛅 mathematical bold small delta
𝛆 mathematical bold small epsilon
𝛇 mathematical bold small zeta
𝛈 mathematical bold small eta
𝛉 mathematical bold small theta
𝛊 mathematical bold small iota
𝛋 mathematical bold small kappa
𝛌 mathematical bold small lamda
𝛍 mathematical bold small mu
𝛎 mathematical bold small nu
𝛏 mathematical bold small xi
𝛐 mathematical bold small omicron
𝛑 mathematical bold small pi
𝛒 mathematical bold small rho
𝛓 mathematical bold small final sigma
𝛔 mathematical bold small sigma
𝛕 mathematical bold small tau
𝛖 mathematical bold small upsilon
𝛗 mathematical bold small phi
𝛘 mathematical bold small chi
𝛙 mathematical bold small psi
𝛚 mathematical bold small omega
𝛛 mathematical bold partial differential
𝛜 mathematical bold epsilon symbol
𝛝 mathematical bold theta symbol
𝛞 mathematical bold kappa symbol
𝛟 mathematical bold phi symbol
𝛠 mathematical bold rho symbol
𝛡 mathematical bold pi symbol
𝛢 mathematical italic capital alpha
𝛣 mathematical italic capital beta
𝛤 mathematical italic capital gamma
𝛥 mathematical italic capital delta
𝛦 mathematical italic capital epsilon
𝛧 mathematical italic capital zeta
𝛨 mathematical italic capital eta
𝛩 mathematical italic capital theta
𝛪 mathematical italic capital iota
𝛫 mathematical italic capital kappa
𝛬 mathematical italic capital lamda
𝛭 mathematical italic capital mu
𝛮 mathematical italic capital nu
𝛯 mathematical italic capital xi
𝛰 mathematical italic capital omicron
𝛱 mathematical italic capital pi
𝛲 mathematical italic capital rho
𝛳 mathematical italic capital theta symbol
𝛴 mathematical italic capital sigma
𝛵 mathematical italic capital tau
𝛶 mathematical italic capital upsilon
𝛷 mathematical italic capital phi
𝛸 mathematical italic capital chi
𝛹 mathematical italic capital psi
𝛺 mathematical italic capital omega
𝛻 mathematical italic nabla
𝛼 mathematical italic small alpha
𝛽 mathematical italic small beta
𝛾 mathematical italic small gamma
𝛿 mathematical italic small delta
𝜀 mathematical italic small epsilon
𝜁 mathematical italic small zeta
𝜂 mathematical italic small eta
𝜃 mathematical italic small theta
𝜄 mathematical italic small iota
𝜅 mathematical italic small kappa
𝜆 mathematical italic small lamda
𝜇 mathematical italic small mu
𝜈 mathematical italic small nu
𝜉 mathematical italic small xi
𝜊 mathematical italic small omicron
𝜋 mathematical italic small pi
𝜌 mathematical italic small rho
𝜍 mathematical italic small final sigma
𝜎 mathematical italic small sigma
𝜏 mathematical italic small tau
𝜐 mathematical italic small upsilon
𝜑 mathematical italic small phi
𝜒 mathematical italic small chi
𝜓 mathematical italic small psi
𝜔 mathematical italic small omega
𝜕 mathematical italic partial differential
𝜖 mathematical italic epsilon symbol
𝜗 mathematical italic theta symbol
𝜘 mathematical italic kappa symbol
𝜙 mathematical italic phi symbol
𝜚 mathematical italic rho symbol
𝜛 mathematical italic pi symbol
𝜜 mathematical bold italic capital alpha
𝜝 mathematical bold italic capital beta
𝜞 mathematical bold italic capital gamma
𝜟 mathematical bold italic capital delta
𝜠 mathematical bold italic capital epsilon
𝜡 mathematical bold italic capital zeta
𝜢 mathematical bold italic capital eta
𝜣 mathematical bold italic capital theta
𝜤 mathematical bold italic capital iota
𝜥 mathematical bold italic capital kappa
𝜦 mathematical bold italic capital lamda
𝜧 mathematical bold italic capital mu
𝜨 mathematical bold italic capital nu
𝜩 mathematical bold italic capital xi
𝜪 mathematical bold italic capital omicron
𝜫 mathematical bold italic capital pi
𝜬 mathematical bold italic capital rho
𝜭 mathematical bold italic capital theta symbol
𝜮 mathematical bold italic capital sigma
𝜯 mathematical bold italic capital tau
𝜰 mathematical bold italic capital upsilon
𝜱 mathematical bold italic capital phi
𝜲 mathematical bold italic capital chi
𝜳 mathematical bold italic capital psi
𝜴 mathematical bold italic capital omega
𝜵 mathematical bold italic nabla
𝜶 mathematical bold italic small alpha
𝜷 mathematical bold italic small beta
𝜸 mathematical bold italic small gamma
𝜹 mathematical bold italic small delta
𝜺 mathematical bold italic small epsilon
𝜻 mathematical bold italic small zeta
𝜼 mathematical bold italic small eta
𝜽 mathematical bold italic small theta
𝜾 mathematical bold italic small iota
𝜿 mathematical bold italic small kappa
𝝀 mathematical bold italic small lamda
𝝁 mathematical bold italic small mu
𝝂 mathematical bold italic small nu
𝝃 mathematical bold italic small xi
𝝄 mathematical bold italic small omicron
𝝅 mathematical bold italic small pi
𝝆 mathematical bold italic small rho
𝝇 mathematical bold italic small final sigma
𝝈 mathematical bold italic small sigma
𝝉 mathematical bold italic small tau
𝝊 mathematical bold italic small upsilon
𝝋 mathematical bold italic small phi
𝝌 mathematical bold italic small chi
𝝍 mathematical bold italic small psi
𝝎 mathematical bold italic small omega
𝝏 mathematical bold italic partial differential
𝝐 mathematical bold italic epsilon symbol
𝝑 mathematical bold italic theta symbol
𝝒 mathematical bold italic kappa symbol
𝝓 mathematical bold italic phi symbol
𝝔 mathematical bold italic rho symbol
𝝕 mathematical bold italic pi symbol
𝝖 mathematical sans-serif bold capital alpha
𝝗 mathematical sans-serif bold capital beta
𝝘 mathematical sans-serif bold capital gamma
𝝙 mathematical sans-serif bold capital delta
𝝚 mathematical sans-serif bold capital epsilon
𝝛 mathematical sans-serif bold capital zeta
𝝜 mathematical sans-serif bold capital eta
𝝝 mathematical sans-serif bold capital theta
𝝞 mathematical sans-serif bold capital iota
𝝟 mathematical sans-serif bold capital kappa
𝝠 mathematical sans-serif bold capital lamda
𝝡 mathematical sans-serif bold capital mu
𝝢 mathematical sans-serif bold capital nu
𝝣 mathematical sans-serif bold capital xi
𝝤 mathematical sans-serif bold capital omicron
𝝥 mathematical sans-serif bold capital pi
𝝦 mathematical sans-serif bold capital rho
𝝧 mathematical sans-serif bold capital theta symbol
𝝨 mathematical sans-serif bold capital sigma
𝝩 mathematical sans-serif bold capital tau
𝝪 mathematical sans-serif bold capital upsilon
𝝫 mathematical sans-serif bold capital phi
𝝬 mathematical sans-serif bold capital chi
𝝭 mathematical sans-serif bold capital psi
𝝮 mathematical sans-serif bold capital omega
𝝯 mathematical sans-serif bold nabla
𝝰 mathematical sans-serif bold small alpha
𝝱 mathematical sans-serif bold small beta
𝝲 mathematical sans-serif bold small gamma
𝝳 mathematical sans-serif bold small delta
𝝴 mathematical sans-serif bold small epsilon
𝝵 mathematical sans-serif bold small zeta
𝝶 mathematical sans-serif bold small eta
𝝷 mathematical sans-serif bold small theta
𝝸 mathematical sans-serif bold small iota
𝝹 mathematical sans-serif bold small kappa
𝝺 mathematical sans-serif bold small lamda
𝝻 mathematical sans-serif bold small mu
𝝼 mathematical sans-serif bold small nu
𝝽 mathematical sans-serif bold small xi
𝝾 mathematical sans-serif bold small omicron
𝝿 mathematical sans-serif bold small pi
𝞀 mathematical sans-serif bold small rho
𝞁 mathematical sans-serif bold small final sigma
𝞂 mathematical sans-serif bold small sigma
𝞃 mathematical sans-serif bold small tau
𝞄 mathematical sans-serif bold small upsilon
𝞅 mathematical sans-serif bold small phi
𝞆 mathematical sans-serif bold small chi
𝞇 mathematical sans-serif bold small psi
𝞈 mathematical sans-serif bold small omega
𝞉 mathematical sans-serif bold partial differential
𝞊 mathematical sans-serif bold epsilon symbol
𝞋 mathematical sans-serif bold theta symbol
𝞌 mathematical sans-serif bold kappa symbol
𝞍 mathematical sans-serif bold phi symbol
𝞎 mathematical sans-serif bold rho symbol
𝞏 mathematical sans-serif bold pi symbol
𝞐 mathematical sans-serif bold italic capital alpha
𝞑 mathematical sans-serif bold italic capital beta
𝞒 mathematical sans-serif bold italic capital gamma
𝞓 mathematical sans-serif bold italic capital delta
𝞔 mathematical sans-serif bold italic capital epsilon
𝞕 mathematical sans-serif bold italic capital zeta
𝞖 mathematical sans-serif bold italic capital eta
𝞗 mathematical sans-serif bold italic capital theta
𝞘 mathematical sans-serif bold italic capital iota
𝞙 mathematical sans-serif bold italic capital kappa
𝞚 mathematical sans-serif bold italic capital lamda
𝞛 mathematical sans-serif bold italic capital mu
𝞜 mathematical sans-serif bold italic capital nu
𝞝 mathematical sans-serif bold italic capital xi
𝞞 mathematical sans-serif bold italic capital omicron
𝞟 mathematical sans-serif bold italic capital pi
𝞠 mathematical sans-serif bold italic capital rho
𝞡 mathematical sans-serif bold italic capital theta symbol
𝞢 mathematical sans-serif bold italic capital sigma
𝞣 mathematical sans-serif bold italic capital tau
𝞤 mathematical sans-serif bold italic capital upsilon
𝞥 mathematical sans-serif bold italic capital phi
𝞦 mathematical sans-serif bold italic capital chi
𝞧 mathematical sans-serif bold italic capital psi
𝞨 mathematical sans-serif bold italic capital omega
𝞩 mathematical sans-serif bold italic nabla
𝞪 mathematical sans-serif bold italic small alpha
𝞫 mathematical sans-serif bold italic small beta
𝞬 mathematical sans-serif bold italic small gamma
𝞭 mathematical sans-serif bold italic small delta
𝞮 mathematical sans-serif bold italic small epsilon
𝞯 mathematical sans-serif bold italic small zeta
𝞰 mathematical sans-serif bold italic small eta
𝞱 mathematical sans-serif bold italic small theta
𝞲 mathematical sans-serif bold italic small iota
𝞳 mathematical sans-serif bold italic small kappa
𝞴 mathematical sans-serif bold italic small lamda
𝞵 mathematical sans-serif bold italic small mu
𝞶 mathematical sans-serif bold italic small nu
𝞷 mathematical sans-serif bold italic small xi
𝞸 mathematical sans-serif bold italic small omicron
𝞹 mathematical sans-serif bold italic small pi
𝞺 mathematical sans-serif bold italic small rho
𝞻 mathematical sans-serif bold italic small final sigma
𝞼 mathematical sans-serif bold italic small sigma
𝞽 mathematical sans-serif bold italic small tau
𝞾 mathematical sans-serif bold italic small upsilon
𝞿 mathematical sans-serif bold italic small phi
𝟀 mathematical sans-serif bold italic small chi
𝟁 mathematical sans-serif bold italic small psi
𝟂 mathematical sans-serif bold italic small omega
𝟃 mathematical sans-serif bold italic partial differential
𝟄 mathematical sans-serif bold italic epsilon symbol
𝟅 mathematical sans-serif bold italic theta symbol
𝟆 mathematical sans-serif bold italic kappa symbol
𝟇 mathematical sans-serif bold italic phi symbol
𝟈 mathematical sans-serif bold italic rho symbol
𝟉 mathematical sans-serif bold italic pi symbol
𝟊 mathematical bold capital digamma
𝟋 mathematical bold small digamma
𝟎 mathematical bold digit zero
𝟏 mathematical bold digit one
𝟐 mathematical bold digit two
𝟑 mathematical bold digit three
𝟒 mathematical bold digit four
𝟓 mathematical bold digit five
𝟔 mathematical bold digit six
𝟕 mathematical bold digit seven
𝟖 mathematical bold digit eight
𝟗 mathematical bold digit nine
𝟘 mathematical double-struck digit zero
𝟙 mathematical double-struck digit one
𝟚 mathematical double-struck digit two
𝟛 mathematical double-struck digit three
𝟜 mathematical double-struck digit four
𝟝 mathematical double-struck digit five
𝟞 mathematical double-struck digit six
𝟟 mathematical double-struck digit seven
𝟠 mathematical double-struck digit eight
𝟡 mathematical double-struck digit nine
𝟢 mathematical sans-serif digit zero
𝟣 mathematical sans-serif digit one
𝟤 mathematical sans-serif digit two
𝟥 mathematical sans-serif digit three
𝟦 mathematical sans-serif digit four
𝟧 mathematical sans-serif digit five
𝟨 mathematical sans-serif digit six
𝟩 mathematical sans-serif digit seven
𝟪 mathematical sans-serif digit eight
𝟫 mathematical sans-serif digit nine
𝟬 mathematical sans-serif bold digit zero
𝟭 mathematical sans-serif bold digit one
𝟮 mathematical sans-serif bold digit two
𝟯 mathematical sans-serif bold digit three
𝟰 mathematical sans-serif bold digit four
𝟱 mathematical sans-serif bold digit five
𝟲 mathematical sans-serif bold digit six
𝟳 mathematical sans-serif bold digit seven
𝟴 mathematical sans-serif bold digit eight
𝟵 mathematical sans-serif bold digit nine
𝟶 mathematical monospace digit zero
𝟷 mathematical monospace digit one
𝟸 mathematical monospace digit two
𝟹 mathematical monospace digit three
𝟺 mathematical monospace digit four
𝟻 mathematical monospace digit five
𝟼 mathematical monospace digit six
𝟽 mathematical monospace digit seven
𝟾 mathematical monospace digit eight
𝟿 mathematical monospace digit nine
𞸀 arabic mathematical alef
𞸁 arabic mathematical beh
𞸂 arabic mathematical jeem
𞸃 arabic mathematical dal
𞸅 arabic mathematical waw
𞸆 arabic mathematical zain
𞸇 arabic mathematical hah
𞸈 arabic mathematical tah
𞸉 arabic mathematical yeh
𞸊 arabic mathematical kaf
𞸋 arabic mathematical lam
𞸌 arabic mathematical meem
𞸍 arabic mathematical noon
𞸎 arabic mathematical seen
𞸏 arabic mathematical ain
𞸐 arabic mathematical feh
𞸑 arabic mathematical sad
𞸒 arabic mathematical qaf
𞸓 arabic mathematical reh
𞸔 arabic mathematical sheen
𞸕 arabic mathematical teh
𞸖 arabic mathematical theh
𞸗 arabic mathematical khah
𞸘 arabic mathematical thal
𞸙 arabic mathematical dad
𞸚 arabic mathematical zah
𞸛 arabic mathematical ghain
𞸜 arabic mathematical dotless beh
𞸝 arabic mathematical dotless noon
𞸞 arabic mathematical dotless feh
𞸟 arabic mathematical dotless qaf
𞸡 arabic mathematical initial beh
𞸢 arabic mathematical initial jeem
𞸤 arabic mathematical initial heh
𞸧 arabic mathematical initial hah
𞸩 arabic mathematical initial yeh
𞸪 arabic mathematical initial kaf
𞸫 arabic mathematical initial lam
𞸬 arabic mathematical initial meem
𞸭 arabic mathematical initial noon
𞸮 arabic mathematical initial seen
𞸯 arabic mathematical initial ain
𞸰 arabic mathematical initial feh
𞸱 arabic mathematical initial sad
𞸲 arabic mathematical initial qaf
𞸴 arabic mathematical initial sheen
𞸵 arabic mathematical initial teh
𞸶 arabic mathematical initial theh
𞸷 arabic mathematical initial khah
𞸹 arabic mathematical initial dad
𞸻 arabic mathematical initial ghain
𞹂 arabic mathematical tailed jeem
𞹇 arabic mathematical tailed hah
𞹉 arabic mathematical tailed yeh
𞹋 arabic mathematical tailed lam
𞹍 arabic mathematical tailed noon
𞹎 arabic mathematical tailed seen
𞹏 arabic mathematical tailed ain
𞹑 arabic mathematical tailed sad
𞹒 arabic mathematical tailed qaf
𞹔 arabic mathematical tailed sheen
𞹗 arabic mathematical tailed khah
𞹙 arabic mathematical tailed dad
𞹛 arabic mathematical tailed ghain
𞹝 arabic mathematical tailed dotless noon
𞹟 arabic mathematical tailed dotless qaf
𞹡 arabic mathematical stretched beh
𞹢 arabic mathematical stretched jeem
𞹤 arabic mathematical stretched heh
𞹧 arabic mathematical stretched hah
𞹨 arabic mathematical stretched tah
𞹩 arabic mathematical stretched yeh
𞹪 arabic mathematical stretched kaf
𞹬 arabic mathematical stretched meem
𞹭 arabic mathematical stretched noon
𞹮 arabic mathematical stretched seen
𞹯 arabic mathematical stretched ain
𞹰 arabic mathematical stretched feh
𞹱 arabic mathematical stretched sad
𞹲 arabic mathematical stretched qaf
𞹴 arabic mathematical stretched sheen
𞹵 arabic mathematical stretched teh
𞹶 arabic mathematical stretched theh
𞹷 arabic mathematical stretched khah
𞹹 arabic mathematical stretched dad
𞹺 arabic mathematical stretched zah
𞹻 arabic mathematical stretched ghain
𞹼 arabic mathematical stretched dotless beh
𞹾 arabic mathematical stretched dotless feh
𞺀 arabic mathematical looped alef
𞺁 arabic mathematical looped beh
𞺂 arabic mathematical looped jeem
𞺃 arabic mathematical looped dal
𞺄 arabic mathematical looped heh
𞺅 arabic mathematical looped waw
𞺆 arabic mathematical looped zain
𞺇 arabic mathematical looped hah
𞺈 arabic mathematical looped tah
𞺉 arabic mathematical looped yeh
𞺋 arabic mathematical looped lam
𞺌 arabic mathematical looped meem
𞺍 arabic mathematical looped noon
𞺎 arabic mathematical looped seen
𞺏 arabic mathematical looped ain
𞺐 arabic mathematical looped feh
𞺑 arabic mathematical looped sad
𞺒 arabic mathematical looped qaf
𞺓 arabic mathematical looped reh
𞺔 arabic mathematical looped sheen
𞺕 arabic mathematical looped teh
𞺖 arabic mathematical looped theh
𞺗 arabic mathematical looped khah
𞺘 arabic mathematical looped thal
𞺙 arabic mathematical looped dad
𞺚 arabic mathematical looped zah
𞺛 arabic mathematical looped ghain
𞺡 arabic mathematical double-struck beh
𞺢 arabic mathematical double-struck jeem
𞺣 arabic mathematical double-struck dal
𞺥 arabic mathematical double-struck waw
𞺦 arabic mathematical double-struck zain
𞺧 arabic mathematical double-struck hah
𞺨 arabic mathematical double-struck tah
𞺩 arabic mathematical double-struck yeh
𞺫 arabic mathematical double-struck lam
𞺬 arabic mathematical double-struck meem
𞺭 arabic mathematical double-struck noon
𞺮 arabic mathematical double-struck seen
𞺯 arabic mathematical double-struck ain
𞺰 arabic mathematical double-struck feh
𞺱 arabic mathematical double-struck sad
𞺲 arabic mathematical double-struck qaf
𞺳 arabic mathematical double-struck reh
𞺴 arabic mathematical double-struck sheen
𞺵 arabic mathematical double-struck teh
𞺶 arabic mathematical double-struck theh
𞺷 arabic mathematical double-struck khah
𞺸 arabic mathematical double-struck thal
𞺹 arabic mathematical double-struck dad
𞺺 arabic mathematical double-struck zah
𞺻 arabic mathematical double-struck ghain
𞻰 arabic mathematical operator meem with hah with tatweel
𞻱 arabic mathematical operator hah with dal
🞄 black slightly small circle
🞌 black tiny square
🞍 black slightly small square
🞗 black tiny diamond
🞘 black very small diamond
🞙 black medium small diamond
🞝 black tiny lozenge
🞞 black very small lozenge
🞟 black medium small lozenge
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

    returncode, stdout = open_main_rofi_window(args.rofi_args, load_emojis(args.file))

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
        '--emoji-file',
        '-f',
        dest='file',
        action='store',
        default=None,
        help='Read emojis from this file instead, one entry per line'
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


def load_emojis(file_name: Union[str, None]):
    if file_name is not None:
        try:
            with open(file_name, "r") as file:
                return file.read()
        except IOError:
            return emoji_list
    else:
        return emoji_list


def open_main_rofi_window(args: List[str], emojis: str) -> Tuple[int, bytes]:
    rofi = Popen(
        [
            'rofi',
            '-dmenu',
            '-markup-rows',
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
            *args
        ],
        stdin=PIPE,
        stdout=PIPE
    )
    (stdout, _) = rofi.communicate(input=emojis.encode('UTF-8'))
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
        'windowfocus',
        '--sync',
        active_window,
        'key',
        '--clearmodifiers',
        'Shift+Insert',
        'sleep',
        '0.05',
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
