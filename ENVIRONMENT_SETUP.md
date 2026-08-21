# Smart Guard - Complete Environment Setup Guide

## Overview
This guide provides comprehensive instructions for setting up the development environment for the Smart Guard project, including both Frontend (React) and Backend (Python/FastAPI) components.

## Prerequisites

### System Requirements
- **Node.js**: v18.0.0 or higher
- **Python**: 3.9 or higher (recommended 3.10+)
- **npm**: v9.0.0 or higher (comes with Node.js)
- **pip**: Latest version (comes with Python)
- **Git**: For version control

### Optional Requirements
- **Redis Server**: For caching (if using Redis features)
- **PostgreSQL**: For production database (optional, SQLite used by default)
- **RTSP Camera**: For video streaming (optional, simulation mode available)

---

## Backend Setup (Python/FastAPI)

### 1. Navigate to Backend Directory
```bash
cd SmartGuard/Backend
```

### 2. Create Python Virtual Environment
```bash
# Windows
python -m venv venv

# Linux/Mac
python3 -m venv venv
```

### 3. Activate Virtual Environment
```bash
# Windows
lastenv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 4. Upgrade pip
```bash
pip install --upgrade pip
```

### 5. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 6. Environment Configuration
Copy the example environment file and configure it:
```bash
copy .env.example .env
```

Edit `.env` file with your actual values:

```env
# Email Configuration (Gmail example)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password

# Moderator Emails
MODERATOR_EMAIL_1=admin@smartguard.com
MODERATOR_EMAIL_2=moderator@smartguard.com

# Supabase Configuration
SUPABASE_URL=https://chjonhyjqztktxspwlkd.supabase.co
SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE=your_supabase_service_role_key

# Twilio Configuration (Optional)
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=+1234567890
TWILIO_WHATSAPP_NUMBER=+1234567890
RECIPIENT_PHONE_NUMBER=+1234567890

# Redis Configuration (Optional)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# Application Settings
DEBUG=False
ENVIRONMENT=development
SECRET_KEY=your_secret_key_here_change_in_production
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALGORITHM=HS256

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

### 7. Verify Backend Installation
```bash
python -c "import fastapi; print(fastapi.__version__)"
python -c "import tensorflow; print(tensorflow.__version__)"
python -c "import cv2; print(cv2.__version__)"
```

### 8. Start Backend Server
```bash
python start_backend.py
```

Backend will start at: `http://127.0.0.1:8001`

API Documentation available at:
- Swagger UI: `http://127.0.0.1:8001/docs`
- ReDoc: `http://127.0.0.1:8001/redoc`

---

## Frontend Setup (React/Vite)

### 1. Navigate to Frontend Directory
```bash
cd SmartGuard/Frontend
```

### 2. Install Node Dependencies
```bash
npm install
```

### 3. Environment Configuration
Create a `.env` file in the Frontend directory:
```env
VITE_API_URL=http://127.0.0.1:8001
VITE_SUPABASE_URL=https://chjonhyjqztktxspwlkd.supabase.co
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
```

### 4. Verify Frontend Installation
```bash
npm list react
npm list vite
```

### 5. Start Development Server
```bash
npm run dev
```

Frontend will be available at: `http://localhost:5173` (or another port if 5173 is occupied)

### 6. Build for Production
```bash
npm run build
```

### 7. Preview Production Build
```bash
npm run preview
```

---

## Complete Backend Dependencies List

### Core Framework
- `fastapi>=0.104.0` - Modern web framework for building APIs
- `uvicorn[standard]>=0.24.0` - ASGI server with hot reload
- `python-multipart>=0.0.6` - Form data parsing
- `pydantic>=2.5.0` - Data validation using Python type annotations
- `python-dotenv>=1.0.0` - Environment variable management

### Data Processing
- `pandas>=2.1.0` - Data manipulation and analysis
- `numpy>=1.24.0` - Numerical computing
- `openpyxl>=3.1.0` - Excel file handling

### Computer Vision & ML
- `opencv-python>=4.8.0` - Computer vision and video processing
- `tensorflow>=2.15.0` - Machine learning framework
- `keras>=2.15.0` - Deep learning API

### Authentication & Security
- `passlib>=1.7.4` - Password hashing
- `bcrypt>=4.1.0` - Password hashing library
- `PyJWT>=2.8.0` - JWT token handling

### HTTP & Async
- `httpx>=0.25.0` - Async HTTP client
- `requests>=2.31.0` - HTTP library
- `aiofiles>=23.2.0` - Async file operations

### External Services
- `twilio>=8.11.0` - SMS and WhatsApp notifications
- `redis>=5.0.0` - Redis client for caching

### Database (Optional)
- `psycopg2-binary>=2.9.0` - PostgreSQL adapter (commented out by default)

---

## Complete Frontend Dependencies List

### Core Dependencies
- `react@^18.2.0` - React UI library
- `react-dom@^18.2.0` - React DOM renderer
- `react-router-dom@^6.20.0` - Client-side routing
- `vite@^5.0.0` - Build tool and dev server

### Supabase Integration
- `@supabase/supabase-js@^2.39.0` - Supabase client

### HTTP Client
- `axios@^1.6.0` - HTTP client for API calls

### Internationalization
- `i18next@^23.7.0` - Internationalization framework
- `i18next-browser-languagedetector@^7.2.0` - Language detection
- `react-i18next@^13.5.0` - React bindings for i18next

### UI Components
- `lucide-react@^0.300.0` - Icon library

### Development Dependencies
- `@vitejs/plugin-react@^4.2.0` - Vite React plugin
- `eslint@^8.55.0` - Code linting
- `eslint-plugin-react-hooks@^4.6.0` - React hooks linting
- `eslint-plugin-react-refresh@^0.4.5` - React refresh linting
- `@types/react@^18.2.0` - React type definitions
- `@types/react-dom@^18.2.0` - React DOM type definitions
- `globals@^13.24.0` - Global variables for ESLint

---

## Project Structure

```
Smart Guard/
├── SmartGuard/
│   ├── Frontend/                 # React Frontend
│   │   ├── src/
│   │   │   ├── components/      # React components
│   │   │   ├── pages/          # Page components
│   │   │   ├── services/       # API services
│   │   │   ├── config/         # Configuration files
│   │   │   └── styles/         # CSS files
│   │   ├── package.json        # Frontend dependencies
│   │   └── vite.config.js      # Vite configuration
│   │
│   ├── Backend/                 # Python Backend
│   │   ├── routers/           # API route handlers
│   │   ├── services/          # Business logic services
│   │   ├── models/            # ML models
│   │   ├── utils/             # Utility functions
│   │   ├── config/            # Configuration
│   │   ├── workers/           # Background workers
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── main.py            # FastAPI application
│   │   ├── requirements.txt   # Python dependencies
│   │   └── .env               # Environment variables
│   │
│   └── supabase/              # Supabase migrations and policies
│
└── package.json               # Root package.json
```

---

## Common Issues & Solutions

### Backend Issues

#### Issue: TensorFlow Installation Fails
**Solution**: 
```bash
# Install CPU version first (faster)
pip install tensorflow-cpu>=2.15.0

# If GPU is needed, install CUDA and cuDNN first, then:
pip install tensorflow>=2.15.0
```

#### Issue: OpenCV Installation Fails
**Solution**:
```bash
# Try alternative package
pip install opencv-python-headless>=4.8.0
```

#### Issue: Port Already in Use
**Solution**:
```bash
# Kill process on port 8001 (Windows)
netstat -ano | findstr :8001
taskkill /PID <PID> /F

# Kill process on port 8001 (Linux/Mac)
lsof -ti:8001 | xargs kill -9
```

### Frontend Issues

#### Issue: Port 5173 Already in Use
**Solution**:
```bash
# Use different port
npm run dev -- --port 5174
```

#### Issue: Module Not Found
**Solution**:
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

#### Issue: Vite Build Fails
**Solution**:
```bash
# Clear Vite cache
rm -rf .vite dist
npm run build
```

---

## Development Workflow

### Starting Both Servers

**Terminal 1 - Backend:**
```bash
cd SmartGuard/Backend
venv\Scripts\activate
python start_backend.py
```

**Terminal 2 - Frontend:**
```bash
cd SmartGuard/Frontend
npm run dev
```

### Running Tests

**Backend:**
```bash
cd SmartGuard/Backend
pytest tests/
```

**Frontend:**
```bash
cd SmartGuard/Frontend
npm test
```

### Code Linting

**Backend:**
```bash
cd SmartGuard/Backend
pylint main.py
```

**Frontend:**
```bash
cd SmartGuard/Frontend
npm run lint
```

---

## Production Deployment

### Backend Deployment

1. **Set Environment Variables**:
   - Update `.env` with production values
   - Set `DEBUG=False`
   - Use strong `SECRET_KEY`

2. **Use Production Server**:
   ```bash
   gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

3. **Database**:
   - Migrate from SQLite to PostgreSQL
   - Install: `pip install psycopg2-binary>=2.9.0`

### Frontend Deployment

1. **Build for Production**:
   ```bash
   npm run build
   ```

2. **Serve Static Files**:
   - Deploy `dist/` folder to any static file server
   - Configure server for SPA routing

---

## Security Best Practices

1. **Never commit `.env` files** - Use `.env.example` as template
2. **Use strong secrets** - Generate random keys for production
3. **Enable CORS only for trusted domains** - Update `allow_origins`
4. **Use HTTPS in production** - Enable SSL/TLS
5. **Keep dependencies updated** - Run `npm audit` and `pip audit` regularly
6. **Implement rate limiting** - Protect API endpoints
7. **Validate all inputs** - Use Pydantic schemas on backend
8. **Use environment-specific configs** - Separate dev/staging/prod configs

---

## Additional Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **React Documentation**: https://react.dev/
- **Vite Documentation**: https://vitejs.dev/
- **Supabase Documentation**: https://supabase.com/docs
- **TensorFlow Documentation**: https://www.tensorflow.org/guide

---

## Support

For issues or questions:
1. Check the logs in `SmartGuard/Backend/logs/`
2. Review API documentation at `http://127.0.0.1:8001/docs`
3. Verify all dependencies are installed correctly
4. Ensure environment variables are set correctly

---

**Last Updated**: June 13, 2026
**Version**: 1.0.0
