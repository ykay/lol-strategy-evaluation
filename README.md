# LoL Strategy Chat Application

This Chainlit-based application serves as an AI assistant that provides basic strategy tips for League of Legends.

## Prerequisites

- Python 3.7+
- API keys for OpenAI

## Installation and Setup

1. **Clone the Repository**:
   ```sh
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create a Virtual Environment**:
   ```sh
   python -m venv .venv
   source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
   ```

3. **Install Dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

## Configuration

1. **API Keys**: 
   - Copy the `.env.sample` file and rename it to `.env`
   - Replace the placeholder values with your actual API keys

2. **Strategy Information Source**:
   - Feel free to modify the `url` in the `app.py` file to use another source.

## Running the Application

1. **Activate the Virtual Environment** (if not already activated):
   ```sh
   source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
   ```

2. **Run the Chainlit App**:
   ```sh
   chainlit run app.py -w
   ```

3. Open your browser and navigate to the URL displayed in the terminal.

## Usage

- Start a conversation with the AI assistant.

## Key Components

- `app.py`: Main application file containing the Chainlit setup and message handling logic.

## License

This project is licensed under the MIT License.



