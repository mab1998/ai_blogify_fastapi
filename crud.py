from firebase_admin import auth, firestore
from models import User, Blog, Subscription

db = firestore.client()

def create_user(user_data):
    user = auth.create_user(
        email=user_data.email,
        password=user_data.password,
        display_name=user_data.display_name
    )
    return user

def get_user(uid):
    user = auth.get_user(uid)
    return User(uid=user.uid, email=user.email, display_name=user.display_name)

def create_blog(blog_data, user_id):
    doc_ref = db.collection("blogs").add({
        "title": blog_data.title,
        "content": blog_data.content,
        "author_id": user_id,
        "created_at": firestore.SERVER_TIMESTAMP
    })
    return doc_ref.id

def create_subscription(subscription_data, user_id):
    doc_ref = db.collection("subscriptions").add({
        "user_id": user_id,
        "plan": subscription_data.plan,
        "start_date": subscription_data.start_date,
        "end_date": subscription_data.end_date
    })
    return doc_ref.id
