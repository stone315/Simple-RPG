import json

hero = { 1: {
  "Career": "Knight",
  "LV": 1,
  "HP": 20,
  "ATK": 4,
  "DEF": 6,
  "SPD": 2,
  "grow": [5,1,3,1]
}, 2: {
  "Career": "Rider",
  "LV": 1,
  "HP": 15,
  "ATK": 5,
  "DEF": 4,
  "SPD": 4,
  "grow": [3,3,2,3]
}, 3: {
  "Career": "Sworder",
  "LV": 1,
  "HP": 13,
  "ATK": 8,
  "DEF": 3,
  "SPD": 4,
  "grow": [3,4,1,2]
}, 4: {
  "Career": "theif",
  "LV": 1,
  "HP": 10,
  "ATK": 12,
  "DEF": 1,
  "SPD": 5,
  "grow": [2,5,1,4]
}}

enemy = { 1: {
  "Name": "Frightbrute",
  "LV": 1,
  "HP": 20,
  "ATK": 4,
  "DEF": 6,
  "SPD": 2,
  "grow": [7,3,4,1]
}, 2: {
  "Name": "Murkmutant",
  "LV": 1,
  "HP": 15,
  "ATK": 5,
  "DEF": 4,
  "SPD": 4,
  "grow": [5,5,4,2]
}, 3: {
  "Name": "Terrorman",
  "LV": 1,
  "HP": 13,
  "ATK": 8,
  "DEF": 3,
  "SPD": 4,
  "grow": [5,6,3,2]
}, 4: {
  "Name": "Shadowstep",
  "LV": 1,
  "HP": 10,
  "ATK": 12,
  "DEF": 1,
  "SPD": 5,
  "grow": [4,8,3,3]
}}

with open('Hero.json', 'w') as outfile:
    json.dump(hero, outfile)


with open('Enemy.json', 'w') as outfile:
    json.dump(enemy, outfile)