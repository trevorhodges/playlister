# playlister
A tool for creating YouTube playlists from forum posts full of embedded YouTube links.

## Getting Started

### Prerequisites

playlister requires Python3.

First, I'd recommend creating a virtual environment. Next, install the preqreq packages:

`pip install -r requirements.txt`

### Executing playlister

Execute playlister on the command line: `python playlister.py <url> <count>`.

playlister takes two arguments:

* url: The forum URL, with the page number replaced with {}
* count: The number of pages within the forum post thread

## Notes

I added a feature to get the title of each video, but didn't end up using it for the final product. However, the `get_title` function works if you'd like to integrate that into the process somehow.

## Caveats

The types of embedded links for YouTube videos is different depending on the forum software. This was built for a single type of forum software and may take some hacking to get it to work with other types of embedded links. But, hopefully this provides you with a good starting point.
