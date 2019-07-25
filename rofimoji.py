#!/usr/bin/python3
# -*- coding: utf-8 -*-
import argparse
from subprocess import Popen, PIPE

emoji_list = """😀 grinning face
😃 grinning face with big eyes
😄 grinning face with smiling eyes
😁 beaming face with smiling eyes
😆 grinning squinting face
😅 grinning face with sweat
🤣 rolling on the floor laughing
😂 face with tears of joy
🙂 slightly smiling face
🙃 upside-down face
😉 winking face
😊 smiling face with smiling eyes
😇 smiling face with halo
🥰 smiling face with hearts
😍 smiling face with heart-eyes
🤩 star-struck
😘 face blowing a kiss
😗 kissing face
☺ smiling face
😚 kissing face with closed eyes
😙 kissing face with smiling eyes
😋 face savoring food
😛 face with tongue
😜 winking face with tongue
🤪 zany face
😝 squinting face with tongue
🤑 money-mouth face
🤗 hugging face
🤭 face with hand over mouth
🤫 shushing face
🤔 thinking face
🤐 zipper-mouth face
🤨 face with raised eyebrow
😐 neutral face
😑 expressionless face
😶 face without mouth
😏 smirking face
😒 unamused face
🙄 face with rolling eyes
😬 grimacing face
🤥 lying face
😌 relieved face
😔 pensive face
😪 sleepy face
🤤 drooling face
😴 sleeping face
😷 face with medical mask
🤒 face with thermometer
🤕 face with head-bandage
🤢 nauseated face
🤮 face vomiting
🤧 sneezing face
🥵 hot face
🥶 cold face
🥴 woozy face
😵 dizzy face
🤯 exploding head
🤠 cowboy hat face
🥳 partying face
😎 smiling face with sunglasses
🤓 nerd face
🧐 face with monocle
😕 confused face
😟 worried face
🙁 slightly frowning face
☹ frowning face
😮 face with open mouth
😯 hushed face
😲 astonished face
😳 flushed face
🥺 pleading face
😦 frowning face with open mouth
😧 anguished face
😨 fearful face
😰 anxious face with sweat
😥 sad but relieved face
😢 crying face
😭 loudly crying face
😱 face screaming in fear
😖 confounded face
😣 persevering face
😞 disappointed face
😓 downcast face with sweat
😩 weary face
😫 tired face
🥱 yawning face
😤 face with steam from nose
😡 pouting face
😠 angry face
🤬 face with symbols on mouth
😈 smiling face with horns
👿 angry face with horns
💀 skull
☠ skull and crossbones
💩 pile of poo
🤡 clown face
👹 ogre
👺 goblin
👻 ghost
👽 alien
👾 alien monster
🤖 robot
😺 grinning cat
😸 grinning cat with smiling eyes
😹 cat with tears of joy
😻 smiling cat with heart-eyes
😼 cat with wry smile
😽 kissing cat
🙀 weary cat
😿 crying cat
😾 pouting cat
🙈 see-no-evil monkey
🙉 hear-no-evil monkey
🙊 speak-no-evil monkey
💋 kiss mark
💌 love letter
💘 heart with arrow
💝 heart with ribbon
💖 sparkling heart
💗 growing heart
💓 beating heart
💞 revolving hearts
💕 two hearts
💟 heart decoration
❣ heart exclamation
💔 broken heart
❤ red heart
🧡 orange heart
💛 yellow heart
💚 green heart
💙 blue heart
💜 purple heart
🤎 brown heart
🖤 black heart
🤍 white heart
💯 hundred points
💢 anger symbol
💥 collision
💫 dizzy
💦 sweat droplets
💨 dashing away
🕳 hole
💣 bomb
💬 speech balloon
👁️‍🗨️ eye in speech bubble
🗨 left speech bubble
🗯 right anger bubble
💭 thought balloon
💤 zzz
👋 waving hand
🤚 raised back of hand
🖐 hand with fingers splayed
✋ raised hand
🖖 vulcan salute
👌 OK hand
🤏 pinching hand
✌ victory hand
🤞 crossed fingers
🤟 love-you gesture
🤘 sign of the horns
🤙 call me hand
👈 backhand index pointing left
👉 backhand index pointing right
👆 backhand index pointing up
🖕 middle finger
👇 backhand index pointing down
☝ index pointing up
👍 thumbs up
👎 thumbs down
✊ raised fist
👊 oncoming fist
🤛 left-facing fist
🤜 right-facing fist
👏 clapping hands
🙌 raising hands
👐 open hands
🤲 palms up together
🤝 handshake
🙏 folded hands
✍ writing hand
💅 nail polish
🤳 selfie
💪 flexed biceps
🦾 mechanical arm
🦿 mechanical leg
🦵 leg
🦶 foot
👂 ear
🦻 ear with hearing aid
👃 nose
🧠 brain
🦷 tooth
🦴 bone
👀 eyes
👁 eye
👅 tongue
👄 mouth
👶 baby
🧒 child
👦 boy
👧 girl
🧑 person
👱 person: blond hair
👨 man
🧔 man: beard
👱‍♂️ man: blond hair
👨‍🦰 man: red hair
👨‍🦱 man: curly hair
👨‍🦳 man: white hair
👨‍🦲 man: bald
👩 woman
👱‍♀️ woman: blond hair
👩‍🦰 woman: red hair
👩‍🦱 woman: curly hair
👩‍🦳 woman: white hair
👩‍🦲 woman: bald
🧓 older person
👴 old man
👵 old woman
🙍 person frowning
🙍‍♂️ man frowning
🙍‍♀️ woman frowning
🙎 person pouting
🙎‍♂️ man pouting
🙎‍♀️ woman pouting
🙅 person gesturing NO
🙅‍♂️ man gesturing NO
🙅‍♀️ woman gesturing NO
🙆 person gesturing OK
🙆‍♂️ man gesturing OK
🙆‍♀️ woman gesturing OK
💁 person tipping hand
💁‍♂️ man tipping hand
💁‍♀️ woman tipping hand
🙋 person raising hand
🙋‍♂️ man raising hand
🙋‍♀️ woman raising hand
🧏 deaf person
🧏‍♂️ deaf man
🧏‍♀️ deaf woman
🙇 person bowing
🙇‍♂️ man bowing
🙇‍♀️ woman bowing
🤦 person facepalming
🤦‍♂️ man facepalming
🤦‍♀️ woman facepalming
🤷 person shrugging
🤷‍♂️ man shrugging
🤷‍♀️ woman shrugging
👨‍⚕️ man health worker
👩‍⚕️ woman health worker
👨‍🎓 man student
👩‍🎓 woman student
👨‍🏫 man teacher
👩‍🏫 woman teacher
👨‍⚖️ man judge
👩‍⚖️ woman judge
👨‍🌾 man farmer
👩‍🌾 woman farmer
👨‍🍳 man cook
👩‍🍳 woman cook
👨‍🔧 man mechanic
👩‍🔧 woman mechanic
👨‍🏭 man factory worker
👩‍🏭 woman factory worker
👨‍💼 man office worker
👩‍💼 woman office worker
👨‍🔬 man scientist
👩‍🔬 woman scientist
👨‍💻 man technologist
👩‍💻 woman technologist
👨‍🎤 man singer
👩‍🎤 woman singer
👨‍🎨 man artist
👩‍🎨 woman artist
👨‍✈️ man pilot
👩‍✈️ woman pilot
👨‍🚀 man astronaut
👩‍🚀 woman astronaut
👨‍🚒 man firefighter
👩‍🚒 woman firefighter
👮 police officer
👮‍♂️ man police officer
👮‍♀️ woman police officer
🕵 detective
🕵️‍♂️ man detective
🕵️‍♀️ woman detective
💂 guard
💂‍♂️ man guard
💂‍♀️ woman guard
👷 construction worker
👷‍♂️ man construction worker
👷‍♀️ woman construction worker
🤴 prince
👸 princess
👳 person wearing turban
👳‍♂️ man wearing turban
👳‍♀️ woman wearing turban
👲 man with Chinese cap
🧕 woman with headscarf
🤵 man in tuxedo
👰 bride with veil
🤰 pregnant woman
🤱 breast-feeding
👼 baby angel
🎅 Santa Claus
🤶 Mrs. Claus
🦸 superhero
🦸‍♂️ man superhero
🦸‍♀️ woman superhero
🦹 supervillain
🦹‍♂️ man supervillain
🦹‍♀️ woman supervillain
🧙 mage
🧙‍♂️ man mage
🧙‍♀️ woman mage
🧚 fairy
🧚‍♂️ man fairy
🧚‍♀️ woman fairy
🧛 vampire
🧛‍♂️ man vampire
🧛‍♀️ woman vampire
🧜 merperson
🧜‍♂️ merman
🧜‍♀️ mermaid
🧝 elf
🧝‍♂️ man elf
🧝‍♀️ woman elf
🧞 genie
🧞‍♂️ man genie
🧞‍♀️ woman genie
🧟 zombie
🧟‍♂️ man zombie
🧟‍♀️ woman zombie
💆 person getting massage
💆‍♂️ man getting massage
💆‍♀️ woman getting massage
💇 person getting haircut
💇‍♂️ man getting haircut
💇‍♀️ woman getting haircut
🚶 person walking
🚶‍♂️ man walking
🚶‍♀️ woman walking
🧍 person standing
🧍‍♂️ man standing
🧍‍♀️ woman standing
🧎 person kneeling
🧎‍♂️ man kneeling
🧎‍♀️ woman kneeling
👨‍🦯 man with probing cane
👩‍🦯 woman with probing cane
👨‍🦼 man in motorized wheelchair
👩‍🦼 woman in motorized wheelchair
👨‍🦽 man in manual wheelchair
👩‍🦽 woman in manual wheelchair
🏃 person running
🏃‍♂️ man running
🏃‍♀️ woman running
💃 woman dancing
🕺 man dancing
🕴 man in suit levitating
👯 people with bunny ears
👯‍♂️ men with bunny ears
👯‍♀️ women with bunny ears
🧖 person in steamy room
🧖‍♂️ man in steamy room
🧖‍♀️ woman in steamy room
🧗 person climbing
🧗‍♂️ man climbing
🧗‍♀️ woman climbing
🤺 person fencing
🏇 horse racing
⛷ skier
🏂 snowboarder
🏌 person golfing
🏌️‍♂️ man golfing
🏌️‍♀️ woman golfing
🏄 person surfing
🏄‍♂️ man surfing
🏄‍♀️ woman surfing
🚣 person rowing boat
🚣‍♂️ man rowing boat
🚣‍♀️ woman rowing boat
🏊 person swimming
🏊‍♂️ man swimming
🏊‍♀️ woman swimming
⛹ person bouncing ball
⛹️‍♂️ man bouncing ball
⛹️‍♀️ woman bouncing ball
🏋 person lifting weights
🏋️‍♂️ man lifting weights
🏋️‍♀️ woman lifting weights
🚴 person biking
🚴‍♂️ man biking
🚴‍♀️ woman biking
🚵 person mountain biking
🚵‍♂️ man mountain biking
🚵‍♀️ woman mountain biking
🤸 person cartwheeling
🤸‍♂️ man cartwheeling
🤸‍♀️ woman cartwheeling
🤼 people wrestling
🤼‍♂️ men wrestling
🤼‍♀️ women wrestling
🤽 person playing water polo
🤽‍♂️ man playing water polo
🤽‍♀️ woman playing water polo
🤾 person playing handball
🤾‍♂️ man playing handball
🤾‍♀️ woman playing handball
🤹 person juggling
🤹‍♂️ man juggling
🤹‍♀️ woman juggling
🧘 person in lotus position
🧘‍♂️ man in lotus position
🧘‍♀️ woman in lotus position
🛀 person taking bath
🛌 person in bed
🧑‍🤝‍🧑 people holding hands
👭 women holding hands
👫 woman and man holding hands
👬 men holding hands
💏 kiss
👩‍❤️‍💋‍👨 kiss: woman, man
👨‍❤️‍💋‍👨 kiss: man, man
👩‍❤️‍💋‍👩 kiss: woman, woman
💑 couple with heart
👩‍❤️‍👨 couple with heart: woman, man
👨‍❤️‍👨 couple with heart: man, man
👩‍❤️‍👩 couple with heart: woman, woman
👪 family
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
🗣 speaking head
👤 bust in silhouette
👥 busts in silhouette
👣 footprints
🦰 red hair
🦱 curly hair
🦳 white hair
🦲 bald
🐵 monkey face
🐒 monkey
🦍 gorilla
🦧 orangutan
🐶 dog face
🐕 dog
🦮 guide dog
🐕‍🦺 service dog
🐩 poodle
🐺 wolf
🦊 fox
🦝 raccoon
🐱 cat face
🐈 cat
🦁 lion
🐯 tiger face
🐅 tiger
🐆 leopard
🐴 horse face
🐎 horse
🦄 unicorn
🦓 zebra
🦌 deer
🐮 cow face
🐂 ox
🐃 water buffalo
🐄 cow
🐷 pig face
🐖 pig
🐗 boar
🐽 pig nose
🐏 ram
🐑 ewe
🐐 goat
🐪 camel
🐫 two-hump camel
🦙 llama
🦒 giraffe
🐘 elephant
🦏 rhinoceros
🦛 hippopotamus
🐭 mouse face
🐁 mouse
🐀 rat
🐹 hamster
🐰 rabbit face
🐇 rabbit
🐿 chipmunk
🦔 hedgehog
🦇 bat
🐻 bear
🐨 koala
🐼 panda
🦥 sloth
🦦 otter
🦨 skunk
🦘 kangaroo
🦡 badger
🐾 paw prints
🦃 turkey
🐔 chicken
🐓 rooster
🐣 hatching chick
🐤 baby chick
🐥 front-facing baby chick
🐦 bird
🐧 penguin
🕊 dove
🦅 eagle
🦆 duck
🦢 swan
🦉 owl
🦩 flamingo
🦚 peacock
🦜 parrot
🐸 frog
🐊 crocodile
🐢 turtle
🦎 lizard
🐍 snake
🐲 dragon face
🐉 dragon
🦕 sauropod
🦖 T-Rex
🐳 spouting whale
🐋 whale
🐬 dolphin
🐟 fish
🐠 tropical fish
🐡 blowfish
🦈 shark
🐙 octopus
🐚 spiral shell
🐌 snail
🦋 butterfly
🐛 bug
🐜 ant
🐝 honeybee
🐞 lady beetle
🦗 cricket
🕷 spider
🕸 spider web
🦂 scorpion
🦟 mosquito
🦠 microbe
💐 bouquet
🌸 cherry blossom
💮 white flower
🏵 rosette
🌹 rose
🥀 wilted flower
🌺 hibiscus
🌻 sunflower
🌼 blossom
🌷 tulip
🌱 seedling
🌲 evergreen tree
🌳 deciduous tree
🌴 palm tree
🌵 cactus
🌾 sheaf of rice
🌿 herb
☘ shamrock
🍀 four leaf clover
🍁 maple leaf
🍂 fallen leaf
🍃 leaf fluttering in wind
🍇 grapes
🍈 melon
🍉 watermelon
🍊 tangerine
🍋 lemon
🍌 banana
🍍 pineapple
🥭 mango
🍎 red apple
🍏 green apple
🍐 pear
🍑 peach
🍒 cherries
🍓 strawberry
🥝 kiwi fruit
🍅 tomato
🥥 coconut
🥑 avocado
🍆 eggplant
🥔 potato
🥕 carrot
🌽 ear of corn
🌶 hot pepper
🥒 cucumber
🥬 leafy green
🥦 broccoli
🧄 garlic
🧅 onion
🍄 mushroom
🥜 peanuts
🌰 chestnut
🍞 bread
🥐 croissant
🥖 baguette bread
🥨 pretzel
🥯 bagel
🥞 pancakes
🧇 waffle
🧀 cheese wedge
🍖 meat on bone
🍗 poultry leg
🥩 cut of meat
🥓 bacon
🍔 hamburger
🍟 french fries
🍕 pizza
🌭 hot dog
🥪 sandwich
🌮 taco
🌯 burrito
🥙 stuffed flatbread
🧆 falafel
🥚 egg
🍳 cooking
🥘 shallow pan of food
🍲 pot of food
🥣 bowl with spoon
🥗 green salad
🍿 popcorn
🧈 butter
🧂 salt
🥫 canned food
🍱 bento box
🍘 rice cracker
🍙 rice ball
🍚 cooked rice
🍛 curry rice
🍜 steaming bowl
🍝 spaghetti
🍠 roasted sweet potato
🍢 oden
🍣 sushi
🍤 fried shrimp
🍥 fish cake with swirl
🥮 moon cake
🍡 dango
🥟 dumpling
🥠 fortune cookie
🥡 takeout box
🦀 crab
🦞 lobster
🦐 shrimp
🦑 squid
🦪 oyster
🍦 soft ice cream
🍧 shaved ice
🍨 ice cream
🍩 doughnut
🍪 cookie
🎂 birthday cake
🍰 shortcake
🧁 cupcake
🥧 pie
🍫 chocolate bar
🍬 candy
🍭 lollipop
🍮 custard
🍯 honey pot
🍼 baby bottle
🥛 glass of milk
☕ hot beverage
🍵 teacup without handle
🍶 sake
🍾 bottle with popping cork
🍷 wine glass
🍸 cocktail glass
🍹 tropical drink
🍺 beer mug
🍻 clinking beer mugs
🥂 clinking glasses
🥃 tumbler glass
🥤 cup with straw
🧃 beverage box
🧉 mate
🧊 ice cube
🥢 chopsticks
🍽 fork and knife with plate
🍴 fork and knife
🥄 spoon
🔪 kitchen knife
🏺 amphora
🌍 globe showing Europe-Africa
🌎 globe showing Americas
🌏 globe showing Asia-Australia
🌐 globe with meridians
🗺 world map
🗾 map of Japan
🧭 compass
🏔 snow-capped mountain
⛰ mountain
🌋 volcano
🗻 mount fuji
🏕 camping
🏖 beach with umbrella
🏜 desert
🏝 desert island
🏞 national park
🏟 stadium
🏛 classical building
🏗 building construction
🧱 brick
🏘 houses
🏚 derelict house
🏠 house
🏡 house with garden
🏢 office building
🏣 Japanese post office
🏤 post office
🏥 hospital
🏦 bank
🏨 hotel
🏩 love hotel
🏪 convenience store
🏫 school
🏬 department store
🏭 factory
🏯 Japanese castle
🏰 castle
💒 wedding
🗼 Tokyo tower
🗽 Statue of Liberty
⛪ church
🕌 mosque
🛕 hindu temple
🕍 synagogue
⛩ shinto shrine
🕋 kaaba
⛲ fountain
⛺ tent
🌁 foggy
🌃 night with stars
🏙 cityscape
🌄 sunrise over mountains
🌅 sunrise
🌆 cityscape at dusk
🌇 sunset
🌉 bridge at night
♨ hot springs
🎠 carousel horse
🎡 ferris wheel
🎢 roller coaster
💈 barber pole
🎪 circus tent
🚂 locomotive
🚃 railway car
🚄 high-speed train
🚅 bullet train
🚆 train
🚇 metro
🚈 light rail
🚉 station
🚊 tram
🚝 monorail
🚞 mountain railway
🚋 tram car
🚌 bus
🚍 oncoming bus
🚎 trolleybus
🚐 minibus
🚑 ambulance
🚒 fire engine
🚓 police car
🚔 oncoming police car
🚕 taxi
🚖 oncoming taxi
🚗 automobile
🚘 oncoming automobile
🚙 sport utility vehicle
🚚 delivery truck
🚛 articulated lorry
🚜 tractor
🏎 racing car
🏍 motorcycle
🛵 motor scooter
🦽 manual wheelchair
🦼 motorized wheelchair
🛺 auto rickshaw
🚲 bicycle
🛴 kick scooter
🛹 skateboard
🚏 bus stop
🛣 motorway
🛤 railway track
🛢 oil drum
⛽ fuel pump
🚨 police car light
🚥 horizontal traffic light
🚦 vertical traffic light
🛑 stop sign
🚧 construction
⚓ anchor
⛵ sailboat
🛶 canoe
🚤 speedboat
🛳 passenger ship
⛴ ferry
🛥 motor boat
🚢 ship
✈ airplane
🛩 small airplane
🛫 airplane departure
🛬 airplane arrival
🪂 parachute
💺 seat
🚁 helicopter
🚟 suspension railway
🚠 mountain cableway
🚡 aerial tramway
🛰 satellite
🚀 rocket
🛸 flying saucer
🛎 bellhop bell
🧳 luggage
⌛ hourglass done
⏳ hourglass not done
⌚ watch
⏰ alarm clock
⏱ stopwatch
⏲ timer clock
🕰 mantelpiece clock
🕛 twelve o’clock
🕧 twelve-thirty
🕐 one o’clock
🕜 one-thirty
🕑 two o’clock
🕝 two-thirty
🕒 three o’clock
🕞 three-thirty
🕓 four o’clock
🕟 four-thirty
🕔 five o’clock
🕠 five-thirty
🕕 six o’clock
🕡 six-thirty
🕖 seven o’clock
🕢 seven-thirty
🕗 eight o’clock
🕣 eight-thirty
🕘 nine o’clock
🕤 nine-thirty
🕙 ten o’clock
🕥 ten-thirty
🕚 eleven o’clock
🕦 eleven-thirty
🌑 new moon
🌒 waxing crescent moon
🌓 first quarter moon
🌔 waxing gibbous moon
🌕 full moon
🌖 waning gibbous moon
🌗 last quarter moon
🌘 waning crescent moon
🌙 crescent moon
🌚 new moon face
🌛 first quarter moon face
🌜 last quarter moon face
🌡 thermometer
☀ sun
🌝 full moon face
🌞 sun with face
🪐 ringed planet
⭐ star
🌟 glowing star
🌠 shooting star
🌌 milky way
☁ cloud
⛅ sun behind cloud
⛈ cloud with lightning and rain
🌤 sun behind small cloud
🌥 sun behind large cloud
🌦 sun behind rain cloud
🌧 cloud with rain
🌨 cloud with snow
🌩 cloud with lightning
🌪 tornado
🌫 fog
🌬 wind face
🌀 cyclone
🌈 rainbow
🌂 closed umbrella
☂ umbrella
☔ umbrella with rain drops
⛱ umbrella on ground
⚡ high voltage
❄ snowflake
☃ snowman
⛄ snowman without snow
☄ comet
🔥 fire
💧 droplet
🌊 water wave
🎃 jack-o-lantern
🎄 Christmas tree
🎆 fireworks
🎇 sparkler
🧨 firecracker
✨ sparkles
🎈 balloon
🎉 party popper
🎊 confetti ball
🎋 tanabata tree
🎍 pine decoration
🎎 Japanese dolls
🎏 carp streamer
🎐 wind chime
🎑 moon viewing ceremony
🧧 red envelope
🎀 ribbon
🎁 wrapped gift
🎗 reminder ribbon
🎟 admission tickets
🎫 ticket
🎖 military medal
🏆 trophy
🏅 sports medal
🥇 1st place medal
🥈 2nd place medal
🥉 3rd place medal
⚽ soccer ball
⚾ baseball
🥎 softball
🏀 basketball
🏐 volleyball
🏈 american football
🏉 rugby football
🎾 tennis
🥏 flying disc
🎳 bowling
🏏 cricket game
🏑 field hockey
🏒 ice hockey
🥍 lacrosse
🏓 ping pong
🏸 badminton
🥊 boxing glove
🥋 martial arts uniform
🥅 goal net
⛳ flag in hole
⛸ ice skate
🎣 fishing pole
🤿 diving mask
🎽 running shirt
🎿 skis
🛷 sled
🥌 curling stone
🎯 direct hit
🪀 yo-yo
🪁 kite
🎱 pool 8 ball
🔮 crystal ball
🧿 nazar amulet
🎮 video game
🕹 joystick
🎰 slot machine
🎲 game die
🧩 puzzle piece
🧸 teddy bear
♠ spade suit
♥ heart suit
♦ diamond suit
♣ club suit
♟ chess pawn
🃏 joker
🀄 mahjong red dragon
🎴 flower playing cards
🎭 performing arts
🖼 framed picture
🎨 artist palette
🧵 thread
🧶 yarn
👓 glasses
🕶 sunglasses
🥽 goggles
🥼 lab coat
🦺 safety vest
👔 necktie
👕 t-shirt
👖 jeans
🧣 scarf
🧤 gloves
🧥 coat
🧦 socks
👗 dress
👘 kimono
🥻 sari
🩱 one-piece swimsuit
🩲 briefs
🩳 shorts
👙 bikini
👚 woman’s clothes
👛 purse
👜 handbag
👝 clutch bag
🛍 shopping bags
🎒 backpack
👞 man’s shoe
👟 running shoe
🥾 hiking boot
🥿 flat shoe
👠 high-heeled shoe
👡 woman’s sandal
🩰 ballet shoes
👢 woman’s boot
👑 crown
👒 woman’s hat
🎩 top hat
🎓 graduation cap
🧢 billed cap
⛑ rescue worker’s helmet
📿 prayer beads
💄 lipstick
💍 ring
💎 gem stone
🔇 muted speaker
🔈 speaker low volume
🔉 speaker medium volume
🔊 speaker high volume
📢 loudspeaker
📣 megaphone
📯 postal horn
🔔 bell
🔕 bell with slash
🎼 musical score
🎵 musical note
🎶 musical notes
🎙 studio microphone
🎚 level slider
🎛 control knobs
🎤 microphone
🎧 headphone
📻 radio
🎷 saxophone
🎸 guitar
🎹 musical keyboard
🎺 trumpet
🎻 violin
🪕 banjo
🥁 drum
📱 mobile phone
📲 mobile phone with arrow
☎ telephone
📞 telephone receiver
📟 pager
📠 fax machine
🔋 battery
🔌 electric plug
💻 laptop computer
🖥 desktop computer
🖨 printer
⌨ keyboard
🖱 computer mouse
🖲 trackball
💽 computer disk
💾 floppy disk
💿 optical disk
📀 dvd
🧮 abacus
🎥 movie camera
🎞 film frames
📽 film projector
🎬 clapper board
📺 television
📷 camera
📸 camera with flash
📹 video camera
📼 videocassette
🔍 magnifying glass tilted left
🔎 magnifying glass tilted right
🕯 candle
💡 light bulb
🔦 flashlight
🏮 red paper lantern
🪔 diya lamp
📔 notebook with decorative cover
📕 closed book
📖 open book
📗 green book
📘 blue book
📙 orange book
📚 books
📓 notebook
📒 ledger
📃 page with curl
📜 scroll
📄 page facing up
📰 newspaper
🗞 rolled-up newspaper
📑 bookmark tabs
🔖 bookmark
🏷 label
💰 money bag
💴 yen banknote
💵 dollar banknote
💶 euro banknote
💷 pound banknote
💸 money with wings
💳 credit card
🧾 receipt
💹 chart increasing with yen
💱 currency exchange
💲 heavy dollar sign
✉ envelope
📧 e-mail
📨 incoming envelope
📩 envelope with arrow
📤 outbox tray
📥 inbox tray
📦 package
📫 closed mailbox with raised flag
📪 closed mailbox with lowered flag
📬 open mailbox with raised flag
📭 open mailbox with lowered flag
📮 postbox
🗳 ballot box with ballot
✏ pencil
✒ black nib
🖋 fountain pen
🖊 pen
🖌 paintbrush
🖍 crayon
📝 memo
💼 briefcase
📁 file folder
📂 open file folder
🗂 card index dividers
📅 calendar
📆 tear-off calendar
🗒 spiral notepad
🗓 spiral calendar
📇 card index
📈 chart increasing
📉 chart decreasing
📊 bar chart
📋 clipboard
📌 pushpin
📍 round pushpin
📎 paperclip
🖇 linked paperclips
📏 straight ruler
📐 triangular ruler
✂ scissors
🗃 card file box
🗄 file cabinet
🗑 wastebasket
🔒 locked
🔓 unlocked
🔏 locked with pen
🔐 locked with key
🔑 key
🗝 old key
🔨 hammer
🪓 axe
⛏ pick
⚒ hammer and pick
🛠 hammer and wrench
🗡 dagger
⚔ crossed swords
🔫 pistol
🏹 bow and arrow
🛡 shield
🔧 wrench
🔩 nut and bolt
⚙ gear
🗜 clamp
⚖ balance scale
🦯 probing cane
🔗 link
⛓ chains
🧰 toolbox
🧲 magnet
⚗ alembic
🧪 test tube
🧫 petri dish
🧬 dna
🔬 microscope
🔭 telescope
📡 satellite antenna
💉 syringe
🩸 drop of blood
💊 pill
🩹 adhesive bandage
🩺 stethoscope
🚪 door
🛏 bed
🛋 couch and lamp
🪑 chair
🚽 toilet
🚿 shower
🛁 bathtub
🪒 razor
🧴 lotion bottle
🧷 safety pin
🧹 broom
🧺 basket
🧻 roll of paper
🧼 soap
🧽 sponge
🧯 fire extinguisher
🛒 shopping cart
🚬 cigarette
⚰ coffin
⚱ funeral urn
🗿 moai
🏧 ATM sign
🚮 litter in bin sign
🚰 potable water
♿ wheelchair symbol
🚹 men’s room
🚺 women’s room
🚻 restroom
🚼 baby symbol
🚾 water closet
🛂 passport control
🛃 customs
🛄 baggage claim
🛅 left luggage
⚠ warning
🚸 children crossing
⛔ no entry
🚫 prohibited
🚳 no bicycles
🚭 no smoking
🚯 no littering
🚱 non-potable water
🚷 no pedestrians
📵 no mobile phones
🔞 no one under eighteen
☢ radioactive
☣ biohazard
⬆ up arrow
↗ up-right arrow
➡ right arrow
↘ down-right arrow
⬇ down arrow
↙ down-left arrow
⬅ left arrow
↖ up-left arrow
↕ up-down arrow
↔ left-right arrow
↩ right arrow curving left
↪ left arrow curving right
⤴ right arrow curving up
⤵ right arrow curving down
🔃 clockwise vertical arrows
🔄 counterclockwise arrows button
🔙 BACK arrow
🔚 END arrow
🔛 ON! arrow
🔜 SOON arrow
🔝 TOP arrow
🛐 place of worship
⚛ atom symbol
🕉 om
✡ star of David
☸ wheel of dharma
☯ yin yang
✝ latin cross
☦ orthodox cross
☪ star and crescent
☮ peace symbol
🕎 menorah
🔯 dotted six-pointed star
♈ Aries
♉ Taurus
♊ Gemini
♋ Cancer
♌ Leo
♍ Virgo
♎ Libra
♏ Scorpio
♐ Sagittarius
♑ Capricorn
♒ Aquarius
♓ Pisces
⛎ Ophiuchus
🔀 shuffle tracks button
🔁 repeat button
🔂 repeat single button
▶ play button
⏩ fast-forward button
⏭ next track button
⏯ play or pause button
◀ reverse button
⏪ fast reverse button
⏮ last track button
🔼 upwards button
⏫ fast up button
🔽 downwards button
⏬ fast down button
⏸ pause button
⏹ stop button
⏺ record button
⏏ eject button
🎦 cinema
🔅 dim button
🔆 bright button
📶 antenna bars
📳 vibration mode
📴 mobile phone off
♀ female sign
♂ male sign
⚕ medical symbol
♾ infinity
♻ recycling symbol
⚜ fleur-de-lis
🔱 trident emblem
📛 name badge
🔰 Japanese symbol for beginner
⭕ hollow red circle
✅ check mark button
☑ check box with check
✔ check mark
✖ multiplication sign
❌ cross mark
❎ cross mark button
➕ plus sign
➖ minus sign
➗ division sign
➰ curly loop
➿ double curly loop
〽 part alternation mark
✳ eight-spoked asterisk
✴ eight-pointed star
❇ sparkle
‼ double exclamation mark
⁉ exclamation question mark
❓ question mark
❔ white question mark
❕ white exclamation mark
❗ exclamation mark
〰 wavy dash
© copyright
® registered
™ trade mark
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
🔠 input latin uppercase
🔡 input latin lowercase
🔢 input numbers
🔣 input symbols
🔤 input latin letters
🅰 A button (blood type)
🆎 AB button (blood type)
🅱 B button (blood type)
🆑 CL button
🆒 COOL button
🆓 FREE button
ℹ information
🆔 ID button
Ⓜ circled M
🆕 NEW button
🆖 NG button
🅾 O button (blood type)
🆗 OK button
🅿 P button
🆘 SOS button
🆙 UP! button
🆚 VS button
🈁 Japanese “here” button
🈂 Japanese “service charge” button
🈷 Japanese “monthly amount” button
🈶 Japanese “not free of charge” button
🈯 Japanese “reserved” button
🉐 Japanese “bargain” button
🈹 Japanese “discount” button
🈚 Japanese “free of charge” button
🈲 Japanese “prohibited” button
🉑 Japanese “acceptable” button
🈸 Japanese “application” button
🈴 Japanese “passing grade” button
🈳 Japanese “vacancy” button
㊗ Japanese “congratulations” button
㊙ Japanese “secret” button
🈺 Japanese “open for business” button
🈵 Japanese “no vacancy” button
🔴 red circle
🟠 orange circle
🟡 yellow circle
🟢 green circle
🔵 blue circle
🟣 purple circle
🟤 brown circle
⚫ black circle
⚪ white circle
🟥 red square
🟧 orange square
🟨 yellow square
🟩 green square
🟦 blue square
🟪 purple square
🟫 brown square
⬛ black large square
⬜ white large square
◼ black medium square
◻ white medium square
◾ black medium-small square
◽ white medium-small square
▪ black small square
▫ white small square
🔶 large orange diamond
🔷 large blue diamond
🔸 small orange diamond
🔹 small blue diamond
🔺 red triangle pointed up
🔻 red triangle pointed down
💠 diamond with a dot
🔘 radio button
🔳 white square button
🔲 black square button
🏁 chequered flag
🚩 triangular flag
🎌 crossed flags
🏴 black flag
🏳 white flag
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
🇲🇰 flag: Macedonia
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

skin_tone_selectable_emojis = {'👃', '🧑', '👇', '👨', '👋', '🏋', '👪', '🖐', '🙏', '🤜', '💅',
                               '🤼', '🎅', '🤦', '🙇', '🤾', '💂', '🧗', '👈', '🤹', '👵', '🤽',
                               '🏄', '🧛', '🧖', '👷', '💁', '🤟', '🧘', '🧏', '👳', '👱', '✊',
                               '👎', '👶', '🧜', '🤘', '🧔', '🕴', '🏃', '🤰', '👌', '🙎', '🧒',
                               '🛀', '🤲', '🧝', '👩', '💪', '🧙', '🤴', '👉', '💑', '🧎', '🧚',
                               '🕺', '💃', '🧍', '🙌', '🚣', '👏', '💏', '🚶', '✋', '🛌', '🏊',
                               '🤸', '🖖', '🧓', '🤱', '💇', '☝', '👧', '👲', '👴', '🤏', '🦹',
                               '🦵', '🧕', '🚴', '🤳', '✌', '💆', '🤷', '🤚', '👍', '👭', '🙆',
                               '🕵', '🤛', '🤶', '🦶', '🙋', '⛹', '👼', '👊', '🙅', '👰', '🦸',
                               '👮', '🏇', '🦻', '👐', '🤞', '✍', '🤙', '🏌', '👂', '👬', '🤵',
                               '🙍', '🏂', '🤝', '👫', '👦', '👸', '👆', '👯', '🖕', '🚵'}

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


def select_skin_tone(selected_emoji: chr, skin_tone: str):
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
            args=[
                'rofi',
                '-dmenu',
                '-i',
                '-multi-select',
                '-p',
                selected_emoji + '   ',
                '-kb-custom-1',
                'Alt+c'
            ],
            stdin=PIPE,
            stdout=PIPE
        )

        (stdout_skin, _) = rofi_skin.communicate(input=modified_emojis.encode('utf-8'))

        if rofi_skin.returncode == 1:
            return ''

        return stdout_skin.split()[0].decode('utf-8')


def insert_emojis(emojis: str, active_window: str, use_clipboard: bool = False):
    if use_clipboard:
        copy_paste_emojis(emojis, active_window)
    else:
        type_emojis(emojis, active_window)


def type_emojis(emojis: str, active_window: str):
    Popen(
        args=[
            'xdotool',
            'type',
            '--clearmodifiers',
            '--window',
            active_window,
            emojis
        ]
    )


def copy_paste_emojis(emojis: str, active_window: str):
    xsel = Popen(args=['xsel', '-o', '-b'], stdout=PIPE)
    old_clipboard_content = xsel.communicate()[0].decode("utf-8")
    xsel = Popen(args=['xsel', '-o', '-p'], stdout=PIPE)
    old_primary_content = xsel.communicate()[0].decode("utf-8")

    xsel = Popen(args=['xsel', '-i', '-b'], stdin=PIPE)
    xsel.communicate(input=emojis.encode('utf-8'))
    xsel = Popen(args=['xsel', '-i', '-p'], stdin=PIPE)
    xsel.communicate(input=emojis.encode('utf-8'))

    Popen(args=['xdotool', 'key', '--clearmodifiers', '--window', active_window,
                'Shift+Insert']).wait()

    xsel = Popen(args=['xsel', '-i', '-b'], stdin=PIPE)
    xsel.communicate(input=old_clipboard_content.encode('utf-8'))
    xsel = Popen(args=['xsel', '-i', '-p'], stdin=PIPE)
    xsel.communicate(input=old_primary_content.encode('utf-8'))


def copy_emojis_to_clipboard(emojis: str):
    xsel = Popen(
        args=[
            'xsel',
            '-i',
            '-b'
        ],
        stdin=PIPE
    )
    xsel.communicate(input=emojis.encode('utf-8'))


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Select, insert or copy Unicode emoji')
    parser.add_argument(
        '--use-clipboard',
        '-c',
        dest='use_clipboard',
        action='store_true',
        help='Do not type the emoji directly, but copy it to the clipboard, insert it from there and then restore the clipboard\'s original value'
    )
    parser.add_argument(
        '--skin-tone',
        '-s',
        dest='skin_tone',
        choices=['neutral', 'light', 'medium-light', 'moderate', 'dark brown', 'black', 'ask'],
        default='ask',
        action='store'
    )
    return parser.parse_args()


def get_active_window() -> str:
    xdotool = Popen(args=['xdotool', 'getactivewindow'], stdout=PIPE)
    return xdotool.communicate()[0].decode("utf-8")[:-1]


def compile_chosen_emojis(chosen_emojis, skin_tone) -> str:
    emojis = ""
    for line in chosen_emojis:
        emoji = line.split()[0].decode('utf-8')

        if emoji in skin_tone_selectable_emojis:
            emoji = select_skin_tone(emoji, skin_tone)

        emojis += emoji

    return emojis


if __name__ == "__main__":
    args = parse_arguments()

    active_window = get_active_window()

    rofi = Popen(
        args=[
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
            'Alt+p'
        ],
        stdin=PIPE,
        stdout=PIPE
    )
    (stdout, stderr) = rofi.communicate(input=emoji_list.encode('utf-8'))

    if rofi.returncode == 1:
        exit()
    else:
        emojis = compile_chosen_emojis(stdout.splitlines(), args.skin_tone)

        if rofi.returncode == 0:
            insert_emojis(emojis, active_window, args.use_clipboard)
        elif rofi.returncode == 10:
            copy_emojis_to_clipboard(emojis)
        elif rofi.returncode == 11:
            type_emojis(emojis, active_window)
        elif rofi.returncode == 12:
            copy_paste_emojis(emojis, active_window)
