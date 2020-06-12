from models import User, Post, db, Tag
from app import app

db.session.commit()
db.drop_all()
db.create_all()

User.query.delete()
Post.query.delete()
Tag.query.delete()

u1 = User(first_name="Clayton", last_name="Whittaker",
          image_url="https://i2.wp.com/sketchbooknation.com/wp-content/uploads/2013/09/manstandingthumb.png?fit=650%2C400&ssl=1")
u2 = User(first_name="Madeline", last_name="Whittaker",
          image_url="https://www.wikihow.com/images/thumb/7/70/Draw-Yourself-As-a-Manga-Girl_Boy-Step-12.jpg/aid766412-v4-1200px-Draw-Yourself-As-a-Manga-Girl_Boy-Step-12.jpg")
u3 = User(first_name="Michale", last_name="Rosenthal",
          image_url="https://www.howtodrawforkids.com/wp-content/uploads/2017/04/11-man-drawing.jpg")
u4 = User(first_name="Lebron", last_name="James",
          image_url="https://image.shutterstock.com/image-vector/continuous-line-drawing-businessman-sitting-260nw-1446881981.jpg")
u5 = User(first_name="Steph", last_name="Curry")

db.session.add_all([u1, u2, u3, u4, u5])
db.session.commit()


t1 = Tag(name="Fun")
t2 = Tag(name="Even More")
t3 = Tag(name="Bloop")
t4 = Tag(name="Zope")
t5 = Tag(name="Curry")

db.session.add_all([t1, t2, t3, t4, t5])
db.session.commit()

p1 = Post(title="My First Post", content="Lorem ipsum, dolor sit amet consectetur adipisicing elit. Corrupti magni laudantium inventore magnam. Eveniet ullam sequi, voluptates, quae voluptatem consequatur repudiandae optio libero vitae natus, eaque similique reiciendis fugiat pariatur?", user_id="1")
p2 = Post(title="My Second Post",
          content="Lorem, ipsum dolor sit amet consectetur adipisicing elit. Doloribus, quos?", user_id="1")
p3 = Post(title="First Post!!!", content="Lorem ipsum, dolor sit amet consectetur adipisicing elit. Corrupti magni laudantium inventore magnam. Eveniet ullam sequi, voluptates, quae voluptatem consequatur repudiandae optio libero vitae natus, eaque similique reiciendis fugiat pariatur?", user_id="1")
p4 = Post(title="My Last Post",
          content="Lorem ipsum, dolor sit amet consectetur adipisicing elit. ", user_id="1")
p5 = Post(title="My Post",
          content="Lorem, ipsum dolor sit amet consectetur adipisicing elit. Doloribus, quos?", user_id="2")
p6 = Post(title="New To This", content="Lorem ipsum, dolor sit amet consectetur adipisicing elit. Corrupti magni laudantium inventore magnam. Eveniet ullam sequi, voluptates, quae voluptatem consequatur repudiandae optio libero vitae natus, eaque similique reiciendis fugiat pariatur?", user_id="3")
p7 = Post(title="Final Post",
          content="Lorem ipsum, dolor sit amet consectetur adipisicing elit. ", user_id="3")
p8 = Post(title="New Blog",
          content="Lorem, ipsum dolor sit amet consectetur adipisicing elit. Doloribus, quos?", user_id="4")
p9 = Post(title="Great News", content="Lorem ipsum, dolor sit amet consectetur adipisicing elit. Corrupti magni laudantium inventore magnam. Eveniet ullam sequi, voluptates, quae voluptatem consequatur repudiandae optio libero vitae natus, eaque similique reiciendis fugiat pariatur?", user_id="4")
p10 = Post(title="What i just found out",
           content="Lorem ipsum, dolor sit amet consectetur adipisicing elit. ", user_id="2")


db.session.add_all([p1, p2, p3, p4, p5, p6, p7, p8, p9, p10])
db.session.commit()
