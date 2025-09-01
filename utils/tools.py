from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.tools import tool

from utils.contants import MODELS
from utils.screenshot_manager import ScreenshotManager

from PIL import Image, ImageDraw, ImageFont
import pyautogui as pg
import base64
import os
import platform

pg.PAUSE = 2

# Initialize screenshot manager
screenshot_manager = ScreenshotManager()

def set_thumbnail_size(size: str):
    """
    Set the default thumbnail size for screenshots.
    
    Args:
        size (str): Thumbnail size ('small', 'medium', 'large')
    """
    screenshot_manager.set_default_size(size)

def get_thumbnail_manager():
    """
    Get the screenshot manager instance for external access.
    
    Returns:
        ScreenshotManager: The screenshot manager instance
    """
    return screenshot_manager

def _load_windows_font(size=25):
    """
    Load a font with Windows-optimized fallback mechanism.
    
    Args:
        size (int): Font size to load
        
    Returns:
        ImageFont: Loaded font object
    """
    # Windows-specific font paths and names
    windows_fonts = [
        # Try common Windows fonts with full paths
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibri.ttf", 
        "C:/Windows/Fonts/tahoma.ttf",
        "C:/Windows/Fonts/verdana.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
        # Try font names (works if fonts are in system path)
        "arial.ttf",
        "calibri.ttf",
        "tahoma.ttf", 
        "verdana.ttf",
        "segoeui.ttf"
    ]
    
    # If on Windows, prioritize Windows fonts
    if platform.system() == "Windows":
        font_candidates = windows_fonts
    else:
        # For non-Windows systems, try common font names first
        font_candidates = [
            "arial.ttf",
            "DejaVuSans.ttf",
            "liberation-sans.ttf"
        ] + windows_fonts
    
    # Try to load fonts in order of preference
    for font_path in font_candidates:
        try:
            if os.path.exists(font_path):
                font = ImageFont.truetype(font_path, size)
                print(f"Successfully loaded font: {font_path}")
                return font
            else:
                # Try loading by name (system will search font directories)
                font = ImageFont.truetype(font_path, size)
                print(f"Successfully loaded font by name: {font_path}")
                return font
        except (IOError, OSError):
            continue
    
    # If all font loading attempts fail, use default font
    print("Warning: Could not load any TrueType fonts, using default font")
    try:
        return ImageFont.load_default()
    except Exception:
        # Last resort - create a minimal font
        print("Warning: Using minimal default font")
        return ImageFont.load_default()

def get_ruled_screenshot(generate_thumbnail=True, thumbnail_size=None):
    """
    Take a screenshot with coordinate grid overlay and optionally generate thumbnail.
    
    Args:
        generate_thumbnail (bool): Whether to generate a thumbnail
        thumbnail_size (str): Size of thumbnail ('small', 'medium', 'large')
        
    Returns:
        str or None: Screenshot ID if thumbnail generated, None otherwise
    """
    image = pg.screenshot()
    # Get the image dimensions
    width, height = image.size

    # Create a new image for the semi-transparent layer
    overlay = Image.new("RGBA", (width, height), (255, 255, 255, 0))  # Transparent layer
    draw = ImageDraw.Draw(overlay)

    # Set the line color (gray) and line opacity (adjusting the alpha value)
    line_color = (200, 200, 0, 128)  # The last value (128) controls opacity, 0 = fully transparent, 255 = fully opaque

    # Load a font for the labels with Windows-optimized fallback mechanism
    font = _load_windows_font(25)

    # Draw vertical and horizontal lines every 100 pixels and add labels
    for x in range(0, width, 50):
        draw.line([(x, 0), (x, height)], fill=line_color, width=1)
        # Add labels at the top for vertical lines
        if x % 100 == 0:
            draw.text((x + 5, 5), str(x), font=font, fill=(250, 250, 0, 128))
            draw.text((x, height - 25), str(x), font=font, fill=(250, 250, 0, 128))

    for y in range(0, height, 50):
        draw.line([(0, y), (width, y)], fill=line_color, width=1)
        # Add labels on the left for horizontal lines
        if y % 100 == 0:
            draw.text((5, y + 5), str(y), font=font, fill=(0, 250, 250, 128))
            text_width, text_height = 35, 15
            draw.text((width - text_width - 5, y + 5), str(y), font=font, fill=(0, 250, 250, 128))

    # Convert screenshot to RGBA for proper merging
    image = image.convert("RGBA")

    # Merge the overlay (with lines and labels) back onto the original image
    combined = Image.alpha_composite(image.convert("RGBA"), overlay)
    combined.save("screenshot.png")
    
    # Generate thumbnail if requested
    screenshot_id = None
    if generate_thumbnail:
        screenshot_id = screenshot_manager.create_screenshot_with_thumbnail(
            "screenshot.png", 
            thumbnail_size
        )
    
    return screenshot_id

class ScreenInfo(BaseModel):
    query: str = Field(description="should be a question about the screenshot of the current screen. Should always be in text.")

@tool(args_schema=ScreenInfo)
def get_screen_info(query: str) -> dict:
    """Tool to get the information about the current screen on the basis of the question of the user. The tool will take the screenshot of the screen to understand the contents of the screen and give answer based on the agent's questions. Do not write code to take screenshot."""
    try:
        # Generate screenshot with thumbnail
        screenshot_id = get_ruled_screenshot(generate_thumbnail=True)
        
        with open(f"screenshot.png", "rb") as image:
            image = base64.b64encode(image.read()).decode("utf-8")
            messages = [
                SystemMessage(
                content="""You are a Computer agent that is responsible for answering questions based on the input provided to you. You will have access to the screenshot of the current screen of the user along with a grid marked with true coordinates of the screen. The size of the screen is 1920 x 1080 px.
                        ONLY rely on the coordinates marked in the screen. DO NOT create an assumption of the coordinates. 
                        Here's how you can help:
                        1. Find out coordinates of a specific thing. You have to be super specific about the coordinates. These coordinates will be passed to PyAutoGUI Agent to perform further tasks. Refer the grid line to get the accurate coordinates.
                        2. Give information on the contents of the screen.
                        3. Analyse the screen to give instructions to perform further steps.
                        
                    """
                ),
                HumanMessage(
                    content=[
                        {
                            "type": "text",
                            "text": f"{query}"
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{image}"}
                        }
                    ]
                )
            ]
            image_model = MODELS["gemini"]
            response = image_model.invoke(messages)
            
            # Return response with screenshot ID for thumbnail integration
            result = {
                "content": response.content,
                "screenshot_id": screenshot_id
            }
            return result
        
    except Exception as e:
        return {"error": str(e)}
