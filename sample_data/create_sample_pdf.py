#!/usr/bin/env python3
"""
Script to create a sample PDF from the research paper text
Run this to generate a PDF for testing the research agent
"""

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    import os
    
    def create_sample_pdf():
        # Read the text file
        with open('sample_research_paper.txt', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create PDF
        doc = SimpleDocTemplate("sample_research_paper.pdf", pagesize=letter)
        styles = getSampleStyleSheet()
        
        # Create custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=30,
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
        )
        
        # Split content into sections
        sections = content.split('\n\n')
        story = []
        
        for i, section in enumerate(sections):
            if not section.strip():
                continue
                
            # First section is title
            if i == 0:
                story.append(Paragraph(section.strip(), title_style))
            # Check if it's a heading (starts with number or is short)
            elif (section.strip().startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.')) or 
                  len(section.strip()) < 50 and not section.strip().endswith('.')):
                story.append(Paragraph(section.strip(), heading_style))
            else:
                story.append(Paragraph(section.strip(), styles['Normal']))
            
            story.append(Spacer(1, 12))
        
        # Build PDF
        doc.build(story)
        print("✅ Created sample_research_paper.pdf")
        
    if __name__ == "__main__":
        create_sample_pdf()
        
except ImportError:
    print("❌ ReportLab not installed. Install with: pip install reportlab")
    print("📝 Alternative: Convert the .txt file to PDF manually using any online converter")
