from fastapi import FastAPI, Depends, HTTPException, Header,Request
from pydantic import BaseModel
from firebase_admin import credentials, firestore, initialize_app
from firebase_admin.auth import verify_id_token
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict
import uvicorn
import logging
from typing import List
from fastapi.staticfiles import StaticFiles


app = FastAPI()

# Firebase Admin SDK setup
cred = credentials.Certificate("./serviceAccountKey.json")  # Update this path if necessary
initialize_app(cred)
db = firestore.client()

# Add CORS middleware
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserData(BaseModel):
    usersCount: str
    subscribedCount: str
    earnedLastMonth: str
    generatedBlogCount: str
    chartData: List[int]  # Add this line to include chart data
    chartLabels: List[str]  # Add this line to include chart labels
    chartTitle: str  # Add this line to include chart title

def verify_token(authorization: str = Header(None)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    try:
        token = authorization.split(" ")[1]
        decoded_token = verify_id_token(token)
        return decoded_token
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/user/{user_id}", response_model=UserData)
async def get_user_data(user_id: str, decoded_token: dict = Depends(verify_token)):
    logging.info(f"Fetching data for user_id: {user_id}")
    logging.info(f"Decoded token: {decoded_token}")
    
    # Example data
    example_data = {
        "usersCount": "100",
        "subscribedCount": "50",
        "earnedLastMonth": "2000",
        "generatedBlogCount": "10",
        "chartData": [12, 19, 3, 5, 2, 3, 9, 18, 12, 14, 15, 23],  # Example chart data
        "chartLabels": ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],  # Example chart labels
        "chartTitle": "Monthly Data"  # Example chart title
    }
    return UserData(**example_data)

class Blog(BaseModel):
    id: int
    title: str
    content: str
    category: str
    image_url: str
    
PEXELS_API_KEY = 'your_pexels_api_key'
PEXELS_URL = 'https://api.pexels.com/v1/search'
def fetch_image_url(query: str) -> str:
    return 'https://via.placeholder.com/150'  # Placeholder image if no image is found

    headers = {
        'Authorization': PEXELS_API_KEY
    }
    params = {
        'query': query,
        'per_page': 1
    }
    response = requests.get(PEXELS_URL, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['photos']:
            return data['photos'][0]['src']['medium']
    return 'https://via.placeholder.com/150'  # Placeholder image if no image is found

@app.get("/blogs", response_model=List[Blog])
async def get_blogs():
    example_blogs = [
        {"id": 1, "title": "Popular admin template you can use for your business.", "content": "It is a long established fact that a reader will be distracted by the readable content.", "category": "Fashion", "image_url": fetch_image_url('fashion')},
        {"id": 2, "title": "New trends in web design for 2024", "content": "Exploring the latest trends in web design and development.", "category": "Web Design", "image_url": fetch_image_url('web design')},
        {"id": 3, "title": "How to start a successful blog", "content": "Tips and tricks to start a successful blog.", "category": "Blogging", "image_url": fetch_image_url('blogging')},
        {"id": 4, "title": "The best programming languages to learn", "content": "An overview of the most popular programming languages.", "category": "Programming", "image_url": fetch_image_url('programming')},
        {"id": 5, "title": "Improving your SEO in 2024", "content": "Effective SEO strategies for the upcoming year.", "category": "SEO", "image_url": fetch_image_url('SEO')},
    ]
    return example_blogs





class SubscriptionPlan(BaseModel):
    name: str
    price: float
    duration: str
    features: List[str]
    credits: int
    supported_platforms: List[str]

# @app.get("/subscriptions", response_model=List[SubscriptionPlan])
# async def get_subscriptions():
#     example_subscriptions = [
#         {"name": "Basic Plan", "price": 5.0, "duration": "5 min", "features": ["5 Credits per M (5 blog)", "SEO Optimization", "150 Supported Language"], "credits": 5, "supported_platforms": ["Youtube"]},
#         {"name": "Premium Plan", "price": 10.0, "duration": "10 min", "features": ["20 Credits per M (20 blog)", "SEO Optimization", "150 Supported Language"], "credits": 20, "supported_platforms": ["Youtube"]},
#         {"name": "Plus Plan", "price": 13.0, "duration": "20 min", "features": ["20 Credits per M (20 blog)", "SEO Optimization", "150 Supported Language"], "credits": 20, "supported_platforms": ["Youtube", "Google Podcast"]},
#         {"name": "Master Plan", "price": 19.0, "duration": "30 min", "features": ["40 Credits per M (30 blog)", "SEO Optimization", "150 Supported Language"], "credits": 40, "supported_platforms": ["Youtube", "Google Podcast", "Spotify", "Vimeo"]},
#     ]
#     return example_subscriptions



import stripe




stripe.api_key = "pk_test_51Pewv5Ck9GCPhNzJc1JcJOPPmDarXHm3zgVK2XISF6VhzubBAo8CqmHR8Ll5DXFZGYN7jdbyNaHPUwtMalCQkBuw00D6GB4oQh"

class SubscriptionPlan(BaseModel):
    name: str
    price: float
    duration: str
    features: List[str]
    credits: int
    supported_platforms: List[str]

# @app.get("/subscriptions", response_model=List[SubscriptionPlan])
# async def get_subscriptions():
#     example_subscriptions = [
#         {"name": "Basic Plan", "price": 5.0, "duration": "5 min", "features": ["5 Credits per M (5 blog)", "SEO Optimization", "150 Supported Language"], "credits": 5, "supported_platforms": ["Youtube"]},
#         {"name": "Premium Plan", "price": 10.0, "duration": "10 min", "features": ["20 Credits per M (20 blog)", "SEO Optimization", "150 Supported Language"], "credits": 20, "supported_platforms": ["Youtube"]},
#         {"name": "Plus Plan", "price": 13.0, "duration": "20 min", "features": ["20 Credits per M (20 blog)", "SEO Optimization", "150 Supported Language"], "credits": 20, "supported_platforms": ["Youtube", "Google Podcast"]},
#         {"name": "Master Plan", "price": 19.0, "duration": "30 min", "features": ["40 Credits per M (30 blog)", "SEO Optimization", "150 Supported Language"], "credits": 40, "supported_platforms": ["Youtube", "Google Podcast", "Spotify", "Vimeo"]},
#     ]
#     return example_subscriptions







class Subscription(BaseModel):
    id: int
    name: str
    price: float
    credits: int
    supported_platforms: List[str]
    enabled: bool

subscriptions = [
    Subscription(id=1, name='Basic', price=10.0, credits=100, supported_platforms=['YouTube', 'Google Podcast'], enabled=True),
    Subscription(id=2, name='Standard', price=20.0, credits=200, supported_platforms=['Spotify', 'Vimeo'], enabled=True),
    Subscription(id=3, name='Premium', price=30.0, credits=300, supported_platforms=['YouTube', 'Spotify', 'Google Podcast', 'Vimeo'], enabled=True),
]

@app.get("/subscriptions", response_model=List[Subscription])
async def get_subscriptions():
    return subscriptions

@app.put("/subscriptions", response_model=List[Subscription])
async def update_subscriptions(updated_subscriptions: List[Subscription]):
    global subscriptions
    for updated_subscription in updated_subscriptions:
        for i, subscription in enumerate(subscriptions):
            if subscription.id == updated_subscription.id:
                subscriptions[i] = updated_subscription
                break
    return subscriptions

@app.post("/create-checkout-session")
async def create_checkout_session(plan: SubscriptionPlan):
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': plan.name,
                        },
                        'unit_amount': int(plan.price * 100),  # Stripe uses cents
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url='http://localhost:3000/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='http://localhost:3000/cancel',
        )
        return {"url": checkout_session.url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')
    event = None

    try:
        # sk_test_51Pewv5Ck9GCPhNzJConNDRijSKZXroxYcPrjBFXZTOeDxrkj0dCHCWFBfbcKPsZMlTGWQtwQeQa5FpxfbHZe8Dok00BnlZjbWB
        event = stripe.Webhook.construct_event(
            payload, sig_header, "your_webhook_secret"
        )
    except ValueError as e:
        # Invalid payload
        raise HTTPException(status_code=400, detail=str(e))
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise HTTPException(status_code=400, detail=str(e))

    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        # Fulfill the purchase
        # You can use session['metadata'] or session['client_reference_id'] to identify the user
        # Add credits to the user's account

    return {"status": "success"}



import datetime


# Dummy data for transactions
transactions = [
    {
        "description": "Transaction 1",
        "method": "Credit Card",
        "status": "Completed",
        "dateTime": "2024-01-01 12:00:00",
        "amount": "$100.00"
    },
    {
        "description": "Transaction 2",
        "method": "PayPal",
        "status": "Pending",
        "dateTime": "2024-01-02 14:30:00",
        "amount": "$200.00"
    },
    {
        "description": "Transaction 3",
        "method": "Bank Transfer",
        "status": "Failed",
        "dateTime": "2024-01-03 16:45:00",
        "amount": "$150.00"
    },
    {
        "description": "Transaction 4",
        "method": "Cash",
        "status": "Completed",
        "dateTime": "2024-01-04 18:15:00",
        "amount": "$50.00"
    }
]

class Transaction(BaseModel):
    description: str
    method: str
    status: str
    dateTime: datetime.datetime
    amount: str

@app.get("/transactions", response_model=List[Transaction])
async def get_transactions():
    return transactions




# Dummy data for users
users = [
    {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "status": "Active",
        "registered": "2023-01-01",
        "role": "Admin"
    },
    {
        "name": "Jane Smith",
        "email": "jane.smith@example.com",
        "status": "Pending",
        "registered": "2023-02-01",
        "role": "User"
    },
    {
        "name": "Bob Johnson",
        "email": "bob.johnson@example.com",
        "status": "Inactive",
        "registered": "2023-03-01",
        "role": "Moderator"
    },
    {
        "name": "Alice Brown",
        "email": "alice.brown@example.com",
        "status": "Active",
        "registered": "2023-04-01",
        "role": "User"
    }
]

class User(BaseModel):
    name: str
    email: str
    status: str
    registered: str
    role: str

@app.get("/users", response_model=List[User])
async def get_users():
    return users


from tinydb import TinyDB, Query

db = TinyDB('db.json')
settings_table = db.table('settings')

from typing import Optional

class Settings(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    current_password: Optional[str] = None
    new_password: Optional[str] = None
    input_language: Optional[str] = None
    blog_language: Optional[str] = None
    openai_key: Optional[str] = None
    whisper_key: Optional[str] = None
    blog_prompt: Optional[str] = None
    plan_basic: Optional[str] = None
    plan_basic_enabled: Optional[bool] = None
    plan_premium: Optional[str] = None
    plan_premium_enabled: Optional[bool] = None
    plan_plus: Optional[str] = None
    plan_plus_enabled: Optional[bool] = None
    plan_master: Optional[str] = None
    plan_master_enabled: Optional[bool] = None
    stripe_key: Optional[str] = None
    paypal_key: Optional[str] = None

@app.get("/settings", response_model=Dict[str, str])
async def get_settings():
    settings = settings_table.all()
    if not settings:
        raise HTTPException(status_code=404, detail="Settings not found")
    return settings[0]

@app.post("/settings")
def update_settings(settings: Settings):
    existing_settings = settings_table.all()
    if existing_settings:
        settings_id = existing_settings[0].doc_id
        update_data = settings.dict(exclude_unset=True)
        settings_table.update(update_data, doc_ids=[settings_id])
    else:
        settings_table.insert(settings.dict(exclude_unset=True))
    return {"message": "Settings updated successfully"}






# Dummy blog data
blogs = [
    {"id": 1, "title": "First Blog", "content": "This is the content of the first blog.", "date": "2024-01-01"},
    {"id": 2, "title": "Second Blog", "content": "This is the content of the second blog.", "date": "2024-02-01"},
    # Add more blogs as needed
]

class Blog(BaseModel):
    id: int
    title: str
    content: str
    date: str

# @app.get("/blogs/{blog_id}", response_model=Blog)
# def get_blog(blog_id: int):
#     for blog in blogs:
#         if blog["id"] == blog_id:
#             return blog
#     raise HTTPException(status_code=404, detail="Blog not found")


# main.py
# from fastapi import FastAPI, HTTPException
# from tinydb import TinyDB, Query
# from pydantic import BaseModel

# app = FastAPI()
# db = TinyDB('db.json')
blogs_table = db.table('blogs')

# main.py
from fastapi import FastAPI, HTTPException

# app = FastAPI()

# Example blogs
blogs = [
    {
        "id": 1,
        "title": "First Blog Post",
        "article": "<p>This is the content of the first blog post.</p>",
        "video_id": "abc123",
        "keywords": ["example", "first", "blog"],
        "transcript": "This is the transcript of the first blog post.",
        "summarization": "This is a summary of the first blog post."
    },
    {
        "id": 2,
        "title": "Second Blog Post",
        "article": "<p>This is the content of the second blog post.</p>",
        "video_id": "def456",
        "keywords": ["example", "second", "blog"],
        "transcript": "This is the transcript of the second blog post.",
        "summarization": "This is a summary of the second blog post."
    },
    {
        "id": 3,
        "title": "Third Blog Post",
        "article": "<p>This is the content of the third blog post.</p>",
        "video_id": "ghi789",
        "keywords": ["example", "third", "blog"],
        "transcript": "This is the transcript of the third blog post.",
        "summarization": "This is a summary of the third blog post."
    },
    {
        "id": 4,
        "title": "Fourth Blog Post",
        "article": "<p>This is the content of the fourth blog post.</p>",
        "video_id": "jkl012",
        "keywords": ["example", "fourth", "blog"],
        "transcript": "This is the transcript of the fourth blog post.",
        "summarization": "This is a summary of the fourth blog post."
    },
    {
        "id": 5,
        "title": "Fifth Blog Post",
        "article": "<p>This is the content of the fifth blog post.</p>",
        "video_id": "mno345",
        "keywords": ["example", "fifth", "blog"],
        "transcript": "This is the transcript of the fifth blog post.",
        "summarization": "This is a summary of the fifth blog post."
    },
    {
        "id": 6,
        "title": "Sixth Blog Post",
        "article": "<p>This is the content of the sixth blog post.</p>",
        "video_id": "pqr678",
        "keywords": ["example", "sixth", "blog"],
        "transcript": "This is the transcript of the sixth blog post.",
        "summarization": "This is a summary of the sixth blog post."
    }
]

@app.get("/blog/{blog_id}")
def get_blog(blog_id: int):
    blog = next((blog for blog in blogs if blog["id"] == blog_id), None)
    if blog:
        return blog
    else:
        raise HTTPException(status_code=404, detail="Blog not found")


@app.post("/blog/{blog_id}/edit")
def edit_blog(blog_id: int, blog_data: dict):
    blog = next((blog for blog in blogs if blog["id"] == blog_id), None)
    if blog:
        blog.update(blog_data)
        return blog
    else:
        raise HTTPException(status_code=404, detail="Blog not found")
    
    
@app.post("/blog/{blog_id}/edit")
def edit_blog(blog_id: int, updated_blog: Blog):
    blog = next((blog for blog in blogs if blog["id"] == blog_id), None)
    if blog:
        if updated_blog.title:
            blog["title"] = updated_blog.title
        if updated_blog.article:
            blog["article"] = updated_blog.article
        return {"message": "Blog updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Blog not found")
    
    
from fpdf import FPDF
import os
from fastapi.responses import FileResponse


class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, self.title, 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

# @app.get("/blog/{blog_id}/download")
# def download_blog(blog_id: int):
#     Blog = Query()
#     blog = blogs_table.get(Blog.id == blog_id)
#     if not blog:
#         raise HTTPException(status_code=404, detail="Blog not found")

#     pdf = PDF()
#     pdf.title = blog['title']
#     pdf.add_page()
#     pdf.set_font("Arial", size=12)
#     pdf.multi_cell(0, 10, blog['article'])

#     file_path = f"blog_{blog_id}.pdf"
#     pdf.output(file_path)

#     return FileResponse(file_path, filename=f"blog_{blog_id}.pdf", media_type='application/pdf')


@app.get("/blog/{blog_id}/download")
def download_blog(blog_id: int):
    blog = next((blog for blog in blogs if blog["id"] == blog_id), None)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    pdf = PDF()
    pdf.title = blog['title']
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, blog['article'])

    file_path = f"blog_{blog_id}.pdf"
    pdf.output(file_path)

    return FileResponse(file_path, filename=f"blog_{blog_id}.pdf", media_type='application/pdf')

import uuid
from fastapi.responses import JSONResponse

class Blog(BaseModel):
    youtube_url: str
    writer_point_of_view: str
    blog_generation_mode: str
    blog_language: str
    media_language: str
    blog_tone: str
    blog_size: str
    article_id: str

# Example blog storage
blogs = {}

# @app.post("/create_article")
# def create_article(blog: Blog):
#     # Generate a unique article ID
#     article_id = str(uuid.uuid4())
    
#     # Store the blog (for example purposes, storing in a dictionary)
#     blogs[article_id] = blog
    
#     # Return success response
#     return JSONResponse(status_code=200, content={"status": "success", "article_id": article_id})

# In-memory storage for demonstration purposes
blogs = []

class Blog(BaseModel):
    id: str
    title: str
    content: str
    category: str
    image_url: str
    
import time

# @app.post("/create_blog")
# def create_blog(blog: Blog):
#     blog.id = str(uuid.uuid4())
#     blogs.append(blog)
#     return {"message": "Blog created successfully", "blog_id": blog.id}
# If you want to add more endpoints, you can define them here

# In-memory store for blog creation status





from fastapi import FastAPI, HTTPException
from pydantic import BaseModel,HttpUrl
from typing import Dict
import time


# In-memory store for blogs
blogs: Dict[str, Dict] = {}

# class BlogCreateRequest(BaseModel):
#     youtube_url: HttpUrl
#     writer_point_of_view: str
#     blog_generation_mode: str
#     blog_language: str
#     media_language: str
#     blog_tone: str
#     blog_size: str
#     article_id: str
    
class BlogCreateRequest(BaseModel):
    youtube_url: HttpUrl
    writer_point_of_view: str
    blog_generation_mode: str
    blog_language: str
    media_language: str
    blog_tone: str
    blog_size: str
    article_id: str
    
# class BlogCreateRequest(BaseModel):
#     youtube_url: str
#     writer_point_of_view: str
#     blog_generation_mode: str
#     blog_language: str
#     media_language: str
#     blog_tone: str
#     blog_size: str
#     article_id: str

# @app.post("/create_article")
# def create_article(request: BlogCreateRequest):
#     blog = {
#         "youtube_url": request.youtube_url,
#         "writer_point_of_view": request.writer_point_of_view,
#         "blog_generation_mode": request.blog_generation_mode,
#         "blog_language": request.blog_language,
#         "media_language": request.media_language,
#         "blog_tone": request.blog_tone,
#         "blog_size": request.blog_size,
#         "status": "processing",
#     }
#     blogs[request.article_id] = blog
    
    
#     blogs[request.article_id] = {
#         "status": "processing",
#         "details": request.dict()
#     }
#     # Simulate blog creation delay
#     time.sleep(5)
#     blogs[request.article_id]["status"] = "completed"
#     return {"status": "Blog creation started", "article_id": request.article_id}



blogs = {}

@app.post("/create_article")
def create_article(request: BlogCreateRequest):
    try:
        blog = {
            "youtube_url": request.youtube_url,
            "writer_point_of_view": request.writer_point_of_view,
            "blog_generation_mode": request.blog_generation_mode,
            "blog_language": request.blog_language,
            "media_language": request.media_language,
            "blog_tone": request.blog_tone,
            "blog_size": request.blog_size,
            "status": "processing",
        }
        blogs[request.article_id] = blog
        
        # Simulate blog creation delay
        time.sleep(5)
        blogs[request.article_id]["status"] = "completed"
        return {"status": "Blog creation started", "article_id": request.article_id}
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))


@app.get("/blog_status/{article_id}")
def blog_status(article_id: str):
    if article_id not in blogs:
        raise HTTPException(status_code=404, detail="Article ID not found")
    return {"article_id": article_id, "status": blogs[article_id]["status"]}


class Navbar(BaseModel):
    logo: Optional[str] = None
    links: List[str]

class Hero(BaseModel):
    title: str
    subtitle: str
    buttonText: str
    buttonLink: str
    image: Optional[str] = None

class FeatureItem(BaseModel):
    title: str
    description: str

class Features(BaseModel):
    title: str
    items: List[FeatureItem]

class About(BaseModel):
    title: str
    content: str

class WhatLookingFor(BaseModel):
    title: str
    content: str
    buttonText: str
    buttonLink: str

class PricingPlan(BaseModel):
    title: str
    price: str
    features: List[str]

class Pricing(BaseModel):
    plans: List[PricingPlan]

class Testimonial(BaseModel):
    name: str
    position: str
    message: str
    image: Optional[str] = None

class FAQItem(BaseModel):
    question: str
    answer: str

class ContactForm(BaseModel):
    name: str
    email: str
    phone: str
    message: str

class Contact(BaseModel):
    address: str
    email: str
    phone: str
    form: ContactForm

class Settings(BaseModel):
    navbar: Navbar
    hero: Hero
    features: Features
    about: About
    whatLookingFor: WhatLookingFor
    pricing: Pricing
    testimonials: List[Testimonial]
    faq: List[FAQItem]
    contact: Contact

settings = Settings(
    navbar=Navbar(logo="", links=[]),
    hero=Hero(title="", subtitle="", buttonText="", buttonLink="", image=""),
    features=Features(title="", items=[FeatureItem(title="", description="") for _ in range(4)]),
    about=About(title="", content=""),
    whatLookingFor=WhatLookingFor(title="", content="", buttonText="", buttonLink=""),
    pricing=Pricing(plans=[PricingPlan(title="", price="", features=[]) for _ in range(2)]),
    testimonials=[Testimonial(name="", position="", message="", image="") for _ in range(6)],
    faq=[FAQItem(question="", answer="") for _ in range(5)],
    contact=Contact(address="", email="", phone="", form=ContactForm(name="", email="", phone="", message=""))
)
from fastapi import FastAPI, File, UploadFile, Form
import shutil


# Function to load settings from TinyDB
def load_settings():
    global settings
    settings_doc = db.get(Query().type == 'settings_styles')
    if settings_doc:
        settings = Settings(**settings_doc['data'])

@app.get("/settings_styles")
async def get_settings():
    load_settings()
    # return {"settings_styles": settings}
    return settings



# 


@app.post("/settings_styles")
async def update_settings(new_settings: Settings):
    global settings
    settings = new_settings
    db.upsert({'type': 'settings_styles', 'data': settings.dict()}, Query().type == 'settings_styles')
    return {"message": "Settings updated successfully"}

# @app.post("/settings")
# async def update_settings(new_settings: Settings):
#     global settings
#     settings = new_settings
#     return {"message": "Settings updated successfully"}




@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"url": f"/{file_path}"}

# @app.post("/upload")
# async def upload_file(file: UploadFile = File(...)):
#     upload_dir = "uploads"
#     os.makedirs(upload_dir, exist_ok=True)
#     file_path = os.path.join(upload_dir, file.filename)
#     with open(file_path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)
#     return {"url": f"/{file_path}"}


app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True, reload_dirs=['D:\\00mabrouk\\Blogify\\fastapi_project'])
