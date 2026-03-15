# Map of all game items
itemMap = {
    0: None,
    1: "Wall",
    2: "Enemy",
    3: "Box",
    "B*": "Button",
    "S": "Spawn",
    "F": "Finish",
    "D*": "Door" # the astrisk stands for a wildcard system allowing me to pass through other values so as an example. D*B1 would link this door to button 1
}

# Names of all items you can collide with
collisionItems = ["Wall", "Door"]

# Name of all items you can move
moveableItems = ["Box"]

# items linked to their image
itemImageMap = {
    "Wall": "assets/wall.png",
    "Enemy": "assets/jay.png",
    "Box": "assets/portalA.png",
    "Button": "assets/button.png",
    "Door": "assets/door.png"
}