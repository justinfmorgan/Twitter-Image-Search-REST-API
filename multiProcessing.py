from searchAndVideo import searchTwitter, searchAndMakeVideo
from multiprocessing import Pool, cpu_count
import sys
import os
import glob
import tweepy

CPU_LIMIT = cpu_count()

def processVideos(listofterms):

    # Remove all files currently in the folder
    files = glob.glob('resources/imageGen/*')
    for f in files:
        os.remove(f)

    # Remove all files currently in the folder
    files = glob.glob('searchVideos/*')
    for f in files:
        os.remove(f)

    # Remove the DS store file on mac if present
    if os.path.exists("resources/imageGen/.DS_Store"):
        os.remove("resources/imageGen/.DS_Store")

    # Sets the number of tweets to search through for images
    numTweets = 100

    # Create a list of lists of the function arguments required to starmap
    # to searchAndMakeVideo
    videoFunctionArguments = []
    for argIndex in range(len(listofterms)):
        currentarg = []
        # Skip over first argument to avoid the script name
        currentarg.append(str(listofterms[argIndex]))
        currentarg.append(numTweets)
        currentarg.append(argIndex)
        currentarg.append(("searchVideos/"+str(listofterms[argIndex]) + ".mp4").replace(" ", "_"))
        videoFunctionArguments.append(currentarg)

    # Run multiprocessing on the arguments
    try:
        # Create the pool, each process is one search term
        p = Pool(len(listofterms))
        # Map the argument array to asynchronous processes and run
        p.starmap_async(searchAndMakeVideo, videoFunctionArguments)
        # Close the pool and join the processes (wait for completion before zip file download)
        p.close()
        p.join()
        # If the tweepy rate has been exceeded then quit (Occurs on any tweep error, not just rate limit)
    except tweepy.error.TweepError:
        sys.exit("Tweepy request rate limit exceeded. Quitting.\n")