import fitz
import markdown2
from bs4 import BeautifulSoup
import textwrap

def generate_pdf_roadmap(career, experience_level, roadmap_content):
    # Convert markdown to HTML
    html = markdown2.markdown(roadmap_content)
    
    # Parse HTML and extract text
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text()

    # Create a new PDF document
    doc = fitz.open()
    page = doc.new_page()

    # Add letterhead to the first page
    letterhead = fitz.Rect(0, 0, page.rect.width, 100)
    page.insert_image(letterhead, filename="img/letterhead.png")

    
    # Add title
    page.insert_text((50, 120), "Your Tech Career Roadmap", fontsize=14, fontname="helv", fontfile=None, set_simple=True)
    
    # Add career and experience level
    page.insert_text((50, 150), f"Career: {career}", fontsize=12, fontname="helv", fontfile=None, set_simple=True)
    page.insert_text((50, 170), f"Experience Level: {experience_level}", fontsize=12, fontname="helv", fontfile=None, set_simple=True)
    

    # Add content
    margin = 50  # Set margin value
    content_width = page.rect.width - 2 * margin
    
    
    y = 200
    for line in text.split('\n'):
        
        if line.strip():
            if line.startswith('##') or line.startswith('****'):
                wrapped_text = textwrap.wrap(line, width=int(content_width / 4.5))
                for wrapped_line in wrapped_text:
                    page.insert_text((margin, y), wrapped_line, fontsize=12, fontname="helv-bold", fontfile=None, set_simple=True)
                    y += 30
            elif line.startswith('#') or line.startswith('****'):  # Main heading
                wrapped_text = textwrap.wrap(line, width=int(content_width / 4.5))
                for wrapped_line in wrapped_text:
                    page.insert_text((margin, y), wrapped_line, fontsize=12, fontname="helv-bold", fontfile=None, set_simple=True)
                    y += 30
            else:  # Regular text
                wrapped_text = textwrap.wrap(line, width=int(content_width / 4.5))
                for wrapped_line in wrapped_text:
                    page.insert_text((margin, y), wrapped_line, fontsize=10, fontname="helv", fontfile=None, set_simple=True)
                    y += 30
            if y > 750:  # Start a new page if we're near the bottom
                page = doc.new_page()
                y = 50

    # Add footer to all pages
    for page in doc:
        page.insert_text((50, 800), "www.ygit.info", fontsize=8, fontname="helv", fontfile=None, set_simple=True)
        page.insert_text((500, 800), f"Page {page.number + 1}", fontsize=8, fontname="helv", fontfile=None, set_simple=True)

    # Save PDF
    filename = f"{career.replace(' ', '_')}_ygit_roadmap.pdf"
    doc.save(filename)
    return filename

