# tweet-to-discord
## Python application that posts new tweets by a specific user to Discord via webhook
---

This application will post the link to a new Tweet by a specific user to Discord, using its Webhook integration.
The user can be chosen by setting their user ID in a `.env` file based on `.env-template`. You can get a user ID from their @ at [tweeter ID](https://tweeterid.com).

To run this application, you will need to get your Twitter API keys and enter them in your `.env` file, along with the webhook URL. The last status ID is optional and will be updated at run time.

The application checks every 30 minutes if any new tweets have been posted. Retweets by the specified user, as well as reply tweets, are ignored.
