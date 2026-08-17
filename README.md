# StyleSenseAI
<<<<<<< HEAD
# StyleSense AI
=======
>>>>>>> 54545bdb22e97544d1b4a91cf4ba51ed39542476

**AI-powered personal styling and beauty assistant that combines skin analysis, personalized recommendations, product discovery, and virtual try-on into one intelligent experience.**

## ✨ Overview

StyleSense AI helps consumers make smarter fashion and beauty decisions using AI.

Instead of browsing through hundreds of products, users can analyze their skin, understand their needs, receive personalized skincare recommendations, discover suitable products based on their preferences and location, and virtually try on clothing before making a purchase.

The goal is to bridge the gap between **AI-powered personalization and real-world shopping**.

## 🚀 Key Features

### 🧴 AI Skin Analysis
- Upload a facial image for skin analysis.
- Uses Perfect Corp./YouCam APIs to analyze:
  - Hydration
  - Texture
  - Brightness/Radiance
  - Acne
- Generates an overall skin-health score.
- Detects potential skin concerns and their severity.

### 🤖 Personalized AI Recommendations
Uses Ollama/LLM-based reasoning to generate:
- Personalized skincare summaries
- Recommendations
- Morning and night routines
- Recommended ingredients
- Product categories
- Reasons behind recommendations

### 🛍️ Intelligent Product Recommendations
Products are filtered according to:
- Recommended ingredients
- Product category
- Budget
- User location
- Availability

The architecture is designed so the temporary catalogue can later be replaced with real retailer or marketplace APIs.

### 📍 Location-Aware Shopping
User profile information is used to personalize product availability based on location such as:
- Country
- State
- City
- Pincode

### 👗 Virtual Try-On
StyleSense AI extends personalization beyond skincare with virtual clothing try-on, allowing users to visualize how clothing can look on them before purchasing.

### 📊 Analysis History
Users can access previous skin analyses including:
- Scores
- AI insights
- Recommendations
- Skincare routines
- Recommended products
- Original analysis results

## 🧠 How It Works

```text
User
 │
 ├── Uploads Skin Image
 │
 ▼
Perfect Corp. / YouCam API
 │
 ▼
Skin Analysis
 │
 ├── Hydration
 ├── Texture
 ├── Brightness
 └── Acne
 │
 ▼
Concern Detection
 │
 ▼
Ollama AI
 │
 ├── Personalized Recommendation
 ├── Skincare Routine
 ├── Ingredients
 └── Product Requirements
 │
 ▼
Product Recommendation Engine
 │
 ├── Ingredient Matching
 ├── Category Matching
 ├── Budget Filtering
 └── Location / Availability
 │
 ▼
Personalized Shopping Experience
```

## 🏗️ Architecture

```text
Frontend
   │
   │ REST API
   ▼
FastAPI Backend
   │
   ├── Authentication
   ├── Skin Analysis Service
   ├── Concern Service
   ├── Product Recommendation Service
   ├── Product Search Service
   └── Virtual Try-On Service
   │
   ├───────────────┐
   ▼               ▼
PostgreSQL       AI Services
                 │
                 ├── Perfect Corp. / YouCam
                 └── Ollama
```

## 🛠️ Tech Stack

### Backend
- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- Uvicorn

### AI
- Ollama
- Large Language Models
- AI-powered recommendation engine

### Computer Vision / Beauty AI
- Perfect Corp. YouCam API
- PIL / Pillow

### Frontend
- React
- JavaScript
- HTML/CSS

### APIs
- Perfect Corp. API
- REST APIs
- Future retailer/marketplace APIs

## 📂 Project Structure

```text
StyleSense-AI/
│
├── backend/
│   ├── app/
│   │   ├── auth/
│   │   ├── core/
│   │   ├── integrations/
│   │   │   └── youcam.py
│   │   ├── models/
│   │   ├── routes/
│   │   │   └── skin_analysis.py
│   │   ├── schemas/
│   │   └── services/
│   │       ├── skin_analysis.py
│   │       ├── concern_service.py
│   │       ├── ollama_service.py
│   │       ├── product_search_service.py
│   │       └── product_recommendation_service.py
│   │
│   └── requirements.txt
│
├── frontend/
│   └── ...
│
├── .env
├── README.md
└── requirements.txt
```

## 🔑 Example User Journey

```text
1. User creates an account
        ↓
2. User uploads a selfie
        ↓
3. StyleSense analyzes their skin
        ↓
4. AI detects hydration concerns
        ↓
5. Ollama generates a personalized routine
        ↓
6. Recommendation engine finds matching products
        ↓
7. Products are filtered based on user preferences/location
        ↓
8. User can explore fashion products
        ↓
9. User virtually tries on selected clothing
        ↓
10. User makes a more informed purchase decision
```

## 💡 Why StyleSense AI?

Traditional shopping platforms primarily recommend products based on browsing history, popularity, or generic categories.

StyleSense AI aims to understand **the person first, and the product second**.

```text
User → Understand → Personalize → Recommend → Visualize → Purchase
```

This creates a more personalized and confidence-driven shopping experience.

## 🎯 Future Scope

- Real-time retailer and marketplace integrations
- More advanced clothing virtual try-on
- Personalized fashion recommendations
- Makeup virtual try-on
- Product price comparison
- Pincode-level delivery availability
- Personalized wardrobe recommendations
- AI stylist/chat assistant
- Feedback-based recommendation learning
- Multi-brand product catalogue

## 🏆 Hackathon Highlight

StyleSense AI combines **AI skin intelligence + personalized recommendations + location-aware product discovery + virtual try-on** into a unified consumer experience.

The project demonstrates how beauty and retail APIs can become more than isolated features—they can act as building blocks for an **AI-powered personal shopping assistant**.

## 👥 Team

<<<<<<< HEAD
Built with ❤️ during the hackathon by the StyleSense AI team.
=======
Built with ❤️ during the hackathon by the StyleSense AI team.
>>>>>>> 54545bdb22e97544d1b4a91cf4ba51ed39542476
