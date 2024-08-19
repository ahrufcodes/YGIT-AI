# import fitz
# import markdown2
# from bs4 import BeautifulSoup
# import textwrap

# def generate_pdf_roadmap(career, experience_level, roadmap_content):
#     # Convert markdown to HTML
#     html = markdown2.markdown(roadmap_content)
    
#     # Parse HTML and extract text
#     soup = BeautifulSoup(html, 'html.parser')
#     text = soup.get_text()

#     # Create a new PDF document
#     doc = fitz.open()
#     page = doc.new_page()

#     # Add letterhead to the first page
#     letterhead = fitz.Rect(0, 0, page.rect.width, 100)
#     page.insert_image(letterhead, filename="img/letterhead.png")

    
#     # Add title
#     page.insert_text((50, 120), "Your Tech Career Roadmap", fontsize=14, fontname="helv", fontfile=None, set_simple=True)
    
#     # Add career and experience level
#     page.insert_text((50, 150), f"Career: {career}", fontsize=12, fontname="helv", fontfile=None, set_simple=True)
#     page.insert_text((50, 170), f"Experience Level: {experience_level}", fontsize=12, fontname="helv", fontfile=None, set_simple=True)
    

#     # Add content
#     margin = 50  # Set margin value
#     content_width = page.rect.width - 2 * margin
    
    
#     y = 200
#     for line in text.split('\n'):
        
#         if line.strip():
#             if line.startswith('##') or line.startswith('****'):
#                 wrapped_text = textwrap.wrap(line, width=int(content_width / 4.5))
#                 for wrapped_line in wrapped_text:
#                     page.insert_text((margin, y), wrapped_line, fontsize=12, fontname="helv-bold", fontfile=None, set_simple=True)
#                     y += 30
#             elif line.startswith('#') or line.startswith('****'):  # Main heading
#                 wrapped_text = textwrap.wrap(line, width=int(content_width / 4.5))
#                 for wrapped_line in wrapped_text:
#                     page.insert_text((margin, y), wrapped_line, fontsize=12, fontname="helv-bold", fontfile=None, set_simple=True)
#                     y += 30
#             else:  # Regular text
#                 wrapped_text = textwrap.wrap(line, width=int(content_width / 4.5))
#                 for wrapped_line in wrapped_text:
#                     page.insert_text((margin, y), wrapped_line, fontsize=10, fontname="helv", fontfile=None, set_simple=True)
#                     y += 30
#             if y > 750:  # Start a new page if we're near the bottom
#                 page = doc.new_page()
#                 y = 50

#     # Add footer to all pages
#     for page in doc:
#         page.insert_text((50, 800), "www.ygit.info", fontsize=8, fontname="helv", fontfile=None, set_simple=True)
#         page.insert_text((500, 800), f"Page {page.number + 1}", fontsize=8, fontname="helv", fontfile=None, set_simple=True)

#     # Save PDF
#     filename = f"{career.replace(' ', '_')}_ygit_roadmap.pdf"
#     doc.save(filename)
#     return filename






import fitz
import markdown2
from bs4 import BeautifulSoup
import textwrap
import re

def generate_pdf_roadmap(career, experience_level, roadmap_content):
    # Convert markdown to HTML
    html = markdown2.markdown(roadmap_content, extras=['break-on-newline'])
    
    # Parse HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Create a new PDF document
    doc = fitz.open()
    page = doc.new_page()

    # Set margins
    margin_left = 50
    margin_right = 50
    margin_top = 50
    margin_bottom = 50

    # Add letterhead to the first page
    letterhead = fitz.Rect(0, 0, page.rect.width, 100)
    page.insert_image(letterhead, filename="img/letterhead.png")

    # Add title
    page.insert_text((margin_left, 120), "Your Tech Career Roadmap", fontsize=18, fontname="helvetica-bold")
    
    # Add career and experience level
    page.insert_text((margin_left, 150), f"Career: {career}", fontsize=14, fontname="helvetica-bold")
    page.insert_text((margin_left, 170), f"Experience Level: {experience_level}", fontsize=14, fontname="helvetica-bold")

    # Add content
    content_width = page.rect.width - margin_left - margin_right
    y = 200

    def insert_text_with_style(text, y, fontsize, is_bold=False, indent=0):
        font = "helvetica-bold" if is_bold else "helvetica"
        wrapped_text = textwrap.wrap(text, width=int((content_width - indent) / (fontsize / 2)))
        for wrapped_line in wrapped_text:
            page.insert_text((margin_left + indent, y), wrapped_line, fontsize=fontsize, fontname=font)
            y += fontsize * 1.2
        return y

    def process_element(element, y, level=0):
        if element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            y += 20  # Extra space before headings
            font_size = 20 - (int(element.name[1]) * 2)  # h1 = 18, h2 = 16, h3 = 14, etc.
            y = insert_text_with_style(element.text.strip(), y, font_size, is_bold=True)
            y += 10  # Extra space after headings
        elif element.name == 'p':
            y = insert_text_with_style(element.text.strip(), y, 11)
            y += 10  # Extra space after paragraphs
        elif element.name in ['ul', 'ol']:
            for i, li in enumerate(element.find_all('li', recursive=False)):
                bullet = '• ' if element.name == 'ul' else f"{i+1}. "
                y = insert_text_with_style(bullet + li.text.strip(), y, 11, indent=level*20)
                y += 5  # Extra space between list items
                # Process nested lists
                for nested_list in li.find_all(['ul', 'ol'], recursive=False):
                    y = process_element(nested_list, y, level+1)
        return y

    for element in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'ul', 'ol']):
        y = process_element(element, y)

        if y > page.rect.height - margin_bottom:
            # Start a new page if we're near the bottom
            page = doc.new_page()
            y = margin_top

    # Add footer to all pages
    for page_num in range(len(doc)):
        page = doc[page_num]
        page.insert_text((margin_left, page.rect.height - 30), "www.ygit.info", fontsize=8, fontname="helvetica")
        page.insert_text((page.rect.width - margin_right - 50, page.rect.height - 30), f"Page {page_num + 1}", fontsize=8, fontname="helvetica")

    # Save PDF
    filename = f"{career.replace(' ', '_')}_ygit_roadmap.pdf"
    doc.save(filename)
    return filename