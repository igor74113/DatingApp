# **MedConnect**

## **Tech Stack**

### **Frontend (Vue 3 + Vue Router + Tailwind CSS)**
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

### **1️⃣ Backend Setup**
```sh
cd src/backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
Django API will be running at: **[`http://127.0.0.1:8000/`](http://127.0.0.1:8000/)**

---

### **2️⃣ Frontend Setup**
```sh
cd ../frontend
npm install
npm run serve
```

---

## **Environment Variables**
Create a **`.env`** file inside the `backend/` directory to store secrets:

```ini
DJANGO_SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=sqlite://user:password@localhost:5432/medconnect
```

For Vue, create a **`.env.local`** inside `frontend/`:

```ini
VUE_APP_API_URL=http://127.0.0.1:8001/api/
```

