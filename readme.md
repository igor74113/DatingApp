# **Health-focused Dating Platform (BETA Version)** 

## **Tech Stack**

### **Frontend (Vue 3 + Vue Router + Tailwind CSS)(Not Available in BETA Version)** 
- Vue.js (3.x)  
- Vue Router  
- Axios (for API calls)  
- Tailwind CSS (UI styling)  

### **Backend (Django + DRF + SQLite)**
- Django (5.x)  
- Django REST Framework (DRF)  
- SimpleJWT (for authentication)  
- Django Channels (WebSockets for chat)  
- SQLite (Database)  
- CORS Headers (For Vue-Django communication)  

---

## **Installation & Setup**

### **1. Backend Setup**
#### **Option 1: Using Pip (`requirements.txt`)**
```sh
cd src/backend
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver


### **2️. Frontend Setup(Not available in Beta Version)**
```sh
cd ../frontend
npm install
npm run serve
```

## **Environment Variables**
Create a **`.env`** file inside the `backend/` directory to store secrets:

```ini
DJANGO_SECRET_KEY=your_secret_key
DJANGO_CORS_ALLOWED_ORIGINS=http://localhost:8001,http://127.0.0.1:8001,http://192.168.1.34:8001
```

For Vue, create a **`.env.local`** inside `frontend/`:

```ini
VUE_APP_API_URL=http://127.0.0.1:8001/api/
```

