#!/usr/bin/env python3
"""
Coffee Advertisement Video Generator
Generates a professional 30-second coffee advertisement video
with customizable scenes, transitions, and branding.
"""

import os
import sys
from pathlib import Path

try:
    from moviepy.editor import (
        VideoFileClip,
        ImageClip,
        TextClip,
        CompositeVideoClip,
        concatenate_videoclips,
        ColorClip,
    )
    from moviepy.audio.io.AudioFileClip import AudioFileClip
except ImportError:
    print("Error: moviepy not installed")
    print("Install with: pip install moviepy")
    sys.exit(1)


class CoffeeAdGenerator:
    """Generate coffee advertisement video"""

    def __init__(
        self,
        output_path="output/coffee_ad.mp4",
        duration=30,
        fps=30,
        width=1920,
        height=1080,
    ):
        self.output_path = output_path
        self.duration = duration
        self.fps = fps
        self.width = width
        self.height = height
        self.scenes = []

        # Ensure output directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    def add_color_scene(self, color, duration, text=None):
        """Add a solid color scene"""
        clip = ColorClip(size=(self.width, self.height), color=color).set_duration(
            duration
        )
        if text:
            text_clip = TextClip(
                text,
                fontsize=70,
                color="white",
                font="Arial-Bold",
                method="caption",
                size=(self.width - 100, None),
            ).set_duration(duration)
            text_clip = text_clip.set_position("center")
            clip = CompositeVideoClip([clip, text_clip])
        self.scenes.append(clip)

    def add_image_scene(self, image_path, duration, zoom=1.0):
        """Add an image scene"""
        if not Path(image_path).exists():
            print(f"Warning: Image not found: {image_path}")
            # Create placeholder
            self.add_color_scene((100, 50, 0), duration)
            return

        clip = ImageClip(image_path).set_duration(duration)
        clip = clip.resize(height=self.height)
        clip = clip.set_position("center")
        self.scenes.append(clip)

    def generate(self):
        """Generate the final video"""
        if not self.scenes:
            print("Error: No scenes added to video")
            return False

        try:
            # Concatenate all scenes
            final_clip = concatenate_videoclips(self.scenes)
            final_clip.write_videofile(
                self.output_path,
                fps=self.fps,
                codec="libx264",
                audio_codec="aac",
                verbose=False,
                logger=None,
            )
            print(f"✓ Video generated successfully: {self.output_path}")
            return True
        except Exception as e:
            print(f"Error generating video: {e}")
            return False


def main():
    """Main execution"""
    print("Coffee Advertisement Video Generator")
    print("=" * 50)

    # Create video generator
    generator = CoffeeAdGenerator(output_path="output/coffee_ad.mp4")

    # Scene 1: Sunrise (5 sec)
    print("Adding Scene 1: Sunrise...")
    generator.add_color_scene((255, 180, 0), 5, "Every morning brings a new opportunity")

    # Scene 2: The Brew (6 sec)
    print("Adding Scene 2: The Brew...")
    generator.add_color_scene(
        (139, 69, 19), 6, "Our premium beans, carefully roasted"
    )

    # Scene 3: First Sip (5 sec)
    print("Adding Scene 3: Satisfaction...")
    generator.add_color_scene((200, 200, 200), 5, "Experience the richness")

    # Scene 4: Productivity Montage (8 sec)
    print("Adding Scene 4: Productivity Montage...")
    generator.add_color_scene((100, 100, 100), 8, "Fuel your day with excellence")

    # Scene 5: Call to Action (6 sec)
    print("Adding Scene 5: Call to Action...")
    generator.add_color_scene(
        (40, 20, 0), 6, "Choose Premium Coffee. Choose Excellence."
    )

    # Generate video
    print("\nGenerating video...")
    if generator.generate():
        print("\n✓ Video production complete!")
        print(f"Output: {generator.output_path}")
    else:
        print("\n✗ Video generation failed")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
