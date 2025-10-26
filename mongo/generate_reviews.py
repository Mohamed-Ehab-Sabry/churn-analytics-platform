import pandas as pd
import random
import json
from datetime import datetime, timedelta

# Load your customer churn data
df = pd.read_csv("Customer-Churn.csv")
sample = df


# Tunable parameters
SKIP_RATE_ACTIVE = 0.4   # 40% of active (non-churned) customers never review
SKIP_RATE_CHURNED = 0.3 # 30% of churned customers never review
MAX_REVIEWS_PER_CUSTOMER = 2

# Positive comments (for active customers)
positive_comments = [
    "Everything works great 👌", "Internet speed is amazing.",
    "Support was super helpful ❤️", "Love the new fiber plan ",
    "Stable connection and fast setup!", "Totally worth it!! 💯",
    "Happy with the service, recommend 👍", "Billing was easy and clear",
    "Been a customer for years, no issues", "Honestly better than expected ",
    "5 stars from me, solid connection ", "Customer care is polite and efficient",
    "Service improved a lot this year", "No lag even when gaming 🔥",
    "Streaming Netflix perfectly fine all day", "Pretty happy overall 😁",
    "Reliable connection and good price", "Quick installation, smooth process",
    "Super fast internet, zero downtime", "Works great even during peak hours",
    "Affordable and solid quality!", "Great value for money 💰",
    "Very happy with the upgrade", "Loving the fiber speed!",
    "No problems since last year 👏", "Customer support was responsive and nice",
    "Streaming and gaming both smooth", "Everything perfect so far!",
    "Very reliable provider", "No complaints, perfect experience"
]

negative_comments = [
    "Connection keeps dropping 😡", "Cancelled my plan last month",
    "Billing errors AGAIN 😤", "Too expensive for what you get ...",
    "Support took forever to answer, useless", "Slow speed and random disconnections",
    "Router always crashing!! 😠", "Customer service didn't care at all",
    "Charged twice in one month!", "Left the company, worst ever 😤",
    "Disconnected without notice 💀", "Lagging every evening… tired of this",
    "Called 3 times, still not fixed!!", "Honestly waste of money",
    "Not worth the price anymore", "Bad experience since day one",
    "Slow internet + rude support", "Never coming back 😒",
    "Moved to another ISP, much better", "0/10 don't recommend",
    "Unstable connection every night", "Customer care didn’t help at all..",
    "Service always down on weekends", "Overcharged multiple times 😤",
    "App doesn’t work properly", "Worst internet ever!!",
    "Cancelled because of poor support", "Super slow and frustrating",
    "They promised speed, but nope", "I regret signing up 😩"
]

neutral_comments = [
    "Service okay but sometimes unstable ", "Average speed, not great not bad 😐",
    "Fine connection, could be better", "Customer support a bit slow",
    "Works okay, price could be lower ", "Not bad overall, just occasional lag",
    "Setup was fine, minor issues only", "Internet okay during day, slower at night",
    "Acceptable service, nothing special", "It's alright, could improve over time",
    "Good when it works, bad when it doesn’t", "Sometimes fast, sometimes not",
    "Normal experience, nothing wow", "Router takes long to reboot 😅",
    "Billing is confusing at times", "Internet drops once or twice a week",
    "Decent quality for the price", "I wish upload speed was higher",
    "Fine for browsing but not gaming", "Service improved after technician visit"
]

# Generate reviews
reviews = []



for _, row in df.iterrows():
    cid = row["customerID"]
    churn = row["Churn"]

    # Skip some customers
    if churn == "Yes":
        if random.random() < SKIP_RATE_CHURNED:
            continue
    else:
        if random.random() < SKIP_RATE_ACTIVE:
            continue

    # Number of reviews for this customer
    for _ in range(random.randint(1, MAX_REVIEWS_PER_CUSTOMER)):
        # Weighted rating logic
        if churn == "Yes":
            rating = random.choices([1, 2, 3], weights=[0.5, 0.3, 0.2])[0]
            comment = random.choice(negative_comments + neutral_comments)
            # Reviews closer to current time (simulating right after churn)
            days_ago = random.randint(0, 120)
        else:
            rating = random.choices([5, 4, 3], weights=[0.5, 0.3, 0.2])[0]
            comment = random.choice(positive_comments + neutral_comments)
            # Reviews can be any time in the last year
            days_ago = random.randint(0, 365)

        review_date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")

        review = {
            "customer_id": cid,
            "review_date": review_date,
            "rating": rating,
            "comment": comment
        }

        # Optional extras (tags and missing fields)
        if random.random() < 0.1:
            review["tags"] = random.choice(["support", "billing", "speed", "general", "setup", "price"])
        if random.random() < 0.03:
            del review["rating"]

        reviews.append(review)

# --- Save outputs ---
# Standard JSON array
with open("customer_reviews.json", "w", encoding="utf-8") as f:
    json.dump(reviews, f, indent=4, ensure_ascii=False)

# JSONL format (MongoDB bulk import ready)
with open("customer_reviews.jsonl", "w", encoding="utf-8") as f:
    for r in reviews:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")

print(f"✅ Generated {len(reviews)} realistic weighted reviews for {len(df)} customers.")
print("📦 Saved as both customer_reviews.json and customer_reviews.jsonl")