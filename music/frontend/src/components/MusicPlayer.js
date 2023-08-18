import React, { Component } from "react";
import {
    Grid,
    Typography,
    Card,
    IconButton,
    LinearProgress
} from "@material-ui/core";
import PlayArrowIcon from "@material-ui/icons/PlayArrow";
import SkipNextIcon from "@material-ui/icons/SkipNext";
import PauseIcon from "@material-ui/icons/Pause";


function MusicPlayer(props) {

    const songProgress = (props.time / props.duration) * 100;

    const playSong = async () => {
        const response = await fetch("/spotify/play", {
            method: "PUT",
            headers: {"Content-Type": "application/json"},
        });
    }

    const pauseSong = async () => {
        const response = await fetch("/spotify/pause", {
            method: "PUT",
            headers: {"Content-Type": "application/json"},
        });
    }

    const skipSong = async () => {
        const response = await fetch("/spotify/skip", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
        });
    }

    return (
        <Card>
            <Grid container align="center" alignItems="center">
                <Grid item xs={4}>
                    <img src={props.image_url} height="100%" width="100%" />
                </Grid>
                <Grid item xs={8}>
                    <Typography component="h5" variant="h5">
                        {props.title}
                    </Typography>
                    <Typography color="textSecondary" variant="subtitle1">
                        {props.artist}
                    </Typography>
                    <div>
                        <IconButton onClick={() => {props.is_playing ? pauseSong() : playSong()}}>
                            {props.is_playing ? <PauseIcon/> : <PlayArrowIcon/>}
                        </IconButton>
                        <IconButton onClick={() => skipSong()}>
                            {props.votes} / {props.votes_required}
                            <SkipNextIcon/>
                        </IconButton>
                    </div>
                </Grid>
            </Grid>
            <LinearProgress variant="determinate" value={songProgress} />
        </Card>
    );
}

export default MusicPlayer
