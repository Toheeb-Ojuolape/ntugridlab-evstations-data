import pandas as pd

# Create a dictionary with the content calendar data
calendar_data = {
    "Week": ["Week 1", "Week 2", "Week 3", "Week 4", "Week 5"],
    "Content Theme": [
        "Introduction to Energy & YPN",
        "Energy Challenges in the West Midlands",
        "Career Opportunities in Energy",
        "Innovative Energy Solutions",
        "Networking & Professional Development in Energy"
    ],
    "Content Type": [
        "Blog Post & Social Media Introduction",
        "Infographic & Case Study",
        "Webinar & Interview",
        "Article & Video Showcase",
        "Networking Event & Social Media Recap"
    ],
    "Key Dates": [
        "Monday: Blog Launch, Wednesday: Social Media Post",
        "Tuesday: Infographic, Thursday: Case Study Release",
        "Wednesday: Webinar, Friday: Interview with a Professional",
        "Thursday: Article Publication, Saturday: Video Release",
        "Friday: Networking Event, Sunday: Social Media Recap"
    ],
    "Platform": [
        "Website, LinkedIn, Twitter",
        "Website, LinkedIn, Instagram",
        "Zoom, LinkedIn, Twitter",
        "Website, YouTube, LinkedIn",
        "Event Platform, LinkedIn, Twitter"
    ],
    "Goals": [
        "Introduce YPN & Energy Institute, Gain Followers",
        "Raise Awareness on Regional Energy Challenges",
        "Highlight Career Paths, Engage with Professionals",
        "Showcase Innovation, Inspire Ideas",
        "Foster Networking, Strengthen Community"
    ]
}

# Convert dictionary to DataFrame
df_calendar = pd.DataFrame(calendar_data)

# Save DataFrame to an Excel file
file_path = "./energy_ypn_content_calendar.xlsx"
df_calendar.to_excel(file_path, index=False)

# Return the file path for download
file_path
