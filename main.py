#Version 1.0.0, made by Birdicodes ®2025
import turtle as t
import random
import math
import time
wn = t.Screen()
wn.setup(width=1000, height=600)
wn.bgcolor("black")
wn.title("Super Turtle Bros v1.0.5")
wn.tracer(0)

players = []
projectiles = []
obstacles = []
keys_held = set()
winner_declared = False

class Player1(t.Turtle):
    def __init__(self, name, color, x, y, owner, super_type, hp=100, is_boss=False, special_type=None):
        super().__init__()
        self.shape("triangle")
        self.color(color)
        self.penup()
        self.goto(x, y)
        self.name = name
        self.owner = owner
        self.health = hp
        self.super_type = super_type
        self.special_type = special_type
        self.is_boss = is_boss
        self.shapesize(4,4) if is_boss else self.shapesize(2,2)

class Player2(t.Turtle):
    def __init__(self, name, color, x, y, owner, super_type, hp=100, is_boss=False, special_type=None):
        super().__init__()
        self.setheading(180)
        self.shape("triangle")
        self.color(color)
        self.penup()
        self.goto(x, y)
        self.name = name
        self.owner = owner
        self.health = hp
        self.super_type = super_type
        self.special_type = special_type
        self.is_boss = is_boss
        self.shapesize(4,4) if is_boss else self.shapesize(2,2)

class Obstacle(t.Turtle):
    def __init__(self, x, y, width=30, height=30, color="gray"):
        super().__init__()
        self.shape("square")
        self.color(color)
        self.penup()
        self.goto(x, y)
        self.width = width
        self.height = height
        self.shapesize(stretch_wid=height/20, stretch_len=width/20)
        obstacles.append(self)

class Projectile(t.Turtle):
    def __init__(self, x, y, dx, dy, owner, size=10, color=None, passes_through=False, damage=5):
        super().__init__()
        self.penup()
        self.goto(x, y)
        self.dx = dx
        self.dy = dy
        self.owner = owner
        self.size = size
        self.passes_through = passes_through
        self.damage = damage
        self.shape("circle")
        self.color(color if color else owner.pencolor())
        self.shapesize(stretch_wid=size/10, stretch_len=size/10)
        projectiles.append(self)

characters = [
    {"name":"Lemon Drops","color":"yellow","super":"minigun"},
    {"name":"Cell","color":"red","super":"shadow"},
    {"name":"AK47","color":"blue","super":"homing"},
    {"name":"8Ball","color":"orange","super":"melee"},
    {"name":"Siocopath Medic","color":"green","super":"heal"},
    {"name":"manysided.exe","color":"purple","super":"burst"},
    {"name":"Sigma Boy","color":"white","super":"op"},
    {"name":"La Vacca Saturnato Saturnata","color":"pink","super":"crazy"},
    {"name":"justblue","color":"cyan","super":"laser"},
    {"name":"Q*Bert","color":"lightblue","super":"flame"},
    {"name":"Icyyyyy","color": "navy","super":"freeze"},
    {"name":"Notdarkatallbutstilldark","color": "lightyellow","super":"shadow_drones"},
    {"name":"Six Seven","color":"gold","super":"jackpot"}
]

def create_obstacles():
    
    Obstacle(0, 0, 20, 100, "darkgray")
    
    
    Obstacle(-300, 150, 40, 40, "brown")
    Obstacle(300, 150, 40, 40, "brown")
    Obstacle(-300, -150, 40, 40, "brown")
    Obstacle(300, -150, 40, 40, "brown")
    
  
    Obstacle(-150, 100, 60, 20, "gray")
    Obstacle(150, 100, 60, 20, "gray")
    Obstacle(-150, -100, 60, 20, "gray")
    Obstacle(150, -100, 60, 20, "gray")

def check_collision_with_obstacles(obj, new_x, new_y):
    obj_size = getattr(obj, "size", 15)
    for obstacle in obstacles:
        if (abs(new_x - obstacle.xcor()) < (obstacle.width / 2 + obj_size / 2) and
            abs(new_y - obstacle.ycor()) < (obstacle.height / 2 + obj_size / 2)):
            return True
    return False


def shoot_normal(player):
    dx = 15 if player.owner=="Player1" else -15
    Projectile(player.xcor(), player.ycor(), dx, 0, player)

def super_attack(player):
    t = player.super_type
    if t=="minigun":
        for i in range(7):
            Projectile(player.xcor(), player.ycor(),
                       random.randint(10,20)*(1 if player.owner=="Player1" else -1),
                       random.randint(-3,3), player, size=7)
    elif t=="shadow":
        for i in range(13):
            Projectile(player.xcor(), player.ycor(),
                       random.randint(8, 18) * (1 if player.owner=="Player1" else -1),
                       random.randint(-8, 8), player, size=8, color="red")
                       
    elif t=="homing":
        for _ in range(5):
            Projectile(player.xcor(), player.ycor(),
            (12 if player.owner=="Player1" else -12),
                        random.randint(-10,10), player, size=12, color="blue")
    elif t=="melee":
        for i in range(3):
            y_offset = (i - 1) * 20 
            Projectile(player.xcor(), player.ycor() + y_offset,
                       (25 if player.owner=="Player1" else -25),
                       random.randint(-3, 3), player, size=25, color="orange", damage=15)

        Projectile(player.xcor() + (30 if player.owner=="Player1" else -30), 
                   player.ycor(),
                   (15 if player.owner=="Player1" else -15),
                   0, player, size=35, color="darkorange", damage=25)
    elif t=="heal":
        player.health = min(100, player.health+30)
        Projectile(player.xcor(), player.ycor(),
                   15 if player.owner=="Player1" else -15, 0, player, size=20, color="green")
    elif t=="burst":
        for angle in range(0,360,30):
            rad=math.radians(angle)
            Projectile(player.xcor(), player.ycor(),
                       16*math.cos(rad),16*math.sin(rad),player,size=12,color="purple")
    elif t=="op":
        for _ in range(20):
            Projectile(player.xcor(), player.ycor(),
                       random.randint(-22,22), random.randint(-22,22), player, size=15, color="white")
    elif t=="crazy":
        for _ in range(30):
            Projectile(player.xcor(), player.ycor(),
                       random.randint(-25,25), random.randint(-25,25), player, size=10, color="pink")
    elif t=="laser":
        step=20
        speed=15 if player.owner=="Player1" else -15
        for i in range(-2,3):
            p=Projectile(player.xcor(), player.ycor()+i*step, speed, 0, player, size=13, color="cyan")
            p.passes_through=False
    elif t=="flame":
        for i in range(7):
            angle = -30 + (i * 10)  
            rad = math.radians(angle)
            dx = 15 * math.cos(rad) * (1 if player.owner=="Player1" else -1)
            dy = 15 * math.sin(rad)
            Projectile(player.xcor(), player.ycor(), dx, dy, player, size=12, color="lightblue")
    elif t=="freeze":
        for wave in range(3):  
            for angle in [-60, -30, 0, 30, 60]:  
                rad = math.radians(angle)
                
                speed = 13
                size = 14 
                dx = speed * math.cos(rad) * (1 if player.owner=="Player1" else -1)
                dy = speed * math.sin(rad)      
                start_x = player.xcor() + (wave * 10 * (1 if player.owner=="Player1" else -1))
                
                proj = Projectile(start_x, player.ycor(), dx, dy, player, 
                                size=size, color="blue", damage=8)
                proj.passes_through = False
        Projectile(player.xcor(), player.ycor(),
                   20 * (1 if player.owner=="Player1" else -1), 0, player,
                   size=3, color="cyan", damage=10, passes_through=False)
    elif t=="shadow_drones":
        for i in range(32):
            drone_x = player.xcor() + random.randint(-40, 40)
            drone_y = player.ycor() + random.randint(-40, 40)
            drone_dx = random.randint(-25, 25)
            drone_dy = random.randint(-25, 25)
            Projectile(drone_x, drone_y, drone_dx, drone_dy, player, size=12, color="gray", damage=15)
    
    elif t == "jackpot":
        for i in range(13):
            angle = i * 27.7
            rad = math.radians(angle)
            speed = random.randint(8, 12)
            Projectile(player.xcor(), player.ycor(), speed * math.cos(rad), speed * math.sin(rad), player, size=12, color="gold", damage=18, passes_through=True)
def update_projectiles():
    for proj in projectiles[:]:
        new_x = proj.xcor() + proj.dx
        new_y = proj.ycor() + proj.dy
        
        if not getattr(proj, 'passes_through', False):
            if check_collision_with_obstacles(proj, new_x, new_y):
                if proj in projectiles:
                    projectiles.remove(proj)
                    proj.hideturtle()
                continue
        
        proj.setx(new_x)
        proj.sety(new_y)
        
       
        for other in projectiles[:]:
            if other is proj or other.owner==proj.owner or other.passes_through or proj.passes_through:
                continue
            if abs(proj.xcor()-other.xcor())<(proj.size+other.size) and abs(proj.ycor()-other.ycor())<(proj.size+other.size):
                if proj in projectiles:
                    projectiles.remove(proj); proj.hideturtle()
                if other in projectiles:
                    projectiles.remove(other); other.hideturtle()
                break
        
        
        for pl in players:
            if pl is not proj.owner and abs(proj.xcor()-pl.xcor())<15 and abs(proj.ycor()-pl.ycor())<15:
                pl.health-=getattr(proj,"damage",5)
                if proj in projectiles and not getattr(proj, 'passes_through', False):
                    projectiles.remove(proj); proj.hideturtle()
                break
        
        
        if abs(proj.xcor())>500 or abs(proj.ycor())>300:
            if proj in projectiles:
                projectiles.remove(proj); proj.hideturtle()

hud=t.Turtle()
hud.hideturtle()
hud.color("white")
hud.penup()

def draw_health():
    hud.clear()
    for i,pl in enumerate(players):
        hud.goto(-480,260-i*20)
        hud.write(f"{pl.name} ({pl.owner}): {pl.health}",font=("Arial",14,"normal"))

def show_winner(winner):
    hud.goto(0,0)
    hud.write(f"{winner.name} ({winner.owner}) WINS!",align="center",font=("Arial",24,"bold"))

def check_winner():
    global winner_declared
    alive=[p for p in players if p.health>0]
    if len(alive)==1 and not winner_declared:
        show_winner(alive[0])
        winner_declared=True
        return True
    return False

def key_press(key): keys_held.add(key)
def key_release(key): keys_held.discard(key)

controls={
    "w":("move","up","Player1"),"s":("move","down","Player1"),
    "a":("move","left","Player1"),"d":("move","right","Player1"),
    "f":("shoot",None,"Player1"),"g":("super",None,"Player1"),
    "Up":("move","up","Player2"),"Down":("move","down","Player2"),
    "Left":("move","left","Player2"),"Right":("move","right","Player2"),
    "m":("shoot",None,"Player2"),"n":("super",None,"Player2")
}

for key in controls:
    wn.onkeypress(lambda k=key:key_press(k),key=key)
    wn.onkeyrelease(lambda k=key:key_release(k),key=key)
wn.listen()

create_obstacles()

p1=random.choice(characters)
p2=random.choice([c for c in characters if c!=p1])
player1=Player1(p1["name"],p1["color"],-200,0,"Player1",p1["super"])
player2=Player2(p2["name"],p2["color"],200,0,"Player2",p2["super"])
players=[player1,player2]

def show_winner(winner):
    
    for p in players:
        p.hideturtle()
    for proj in projectiles:
        proj.hideturtle()
    for obstacle in obstacles:
        obstacle.hideturtle()
    projectiles.clear()
    hud.clear()
    hud.goto(0,0)
    hud.write(f"{winner.name} ({winner.owner}) WINS!", align="center", font=("Arial", 36, "bold"))
    wn.update()
    time.sleep(3)
    wn.bye()

def handle_wraparound():
    for pl in players:
        if pl.xcor() > 500:
            pl.setx(-490)
        elif pl.xcor() < -500:
            pl.setx(490)
        
        if pl.ycor() > 300:
            pl.sety(-290)
        elif pl.ycor() < -300:
            pl.sety(290)

while True:
    wn.update()
    for key in list(keys_held):
        action,param,owner=controls[key]
        player=player1 if owner=="Player1" else player2
        if action=="move":
            new_x, new_y = player.xcor(), player.ycor()
            if param=="up": new_y += 5
            elif param=="down": new_y -= 5
            elif param=="left": new_x -= 5
            elif param=="right": new_x += 5
            
            if not check_collision_with_obstacles(player, new_x, new_y):
                player.setx(new_x)
                player.sety(new_y)
                
        elif action=="shoot":
            shoot_normal(player)
        elif action=="super":
            super_attack(player)
    
    update_projectiles()
    draw_health()
    handle_wraparound()
    if check_winner():
        time.sleep(3)
        wn.bye()
        break


