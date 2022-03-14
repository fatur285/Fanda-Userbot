# Using Python Slim-Buster
FROM kyyex/kyy-userbot:buster

#━━━━━ Userbot Telegram ━━━━━
#━━━━━ By Fanda-Userbot ━━━━━
#━━━━━ By Man-Userbot ━━━━━
#━━━━━ By Skyzuu-Userbot ━━━━━
#━━━━━ By Dior-Userbot ━━━━━
#━━━━━ By Kyy-Userbot ━━━━━
#Diapus gua santet online

RUN apt-get update && apt-get upgrade -y
RUN apt-get install ffmpeg -y
RUN curl -sL https://deb.nodesource.com/setup_16.x | bash - && \
    apt-get install -y nodejs && \
    npm i -g npm
    
RUN git clone -b Fanda-Userbot https://github.com/DIORrios285/Fanda-Userbot /root/userbot
RUN mkdir /root/userbot/.bin
RUN pip install --upgrade pip setuptools
WORKDIR /root/userbot

#Install python requirements
RUN pip3 install -r https://raw.githubusercontent.com/DIORrios285/Fanda-Userbot/Fanda-Userbot/requirements.txt

EXPOSE 80 443

# Finalization
CMD ["python3", "-m", "userbot"]
