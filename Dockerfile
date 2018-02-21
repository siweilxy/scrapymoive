FROM siwei/ubuntu
MAINTAINER siwei

copy getMovies/ getMovies/
copy scrapy.cfg /
copy startBug.py /
CMD python startBug.py
