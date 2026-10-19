name: Render Vertical Space Mystery

on:
  workflow_dispatch: # Allows you to manually trigger the render
  push:
    paths:
      - 'scene.py'   # Automatically runs when you save changes to scene.py

jobs:
  render:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install System Dependencies (FFmpeg & LaTeX)
        run: |
          sudo apt update
          sudo apt install -y ffmpeg libcairo2-dev libpango1.0-dev texlive texlive-latex-extra

      - name: Install Manim
        run: |
          pip install manim

      - name: Render Vertical Video
        run: |
          manim -qh -r 1080,1920 scene.py SpaceMystery -o output.mp4

      - name: Upload Finished Video
        uses: actions/upload-artifact@v4
        with:
          name: space-mystery-short
          # The **/*.mp4 wildcard tells GitHub to grab the video 
          # no matter what folder resolution Manim creates
          path: media/videos/**/*.mp4
          retention-days: 3
