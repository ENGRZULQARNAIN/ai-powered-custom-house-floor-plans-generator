# 🏠 AI-Powered Floor Plan Generator

This project is an AI-driven system that automatically generates house floor plans based on user input. Leveraging cutting-edge AI models, the backend processes natural language descriptions from users (e.g., number of rooms, house type, floors, etc.) and returns visual floor plans rendered from SVG code.

## 🚀 Key Features

- Generate floor plans using natural language inputs.
- Supports customizable parameters like:
  - Number of rooms
  - Type of house (e.g., villa, bungalow)
  - Total area
  - Number of floors
- SVG-based plan rendering
- Image export functionality
- Seamless integration with a frontend web application

---

## 🧠 How It Works

This project utilizes **Anthropic's Claude Sonnet 3.5** — a powerful large language model — to generate SVG representations of house floor plans based on structured prompt templates. Here's how the system works end-to-end:

### 📝 1. User Input Collection

The system collects structured information from users via a web form or API request:
- Number of rooms
- Type of house (villa, bungalow, etc.)
- Floor count
- Total area
- Special requirements (optional)

### 📄 2. Prompt Template Construction

A predefined **prompt template** is used to instruct the AI model. The system dynamically inserts the user-provided values into this prompt, which helps ensure consistent and high-quality SVG outputs.


### 🤖 3. AI-Based SVG Generation

The constructed prompt is sent to **Anthropic Sonnet 3.5**, which returns SVG code representing a floor plan.

### 🧩 4. SVG Rendering and Export

The system renders the received SVG into a viewable image (on the frontend) and allows the user to download or export it as a `.png` or `.svg` file.

---

## 🛠️ Tech Stack

| Layer       | Technology                    |
|-------------|-------------------------------|
| Backend     | [FastAPI](https://fastapi.tiangolo.com/) |
| AI Model    | [Anthropic Claude Sonnet 3.5](https://www.anthropic.com/index/claude-3) |
| Frontend    | (Assumed) Web-based (HTML/CSS/JS or framework) |
| Image Export| SVG to PNG converter (e.g., CairoSVG or frontend libs) |
| Hosting     | Deployable on any cloud (e.g., Vercel, AWS, etc.) |

---


{
  "house_type": "villa",
  "number_of_rooms": 4,
  "number_of_floors": 2,
  "total_area": 2500
}

{
  "svg_code": "<svg>...</svg>",
  "image_url": "/static/exported_images/plan_123.png"
}

