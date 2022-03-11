# Using Python Slim-Buster
FROM kyyex/kyy-userbot:buster

#━━━━━ Userbot Telegram ━━━━━
#━━━━━ By Man-Userbot ━━━━━
#━━━━━ By Skyzuu-Userbot ━━━━━
#━━━━━ By Dior-Userbot ━━━━━
#━━━━━ By Kyy-Userbot ━━━━━

#Diapus gua santet online

RUN git clone -b main https://github.com/DIORrios285/Fanda-Userbot /root/userbot
RUN mkdir /root/userbot/.bin
RUN pip install --upgrade pip setuptools
WORKDIR /root/userbot

#Install python requirements
RUN pip3 install -r https://raw.githubusercontent.com/muhammadrizky16/Kyy-Userbot/Kyy-Userbot/requirements.txt

EXPOSE 80 443

# Finalization
CMD ["python3", "-m", "userbot"]
