## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/aiken-kazin/AI-text-humanizer.git
   cd AI-text-humanizer
   ```
   
2. **create an environment**:
   ```bash
   conda create -n humanizer_env python=3.10 -y
   ```
3. **Activate  envireonment**
   ```bash
   conda activate humanizer_env
   ```
3. **Install Python dependencies**:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
4. In AI-text-humanizer folder create `.env` file and save:
`OPENAI_API_KEY=your_openai_api_key`

5. **In AI-text-humanizer Root run in command line**
   ```bash
    uvicorn main:app --reload
   ```
