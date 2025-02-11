# Set Up and Usage

## Cloud
- The easiest way to use the site is to access https://timm167.github.io/lms-frontend/
- The backend is hosted remotely on render
- Note that it is hosted on a free plan so uptime is not gauranteeed. It is redeployed every two hours so downtime should not last longer than that.
- Limited memory means that the 'generate data' button in playground does not work well unless deployed locally.
- Also the database may take time to update meaning the experience is slow.

Check Server availability at: https://stats.uptimerobot.com/0pKZ4j5FWK

## Deploying Server Locally (Recommended)
⚠️ **Note**: If deploying server locally, you MUST deploy the frontend locally. Instructions below.

### Prerequisites
Ensure you have **Python** installed.

Ensure local port 8000 is free, otherwise manually change the base_url in the frontend at src/service/base_url.

### Steps to Deploy and Use Backend Locally

1. **Clone the Repository**
   ```sh
   git clone https://github.com/timm167/lms-backend
   cd lms-backend/lms-backend
   ```

2. **Create a Virtual Environment** (optional but recommended)
   ```sh
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate     # On Windows
   ```

3. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```

4. **Run Migrations**
   ```sh
   python manage.py migrate
   ```

6. **Start the Development Server**
   ```sh
   python manage.py runserver
   ```

7. **Access the Application**
   Clone and run the frontend or access with swagger UI using http://localhost:8000/swagger/.

## Deploying Frontend Locally

If deploying server locally, in a seperate terminal

```
git clone https://github.com/timm167/lms-frontend-local.git
cd lms-frontend-local
npm install
npm run dev
```

Go to http://localhost:5173/lms-frontend-local/

If using the remote server on render (not recommended)

```
git clone https://github.com/timm167/lms-frontend.git
cd lms-frontend-local
npm install
npm run dev
```

Go to http://localhost:5173/lms-frontend/

