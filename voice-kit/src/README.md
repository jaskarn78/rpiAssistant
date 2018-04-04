This code is uses snowboy to create a local hotword detector for the AIY Voice Kit api version 2. Also allows voice activation. You can demo the system by using the snowboy.umdl file and "snowboy" as the hotword. 

Otherwise you need to get an account with snowboy to create your own hotword file. Use recordKeyword to create this file. You will need to update the following details in recordKeyword.py including the token from your snowboy account. This will be downloaded to your resources folder.

    ############# MODIFY THE FOLLOWING #############
    token = "put_your_snowboy_token_here"
    hotword_name = "name_of_your_hotword"
    language = "en"
    age_group = "50_59"
    gender = "M"
    microphone = "voicehat"
    durationSecs=2
    ############### END OF MODIFY ##################

When you have created your hotword you need to update the name of the file in miaHotword.py.

      ############# MODIFY THE FOLLOWING #############
      model_file='./resources/your_hotword_name.pmdl' # put your hotword file here. if you want to just try out use ./resources/snowboy.umdl
      sensitivity = 0.5
      ############### END OF MODIFY ##################

Once you have done this run either python HotwordDemo.py and ask something about holidays to use the google cloud services or python assistant_grpc_hotworddemo.py for the google assistant.

To run snowboy you may need to install libatlas, but other than that you don't need to install the other snowboy prerequisites such as pyaudio and sox as this is using the voice hat for the recording

sudo apt-get install libatlas-base-dev

Everything here is using Python 3 so run the /home/pi/bin/AIY-voice-kit-shell.sh which should set this up for you. I have made available all the snowboy files which work with Python 3 as they aren't available on the snowboy site and there doesn't seem to be a correct version of Swig to compile for the pi. But this all works on my machine as they say. If I've missed something then let me know. The easiest way is to copy all these files and the resources folder into the src folder.

For more details see my blog https://danicymru.wordpress.com/2017/12/21/aiy-voice-kit-voice-vad-or-hotword-activation/. Let me know if there are any issues and any comments are welcome.