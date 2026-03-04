# True Crime Story Generation Guide

This document contains the instructions and style guidelines for generating long-form True Crime stories for the TTS application.

## Specifications

*   **Length:** Minimum 2 hours of audio (approximately 100,000 characters).
*   **Structure:** Divided into at least 8 chapters to prevent TTS overload and browser crashes.
*   **Input:** User provides a famous killer's name, an unsolved case, or a True Crime topic. The AI researches and generates the story based on these guidelines.

## Style and Tone

*   **Format:** Cinematic script style, designed for voice-over narration (specifically for dark YouTube documentaries).
*   **Atmosphere:** Dense from the beginning. Extensive, slow, and immersive introduction. Build context, landscape, emotional climate, and social environment before the central event. The city, house, night, and silence play a starring role.
*   **Tone:** Serious, sober, and dramatic. Avoid colloquial language; use formal narration with deep psychological descriptions.
*   **Focus:** Strong emphasis on mental states: manipulation, anxiety, emotional dependence, internal tension. Explore the psychological process leading to the outcome rather than just fast-paced actions.
*   **Structure per Chapter:** Long chapters (several thousand words) without visual separators. Each chapter has a clear narrative function: extensive introduction, psychological escalation, revelation of intentions, violent climax, and judicial/social consequences. Information is dosed, not revealed all at once.
*   **Theme:** Real crime, manipulation, obsession, toxic relationships, psychological pressure, and moral collapse. Focus on *how* it happened, not just the graphic impact.
*   **Pacing:** Slow but steadily building. Starts contemplative, almost documentary-like, and intensifies tension up to the climax, followed by the social reaction, investigation, and community impact.

## AI Agent Workflow (Instructions for the Assistant)

Whenever the user requests a new long-form True Crime story, the AI Assistant MUST follow these execution steps:

1.  **Story Generation:** Research and write the story (at least 100,000 characters, divided into 8+ chapters) strictly following the Style and Tone guidelines above.
2.  **Directory Creation:** Create a dedicated folder for this specific case inside `d:\Luminares app\long-tts-app\cuentos\` (e.g., `cuentos\John_Wayne_Gacy\`).
3.  **Audio Processing:** Generate the TTS audio chapter by chapter (to avoid overwhelming the system) and save the resulting MP3/audio files directly into the newly created case folder.
4.  **Thumbnail Generation:** Prompt the image generation tool (`generate_image`) to create a YouTube-style thumbnail for the story.
    *   **Image Style:** Dark, True Crime documentary aesthetic. It MUST feature prominent police tape ("POLICE LINE DO NOT CROSS") in the background, dramatic lighting (e.g., police sirens red/blue glow). 
    *   **Image Text:** The thumbnail MUST prominently display the Name of the Killer or the Case in bold, impactful typography (similar to the red and white thick bordered text in the user's reference).
    *   **Save Location:** Save the generated thumbnail image directly into the case's dedicated folder.
