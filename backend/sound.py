import requests


def sound(source,voice,vocoder="high",denoiser_strength=0.03,cache=False)->bytes:
    """
    inputsounds,outputvoice

    :paramsource:
    :paramvoice:
    :paramvocoder:
    :paramdenoiser_strength:
    :paramcache:
    :return:
    """
    """
    http://localhost:5500/api/tts?voice=glow-speak%3Afr_siwis&text=pas%20DE%20patience&vocoder=high&denoiserStrength=0.03&cache=false
    """
    payload ={
        'voice':voice,
        'text':source,
        'vocoder':vocoder,
        'denoiserStrength':str(denoiser_strength),
        'cache':str(cache)
    }
    r =requests.get(
        'http://localhost:5500/api/tts',
        params=payload
    )
    #TODO:errorhandling
    return r.content


#ret=sound("ilyabeaucoupdepersonnesquitravaillentàMicrosoft",'glow-speak:fr_siwis')
#withopen('test.wav','wb')asf:
#f.write(ret)