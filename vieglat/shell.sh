#!/bin/sh
cd $HOME/vieglat
python3 full.py || python3 sendMe.py "full" || echo 'fuck it'
python3 labs.py || python3 sendMe.py "labs" || echo 'fuck it'
python3 labsfinal.py || python3 sendMe.py "labsfinal" || echo 'fuck it'
python3 final.py || python3 sendMe.py "final" || echo 'fuck it'