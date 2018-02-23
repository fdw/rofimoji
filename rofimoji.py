#!/usr/bin/python3
# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE

emojis="""
😀 Grinning Face
😁 Beaming Face With Smiling Eyes
😂 Face With Tears of Joy
🤣 Rolling on the Floor Laughing
😃 Grinning Face With Big Eyes
😄 Grinning Face With Smiling Eyes
😅 Grinning Face With Sweat
😆 Grinning Squinting Face
😉 Winking Face
😊 Smiling Face With Smiling Eyes
😋 Face Savoring Food
😎 Smiling Face With Sunglasses
😍 Smiling Face With Heart-Eyes
😘 Face Blowing a Kiss
😗 Kissing Face
😙 Kissing Face With Smiling Eyes
😚 Kissing Face With Closed Eyes
☺ Smiling Face
🙂 Slightly Smiling Face
🤗 Hugging Face
🤩 Star-Struck
🤔 Thinking Face
🤨 Face With Raised Eyebrow
😐 Neutral Face
😑 Expressionless Face
😶 Face Without Mouth
🙄 Face With Rolling Eyes
😏 Smirking Face
😣 Persevering Face
😥 Sad but Relieved Face
😮 Face With Open Mouth
🤐 Zipper-Mouth Face
😯 Hushed Face
😪 Sleepy Face
😫 Tired Face
😴 Sleeping Face
😌 Relieved Face
😛 Face With Tongue
😜 Winking Face With Tongue
😝 Squinting Face With Tongue
🤤 Drooling Face
😒 Unamused Face
😓 Downcast Face With Sweat
😔 Pensive Face
😕 Confused Face
🙃 Upside-Down Face
🤑 Money-Mouth Face
😲 Astonished Face
☹ Frowning Face
🙁 Slightly Frowning Face
😖 Confounded Face
😞 Disappointed Face
😟 Worried Face
😤 Face With Steam From Nose
😢 Crying Face
😭 Loudly Crying Face
😦 Frowning Face With Open Mouth
😧 Anguished Face
😨 Fearful Face
😩 Weary Face
🤯 Exploding Head
😬 Grimacing Face
😰 Anxious Face With Sweat
😱 Face Screaming in Fear
😳 Flushed Face
🤪 Zany Face
😵 Dizzy Face
😡 Pouting Face
😠 Angry Face
🤬 Face With Symbols on Mouth
😷 Face With Medical Mask
🤒 Face With Thermometer
🤕 Face With Head-Bandage
🤢 Nauseated Face
🤮 Face Vomiting
🤧 Sneezing Face
😇 Smiling Face With Halo
🤠 Cowboy Hat Face
🤡 Clown Face
🤥 Lying Face
🤫 Shushing Face
🤭 Face With Hand Over Mouth
🧐 Face With Monocle
🤓 Nerd Face
😈 Smiling Face With Horns
👿 Angry Face With Horns
👹 Ogre
👺 Goblin
💀 Skull
👻 Ghost
👽 Alien
🤖 Robot Face
💩 Pile of Poo
😺 Grinning Cat Face
😸 Grinning Cat Face With Smiling Eyes
😹 Cat Face With Tears of Joy
😻 Smiling Cat Face With Heart-Eyes
😼 Cat Face With Wry Smile
😽 Kissing Cat Face
🙀 Weary Cat Face
😿 Crying Cat Face
😾 Pouting Cat Face
👶 Baby
👦 Boy
👧 Girl
👨 Man
👩 Woman
👴 Old Man
👵 Old Woman
👨‍⚕️ Man Health Worker
👩‍⚕️ Woman Health Worker
👨‍🎓 Man Student
👩‍🎓 Woman Student
👨‍⚖️ Man Judge
👩‍⚖️ Woman Judge
👨‍🌾 Man Farmer
👩‍🌾 Woman Farmer
👨‍🍳 Man Cook
👩‍🍳 Woman Cook
👨‍🔧 Man Mechanic
👩‍🔧 Woman Mechanic
👨‍🏭 Man Factory Worker
👩‍🏭 Woman Factory Worker
👨‍💼 Man Office Worker
👩‍💼 Woman Office Worker
👨‍🔬 Man Scientist
👩‍🔬 Woman Scientist
👨‍💻 Man Technologist
👩‍💻 Woman Technologist
👨‍🎤 Man Singer
👩‍🎤 Woman Singer
👨‍🎨 Man Artist
👩‍🎨 Woman Artist
👨‍✈️ Man Pilot
👩‍✈️ Woman Pilot
👨‍🚀 Man Astronaut
👩‍🚀 Woman Astronaut
👨‍🚒 Man Firefighter
👩‍🚒 Woman Firefighter
👮 Police Officer
👮‍♂️ Man Police Officer
👮‍♀️ Woman Police Officer
🕵 Detective
🕵️‍♂️ Man Detective
🕵️‍♀️ Woman Detective
💂 Guard
💂‍♂️ Man Guard
💂‍♀️ Woman Guard
👷 Construction Worker
👷‍♂️ Man Construction Worker
👷‍♀️ Woman Construction Worker
🤴 Prince
👸 Princess
👳 Person Wearing Turban
👳‍♂️ Man Wearing Turban
👳‍♀️ Woman Wearing Turban
👲 Man With Chinese Cap
🧕 Woman With Headscarf
🧔 Bearded Person
👱 Blond-Haired Person
👱‍♂️ Blond-Haired Man
👱‍♀️ Blond-Haired Woman
🤵 Man in Tuxedo
👰 Bride With Veil
🤰 Pregnant Woman
🤱 Breast-Feeding
👼 Baby Angel
🎅 Santa Claus
🤶 Mrs. Claus
🧙‍♀️ Woman Mage
🧙‍♂️ Man Mage
🧚‍♀️ Woman Fairy
🧚‍♂️ Man Fairy
🧛‍♀️ Woman Vampire
🧛‍♂️ Man Vampire
🧜‍♀️ Mermaid
🧜‍♂️ Merman
🧝‍♀️ Woman Elf
🧝‍♂️ Man Elf
🧞‍♀️ Woman Genie
🧞‍♂️ Man Genie
🧟‍♀️ Woman Zombie
🧟‍♂️ Man Zombie
🙍 Person Frowning
🙍‍♂️ Man Frowning
🙍‍♀️ Woman Frowning
🙎 Person Pouting
🙎‍♂️ Man Pouting
🙎‍♀️ Woman Pouting
🙅 Person Gesturing No
🙅‍♂️ Man Gesturing No
🙅‍♀️ Woman Gesturing No
🙆 Person Gesturing OK
🙆‍♂️ Man Gesturing OK
🙆‍♀️ Woman Gesturing OK
💁 Person Tipping Hand
💁‍♂️ Man Tipping Hand
💁‍♀️ Woman Tipping Hand
🙋 Person Raising Hand
🙋‍♂️ Man Raising Hand
🙋‍♀️ Woman Raising Hand
🙇 Person Bowing
🙇‍♂️ Man Bowing
🙇‍♀️ Woman Bowing
🤦 Person Facepalming
🤦‍♂️ Man Facepalming
🤦‍♀️ Woman Facepalming
🤷 Person Shrugging
🤷‍♂️ Man Shrugging
🤷‍♀️ Woman Shrugging
💆 Person Getting Massage
💆‍♂️ Man Getting Massage
💆‍♀️ Woman Getting Massage
💇 Person Getting Haircut
💇‍♂️ Man Getting Haircut
💇‍♀️ Woman Getting Haircut
🚶 Person Walking
🚶‍♂️ Man Walking
🚶‍♀️ Woman Walking
🏃 Person Running
🏃‍♂️ Man Running
🏃‍♀️ Woman Running
💃 Woman Dancing
🕺 Man Dancing
👯 People With Bunny Ears
👯‍♂️ Men With Bunny Ears
👯‍♀️ Women With Bunny Ears
🧖‍♀️ Woman in Steamy Room
🧖‍♂️ Man in Steamy Room
🕴 Man in Suit Levitating
🗣 Speaking Head
👤 Bust in Silhouette
👥 Busts in Silhouette
👫 Man and Woman Holding Hands
👬 Two Men Holding Hands
👭 Two Women Holding Hands
💏 Kiss
👨‍❤️‍💋‍👨 Kiss: Man, Man
👩‍❤️‍💋‍👩 Kiss: Woman, Woman
💑 Couple With Heart
👨‍❤️‍👨 Couple With Heart: Man, Man
👩‍❤️‍👩 Couple With Heart: Woman, Woman
👪 Family
👨‍👩‍👦 Family: Man, Woman, Boy
👨‍👩‍👧 Family: Man, Woman, Girl
👨‍👩‍👧‍👦 Family: Man, Woman, Girl, Boy
👨‍👩‍👦‍👦 Family: Man, Woman, Boy, Boy
👨‍👩‍👧‍👧 Family: Man, Woman, Girl, Girl
👨‍👨‍👦 Family: Man, Man, Boy
👨‍👨‍👧 Family: Man, Man, Girl
👨‍👨‍👧‍👦 Family: Man, Man, Girl, Boy
👨‍👨‍👦‍👦 Family: Man, Man, Boy, Boy
👨‍👨‍👧‍👧 Family: Man, Man, Girl, Girl
👩‍👩‍👦 Family: Woman, Woman, Boy
👩‍👩‍👧 Family: Woman, Woman, Girl
👩‍👩‍👧‍👦 Family: Woman, Woman, Girl, Boy
👩‍👩‍👦‍👦 Family: Woman, Woman, Boy, Boy
👩‍👩‍👧‍👧 Family: Woman, Woman, Girl, Girl
👨‍👦 Family: Man, Boy
👨‍👦‍👦 Family: Man, Boy, Boy
👨‍👧 Family: Man, Girl
👨‍👧‍👦 Family: Man, Girl, Boy
👨‍👧‍👧 Family: Man, Girl, Girl
👩‍👦 Family: Woman, Boy
👩‍👦‍👦 Family: Woman, Boy, Boy
👩‍👧 Family: Woman, Girl
👩‍👧‍👦 Family: Woman, Girl, Boy
👩‍👧‍👧 Family: Woman, Girl, Girl
🤳 Selfie
💪 Flexed Biceps
👈 Backhand Index Pointing Left
👉 Backhand Index Pointing Right
☝ Index Pointing Up
👆 Backhand Index Pointing Up
🖕 Middle Finger
👇 Backhand Index Pointing Down
✌ Victory Hand
🤞 Crossed Fingers
🖖 Vulcan Salute
🤘 Sign of the Horns
🖐 Hand With Fingers Splayed
✋ Raised Hand
👌 OK Hand
👍 Thumbs Up
👎 Thumbs Down
✊ Raised Fist
👊 Oncoming Fist
🤛 Left-Facing Fist
🤜 Right-Facing Fist
🤚 Raised Back of Hand
👋 Waving Hand
🤟 Love-You Gesture
✍ Writing Hand
👏 Clapping Hands
👐 Open Hands
🙌 Raising Hands
🤲 Palms Up Together
🙏 Folded Hands
🤝 Handshake
💅 Nail Polish
👂 Ear
👃 Nose
👣 Footprints
👀 Eyes
👁 Eye
🧠 Brain
👅 Tongue
👄 Mouth
💋 Kiss Mark
👓 Glasses
🕶 Sunglasses
👔 Necktie
👕 T-Shirt
👖 Jeans
🧣 Scarf
🧤 Gloves
🧥 Coat
🧦 Socks
👗 Dress
👘 Kimono
👙 Bikini
👚 Woman’s Clothes
👛 Purse
👜 Handbag
👝 Clutch Bag
🎒 School Backpack
👞 Man’s Shoe
👟 Running Shoe
👠 High-Heeled Shoe
👡 Woman’s Sandal
👢 Woman’s Boot
👑 Crown
👒 Woman’s Hat
🎩 Top Hat
🎓 Graduation Cap
🧢 Billed Cap
⛑ Rescue Worker’s Helmet
💄 Lipstick
💍 Ring
🌂 Closed Umbrella
☂ Umbrella
💼 Briefcase
🙈 See-No-Evil Monkey
🙉 Hear-No-Evil Monkey
🙊 Speak-No-Evil Monkey
💥 Collision
💦 Sweat Droplets
💨 Dashing Away
💫 Dizzy
🐵 Monkey Face
🐒 Monkey
🦍 Gorilla
🐶 Dog Face
🐕 Dog
🐩 Poodle
🐺 Wolf Face
🦊 Fox Face
🐱 Cat Face
🐈 Cat
🦁 Lion Face
🐯 Tiger Face
🐅 Tiger
🐆 Leopard
🐴 Horse Face
🐎 Horse
🦄 Unicorn Face
🦓 Zebra
🐮 Cow Face
🐂 Ox
🐃 Water Buffalo
🐄 Cow
🐷 Pig Face
🐖 Pig
🐗 Boar
🐽 Pig Nose
🐏 Ram
🐑 Ewe
🐐 Goat
🐪 Camel
🐫 Two-Hump Camel
🦒 Giraffe
🐘 Elephant
🦏 Rhinoceros
🐭 Mouse Face
🐁 Mouse
🐀 Rat
🐹 Hamster Face
🐰 Rabbit Face
🐇 Rabbit
🐿 Chipmunk
🦔 Hedgehog
🦇 Bat
🐻 Bear Face
🐨 Koala
🐼 Panda Face
🐾 Paw Prints
🦃 Turkey
🐔 Chicken
🐓 Rooster
🐣 Hatching Chick
🐤 Baby Chick
🐥 Front-Facing Baby Chick
🐦 Bird
🐧 Penguin
🕊 Dove
🦅 Eagle
🦆 Duck
🦉 Owl
🐸 Frog Face
🐊 Crocodile
🐢 Turtle
🦎 Lizard
🐍 Snake
🐲 Dragon Face
🐉 Dragon
🦕 Sauropod
🦖 T-Rex
🐳 Spouting Whale
🐋 Whale
🐬 Dolphin
🐟 Fish
🐠 Tropical Fish
🐡 Blowfish
🦈 Shark
🐙 Octopus
🐚 Spiral Shell
🦀 Crab
🦐 Shrimp
🦑 Squid
🐌 Snail
🦋 Butterfly
🐛 Bug
🐜 Ant
🐝 Honeybee
🐞 Lady Beetle
🦗 Cricket
🕷 Spider
🕸 Spider Web
🦂 Scorpion
💐 Bouquet
🌸 Cherry Blossom
💮 White Flower
🏵 Rosette
🌹 Rose
🥀 Wilted Flower
🌺 Hibiscus
🌻 Sunflower
🌼 Blossom
🌷 Tulip
🌱 Seedling
🌲 Evergreen Tree
🌳 Deciduous Tree
🌴 Palm Tree
🌵 Cactus
🌾 Sheaf of Rice
🌿 Herb
☘ Shamrock
🍀 Four Leaf Clover
🍁 Maple Leaf
🍂 Fallen Leaf
🍃 Leaf Fluttering in Wind
🍄 Mushroom
🌰 Chestnut
🌍 Globe Showing Europe-Africa
🌎 Globe Showing Americas
🌏 Globe Showing Asia-Australia
🌐 Globe With Meridians
🌑 New Moon
🌒 Waxing Crescent Moon
🌓 First Quarter Moon
🌔 Waxing Gibbous Moon
🌕 Full Moon
🌖 Waning Gibbous Moon
🌗 Last Quarter Moon
🌘 Waning Crescent Moon
🌙 Crescent Moon
🌚 New Moon Face
🌛 First Quarter Moon Face
🌜 Last Quarter Moon Face
☀ Sun
🌝 Full Moon Face
🌞 Sun With Face
⭐ White Medium Star
🌟 Glowing Star
🌠 Shooting Star
☁ Cloud
⛅ Sun Behind Cloud
⛈ Cloud With Lightning and Rain
🌤 Sun Behind Small Cloud
🌥 Sun Behind Large Cloud
🌦 Sun Behind Rain Cloud
🌧 Cloud With Rain
🌨 Cloud With Snow
🌩 Cloud With Lightning
🌪 Tornado
🌫 Fog
🌬 Wind Face
🌈 Rainbow
☂ Umbrella
☔ Umbrella With Rain Drops
⚡ High Voltage
❄ Snowflake
☃ Snowman
⛄ Snowman Without Snow
☄ Comet
🔥 Fire
💧 Droplet
🌊 Water Wave
🎄 Christmas Tree
✨ Sparkles
🎋 Tanabata Tree
🎍 Pine Decoration
🍇 Grapes
🍈 Melon
🍉 Watermelon
🍊 Tangerine
🍋 Lemon
🍌 Banana
🍍 Pineapple
🍎 Red Apple
🍏 Green Apple
🍐 Pear
🍑 Peach
🍒 Cherries
🍓 Strawberry
🥝 Kiwi Fruit
🍅 Tomato
🥥 Coconut
🥑 Avocado
🍆 Eggplant
🥔 Potato
🥕 Carrot
🌽 Ear of Corn
🌶 Hot Pepper
🥒 Cucumber
🥦 Broccoli
🍄 Mushroom
🥜 Peanuts
🌰 Chestnut
🍞 Bread
🥐 Croissant
🥖 Baguette Bread
🥨 Pretzel
🥞 Pancakes
🧀 Cheese Wedge
🍖 Meat on Bone
🍗 Poultry Leg
🥩 Cut of Meat
🥓 Bacon
🍔 Hamburger
🍟 French Fries
🍕 Pizza
🌭 Hot Dog
🥪 Sandwich
🌮 Taco
🌯 Burrito
🍳 Cooking
🍲 Pot of Food
🥣 Bowl With Spoon
🥗 Green Salad
🍿 Popcorn
🥫 Canned Food
🍱 Bento Box
🍘 Rice Cracker
🍙 Rice Ball
🍚 Cooked Rice
🍛 Curry Rice
🍜 Steaming Bowl
🍝 Spaghetti
🍠 Roasted Sweet Potato
🍢 Oden
🍣 Sushi
🍤 Fried Shrimp
🍥 Fish Cake With Swirl
🍡 Dango
🥟 Dumpling
🥠 Fortune Cookie
🥡 Takeout Box
🍦 Soft Ice Cream
🍧 Shaved Ice
🍨 Ice Cream
🍩 Doughnut
🍪 Cookie
🎂 Birthday Cake
🍰 Shortcake
🥧 Pie
🍫 Chocolate Bar
🍬 Candy
🍭 Lollipop
🍮 Custard
🍯 Honey Pot
🍼 Baby Bottle
🥛 Glass of Milk
☕ Hot Beverage
🍵 Teacup Without Handle
🍶 Sake
🍾 Bottle With Popping Cork
🍷 Wine Glass
🍸 Cocktail Glass
🍹 Tropical Drink
🍺 Beer Mug
🍻 Clinking Beer Mugs
🥂 Clinking Glasses
🥃 Tumbler Glass
🥤 Cup With Straw
🥢 Chopsticks
🍽 Fork and Knife With Plate
🍴 Fork and Knife
🥄 Spoon
👾 Alien Monster
🧗‍♀️ Woman Climbing
🧗‍♂️ Man Climbing
🧘‍♀️ Woman in Lotus Position
🧘‍♂️ Man in Lotus Position
🕴 Man in Suit Levitating
🏇 Horse Racing
⛷ Skier
🏂 Snowboarder
🏌 Person Golfing
🏌️‍♂️ Man Golfing
🏌️‍♀️ Woman Golfing
🏄 Person Surfing
🏄‍♂️ Man Surfing
🏄‍♀️ Woman Surfing
🚣 Person Rowing Boat
🚣‍♂️ Man Rowing Boat
🚣‍♀️ Woman Rowing Boat
🏊 Person Swimming
🏊‍♂️ Man Swimming
🏊‍♀️ Woman Swimming
⛹ Person Bouncing Ball
⛹️‍♂️ Man Bouncing Ball
⛹️‍♀️ Woman Bouncing Ball
🏋 Person Lifting Weights
🏋️‍♂️ Man Lifting Weights
🏋️‍♀️ Woman Lifting Weights
🚴 Person Biking
🚴‍♂️ Man Biking
🚴‍♀️ Woman Biking
🚵 Person Mountain Biking
🚵‍♂️ Man Mountain Biking
🚵‍♀️ Woman Mountain Biking
🤸 Person Cartwheeling
🤸‍♂️ Man Cartwheeling
🤸‍♀️ Woman Cartwheeling
🤼 People Wrestling
🤼‍♂️ Men Wrestling
🤼‍♀️ Women Wrestling
🤽 Person Playing Water Polo
🤽‍♂️ Man Playing Water Polo
🤽‍♀️ Woman Playing Water Polo
🤾 Person Playing Handball
🤾‍♂️ Man Playing Handball
🤾‍♀️ Woman Playing Handball
🤹 Person Juggling
🤹‍♂️ Man Juggling
🤹‍♀️ Woman Juggling
🎪 Circus Tent
🎗 Reminder Ribbon
🎟 Admission Tickets
🎫 Ticket
🎖 Military Medal
🏆 Trophy
🏅 Sports Medal
🥇 1st Place Medal
🥈 2nd Place Medal
🥉 3rd Place Medal
⚽ Soccer Ball
⚾ Baseball
🏀 Basketball
🏐 Volleyball
🏈 American Football
🏉 Rugby Football
🎾 Tennis
🎳 Bowling
🏏 Cricket Game
🏑 Field Hockey
🏒 Ice Hockey
🏓 Ping Pong
🏸 Badminton
🥊 Boxing Glove
🥋 Martial Arts Uniform
⛳ Flag in Hole
⛸ Ice Skate
🎣 Fishing Pole
🎽 Running Shirt
🎿 Skis
🛷 Sled
🥌 Curling Stone
🎯 Direct Hit
🎱 Pool 8 Ball
🎮 Video Game
🎰 Slot Machine
🎲 Game Die
🎭 Performing Arts
🎨 Artist Palette
🎼 Musical Score
🎤 Microphone
🎧 Headphone
🎷 Saxophone
🎸 Guitar
🎹 Musical Keyboard
🎺 Trumpet
🎻 Violin
🥁 Drum
🎬 Clapper Board
🏹 Bow and Arrow
🚣 Person Rowing Boat
🏎 Racing Car
🏍 Motorcycle
🗾 Map of Japan
🏔 Snow-Capped Mountain
⛰ Mountain
🌋 Volcano
🗻 Mount Fuji
🏕 Camping
🏖 Beach With Umbrella
🏜 Desert
🏝 Desert Island
🏞 National Park
🏟 Stadium
🏛 Classical Building
🏗 Building Construction
🏘 Houses
🏚 Derelict House
🏠 House
🏡 House With Garden
🏢 Office Building
🏣 Japanese Post Office
🏤 Post Office
🏥 Hospital
🏦 Bank
🏨 Hotel
🏩 Love Hotel
🏪 Convenience Store
🏫 School
🏬 Department Store
🏭 Factory
🏯 Japanese Castle
🏰 Castle
💒 Wedding
🗼 Tokyo Tower
🗽 Statue of Liberty
⛪ Church
🕌 Mosque
🕍 Synagogue
⛩ Shinto Shrine
🕋 Kaaba
⛲ Fountain
⛺ Tent
🌁 Foggy
🌃 Night With Stars
🏙 Cityscape
🌄 Sunrise Over Mountains
🌅 Sunrise
🌆 Cityscape at Dusk
🌇 Sunset
🌉 Bridge at Night
🌌 Milky Way
🎠 Carousel Horse
🎡 Ferris Wheel
🎢 Roller Coaster
🚂 Locomotive
🚃 Railway Car
🚄 High-Speed Train
🚅 Bullet Train
🚆 Train
🚇 Metro
🚈 Light Rail
🚉 Station
🚊 Tram
🚝 Monorail
🚞 Mountain Railway
🚋 Tram Car
🚌 Bus
🚍 Oncoming Bus
🚎 Trolleybus
🚐 Minibus
🚑 Ambulance
🚒 Fire Engine
🚓 Police Car
🚔 Oncoming Police Car
🚕 Taxi
🚖 Oncoming Taxi
🚗 Automobile
🚘 Oncoming Automobile
🚚 Delivery Truck
🚛 Articulated Lorry
🚜 Tractor
🚲 Bicycle
🛴 Kick Scooter
🛵 Motor Scooter
🚏 Bus Stop
🛤 Railway Track
⛽ Fuel Pump
🚨 Police Car Light
🚥 Horizontal Traffic Light
🚦 Vertical Traffic Light
🚧 Construction
⚓ Anchor
⛵ Sailboat
🚤 Speedboat
🛳 Passenger Ship
⛴ Ferry
🛥 Motor Boat
🚢 Ship
✈ Airplane
🛩 Small Airplane
🛫 Airplane Departure
🛬 Airplane Arrival
💺 Seat
🚁 Helicopter
🚟 Suspension Railway
🚠 Mountain Cableway
🚡 Aerial Tramway
🛰 Satellite
🚀 Rocket
🛸 Flying Saucer
🌠 Shooting Star
⛱ Umbrella on Ground
🎆 Fireworks
🎇 Sparkler
🎑 Moon Viewing Ceremony
💴 Yen Banknote
💵 Dollar Banknote
💶 Euro Banknote
💷 Pound Banknote
🗿 Moai
🛂 Passport Control
🛃 Customs
🛄 Baggage Claim
🛅 Left Luggage
☠ Skull and Crossbones
🛀 Person Taking Bath
🛌 Person in Bed
💌 Love Letter
💣 Bomb
🕳 Hole
🛍 Shopping Bags
📿 Prayer Beads
💎 Gem Stone
🔪 Kitchen Knife
🏺 Amphora
🗺 World Map
💈 Barber Pole
🛢 Oil Drum
🛎 Bellhop Bell
⌛ Hourglass Done
⏳ Hourglass Not Done
⌚ Watch
⏰ Alarm Clock
⏱ Stopwatch
⏲ Timer Clock
🕰 Mantelpiece Clock
🌡 Thermometer
⛱ Umbrella on Ground
🎈 Balloon
🎉 Party Popper
🎊 Confetti Ball
🎎 Japanese Dolls
🎏 Carp Streamer
🎐 Wind Chime
🎀 Ribbon
🎁 Wrapped Gift
🔮 Crystal Ball
🕹 Joystick
🖼 Framed Picture
📯 Postal Horn
🎙 Studio Microphone
🎚 Level Slider
🎛 Control Knobs
📻 Radio
📱 Mobile Phone
📲 Mobile Phone With Arrow
☎ Telephone
📞 Telephone Receiver
📟 Pager
📠 Fax Machine
🔋 Battery
🔌 Electric Plug
💻 Laptop Computer
🖥 Desktop Computer
🖨 Printer
⌨ Keyboard
🖱 Computer Mouse
🖲 Trackball
💽 Computer Disk
💾 Floppy Disk
💿 Optical Disk
📀 DVD
🎥 Movie Camera
🎞 Film Frames
📽 Film Projector
📺 Television
📷 Camera
📸 Camera With Flash
📹 Video Camera
📼 Videocassette
🔍 Magnifying Glass Tilted Left
🔎 Magnifying Glass Tilted Right
🕯 Candle
💡 Light Bulb
🔦 Flashlight
🏮 Red Paper Lantern
📔 Notebook With Decorative Cover
📕 Closed Book
📖 Open Book
📗 Green Book
📘 Blue Book
📙 Orange Book
📚 Books
📓 Notebook
📃 Page With Curl
📜 Scroll
📄 Page Facing Up
📰 Newspaper
🗞 Rolled-Up Newspaper
📑 Bookmark Tabs
🔖 Bookmark
🏷 Label
💰 Money Bag
💴 Yen Banknote
💵 Dollar Banknote
💶 Euro Banknote
💷 Pound Banknote
💸 Money With Wings
💳 Credit Card
✉ Envelope
📧 E-Mail
📨 Incoming Envelope
📩 Envelope With Arrow
📤 Outbox Tray
📥 Inbox Tray
📦 Package
📫 Closed Mailbox With Raised Flag
📪 Closed Mailbox With Lowered Flag
📬 Open Mailbox With Raised Flag
📭 Open Mailbox With Lowered Flag
📮 Postbox
🗳 Ballot Box With Ballot
✏ Pencil
✒ Black Nib
🖋 Fountain Pen
🖊 Pen
🖌 Paintbrush
🖍 Crayon
📝 Memo
📁 File Folder
📂 Open File Folder
🗂 Card Index Dividers
📅 Calendar
📆 Tear-Off Calendar
🗒 Spiral Notepad
🗓 Spiral Calendar
📇 Card Index
📈 Chart Increasing
📉 Chart Decreasing
📊 Bar Chart
📋 Clipboard
📌 Pushpin
📍 Round Pushpin
📎 Paperclip
🖇 Linked Paperclips
📏 Straight Ruler
📐 Triangular Ruler
✂ Scissors
🗃 Card File Box
🗄 File Cabinet
🗑 Wastebasket
🔒 Locked
🔓 Unlocked
🔏 Locked With Pen
🔐 Locked With Key
🔑 Key
🗝 Old Key
🔨 Hammer
⛏ Pick
⚒ Hammer and Pick
🛠 Hammer and Wrench
🗡 Dagger
⚔ Crossed Swords
🔫 Pistol
🛡 Shield
🔧 Wrench
🔩 Nut and Bolt
⚙ Gear
🗜 Clamp
⚖ Balance Scale
🔗 Link
⛓ Chains
⚗ Alembic
🔬 Microscope
🔭 Telescope
📡 Satellite Antenna
💉 Syringe
💊 Pill
🚪 Door
🛏 Bed
🛋 Couch and Lamp
🚽 Toilet
🚿 Shower
🛁 Bathtub
🚬 Cigarette
⚰ Coffin
⚱ Funeral Urn
🗿 Moai
🚰 Potable Water
👁️‍🗨️ Eye in Speech Bubble
💘 Heart With Arrow
❤ Red Heart
💓 Beating Heart
💔 Broken Heart
💕 Two Hearts
💖 Sparkling Heart
💗 Growing Heart
💙 Blue Heart
💚 Green Heart
💛 Yellow Heart
🧡 Orange Heart
💜 Purple Heart
🖤 Black Heart
💝 Heart With Ribbon
💞 Revolving Hearts
💟 Heart Decoration
❣ Heavy Heart Exclamation
💤 Zzz
💢 Anger Symbol
💬 Speech Balloon
🗯 Right Anger Bubble
💭 Thought Balloon
💮 White Flower
♨ Hot Springs
💈 Barber Pole
🛑 Stop Sign
🕛 Twelve O’clock
🕧 Twelve-Thirty
🕐 One O’clock
🕜 One-Thirty
🕑 Two O’clock
🕝 Two-Thirty
🕒 Three O’clock
🕞 Three-Thirty
🕓 Four O’clock
🕟 Four-Thirty
🕔 Five O’clock
🕠 Five-Thirty
🕕 Six O’clock
🕡 Six-Thirty
🕖 Seven O’clock
🕢 Seven-Thirty
🕗 Eight O’clock
🕣 Eight-Thirty
🕘 Nine O’clock
🕤 Nine-Thirty
🕙 Ten O’clock
🕥 Ten-Thirty
🕚 Eleven O’clock
🕦 Eleven-Thirty
🌀 Cyclone
♠ Spade Suit
♥ Heart Suit
♦ Diamond Suit
♣ Club Suit
🃏 Joker
🀄 Mahjong Red Dragon
🎴 Flower Playing Cards
🔇 Muted Speaker
🔈 Speaker Low Volume
🔉 Speaker Medium Volume
🔊 Speaker High Volume
📢 Loudspeaker
📣 Megaphone
📯 Postal Horn
🔔 Bell
🔕 Bell With Slash
🎵 Musical Note
🎶 Musical Notes
🏧 Atm Sign
🚮 Litter in Bin Sign
🚰 Potable Water
♿ Wheelchair Symbol
🚹 Men’s Room
🚺 Women’s Room
🚻 Restroom
🚼 Baby Symbol
🚾 Water Closet
⚠ Warning
🚸 Children Crossing
⛔ No Entry
🚫 Prohibited
🚳 No Bicycles
🚭 No Smoking
🚯 No Littering
🚱 Non-Potable Water
🚷 No Pedestrians
🔞 No One Under Eighteen
☢ Radioactive
☣ Biohazard
⬆ Up Arrow
↗ Up-Right Arrow
➡ Right Arrow
↘ Down-Right Arrow
⬇ Down Arrow
↙ Down-Left Arrow
⬅ Left Arrow
↖ Up-Left Arrow
↕ Up-Down Arrow
↔ Left-Right Arrow
↩ Right Arrow Curving Left
↪ Left Arrow Curving Right
⤴ Right Arrow Curving Up
⤵ Right Arrow Curving Down
🔃 Clockwise Vertical Arrows
🔄 Counterclockwise Arrows Button
🔙 Back Arrow
🔚 End Arrow
🔛 On! Arrow
🔜 Soon Arrow
🔝 Top Arrow
🛐 Place of Worship
⚛ Atom Symbol
🕉 Om
✡ Star of David
☸ Wheel of Dharma
☯ Yin Yang
✝ Latin Cross
☦ Orthodox Cross
☪ Star and Crescent
☮ Peace Symbol
🕎 Menorah
🔯 Dotted Six-Pointed Star
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
🔀 Shuffle Tracks Button
🔁 Repeat Button
🔂 Repeat Single Button
▶ Play Button
⏩ Fast-Forward Button
◀ Reverse Button
⏪ Fast Reverse Button
🔼 Upwards Button
⏫ Fast Up Button
🔽 Downwards Button
⏬ Fast Down Button
⏹ Stop Button
⏏ Eject Button
🎦 Cinema
🔅 Dim Button
🔆 Bright Button
📶 Antenna Bars
📳 Vibration Mode
📴 Mobile Phone Off
♻ Recycling Symbol
🔱 Trident Emblem
📛 Name Badge
🔰 Japanese Symbol for Beginner
⭕ Heavy Large Circle
✅ White Heavy Check Mark
☑ Ballot Box With Check
✔ Heavy Check Mark
✖ Heavy Multiplication X
❌ Cross Mark
❎ Cross Mark Button
➕ Heavy Plus Sign
➖ Heavy Minus Sign
➗ Heavy Division Sign
➰ Curly Loop
➿ Double Curly Loop
〽 Part Alternation Mark
✳ Eight-Spoked Asterisk
✴ Eight-Pointed Star
❇ Sparkle
‼ Double Exclamation Mark
⁉ Exclamation Question Mark
❓ Question Mark
❔ White Question Mark
❕ White Exclamation Mark
❗ Exclamation Mark
© Copyright
® Registered
™ Trade Mark
#️⃣ Keycap Number Sign
0️⃣ Keycap Digit Zero
1️⃣ Keycap Digit One
2️⃣ Keycap Digit Two
3️⃣ Keycap Digit Three
4️⃣ Keycap Digit Four
5️⃣ Keycap Digit Five
6️⃣ Keycap Digit Six
7️⃣ Keycap Digit Seven
8️⃣ Keycap Digit Eight
9️⃣ Keycap Digit Nine
🔟 Keycap 10
💯 Hundred Points
🔠 Input Latin Uppercase
🔡 Input Latin Lowercase
🔢 Input Numbers
🔣 Input Symbols
🔤 Input Latin Letters
🅰 A Button (blood Type)
🆎 Ab Button (blood Type)
🅱 B Button (blood Type)
🆑 CL Button
🆒 Cool Button
🆓 Free Button
ℹ Information
🆔 ID Button
Ⓜ Circled M
🆕 New Button
🆖 NG Button
🅾 O Button (blood Type)
🆗 OK Button
🅿 P Button
🆘 SOS Button
🆙 Up! Button
🆚 Vs Button
🈁 Japanese “here” Button
🈂 Japanese “service Charge” Button
🈷 Japanese “monthly Amount” Button
🈶 Japanese “not Free of Charge” Button
🈯 Japanese “reserved” Button
🉐 Japanese “bargain” Button
🈹 Japanese “discount” Button
🈚 Japanese “free of Charge” Button
🈲 Japanese “prohibited” Button
🉑 Japanese “acceptable” Button
🈸 Japanese “application” Button
🈴 Japanese “passing Grade” Button
🈳 Japanese “vacancy” Button
㊗ Japanese “congratulations” Button
㊙ Japanese “secret” Button
🈺 Japanese “open for Business” Button
🈵 Japanese “no Vacancy” Button
▪ Black Small Square
▫ White Small Square
◻ White Medium Square
◼ Black Medium Square
◽ White Medium-Small Square
◾ Black Medium-Small Square
⬛ Black Large Square
⬜ White Large Square
🔶 Large Orange Diamond
🔷 Large Blue Diamond
🔸 Small Orange Diamond
🔹 Small Blue Diamond
🔺 Red Triangle Pointed Up
🔻 Red Triangle Pointed Down
💠 Diamond With a Dot
🔲 Black Square Button
🔳 White Square Button
⚪ White Circle
⚫ Black Circle
🔴 Red Circle
🔵 Blue Circle
🏁 Chequered Flag
🚩 Triangular Flag
🎌 Crossed Flags
🏴 Black Flag
🏳 White Flag
🏳️‍🌈 Rainbow Flag
🏴‍☠️ Pirate Flag
🇦🇨 Ascension Island
🇦🇩 Andorra
🇦🇪 United Arab Emirates
🇦🇫 Afghanistan
🇦🇬 Antigua & Barbuda
🇦🇮 Anguilla
🇦🇱 Albania
🇦🇲 Armenia
🇦🇴 Angola
🇦🇶 Antarctica
🇦🇷 Argentina
🇦🇸 American Samoa
🇦🇹 Austria
🇦🇺 Australia
🇦🇼 Aruba
🇦🇽 Åland Islands
🇦🇿 Azerbaijan
🇧🇦 Bosnia & Herzegovina
🇧🇧 Barbados
🇧🇩 Bangladesh
🇧🇪 Belgium
🇧🇫 Burkina Faso
🇧🇬 Bulgaria
🇧🇭 Bahrain
🇧🇮 Burundi
🇧🇯 Benin
🇧🇱 St. Barthélemy
🇧🇲 Bermuda
🇧🇳 Brunei
🇧🇴 Bolivia
🇧🇶 Caribbean Netherlands
🇧🇷 Brazil
🇧🇸 Bahamas
🇧🇹 Bhutan
🇧🇻 Bouvet Island
🇧🇼 Botswana
🇧🇾 Belarus
🇧🇿 Belize
🇨🇦 Canada
🇨🇨 Cocos (Keeling) Islands
🇨🇩 Congo - Kinshasa
🇨🇫 Central African Republic
🇨🇬 Congo - Brazzaville
🇨🇭 Switzerland
🇨🇮 Côte D’Ivoire
🇨🇰 Cook Islands
🇨🇱 Chile
🇨🇲 Cameroon
🇨🇳 China
🇨🇴 Colombia
🇨🇵 Clipperton Island
🇨🇷 Costa Rica
🇨🇺 Cuba
🇨🇻 Cape Verde
🇨🇼 Curaçao
🇨🇽 Christmas Island
🇨🇾 Cyprus
🇨🇿 Czechia
🇩🇪 Germany
🇩🇬 Diego Garcia
🇩🇯 Djibouti
🇩🇰 Denmark
🇩🇲 Dominica
🇩🇴 Dominican Republic
🇩🇿 Algeria
🇪🇦 Ceuta & Melilla
🇪🇨 Ecuador
🇪🇪 Estonia
🇪🇬 Egypt
🇪🇭 Western Sahara
🇪🇷 Eritrea
🇪🇸 Spain
🇪🇹 Ethiopia
🇪🇺 European Union
🇫🇮 Finland
🇫🇯 Fiji
🇫🇰 Falkland Islands
🇫🇲 Micronesia
🇫🇴 Faroe Islands
🇫🇷 France
🇬🇦 Gabon
🇬🇧 United Kingdom
🇬🇩 Grenada
🇬🇪 Georgia
🇬🇫 French Guiana
🇬🇬 Guernsey
🇬🇭 Ghana
🇬🇮 Gibraltar
🇬🇱 Greenland
🇬🇲 Gambia
🇬🇳 Guinea
🇬🇵 Guadeloupe
🇬🇶 Equatorial Guinea
🇬🇷 Greece
🇬🇸 South Georgia & South Sandwich Islands
🇬🇹 Guatemala
🇬🇺 Guam
🇬🇼 Guinea-Bissau
🇬🇾 Guyana
🇭🇰 Hong Kong Sar China
🇭🇲 Heard & Mcdonald Islands
🇭🇳 Honduras
🇭🇷 Croatia
🇭🇹 Haiti
🇭🇺 Hungary
🇮🇨 Canary Islands
🇮🇩 Indonesia
🇮🇪 Ireland
🇮🇱 Israel
🇮🇲 Isle of Man
🇮🇳 India
🇮🇴 British Indian Ocean Territory
🇮🇶 Iraq
🇮🇷 Iran
🇮🇸 Iceland
🇮🇹 Italy
🇯🇪 Jersey
🇯🇲 Jamaica
🇯🇴 Jordan
🇯🇵 Japan
🇰🇪 Kenya
🇰🇬 Kyrgyzstan
🇰🇭 Cambodia
🇰🇮 Kiribati
🇰🇲 Comoros
🇰🇳 St. Kitts & Nevis
🇰🇵 North Korea
🇰🇷 South Korea
🇰🇼 Kuwait
🇰🇾 Cayman Islands
🇰🇿 Kazakhstan
🇱🇦 Laos
🇱🇧 Lebanon
🇱🇨 St. Lucia
🇱🇮 Liechtenstein
🇱🇰 Sri Lanka
🇱🇷 Liberia
🇱🇸 Lesotho
🇱🇹 Lithuania
🇱🇺 Luxembourg
🇱🇻 Latvia
🇱🇾 Libya
🇲🇦 Morocco
🇲🇨 Monaco
🇲🇩 Moldova
🇲🇪 Montenegro
🇲🇫 St. Martin
🇲🇬 Madagascar
🇲🇭 Marshall Islands
🇲🇰 Macedonia
🇲🇱 Mali
🇲🇲 Myanmar (Burma)
🇲🇳 Mongolia
🇲🇴 Macau Sar China
🇲🇵 Northern Mariana Islands
🇲🇶 Martinique
🇲🇷 Mauritania
🇲🇸 Montserrat
🇲🇹 Malta
🇲🇺 Mauritius
🇲🇻 Maldives
🇲🇼 Malawi
🇲🇽 Mexico
🇲🇾 Malaysia
🇲🇿 Mozambique
🇳🇦 Namibia
🇳🇨 New Caledonia
🇳🇪 Niger
🇳🇫 Norfolk Island
🇳🇬 Nigeria
🇳🇮 Nicaragua
🇳🇱 Netherlands
🇳🇴 Norway
🇳🇵 Nepal
🇳🇷 Nauru
🇳🇺 Niue
🇳🇿 New Zealand
🇴🇲 Oman
🇵🇦 Panama
🇵🇪 Peru
🇵🇫 French Polynesia
🇵🇬 Papua New Guinea
🇵🇭 Philippines
🇵🇰 Pakistan
🇵🇱 Poland
🇵🇲 St. Pierre & Miquelon
🇵🇳 Pitcairn Islands
🇵🇷 Puerto Rico
🇵🇸 Palestinian Territories
🇵🇹 Portugal
🇵🇼 Palau
🇵🇾 Paraguay
🇶🇦 Qatar
🇷🇪 Réunion
🇷🇴 Romania
🇷🇸 Serbia
🇷🇺 Russia
🇷🇼 Rwanda
🇸🇦 Saudi Arabia
🇸🇧 Solomon Islands
🇸🇨 Seychelles
🇸🇩 Sudan
🇸🇪 Sweden
🇸🇬 Singapore
🇸🇭 St. Helena
🇸🇮 Slovenia
🇸🇯 Svalbard & Jan Mayen
🇸🇰 Slovakia
🇸🇱 Sierra Leone
🇸🇲 San Marino
🇸🇳 Senegal
🇸🇴 Somalia
🇸🇷 Suriname
🇸🇸 South Sudan
🇸🇹 São Tomé & Príncipe
🇸🇻 El Salvador
🇸🇽 Sint Maarten
🇸🇾 Syria
🇸🇿 Swaziland
🇹🇦 Tristan Da Cunha
🇹🇨 Turks & Caicos Islands
🇹🇩 Chad
🇹🇫 French Southern Territories
🇹🇬 Togo
🇹🇭 Thailand
🇹🇯 Tajikistan
🇹🇰 Tokelau
🇹🇱 Timor-Leste
🇹🇲 Turkmenistan
🇹🇳 Tunisia
🇹🇴 Tonga
🇹🇷 Turkey
🇹🇹 Trinidad & Tobago
🇹🇻 Tuvalu
🇹🇼 Taiwan
🇹🇿 Tanzania
🇺🇦 Ukraine
🇺🇬 Uganda
🇺🇲 U.S. Outlying Islands
🇺🇳 United Nations
🇺🇸 United States
🇺🇾 Uruguay
🇺🇿 Uzbekistan
🇻🇦 Vatican City
🇻🇨 St. Vincent & Grenadines
🇻🇪 Venezuela
🇻🇬 British Virgin Islands
🇻🇮 U.S. Virgin Islands
🇻🇳 Vietnam
🇻🇺 Vanuatu
🇼🇫 Wallis & Futuna
🇼🇸 Samoa
🇽🇰 Kosovo
🇾🇪 Yemen
🇾🇹 Mayotte
🇿🇦 South Africa
🇿🇲 Zambia
🇿🇼 Zimbabwe
🏴󠁧󠁢󠁥󠁮󠁧󠁿 England
🏴󠁧󠁢󠁳󠁣󠁴󠁿 Scotland
🏴󠁧󠁢󠁷󠁬󠁳󠁿 Wales
"""

rofi = Popen(
    args=[
        'rofi',
        '-dmenu',
        '-i',
        '-p',
        ' 😀   ',
        '-kb-custom-1',
        'Alt+c'
    ],
    stdin=PIPE,
    stdout=PIPE
)
(stdout, stderr) = rofi.communicate(input=emojis.encode('utf-8'))

if rofi.returncode == 1:
    exit()
else:
    emoji = stdout.split()[0]
    if rofi.returncode == 0:
        Popen(
            args=[
                'xdotool',
                'type',
                '--clearmodifiers',
                emoji.decode('utf-8')
            ]
        )
    elif rofi.returncode == 10:
        xsel = Popen(
            args=[
                'xsel',
                '-i',
                '-b'
            ],
            stdin=PIPE
        )
        xsel.communicate(input=emoji)
