from tortoise import fields
from tortoise.models import Model

class Resume(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255, null=True)
    phone = fields.CharField(max_length=50, null=True)
    total_years_experience = fields.FloatField(null=True)
    
    # Last job details
    last_job_title = fields.CharField(max_length=255, null=True)
    last_job_company = fields.CharField(max_length=255, null=True)
    last_job_duration = fields.CharField(max_length=100, null=True)
    
    # Educational details
    highest_degree = fields.CharField(max_length=255, null=True)
    university = fields.CharField(max_length=255, null=True)
    graduation_year = fields.CharField(max_length=50, null=True)
    
    # Special highlights
    special_highlights = fields.TextField(null=True)
    
    # Skills
    skills = fields.TextField(null=True)
    
    # Metadata
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    
    class Meta:
        table = "resumes"
    
    async def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "total_years_experience": self.total_years_experience,
            "last_job": {
                "title": self.last_job_title,
                "company": self.last_job_company,
                "duration": self.last_job_duration
            },
            "education": {
                "highest_degree": self.highest_degree,
                "university": self.university,
                "graduation_year": self.graduation_year
            },
            "special_highlights": self.special_highlights,
            "skills": self.skills,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }