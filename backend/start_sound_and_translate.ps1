conda activate env_vocabulary_builder
Start-Process libretranslate
docker run -it --detach -p 5500:5500 synesthesiam/opentts:fr
