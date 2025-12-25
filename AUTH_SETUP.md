# Authentication Setup Required

To run the Kaggle notebooks, you must set up authentication externally:

1. Get your Kaggle API token from: https://www.kaggle.com/settings/account
2. Set the environment variable: `export KAGGLE_API_TOKEN="your_token_here"`
3. Create the authentication file:
   ```bash
   mkdir -p ~/.kaggle
   echo '{"username": "erickmagyar", "key": "'"$KAGGLE_API_TOKEN"'"}' > ~/.kaggle/kaggle.json
   chmod 600 ~/.kaggle/kaggle.json
   ```

The kaggle_setup.sh script expects the KAGGLE_API_TOKEN environment variable to be available.

For security reasons, API tokens are not stored in the repository.