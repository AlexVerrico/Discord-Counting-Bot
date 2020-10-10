# Discord Counting Bot 
### A fun little game for your discord server
#### Setup Instructions:
Add the bot to your server using the following link: [https://discord.com/api/oauth2/authorize?client_id=764432909011517491&permissions=116736&scope=bot](https://discord.com/api/oauth2/authorize?client_id=764432909011517491&permissions=116736&scope=bot)  
You will need to have the `count master` role to use the management commands for this bot.  
To setup the bot, first go into the channel that you want to count in and run `!count counting_channel this_channel`  
You can also setup a separate channel to keep a log of who has got the count wrong by running `!count log_channel this_channel`, otherwise it will use the counting channel.  
To setup custom messages you can run `!count wrong_message your_message` for the message that is sent when someone enters the wrong number, and `!count greedy_message your_message` for the message that is sent when someone types 2 messages in a row in the counting channel.  
Both commands will replace `{{{user}}}` with the username of whoever made the mistake, eg. `!count wrong_message {{{user}}} couldn't keep count` will result in the message "JohnS#1000 couldn't keep count"
#### Usage instructions:  
It's pretty straight forward, you just count up starting from 1 until someone makes a mistake and the count is reset, eg. you type `1`, a friend types `2`, you type `3`, and so on.  
Anything after the first space is ignored, so typing `1 hello` is the same as typing `1`
