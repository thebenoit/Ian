# moveout3.0

# Setup Instructions

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Unix/macOS
   # OR
   .\venv\Scripts\activate  # On Windows
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   # If installing from requirements.txt doesn't work, install packages directly:
   pip install apsw==3.50.2.0 bases==0.3.0 bs4==0.0.2 blinker==1.6.0 beautifulsoup4==4.13.4 ipython==8.12.3 langchain==0.3.26 langchain_core==0.3.68 langgraph==0.5.1 osmium==4.0.2 pydantic==2.11.7 pymongo==4.13.2 python-dotenv==1.1.1 Requests==2.32.4 requests_ip_rotator==1.0.14 selenium==4.34.0 selenium_wire==5.1.0 SQLAlchemy==2.0.41 urllib3>=2.4.0,<3.0.0 setuptools==80.9.0 spatialite==0.0.3 trio==0.30.0 trio-websocket==0.12.2 typing_extensions>=4.14.0,<5.0.0 undetected-chromedriver==3.5.5
   ```
   ```

3. Set up your environment variables:
   - Create a `.env` file in the root directory
   - Add your OpenAI API key and other required credentials

4. Run the agent:
   ```bash
   python3 ian.py
   ```

5. Interact with the agent:
   - Type your housing preferences when prompted
   - Type 'quit' or 'exit' to end the session
