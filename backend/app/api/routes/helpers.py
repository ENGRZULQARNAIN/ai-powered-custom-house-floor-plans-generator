import io
import base64
from PIL import Image

# Option 1: Using wand (ImageMagick wrapper)
def svg_to_png_wand(svg_data, width=None, height=None):
    """
    Convert SVG to PNG using Wand (ImageMagick wrapper).
    Handles both string SVG code and binary SVG data.
    
    Args:
        svg_data (str or bytes): The SVG as a string or bytes
        width (int, optional): Desired width of the output PNG
        height (int, optional): Desired height of the output PNG
        
    Returns:
        bytes: PNG image as bytes
    """
    from wand.image import Image as WandImage
    
    # Check if the input is already bytes
    if not isinstance(svg_data, bytes):
        try:
            svg_data = svg_data.encode('utf-8')
        except (UnicodeDecodeError, AttributeError):
            # If it's not a string or already bytes in an incompatible format
            raise ValueError("Input must be SVG code as string or SVG data as bytes")
    
    try:
        with WandImage(blob=svg_data, format='svg') as img:
            if width and height:
                img.resize(width, height)
            png_binary = img.make_blob('png')
        
        return png_binary
    except Exception as e:
        # Check if the input might already be PNG or another format
        try:
            with WandImage(blob=svg_data) as img:
                if width and height:
                    img.resize(width, height)
                png_binary = img.make_blob('png')
            return png_binary
        except:
            # Re-raise the original error if this also fails
            raise e

# Option 2: Using svglib and reportlab
def svg_to_png_svglib(svg_code, width=None, height=None):
    """
    Convert SVG to PNG using svglib and reportlab.
    
    Args:
        svg_code (str): The SVG code as a string
        width (int, optional): Desired width of the output PNG
        height (int, optional): Desired height of the output PNG
        
    Returns:
        bytes: PNG image as bytes
    """
    from svglib.svglib import svg2rlg
    from reportlab.graphics import renderPM
    import tempfile
    
    # Create a temporary file to write the SVG
    with tempfile.NamedTemporaryFile(suffix='.svg', delete=False) as temp_svg:
        temp_svg.write(svg_code.encode('utf-8'))
        temp_svg_path = temp_svg.name
    
    # Convert SVG to ReportLab drawing
    drawing = svg2rlg(temp_svg_path)
    
    # Calculate scaling if needed
    if width or height:
        original_width, original_height = drawing.width, drawing.height
        scale_x = width / original_width if width else 1
        scale_y = height / original_height if height else 1
        
        if width and height:
            drawing.width, drawing.height = width, height
            drawing.scale(scale_x, scale_y)
        elif width:
            drawing.width = width
            drawing.height = original_height * scale_x
            drawing.scale(scale_x, scale_x)
        elif height:
            drawing.width = original_width * scale_y
            drawing.height = height
            drawing.scale(scale_y, scale_y)
    
    # Create a bytes buffer
    png_io = io.BytesIO()
    
    # Render the drawing to PNG
    renderPM.drawToFile(drawing, png_io, fmt='PNG')
    png_io.seek(0)
    
    # Clean up temp file
    import os
    os.unlink(temp_svg_path)
    
    return png_io.getvalue()

# Option 3: Using Selenium (for complex SVGs that need browser rendering)
def svg_to_png_selenium(svg_code, width=400, height=400):
    """
    Convert SVG to PNG using Selenium browser automation.
    Good for complex SVGs that need proper browser rendering.
    
    Args:
        svg_code (str): The SVG code as a string
        width (int): Width of the browser viewport
        height (int): Height of the browser viewport
        
    Returns:
        bytes: PNG image as bytes
    """
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    import base64
    import tempfile
    
    # Create HTML file with the SVG
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ margin: 0; padding: 0; }}
            svg {{ width: 100%; height: 100%; }}
        </style>
    </head>
    <body>
        {svg_code}
    </body>
    </html>
    """
    
    with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as temp_html:
        temp_html.write(html.encode('utf-8'))
        temp_html_path = temp_html.name
    
    # Set up headless browser
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument(f"--window-size={width},{height}")
    
    # Start browser and navigate to the HTML file
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(f"file://{temp_html_path}")
    
    # Take screenshot
    png_data = driver.get_screenshot_as_png()
    
    # Clean up
    driver.quit()
    import os
    os.unlink(temp_html_path)
    
    return png_data