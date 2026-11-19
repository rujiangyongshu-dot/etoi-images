# etoi-images

Images for the Instagram account @etoi.art (ETOI). Public-domain artworks only.

- `posts/NN/01.jpg` … `10.jpg` : carousel slides (1080×1440), `caption.txt`, `cfg.py` (slide layout), `sources.md`
- `tools/etoi_carousel.py` : renderer (`python3 tools/etoi_carousel.py posts/NN/cfg.py posts/NN`)
- `tools/fetch.py` : downloads a museum image (`python3 tools/fetch.py URL posts/NN/src.jpg`)
- `tools/post.py` : publishes a carousel through the Instagram Graph API

Image credits are listed in each `caption.txt`.
