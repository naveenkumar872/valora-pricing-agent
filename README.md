# Valora - AI-Powered Dynamic Pricing Optimizer

Valora is an intelligent dynamic pricing tool that determines the optimal selling price for products by analyzing real-time competitor data from Flipkart. It combines Large Language Models (LLMs) for natural language understanding with Reinforcement Learning (Q-Learning) to simulate market demand and maximize profit margins.

## 🚀 Features

-   **Natural Language Interface:** Simply describe your product and its base cost (e.g., "I want to sell a gaming mouse, base cost 500").
-   **LLM Integration:** Uses **Llama 3.1 (via NVIDIA AI Endpoints)** to extract structured product data from your description.
-   **Real-Time Market Data:** Scrapes live competitor pricing from **Flipkart** using Selenium and BeautifulSoup.
-   **Dynamic Pricing Simulation:** Simulates a market environment to estimate sales volume based on price competitiveness.
-   **Reinforcement Learning:** A **Q-Learning agent** trains on the simulated data to find the price point that yields the highest profit over time.
-   **Web Dashboard:** Simple Flask-based web interface for easy interaction.

## 🛠️ Tech Stack

-   **Backend:** Python, Flask
-   **AI & LLM:** LangChain, NVIDIA AI Endpoints
-   **Web Scraping:** Selenium, BeautifulSoup4
-   **Data & Math:** NumPy, Matplotlib

## 📋 Prerequisites

Before running the project, ensure you have the following installed:

-   Python 3.10+
-   Google Chrome (for Selenium scraping)
-   [NVIDIA AI API Key](https://build.nvidia.com/explore/discover) (for Llama 3.1)

## 📦 Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/valora.git
    cd valora
    ```

2.  **Install dependencies:**
    Since `requirements.txt` might be empty, install the necessary packages directly:
    ```bash
    pip install flask langchain-nvidia-ai-endpoints langchain beautifulsoup4 selenium numpy matplotlib requests
    ```

## ⚙️ Configuration

1.  **API Key Setup:**
    Open `llm.py` and replace the placeholder or existing API key with your own NVIDIA API key:
    ```python
    # llm.py
    test_llm = ChatNVIDIA(
        model="meta/llama-3.1-70b-instruct",
        api_key="YOUR_NVIDIA_API_KEY" # Replace this
    )
    ```
    *(Recommended: Use environment variables for better security)*

2.  **Selenium Driver:**
    Selenium 4.x usually manages drivers automatically. If you encounter issues, ensure your Chrome browser is up to date.

## ▶️ Usage

1.  **Start the application:**
    ```bash
    python main.py
    ```

2.  **Access the dashboard:**
    Open your browser and go to `http://127.0.0.1:5000`.

3.  **Run a simulation:**
    -   Enter a product description (e.g., *"Sony WH-1000XM5 headphones with base cost 15000"*).
    -   (Optional) Adjust the number of simulation rounds.
    -   Click **Submit**.
    -   The system will scrape prices, run the Q-learning agent, and display the results.

## 🧠 How It Works

1.  **Input Processing:** The user's input is sent to the Llama 3.1 model to extract the search query and base cost.
2.  **Market Analysis:** The system searches Flipkart for the product and extracts competitor prices.
3.  **Simulation:** A `PricingEnv` is created where demand curves are generated based on competitor averages.
4.  **Optimization:** The Q-Learning agent interacts with this environment, exploring different price points and learning which one maximizes profit (Revenue - Cost).

## ⚠️ Disclaimer

This project uses web scraping (Selenium) to gather data from Flipkart. This is for educational and research purposes only. Ensure you comply with the website's `robots.txt` and terms of service when using scraping tools.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
