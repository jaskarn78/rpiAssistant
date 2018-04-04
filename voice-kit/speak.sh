#!/bin/bash
aws polly synthesize-speech --output-format mp3 --voice-id Brian --text '$1' polly.mp3 && mpg321 polly.mp3