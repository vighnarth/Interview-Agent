# Voice Sample Instructions

To enable voice cloning with Chatterbox TTS, record a short audio clip of yourself speaking naturally.

## Requirements
- **Duration**: 10–30 seconds (more = better clone quality)
- **Format**: WAV, MP3, or M4A
- **Quality**: Quiet room, no background music, no reverb
- **Content**: Read anything naturally — you can use the sample text below

## Sample Text to Read
> "Hi, I'm Divya Sharma. I'm a machine learning engineer with about three years of experience, 
> mostly focused on NLP and recommendation systems. I enjoy working on technically hard problems 
> and building things that actually get used. I tend to be pretty direct — I'd rather say 
> something straightforwardly than talk around it."

## How to Record on Windows
1. Open **Voice Recorder** (search in Start menu)
2. Record yourself reading the sample text above
3. Export as WAV (or use Audacity to convert)
4. Save the file as `voice_sample/sample.wav`

## How to Enable Cartesia Voice Cloning
Once you have your `voice_sample/sample.wav` documented above, follow these steps to clone your voice and use it in the agent:

1. **Create a Cartesia Account:** Go to [Cartesia.ai](https://cartesia.ai) and sign up for a free tier account.
2. **Generate API Key:** In your Cartesia dashboard, generate a new API key and add it to your `.env` file:
   ```env
   CARTESIA_API_KEY=your_key_here
   ```
3. **Clone Your Voice:** In the Cartesia "Voice Library" dashboard, upload your `sample.wav` to create a new voice clone.
4. **Copy the Voice ID:** Once created, copy the unique Voice ID (e.g., `248be419-c632-4f23-adf1-5324ed7dbf1d`).
5. **Update `.env`:** Add the Voice ID to your `.env` file:
   ```env
   CARTESIA_VOICE_ID=your_voice_id_here
   ```
6. **Restart the Agent:** The agent is already coded to use `CARTESIA_VOICE_ID` dynamically if Cartesia is selected.

## Current Status
✅ **Cartesia is enabled!** The agent is currently using a default Cartesia high-quality voice. To switch to your own cloned voice, update the `CARTESIA_VOICE_ID` variable in your `.env` file as shown above.
