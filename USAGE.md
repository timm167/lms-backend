# Set Up and Usage

For simplified instructions on recommended setup and usage, checkout

---

## Remote Server access (not recommended)
- The easiest way to use the site is to access https://timm167.github.io/lms-frontend/
- The backend is hosted remotely on render
- Note that it is hosted on a free plan so uptime is not gauranteeed. It is redeployed every two hours so downtime should not last longer than that.
- ⚠️ Playground features are unreliable on remote server due non-persisting data and memory limits.

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

Go to http://localhost:5173/lms-frontend-local/ (or check terminal for url)

If using the remote server on render (not recommended)

```
git clone https://github.com/timm167/lms-frontend.git
cd lms-frontend-local
npm install
npm run dev
```

Go to http://localhost:5173/lms-frontend/ (or check terminal for url)

--- 
### Use the App

- This is a demo only app, it should not be used for other purposes.
- Once both the backend and frontend are running, you should be able to use the site freely.
- Data will not persist due to using a sqlite database
- For navigation support, checkout the frontend documentation at https://github.com/timm167/lms-frontend

---
## Questions

Please feel free to reach out to me if you have any questions or you are having problems.

Email: tim.charterii@gmail.com
GitHub: https://github.com/timm167
