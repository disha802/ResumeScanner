# Resume Parser Application

AI-powered bulk resume parsing application using FastAPI, Groq (Llama 3.3), and Neon DB with Tortoise ORM.

## Features

- ✅ Bulk upload of resumes (PDF, DOCX)
- ✅ AI-powered extraction using Groq's Llama 3.3 70B
- ✅ Extracts: Name, Contact, Experience, Last Job, Education, Special Highlights
- ✅ Transactional database operations with Tortoise ORM
- ✅ Neon DB (PostgreSQL) integration
- ✅ Beautiful demo UI with vanilla HTML/CSS/JS
- ✅ RESTful API with FastAPI

## Project Structure

```
resume-parser/
├── main.py              # FastAPI application
├── models.py            # Tortoise ORM models
├── database.py          # Database configuration
├── services.py          # Resume parsing service
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables
├── .env.example         # Example environment file
├── index.html           # Demo UI
└── README.md            # This file
```

## Prerequisites

- Python 3.9+
- Groq API Key
- Neon DB account and database

## Setup Instructions

### 1. Clone or Create Project Directory

```bash
mkdir resume-parser
cd resume-parser
```

### 2. Create Virtual Environment

```bash
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

### 4. Set Up Neon Database

1. Go to [Neon Console](https://console.neon.tech/)
2. Create a new project
3. Create a new database (or use the default)
4. Copy your connection string (it looks like):
   ```
   postgresql://username:password@ep-xxx-xxx.region.aws.neon.tech/dbname?sslmode=require
   ```

### 5. Configure Environment Variables

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your credentials:
   ```env
   GROQ_API_KEY=your_actual_groq_api_key
   DATABASE_URL=your_actual_neon_connection_string
   ```

### 6. Run the Application

```bash
python main.py
```

The API will start at `http://localhost:8000`

### 7. Open the Demo UI

1. Open `index.html` in your web browser
2. Or serve it using Python:
   ```bash
   python -m http.server 8080
   ```
   Then visit `http://localhost:8080`

## API Endpoints

### Upload Resumes (Bulk)
```http
POST /upload/bulk
Content-Type: multipart/form-data

files: [file1.pdf, file2.docx, ...]
```

### Get All Resumes
```http
GET /resumes?skip=0&limit=100
```

### Get Single Resume
```http
GET /resumes/{resume_id}
```

### Delete Resume
```http
DELETE /resumes/{resume_id}
```

### Delete All Resumes
```http
DELETE /resumes
```

## Database Schema

The `resumes` table includes:

- `id`: Primary key
- `name`: Candidate name
- `email`: Email address
- `phone`: Phone number
- `total_years_experience`: Total years of experience
- `last_job_title`: Most recent job title
- `last_job_company`: Most recent company
- `last_job_duration`: Duration of last job
- `highest_degree`: Highest educational degree
- `university`: University name
- `graduation_year`: Year of graduation
- `special_highlights`: Notable achievements/awards
- `skills`: Technical and professional skills
- `created_at`: Timestamp
- `updated_at`: Timestamp

## Transactional Processing

The application uses Tortoise ORM's built-in transaction support. Each resume upload is processed atomically:

- If parsing fails, no database entry is created
- Bulk uploads process each file independently
- Failed uploads don't affect successful ones
- Database operations are automatically rolled back on errors

## How It Works

1. **Upload**: User uploads multiple resume files (PDF/DOCX)
2. **Text Extraction**: Text is extracted from files using PyPDF2/python-docx
3. **AI Processing**: Groq's Llama 3.3 analyzes the text and extracts structured data
4. **Database Storage**: Parsed data is saved to Neon DB using Tortoise ORM
5. **Results Display**: UI shows success/failure for each file

## Supported File Formats

- PDF (.pdf)
- Microsoft Word (.docx, .doc)

## Error Handling

- Invalid file formats are rejected
- Failed parsing doesn't stop other files from processing
- Detailed error messages for debugging
- Graceful handling of missing fields

## Development

### Run with Auto-reload
```bash
uvicorn main:app --reload
```

### Check API Documentation
Visit `http://localhost:8000/docs` for interactive API documentation

## Troubleshooting

### Database Connection Issues
- Verify your DATABASE_URL is correct
- Check that your Neon database is active
- Ensure SSL mode is enabled in connection string

### Groq API Issues
- Verify your GROQ_API_KEY is valid
- Check your API usage limits
- Ensure you have access to llama-3.3-70b-versatile

### File Upload Issues
- Check file size limits
- Verify file format is supported
- Ensure proper CORS configuration

## Production Deployment

For production deployment:

1. Set proper CORS origins in `main.py`
2. Use environment variables for all secrets
3. Enable HTTPS
4. Set up proper logging
5. Configure rate limiting
6. Use a production ASGI server (Gunicorn + Uvicorn)

## License

MIT License

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## Support

For issues or questions, please create an issue in the repository.