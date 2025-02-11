# Set Up and Usage

## Cloud
- The easiest way to use the site is to access https://timm167.github.io/lms-frontend/
- The backend is hosted remotely on render
- Note that it is hosted on a free plan so uptime is not gauranteeed. It is redeployed every two hours so downtime should not last longer than that.

Check Server availability at: https://stats.uptimerobot.com/0pKZ4j5FWK

## Deploying Server Locally
⚠️ **Note**: If deploying server locally, access via https://timm167.github.io/lms-frontend-local/ or deploy the frontend locally (instructions-below)
The other link will not work

### Prerequisites
Ensure you have **Python** installed.

### Steps to Deploy and Use Backend Locally

1. **Clone the Repository**
   ```sh
   git clone https://github.com/timm167/lms-backend
   cd lms-backend
   ```

2. **Create a Virtual Environment** (optional but recommended)
   ```sh
   python -m venv venv
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

1. 
- If using local server, clone https://timm167.github.io/lms-frontend-local/
- if using remote server, clone https://timm167.github.io/lms-frontend/

2. 
