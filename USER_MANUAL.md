# ResumeScanner User Manual

**Version 1.0.0**  
**Last Updated: December 2025**

---

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Uploading Resumes](#uploading-resumes)
4. [Viewing Parsed Results](#viewing-parsed-results)
5. [Managing Resume Data](#managing-resume-data)
6. [Exporting to Excel](#exporting-to-excel)
7. [Understanding the Data](#understanding-the-data)
8. [Troubleshooting](#troubleshooting)
9. [Frequently Asked Questions (FAQ)](#frequently-asked-questions-faq)

---

## Introduction

### What is ResumeScanner?

ResumeScanner is an intelligent resume parsing application that automatically extracts structured information from resume files. Using advanced AI technology, it can process multiple resumes at once and organize the data in an easy-to-read format.

### What Can It Do?

- **Bulk Processing**: Upload and process multiple resumes simultaneously
- **Smart Extraction**: Automatically extracts names, contact info, work experience, education, and skills
- **Data Management**: View, search, and manage all parsed resume data
- **Excel Export**: Download all data as an Excel spreadsheet for further analysis
- **User-Friendly**: Simple web interface - no technical knowledge required

### Who Is This For?

- HR professionals managing job applications
- Recruiters processing candidate resumes
- Hiring managers reviewing applicants
- Anyone who needs to organize resume data efficiently

---

## Getting Started

### Accessing ResumeScanner

1. **Open Your Web Browser**
   - Use Chrome, Firefox, Safari, or Edge
   - Recommended: Use the latest version for best performance

2. **Navigate to the Application**
   - If running locally: Open `index.html` in your browser
   - If deployed: Visit the URL provided by your administrator
   - Example: `http://localhost:8080` or `https://your-company-resume-scanner.com`

3. **You Should See**
   - A purple gradient header with "📄 Resume Parser"
   - An upload section with a "Choose Files" button
   - A section showing all parsed resumes below

### System Requirements

- **Browser**: Modern web browser (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+)
- **Internet Connection**: Required for AI processing
- **File Formats Supported**: PDF (.pdf), Microsoft Word (.docx, .doc)

---

## Uploading Resumes

### Step-by-Step Upload Process

#### Step 1: Select Resume Files

1. Click the **"📁 Choose Files"** button in the upload section
2. A file browser window will open
3. Navigate to the folder containing your resume files
4. Select one or more resume files:
   - **Single file**: Click on the file
   - **Multiple files**: Hold `Ctrl` (Windows) or `Cmd` (Mac) and click each file
   - **Range of files**: Click first file, hold `Shift`, click last file

#### Step 2: Review Selected Files

After selecting files, you'll see:
- A list of selected files with their names and sizes
- Example: `John_Doe_Resume.pdf (245.67 KB)`
- A **Remove** button next to each file if you want to deselect it

**To Remove a File:**
- Click the red **Remove** button next to the filename
- The file will be removed from the upload queue

#### Step 3: Upload and Process

1. Click the green **"Upload & Process Resumes"** button
2. You'll see:
   - The button changes to "Processing..." with a loading animation
   - A progress bar appears showing processing status
3. Wait for processing to complete (usually 5-15 seconds per resume)

#### Step 4: View Results

After processing completes:
- A summary box appears showing:
  - **Total Files**: Number of files uploaded
  - **Successful**: Number of successfully processed resumes
  - **Failed**: Number of files that couldn't be processed
- The resume list automatically refreshes with new entries
- A success message appears at the top

### Supported File Types

| Format | Extension | Notes |
|--------|-----------|-------|
| PDF | `.pdf` | Most common format, best compatibility |
| Microsoft Word | `.docx` | Modern Word format (2007+) |
| Microsoft Word | `.doc` | Older Word format (pre-2007) |

### File Size Limits

- **Recommended**: Under 5 MB per file
- **Maximum**: 10 MB per file
- Larger files may take longer to process

### Tips for Best Results

✅ **DO:**
- Use clear, well-formatted resumes
- Ensure PDFs contain actual text (not just images)
- Use standard resume formats
- Check that files aren't password-protected

❌ **DON'T:**
- Upload scanned images without OCR
- Use heavily formatted or graphical resumes
- Upload corrupted or damaged files
- Upload non-resume documents

---

## Viewing Parsed Results

### The Resume List

After uploading, all parsed resumes appear in a table with the following columns:

| Column | Description |
|--------|-------------|
| **ID** | Unique identifier for each resume |
| **Name** | Candidate's full name |
| **Email** | Email address |
| **Experience** | Total years of work experience |
| **Last Job** | Most recent job title and company |
| **Actions** | View and Delete buttons |

### Viewing Detailed Information

To see complete details for a resume:

1. Find the resume in the list
2. Click the blue **"View"** button in the Actions column
3. A detailed view expands below the row showing:
   - **Phone**: Contact number
   - **Total Experience**: Years of professional experience
   - **Last Job Duration**: Time period of most recent job
   - **Education**: Degree, university, and graduation year
   - **Skills**: List of technical and professional skills
   - **Special Highlights**: Achievements, awards, certifications

4. Click **"View"** again to collapse the details

### Refreshing the List

To update the list with the latest data:
- Click the **"🔄 Refresh List"** button at the top
- The list will reload with current database information

---

## Managing Resume Data

### Deleting a Single Resume

To remove one resume from the database:

1. Locate the resume in the list
2. Click the red **"Delete"** button in the Actions column
3. A confirmation dialog appears: "Are you sure you want to delete this resume?"
4. Click **"OK"** to confirm or **"Cancel"** to abort
5. If confirmed, the resume is permanently deleted
6. The list automatically refreshes

### Deleting All Resumes

To clear the entire database:

1. Click the red **"🗑️ Clear All Resumes"** button at the top
2. A confirmation dialog appears: "Are you sure you want to delete ALL resumes? This cannot be undone."
3. Click **"OK"** to confirm or **"Cancel"** to abort
4. If confirmed, all resumes are permanently deleted
5. The list shows "No resumes found"

⚠️ **Warning**: This action cannot be undone! Make sure to export data to Excel before clearing if you need to keep records.

---

## Exporting to Excel

### How to Export Data

1. Click the green **"📥 Download Excel"** button at the top of the page
2. The button changes to "⏳ Generating Excel..." while processing
3. An Excel file automatically downloads to your computer
4. The file is named: `resumes_export_YYYY-MM-DD.xlsx` (with current date)

### What's Included in the Export

The Excel file contains one sheet named "Resumes" with all resume data:

| Column | Data |
|--------|------|
| ID | Unique identifier |
| Name | Candidate name |
| Email | Email address |
| Phone | Phone number |
| Total Experience (Years) | Years of work experience |
| Last Job Title | Most recent position |
| Last Job Company | Most recent employer |
| Last Job Duration | Time period of last job |
| Highest Degree | Educational qualification |
| University | Educational institution |
| Graduation Year | Year of graduation |
| Skills | Comma-separated skills list |
| Special Highlights | Achievements and awards |
| Created At | When the resume was uploaded |

### Using the Excel File

Once downloaded, you can:
- Open in Microsoft Excel, Google Sheets, or LibreOffice
- Sort and filter candidates
- Create pivot tables and charts
- Share with team members
- Import into other systems (ATS, CRM, etc.)
- Perform data analysis

### Export Tips

- Export regularly to keep backups of your data
- Use filters in Excel to find candidates with specific skills
- Sort by experience level to prioritize candidates
- Create multiple exports with different date ranges for tracking

---

## Understanding the Data

### Personal Information

**Name**
- Extracted from the top of the resume
- Usually includes first and last name
- May include middle name or initials

**Email**
- Primary email address from the resume
- Usually found in contact information section

**Phone**
- Contact phone number
- May include country code and formatting

### Work Experience

**Total Years of Experience**
- Calculated from all professional work positions
- **Excludes** education years and internships
- Counts only actual employment time
- Example: 5 years means 5 years of professional work

**Last Job Title**
- Most recent position held
- Example: "Senior Software Engineer", "Marketing Manager"

**Last Job Company**
- Name of the most recent employer
- Example: "Google", "Microsoft", "ABC Corporation"

**Last Job Duration**
- Time period of the most recent job
- Format: "Month Year - Month Year" or "Month Year - Present"
- Example: "Jan 2020 - Present", "Mar 2018 - Dec 2021"

### Education

**Highest Degree**
- Highest educational qualification
- Examples: "Bachelor's in Computer Science", "MBA", "Master's in Engineering"

**University**
- Name of the educational institution
- Examples: "Stanford University", "MIT", "Harvard Business School"

**Graduation Year**
- Year of graduation or completion
- Example: "2020", "2018"

### Additional Information

**Skills**
- Comma-separated list of technical and professional skills
- Examples: "Python, JavaScript, Project Management, SQL, Leadership"

**Special Highlights**
- Notable achievements, awards, certifications
- Volunteer work or community involvement
- Publications or patents
- Professional certifications

---

## Troubleshooting

### Upload Issues

#### Problem: "No files uploaded" error

**Solution:**
- Make sure you've selected at least one file
- Click "Choose Files" and select files before clicking "Upload & Process"

#### Problem: "Unsupported file type" error

**Solution:**
- Only PDF (.pdf) and Word (.docx, .doc) files are supported
- Convert other formats to PDF before uploading
- Check that the file extension is correct

#### Problem: Files upload but parsing fails

**Possible Causes & Solutions:**

1. **Scanned PDF (image-based)**
   - The PDF contains images of text, not actual text
   - Solution: Use OCR software to convert to text-based PDF

2. **Password-protected file**
   - File is encrypted or password-protected
   - Solution: Remove password protection before uploading

3. **Corrupted file**
   - File is damaged or incomplete
   - Solution: Try re-downloading or re-creating the file

4. **Non-standard format**
   - Resume uses unusual formatting or layout
   - Solution: Try converting to a simpler format

### Display Issues

#### Problem: Resume list doesn't show uploaded resumes

**Solution:**
- Click the "🔄 Refresh List" button
- Check if upload was successful (look for success message)
- Refresh your browser page (F5 or Ctrl+R)

#### Problem: Details don't expand when clicking "View"

**Solution:**
- Refresh the browser page
- Try clicking again
- Check browser console for errors (F12)

### Excel Export Issues

#### Problem: Excel download doesn't start

**Solution:**
- Check that at least one resume exists in the database
- Ensure browser allows downloads (check browser settings)
- Try a different browser
- Check your download folder - it may have downloaded silently

#### Problem: Excel file is empty or incomplete

**Solution:**
- Verify resumes exist by checking the resume list
- Try refreshing the page and exporting again
- Check if your browser blocked the download

### Connection Issues

#### Problem: "Error uploading files" or "Error loading resumes"

**Solution:**
- Check your internet connection
- Verify the API server is running
- Contact your system administrator
- Try refreshing the page

#### Problem: Page loads but buttons don't work

**Solution:**
- Check that JavaScript is enabled in your browser
- Try clearing browser cache (Ctrl+Shift+Delete)
- Try a different browser
- Disable browser extensions that might interfere

### Data Quality Issues

#### Problem: Extracted data is incorrect or incomplete

**Possible Causes:**

1. **Resume format is non-standard**
   - AI may have difficulty parsing unusual layouts
   - Solution: Manually correct data if needed

2. **Resume contains minimal information**
   - Not enough data in the original resume
   - Solution: Request updated resume from candidate

3. **PDF text extraction issues**
   - Text may be scrambled or in wrong order
   - Solution: Try converting to Word format first

---

## Frequently Asked Questions (FAQ)

### General Questions

**Q: How many resumes can I upload at once?**  
A: You can upload as many as you want simultaneously. However, processing time increases with more files. We recommend batches of 10-20 for optimal performance.

**Q: How long does processing take?**  
A: Typically 5-15 seconds per resume, depending on file size and complexity. Larger batches may take a few minutes.

**Q: Is my data secure?**  
A: Yes. All data is stored in a secure database. Consult your system administrator about specific security measures in place.

**Q: Can I edit the extracted data?**  
A: The current version doesn't support editing through the UI. You can export to Excel and edit there, or contact your administrator about database access.

### File Format Questions

**Q: Why doesn't it work with scanned PDFs?**  
A: Scanned PDFs are images, not text. The system needs actual text to parse. Use OCR software to convert scanned PDFs to text-based PDFs first.

**Q: Can I upload other formats like RTF or TXT?**  
A: Currently, only PDF and Word (.docx, .doc) formats are supported. Convert other formats to one of these before uploading.

**Q: What if the resume is in multiple languages?**  
A: The AI primarily works with English resumes. Other languages may have reduced accuracy.

### Data Questions

**Q: Why is the experience calculation sometimes wrong?**  
A: The AI calculates based on job dates in the resume. If dates are unclear or formatted unusually, it may miscalculate. Education years are excluded from the calculation.

**Q: What if some fields are empty?**  
A: If information isn't found in the resume, fields will show "N/A" or be empty. This means the data wasn't present or couldn't be extracted.

**Q: Can I search for specific candidates?**  
A: Use the Excel export feature and apply filters in Excel to search by name, skills, experience, etc.

### Technical Questions

**Q: Do I need to install anything?**  
A: No. ResumeScanner is a web application - just use your browser. Your administrator handles the installation.

**Q: Can I use this on my phone or tablet?**  
A: Yes, the interface is responsive and works on mobile devices, though the experience is optimized for desktop.

**Q: What browsers are supported?**  
A: Modern versions of Chrome, Firefox, Safari, and Edge. We recommend keeping your browser updated.

**Q: Can I use this offline?**  
A: No. An internet connection is required for AI processing and database access.

### Usage Questions

**Q: Can multiple people use this at the same time?**  
A: Yes. Multiple users can upload and view resumes simultaneously.

**Q: How do I organize resumes by job position?**  
A: Export to Excel and use filters or create separate sheets for different positions.

**Q: Can I recover deleted resumes?**  
A: No. Deletion is permanent. Always export to Excel before deleting if you might need the data later.

**Q: Is there a limit to how many resumes I can store?**  
A: This depends on your database configuration. Contact your administrator for specific limits.

---

## Getting Help

### If You Need Assistance

1. **Check this manual** - Most common questions are answered here
2. **Try the Troubleshooting section** - Solutions to common problems
3. **Contact your system administrator** - For technical issues or access problems
4. **Report bugs** - If you find a bug, document the steps to reproduce it and report to your administrator

### Best Practices

✅ **Regular Exports** - Export data to Excel regularly as a backup

✅ **File Organization** - Keep original resume files organized in folders

✅ **Quality Check** - Review extracted data for accuracy, especially for important candidates

✅ **Batch Processing** - Upload resumes in reasonable batches (10-20 at a time)

✅ **Browser Updates** - Keep your web browser updated for best performance

---

## Appendix: Quick Reference

### Common Actions

| Action | Steps |
|--------|-------|
| Upload resumes | Choose Files → Select files → Upload & Process |
| View details | Click "View" button next to resume |
| Delete one resume | Click "Delete" button → Confirm |
| Delete all resumes | Click "Clear All Resumes" → Confirm |
| Export to Excel | Click "Download Excel" button |
| Refresh list | Click "Refresh List" button |

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| F5 or Ctrl+R | Refresh page |
| Ctrl+Click | Select multiple files |
| Shift+Click | Select range of files |

### File Format Support

| Format | Extension | Supported |
|--------|-----------|-----------|
| PDF | .pdf | ✅ Yes |
| Word (Modern) | .docx | ✅ Yes |
| Word (Legacy) | .doc | ✅ Yes |
| Rich Text | .rtf | ❌ No |
| Plain Text | .txt | ❌ No |
| Images | .jpg, .png | ❌ No |

---

**End of User Manual**

For technical documentation, please refer to the README.md file.

---

*ResumeScanner v1.0.0 - Powered by AI*
