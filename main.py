from fastapi import FastAPI, Depends, HTTPException, Header,Request
from pydantic import BaseModel
from firebase_admin import credentials, firestore, initialize_app
from firebase_admin.auth import verify_id_token
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict
import uvicorn
import logging
from typing import List


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

@app.get("/subscriptions", response_model=List[SubscriptionPlan])
async def get_subscriptions():
    example_subscriptions = [
        {"name": "Basic Plan", "price": 5.0, "duration": "5 min", "features": ["5 Credits per M (5 blog)", "SEO Optimization", "150 Supported Language"], "credits": 5, "supported_platforms": ["Youtube"]},
        {"name": "Premium Plan", "price": 10.0, "duration": "10 min", "features": ["20 Credits per M (20 blog)", "SEO Optimization", "150 Supported Language"], "credits": 20, "supported_platforms": ["Youtube"]},
        {"name": "Plus Plan", "price": 13.0, "duration": "20 min", "features": ["20 Credits per M (20 blog)", "SEO Optimization", "150 Supported Language"], "credits": 20, "supported_platforms": ["Youtube", "Google Podcast"]},
        {"name": "Master Plan", "price": 19.0, "duration": "30 min", "features": ["40 Credits per M (30 blog)", "SEO Optimization", "150 Supported Language"], "credits": 40, "supported_platforms": ["Youtube", "Google Podcast", "Spotify", "Vimeo"]},
    ]
    return example_subscriptions

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
# If you want to add more endpoints, you can define them here

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True, reload_dirs=['D:\\00mabrouk\\Blogify\\fastapi_project'])
