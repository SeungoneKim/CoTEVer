# CoT-Verification-Toolbox-Middleware

## Requirements
```shell
pip install "fastapi[all]" readability-lxml google-api-python-client openai transformers sentence_transformers scikit-learn torch
```

## Personalization
### Keys
First, You will need these keys:
1. GPT-3 API Key (https://beta.openai.com/account/api-keys)
2. Google Custom Search API Key (https://developers.google.com/custom-search/v1/overview)
3. Google Custom Engine ID Key (https://developers.google.com/custom-search/v1/overview)

Then you will need to set your environment variables with following commands
```shell
export GPT3_KEY=$YOUR_KEY
export GOOGLE_SEARCH_API_KEY=$YOUR_KEY 
export GOOGLE_ENGINE_ID_KEY=$YOUR_KEY 
```

If you want your environment variables to persist across sessions, please copy & paste code block above to `~/.profile`.