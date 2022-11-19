# Final project for the LSML course

### Problem


I've built the Telegram bot for lyrics generator.

Model - LSTM with Torch

Dataset - [kaggle source](https://www.kaggle.com/code/ivankhrulenko/pop-rap-or-heavy-metal-lyrics-classifier/data). 

Example usage:
<img src="https://github.com/gaisha/telegram_bot_final_project/blob/main/bot_example_image.png" width=50% height=50%>

### Data processing

The dataset itself was  very noisy.
The following processing was done:
- data was cleaned from unnecessary columns
- data was converted for a processable format for language detection.
- I repeated some steps of preprocessing many times, that's how I understood where the noise would come from. For example, first wordcloud contained "Chorus", "Instrumental", "x  times". 
I understood that some rows contain only noise. See more details in  ```Preprocessing.ipynb``` file.  There i commented every step,cleaned the data  and created Corpus.
 

### Training the model

Model training code  Colab Notebook ```Gaisha_lyrics_generator_LSTM.ipynb```.  

Loss function - CrossEntropyLoss

Optimizer - Adam

I've created pretrained model to be used in the Telegram bot. Before starting polling for user requests in the bot implementation, I load the pretrained model first.
Bot is listening to user's messages and is responding with generated lyrics based on the user message. Messages have to be at least 50 characters long. When using bot for the first time and openning the menu - there's an additional explanation on how to use it with examples provided.


### Try it yourself!

Download the folder to your local machine. Then run the following commands:


```docker compose build```

```docker compose --env-file .env up```

Then go to Telegram and open bot with the following link: https://t.me/gaisha_ml_project_bot

Once you select ```/start``` you can follow the instructions from the bot!
