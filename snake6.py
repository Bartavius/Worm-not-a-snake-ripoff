import turtle
import random
import time

print('The controls are: [wasd]')

win = turtle.Screen()
winw,winh = 550,550
win.setup(winw,winh)
win.title('Worm! Totally Not a Snake Ripoff!')
win.bgcolor('black')
win.tracer(0)

outline = turtle.Turtle(shape='blank')
outline.pu()
outline.pencolor('white')
outline.pensize(2)
outline.goto(-winw/2,-winh/2-3)
outline.pd()
for i in range(2):
    outline.fd(winw+3)
    outline.lt(90)
    outline.fd(winh+3)
    outline.lt(90)
    
rad = winh/34/10
radw = winw/34/10

gridx = []
gridy = []

c1 = ['#211307','#4d3119']
outline.shapesize(radw,rad)
outline.shape('square')
for i in range(17):
    outline.pu()
    outline.setx(-winw/2+rad*10)
    outline.sety(winh/2-rad*10-i*rad*20)
    gridy.append(round(outline.ycor(),3))
    for f in range(17):
        outline.fillcolor(c1[(i+f)%len(c1)])
        outline.pencolor(c1[(i+f)%len(c1)])
        outline.setx(-winw/2+rad*10+f*rad*20)
        if i == 0:
            gridx.append(round(outline.xcor(),3))
        outline.stamp()

outline.ht()

rad = winh/34/10 - rad/5
radw = winw/34/10 - radw/5

h = turtle.Turtle(shape = 'square')
h.fillcolor('pink')
h.pencolor('black')
h.shapesize(radw,rad)
h.pu()

win.update()

# the explanation for grided movement is that instead of having keypress change
# direction of the turtle object, it simply queues up an action in the action
# list, which the while loop will check if there's any items in the queue
# Also, the reason I rounded the coordinates, is that python stores variables
# in lists, so the 20 digit decimals won't always end up the same number that
# it's supposed to be (for example, some division equations would end up as 1.00000000000000004
# when it should've just been 1.0

action = []

def up():
    if len(action)>1:
        return
    if h.heading() != 270:
        action.append(90)

def right():
    if len(action)>1:
        return
    if h.heading() != 180:
        action.append(0)

def left():
    if len(action)>1:
        return
    if h.heading() != 0:
        action.append(180)

def down():
    if len(action)>1:
        return
    if h.heading() != 90:
        action.append(270)

# arrows create more delays for some strange reason so I used wasd
win.onkey(up,'w')
win.onkey(right,'d')
win.onkey(left,'a')
win.onkey(down,'s')
win.listen()

a = turtle.Turtle(shape='circle')
a.shapesize(rad)
a.fillcolor('#33b007')
a.pu()

l = 0
body = []
bcor = []

def spawn():
    a.goto(random.choice(gridx),random.choice(gridy))
    if bcor:
        for i in bcor:
            if a.distance(i) - rad*10 <= rad*10:
                spawn()

def keepscore(score,scr = turtle.Turtle(shape='blank')):
    scr.clear()
    scr.pu()
    scr.goto(-winw/2+25,winh/2+15)
    scr.pd()
    scr.pencolor('white')
    scr.write(f'Score: {score}',align='left',font=('courier',20,'bold'))

def keephigh(score,hs = turtle.Turtle(shape = 'blank')):
    hs.clear()
    hs.pu()
    hs.goto(winw/2-25,winh/2+15)
    hs.pd()
    hs.pencolor('white')
    hs.write(f'Highscore: {score}',align='right',font=('courier',20,'bold'))

def death(ent = turtle.Turtle(shape='square',visible = False)):
    ent.st()
    ent.fillcolor('red')
    ent.pu()
    p = []
    for i in range(random.randint(1,3)*10):
        ent.goto(h.xcor(),h.ycor())
        ent.shapesize(random.uniform(0.2,0.75))
        ent.seth(random.randint(0,360))
        ent.fd(random.randint(15,80))
        p.append(ent.stamp())
    ent.ht()
    win.update()
    time.sleep(1)
    for i in p:
        ent.clearstamp(i)
    

keepscore(0)
keephigh(0)
highscore = 0
score = 0
spawn()

win.setup(winw+100,winh+100)

while True:
    
    
    # change the direction of the head if an action has been queued
    if action:
        if round(h.xcor(),3) in gridx and round(h.ycor(),3) in gridy:
            h.seth(action[0])
            action.pop(0)
            
    # moving the head
    win.update()
    h.fd(round((winw+winh)/2/17/6,8))

    # checking if it's within itself; dies
    if bcor:
        for i in bcor:
            if h.distance(i) < rad*3:
                death()
                for f in body:
                    h.clearstamp(f)
                l = 0
                body.clear()
                bcor.clear()
                h.goto(0,0)
                score = 0
                keepscore(score)
                spawn()

    # adding the body to imitate movement by stamping
    body.append(h.stamp())
    bcor.append((h.xcor(),h.ycor()))

    # clearing the tail to imitate movement
    if len(body) > l:
        h.clearstamp(body[0])
        body.pop(0)
        bcor.pop(0)

    # check if it hits walls
    if h.xcor() >= winw/2 or h.xcor() <= -winw/2 or h.ycor() >= winh/2 or h.ycor() <= -winh/2:
        death()
        for i in body:
            h.clearstamp(i)
        l = 0
        body.clear()
        bcor.clear()
        h.goto(0,0)
        score = 0
        keepscore(0)
        spawn()

    # check if it has hit the leaf
    if h.distance(a) - rad*10 <= rad*10:
        spawn()

        l += 6

        # scoring / highscore
        score += 100
        keepscore(score)
        if score > highscore:
            keephigh(score)
            highscore = score

    time.sleep(0.015)
    
