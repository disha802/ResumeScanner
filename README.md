# ResumeScanner - AI-Powered Resume Parser

An intelligent bulk resume parsing application powered by Groq's Llama 3.3 70B AI model, FastAPI, and Neon PostgreSQL database. Extract structured data from resumes automatically with high accuracy.

## ✨ Features

- 📤 **Bulk Upload** - Process multiple resumes simultaneously (PDF, DOCX formats)
- 🤖 **AI-Powered Extraction** - Uses Groq's Llama 3.3 70B for intelligent data extraction
- 📊 **Comprehensive Data Extraction**:
  - Personal Information (Name, Email, Phone)
  - Work Experience (Total years, Last job details)
  - Education (Degree, University, Graduation year)
  - Skills and Special Highlights
- 💾 **Robust Database** - PostgreSQL (Neon DB) with Tortoise ORM
- 🔄 **Transactional Processing** - Atomic operations with automatic rollback on errors
- 📥 **Excel Export** - Download all parsed resumes as Excel spreadsheet
- 🎨 **Beautiful Web UI** - Modern, responsive interface built with vanilla HTML/CSS/JS
- 🔌 **RESTful API** - Complete API with FastAPI and automatic documentation
- ⚡ **Rate Limit Handling** - Automatic retry logic for API rate limits
- 🔍 **Advanced PDF Parsing** - Dual extraction methods (PyPDF2 + pdfplumber) for maximum compatibility

## 📁 Project Structure

```
ResumeScanner/
├── main.py              # FastAPI application with all endpoints
├── models.py            # Tortoise ORM database models
├── database.py          # Database configuration and initialization
├── services.py          # Resume parsing service with AI integration
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (not in git)
├── .gitignore          # Git ignore rules
├── index.html          # Web UI for end users
├── README.md           # This file
└── USER_MANUAL.md      # End-user documentation
```

## 🔧 Prerequisites

- **Python 3.9+** installed on your system
- **Groq API Key** - Get one free at [console.groq.com](https://console.groq.com)
- **Neon Database** - Free PostgreSQL database at [neon.tech](https://neon.tech)

## 🚀 Setup Instructions

### 1. Clone or Download the Project

```bash
cd ResumeScanner
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies include:**
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `tortoise-orm` - Async ORM
- `asyncpg` - PostgreSQL driver
- `groq` - Groq AI SDK
- `PyPDF2` & `pdfplumber` - PDF text extraction
- `python-docx` - DOCX text extraction
- `pandas` & `openpyxl` - Excel export functionality
- `python-dotenv` - Environment variable management

### 4. Set Up Neon Database

1. Go to [Neon Console](https://console.neon.tech/)
2. Create a new project (or use existing)
3. Create a new database or use the default `neondb`
4. Copy your connection string from the dashboard:
   ```
   postgresql://username:password@ep-xxx-xxx.region.aws.neon.tech/dbname?sslmode=require
   ```

### 5. Get Groq API Key

1. Visit [console.groq.com](https://console.groq.com)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key (you won't be able to see it again!)

### 6. Configure Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=gsk_your_actual_groq_api_key_here
DATABASE_URL=postgresql://user:pass@ep-xxx.region.aws.neon.tech/dbname?sslmode=require
```

**Important:** Never commit your `.env` file to version control!

### 7. Run the Application

```bash
python main.py
```

The API server will start at `http://localhost:8000`

You should see output like:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 8. Access the Web UI

**Option 1:** Open `index.html` directly in your browser

**Option 2:** Serve it with Python (recommended):
```bash
# In a new terminal window
python -m http.server 8080
```
Then visit `http://localhost:8080`

## 📚 API Documentation

### Interactive API Docs

Visit `http://localhost:8000/docs` for interactive Swagger UI documentation.

### API Endpoints

#### Health Check
```http
GET /
```
Returns API status.

#### Test Groq Connection
```http
GET /test/groq
```
Tests if Groq API is working correctly.

#### Upload Resumes (Bulk)
```http
POST /upload/bulk
Content-Type: multipart/form-data

files: [file1.pdf, file2.docx, ...]
```

**Response:**
```json
{
  "total": 5,
  "successful": 4,
  "failed": 1,
  "errors": [...],
  "resumes": [...]
}
```

#### Get All Resumes
```http
GET /resumes?skip=0&limit=100
```

**Query Parameters:**
- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Maximum records to return (default: 100)

#### Get Single Resume
```http
GET /resumes/{resume_id}
```

#### Delete Resume
```http
DELETE /resumes/{resume_id}
```

#### Delete All Resumes
```http
DELETE /resumes
```

#### Export to Excel
```http
GET /export/excel
```

Downloads an Excel file with all parsed resume data. The file includes:
- All candidate information
- Work experience details
- Education information
- Skills and highlights
- Timestamps

## 🗄️ Database Schema

The `resumes` table structure:

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer | Primary key (auto-increment) |
| `name` | String(255) | Candidate full name |
| `email` | String(255) | Email address |
| `phone` | String(50) | Phone number |
| `total_years_experience` | Float | Total years of professional experience |
| `last_job_title` | String(255) | Most recent job title |
| `last_job_company` | String(255) | Most recent company name |
| `last_job_duration` | String(100) | Duration of last job (e.g., "Jan 2020 - Present") |
| `highest_degree` | String(255) | Highest educational degree |
| `university` | String(255) | University/college name |
| `graduation_year` | String(50) | Year of graduation |
| `special_highlights` | Text | Achievements, awards, certifications |
| `skills` | Text | Comma-separated skills list |
| `created_at` | DateTime | Record creation timestamp |
| `updated_at` | DateTime | Last update timestamp |

## 🔄 How It Works

1. **Upload** - User uploads multiple resume files through the web UI
2. **Text Extraction** - System extracts text from PDF/DOCX files using dual extraction methods
3. **AI Processing** - Groq's Llama 3.3 70B analyzes text and extracts structured data
4. **Validation** - Data is validated and normalized
5. **Database Storage** - Parsed data is saved to Neon DB using transactional operations
6. **Results Display** - UI shows success/failure status for each file

## 🛡️ Transactional Processing

The application uses Tortoise ORM's transaction support for data integrity:

- Each resume upload is processed atomically
- If parsing fails, no database entry is created
- Bulk uploads process each file independently
- Failed uploads don't affect successful ones
- Database operations automatically roll back on errors

## 📄 Supported File Formats

- **PDF** (.pdf) - Uses PyPDF2 with pdfplumber fallback
- **Microsoft Word** (.docx, .doc)

## ⚠️ Error Handling

- Invalid file formats are rejected with clear error messages
- Failed parsing doesn't stop other files from processing
- Rate limit errors trigger automatic retry with exponential backoff
- Detailed error messages for debugging
- Graceful handling of missing or malformed data

## 🔧 Development

### Run with Auto-reload

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### View Logs

The application logs processing details to console. Look for:
- File processing status
- AI parsing results
- Database operation confirmations
- Error messages with stack traces

## 🐛 Troubleshooting

### Database Connection Issues

**Problem:** `Could not connect to database`

**Solutions:**
- Verify your `DATABASE_URL` in `.env` is correct
- Check that your Neon database is active (not paused)
- Ensure `?sslmode=require` is at the end of the connection string
- Test connection from Neon dashboard

### Groq API Issues

**Problem:** `API key invalid` or `Rate limit exceeded`

**Solutions:**
- Verify your `GROQ_API_KEY` in `.env` is valid
- Check your API usage limits at console.groq.com
- Ensure you have access to `llama-3.3-70b-versatile` model
- Wait a few minutes if rate limited (automatic retry is built-in)

### File Upload Issues

**Problem:** Files not uploading or parsing fails

**Solutions:**
- Check file size (very large files may timeout)
- Verify file format is supported (.pdf, .docx, .doc)
- Ensure file is not corrupted or password-protected
- Check browser console for CORS errors
- Verify API server is running on port 8000

### PDF Extraction Issues

**Problem:** Text extraction returns empty or garbled text

**Solutions:**
- Some PDFs are image-based (scanned) - these require OCR
- Try re-saving the PDF with text layer
- Check if PDF is encrypted or protected
- The system tries PyPDF2 first, then falls back to pdfplumber

### Excel Export Not Working

**Problem:** Excel download fails or file is empty

**Solutions:**
- Ensure at least one resume is in the database
- Check that `pandas` and `openpyxl` are installed
- Verify browser allows file downloads
- Check browser's download folder

### CORS Errors in Browser

**Problem:** `CORS policy blocked` errors

**Solutions:**
- Ensure API server is running
- Check that `API_URL` in `index.html` matches your server URL
- For production, update CORS origins in `main.py`

## 🚀 Production Deployment

For production deployment, consider these steps:

### 1. Update CORS Configuration

In `main.py`, replace:
```python
allow_origins=["*"]
```

With specific origins:
```python
allow_origins=["https://yourdomain.com", "https://www.yourdomain.com"]
```

### 2. Environment Variables

- Use secure environment variable management
- Never commit `.env` to version control
- Use platform-specific secrets (e.g., Heroku Config Vars, Railway Variables)

### 3. Enable HTTPS

- Use a reverse proxy (Nginx, Caddy)
- Enable SSL/TLS certificates (Let's Encrypt)
- Ensure database connection uses SSL

### 4. Production Server

Replace `uvicorn` direct run with Gunicorn + Uvicorn workers:

```bash
pip install gunicorn
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### 5. Rate Limiting

Consider adding rate limiting middleware to prevent abuse:

```bash
pip install slowapi
```

### 6. Logging

Configure proper logging for production:

```python
import logging
logging.basicConfig(level=logging.INFO)
```

### 7. Monitoring

- Set up application monitoring (e.g., Sentry)
- Monitor database performance
- Track API usage and costs

## 📝 License

MIT License - feel free to use this project for personal or commercial purposes.

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 💡 Future Enhancements

Potential features for future versions:

- [ ] OCR support for scanned PDFs
- [ ] Multiple language support
- [ ] Batch job status tracking
- [ ] Resume ranking/scoring system
- [ ] Advanced search and filtering
- [ ] Email notification on completion
- [ ] Resume comparison tool
- [ ] API authentication and user management

## 📞 Support

For issues, questions, or feature requests:

- Create an issue in the repository
- Check existing issues for solutions
- Review the troubleshooting section above

## 🙏 Acknowledgments

- **Groq** - For providing fast and accurate AI inference
- **Neon** - For serverless PostgreSQL database
- **FastAPI** - For the excellent web framework
- **Tortoise ORM** - For async database operations

---

**Version:** 1.0.0  
**Last Updated:** December 2025  
**Python Version:** 3.9+