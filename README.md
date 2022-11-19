# Final project for the LSML course

### Problem
Lyrics generation based on the begining of the song. 

I took data from  this [kaggle source](https://www.kaggle.com/code/ivankhrulenko/pop-rap-or-heavy-metal-lyrics-classifier/data). 


### Data processing

Data is used from this source (link)
The dataset itself was  very noisy.
The following processing was done:
- data was cleaned from unnecessary columns
- data was converted for a processable format for language detection.
- I repeated some steps of preprocessing many times, that's how I understood where the noise would come from. For example, first wordcloud contained "Chorus", "Instrumental", "x  times". 
I understood that some rows contain only noise. See more details in  Preprocessing.ipynb file.  There i commented every step,cleaned the data  and created Corpus.
 

### Training the model
The model LSTM was used to generate lyrics in a particular style.


### Try it yourself!

Download the folder to your local machine. Then run the following commands:


```docker compose build```

```docker compose --env-file .env up```

Then go to Telegram and open bot with the following link: https://t.me/gaisha_ml_project_bot

Once you select ```/start``` you can follow the instructions from the bot!

Here's an example:
![image](https://github.com/gaisha/telegram_bot_final_project/blob/main/bot_example_image.png)
