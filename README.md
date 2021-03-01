# `movie-memes` Find snapshots of your favorite movie lines

## Preprocessing stage

In order to serve an indexed database of scenes and lines from movies, 
one must first create the database. The code included in `moviememes/preprocessor/`
does this for you. To use it:

**Step 1.** First, build a Docker image that can run the preprocessor.

    docker build --target preprocessor -t preproc .

This image includes the Python setup, `ffmpeg`, and everything else needed to
create your database.

**Step 2.** Choose a file on your computer (say, `/path/to/my/movies`), and put your movies 
and their subtitles into it. Then, create a YAML configuration in the same folder, structured
like this:

    output_dir: /output
    clear_output: true
    sqlite_filename: moviememes.sqlite3

    movies:
        star-wars-ep-1:
            title: The Phantom Menace
            video: ./phantom-menace.avi
            subtitles: ./phantom-menace.srt
            subtitle_attribution_text: Yippee!!
            subtitle_attribution_url: https://now.this/is/podracing
        star-wars-ep-2:
            title: Attack of the Clones
            video: ./aotc.avi
            subtitles: ./aotc.srt
            subtitle_attribution_text: I don't like sand
            subtitle_attribution_url: https://now.this/is/podracing

**Step 3.** Run the docker image, mapping your movie folder as an input volume, and
a different folder as an output volume. Specify your YAML config file as an argument
to the container.

    docker run -t 
        -v '/path/to/my/movies:/input:ro'
        -v '/path/to/outputs:/output:rw'
        preproc /input/config.yaml
        
**Step 4.** That's it. The output path will now contain a structure that looks like this:

    output/
        moviememes.sqlite3
        star-wars-ep-1/
            screenshot_plain_123.45-234.56.jpg
            screenshot_subtitle_123.45-234.56.jpg
            clip_subtitle_123.45-234.56.mp4
            <...>
        star-wars-ep-2/
            screenshot_plain_123.45-234.56.jpg
            screenshot_subtitle_123.45-234.56.jpg
            clip_subtitle_123.45-234.56.mp4
            <...>

The `sqlite3` file contains a searchable table of all the lines, with a quick reference to 
their movie and the files they can be found in. The filename indicates whether the capture
is subtitled or not, and what timestamps (in seconds) it occurs at.

Integrating this into a webservice is TBD.

## Lambda function

Build the lambda function using:

    docker build --target lambda -t mmlambda .

Run it locally to test, using:

    docker run -p 9000:8080 mmlambda

Query example using CURL/jq:

    $ curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"action": "hello"}' | jq '.body_parsed = (.body | fromjson)'

    {
      "statusCode": 200,
      "body": "{\"ok\": true, \"context\": {\"function_name\": \"test_function\", \"function_version\": \"$LATEST\", \"hot_time\": 447.566876}}",
      "body_parsed": {
        "ok": true,
        "context": {
          "function_name": "test_function",
          "function_version": "$LATEST",
          "hot_time": 447.566876
        }
      }
    }
