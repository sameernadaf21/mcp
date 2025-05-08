# from typing import Any
# import httpx
# from mcp.server.fastmcp import FastMCP

# # Initialize FastMCP server
# mcp = FastMCP("weather")

# # Constants
# NWS_API_BASE = "https://api.weather.gov"
# USER_AGENT = "weather-app/1.0"

# async def make_nws_request(url: str) -> dict[str, Any] | None:
#     """Make a request to the NWS API with proper error handling."""
#     headers = {
#         "User-Agent": USER_AGENT,
#         "Accept": "application/geo+json"
#     }
#     async with httpx.AsyncClient() as client:
#         try:
#             response = await client.get(url, headers=headers, timeout=30.0)
#             response.raise_for_status()
#             return response.json()
#         except Exception:
#             return None

# def format_alert(feature: dict) -> str:
#     """Format an alert feature into a readable string."""
#     props = feature["properties"]
#     return f"""
# Event: {props.get('event', 'Unknown')}
# Area: {props.get('areaDesc', 'Unknown')}
# Severity: {props.get('severity', 'Unknown')}
# Description: {props.get('description', 'No description available')}
# Instructions: {props.get('instruction', 'No specific instructions provided')}
# """

# @mcp.tool()
# async def get_alerts(state: str) -> str:
#     """Get weather alerts for a US state.

#     Args:
#         state: Two-letter US state code (e.g. CA, NY)
#     """
#     url = f"{NWS_API_BASE}/alerts/active/area/{state}"
#     data = await make_nws_request(url)

#     if not data or "features" not in data:
#         return "Unable to fetch alerts or no alerts found."

#     if not data["features"]:
#         return "No active alerts for this state."

#     alerts = [format_alert(feature) for feature in data["features"]]
#     return "\n---\n".join(alerts)

# @mcp.tool()
# async def get_forecast(latitude: float, longitude: float) -> str:
#     """Get weather forecast for a location.

#     Args:
#         latitude: Latitude of the location
#         longitude: Longitude of the location
#     """
#     # First get the forecast grid endpoint
#     points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
#     points_data = await make_nws_request(points_url)

#     if not points_data:
#         return "Unable to fetch forecast data for this location."

#     # Get the forecast URL from the points response
#     forecast_url = points_data["properties"]["forecast"]
#     forecast_data = await make_nws_request(forecast_url)

#     if not forecast_data:
#         return "Unable to fetch detailed forecast."

#     # Format the periods into a readable forecast
#     periods = forecast_data["properties"]["periods"]
#     forecasts = []
#     for period in periods[:5]:  # Only show next 5 periods
#         forecast = f"""
# {period['name']}:
# Temperature: {period['temperature']}°{period['temperatureUnit']}
# Wind: {period['windSpeed']} {period['windDirection']}
# Forecast: {period['detailedForecast']}
# """
#         forecasts.append(forecast)

#     return "\n---\n".join(forecasts)


# if __name__ == "__main__":
#     # Initialize and run the server
#     mcp.run(transport='stdio')


from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("about-me")

@mcp.tool()
def get_education() -> str:
    return """\
Bachelor of Engineering in Computer Science (AI)
KLE Technological University, Hubballi, Karnataka (CGPA: 9.05)
Class XII – Kendriya Vidyalaya Hubli (82%)
Class X – Kendriya Vidyalaya Hubli (79.2%)
"""

@mcp.tool()
def get_experience() -> str:
    return """\
1. Infosys (STG Unit) - Specialist Programmer Trainee (Feb 2025 – Present)
   - Java, Spring Boot, Microservices, React (TS), Satellite Data Processing.

2. Nvidia – Project Intern (Aug 2023 – Feb 2024)
   - AI-based test case generation using PyTorch.
"""

@mcp.tool()
def get_projects() -> str:
    return """\
1. Image Denoising and Deblurring using KIRNET
   - PSNR: 39.54, SSIM: 0.9579

2. Optimizing SRGAN using Knowledge Distillation
   - Reduced params from 1.54M to 193.59K

3. RESTful API for Task Management (Spring Boot + MySQL + JWT)

4. AI-Powered Resume Tailoring Assistant (Streamlit + Gemini API)
"""

@mcp.tool()
def get_skills() -> str:
    return """\
Languages: C, C++, Python, Java
Core: DSA, OOP, OS, CN, DBMS, ML
Frameworks: PyTorch, TensorFlow, Flask, Streamlit, Flower, Spring Boot, React (TypeScript)
Tools: VS Code, Git, Android Studio
Soft Skills: Leadership, Problem-Solving, Teamwork, Critical Thinking, Communication
"""

@mcp.tool()
def get_certifications() -> str:
    return """\
- JNCIA-Junos (Juniper Certified Associate)
- DSA with C/C++ (Udemy)
"""

@mcp.tool()
def get_publications() -> str:
    return """\
1. Survey on Federated Learning – covers core ideas, challenges, and future directions.
2. PosePerfect – Yoga Posture Classification using HRNet and Gemini Vision Pro.
"""

@mcp.tool()
def get_achievements() -> str:
    return """\
- Won 1st Prize for Hand Gesture Controlled Bot (Exploration event)
- Solved 300+ DSA problems on LeetCode/GFG
"""

@mcp.tool()
def get_contact() -> str:
    return """\
Phone: +91 8217874287
Email: sameernadaf787@gmail.com
LinkedIn: https://www.linkedin.com/in/sameernadaf/
GitHub: https://github.com/sameernadaf21
"""

@mcp.tool()
def get_summary() -> str:
    return (
        "👤 **Sameer M Nadaf – Software Developer & AI Enthusiast**\n\n"
        "🎯 *Career Objective:*\n"
        "Aspiring software developer with a strong interest in AI, ML, and full-stack development. Passionate about building intelligent, scalable, and user-centric solutions.\n\n"

        "🎓 *Education:*\n"
        "• B.E. in Computer Science (AI), KLE Technological University (CGPA: 9.05)\n"
        "• Class XII – Kendriya Vidyalaya Hubli (82%)\n"
        "• Class X – Kendriya Vidyalaya Hubli (79.2%)\n\n"

        "💼 *Experience:*\n"
        "• Infosys – Specialist Programmer Trainee (Java, Spring Boot, React, Satellite Data)\n"
        "• Nvidia – Project Intern (AI-driven test case generation using PyTorch)\n\n"

        "🚀 *Projects:*\n"
        "1. Image Denoising and Deblurring (KIRNET)\n"
        "2. SRGAN Optimization for Edge Devices using Knowledge Distillation\n"
        "3. Task Manager API using Spring Boot, MySQL, JWT\n"
        "4. Resume Tailoring Assistant (Streamlit + Gemini API)\n\n"

        "🛠️ *Skills:*\n"
        "Languages: Python, Java, C, C++ | Frameworks: React (TS), Spring Boot, TensorFlow, PyTorch, Flask, Streamlit\n"
        "Core: DSA, OOP, OS, CN, DBMS, ML | Tools: VS Code, Git, Android Studio\n\n"

        "📚 *Certifications:*\n"
        "• JNCIA-Junos (Juniper Networks)\n"
        "• DSA with C/C++ (Udemy)\n\n"

        "📝 *Publications:*\n"
        "• Survey on Federated Learning\n"
        "• PosePerfect: Yoga Posture Classification with HRNet + Gemini Vision Pro\n\n"

        "🏆 *Achievements:*\n"
        "• 1st Prize – Hand Gesture Controlled Bot\n"
        "• 300+ DSA Problems Solved\n\n"

        "📬 *Contact:*\n"
        "• Phone: +91 8217874287\n"
        "• Email: sameernadaf787@gmail.com\n"
        "• LinkedIn: https://www.linkedin.com/in/sameernadaf/\n"
        "• GitHub: https://github.com/sameernadaf21\n"
    )

if __name__ == "__main__":
    mcp.run(transport="stdio")
