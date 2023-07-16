# Python Clip Combiner

A python script to make short videos.

## Installation

```bash
python3 -m venv .env
pip install -r requirements.txt
sudo apt install ImageMagick
```

some configurations in "image magick"

```bash
sudo apt install python3-tk
sudo nano etc/ImageMagick-6/policy.xml
```

modify this line

```bash
<policy domain="path" rights="none" pattern="@*"/>
```

to

```bash
<policy domain="path" rights="read | write" pattern="@*"/>
```

Then You Ready To Go... Run

```bash
python main.py
```
