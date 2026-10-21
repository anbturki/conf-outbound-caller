from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="REPLACE_ELEVENLABS_API_KEY",
)


def get_voices():
    voices = client.voices.search()

    return {
        **voices.model_dump(),
        "voices": [
            {
                "id": voice.voice_id,
                "name": voice.name,
                "category": voice.category,
                "preview_url": voice.preview_url,
                "labels": voice.labels,
            }
            for voice in voices.voices
        ],
    }
