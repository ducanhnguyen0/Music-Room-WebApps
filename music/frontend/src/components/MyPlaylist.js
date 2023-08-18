import React, { useState, useEffect } from "react";
import { Grid, Button, Typography, IconButton } from "@material-ui/core";
import { Link } from "react-router-dom";

function MyPlaylist(props) {

    const [myPlaylist, setMyPlaylist] = useState([])

    const fetchData = async () => {
        const response = await fetch("/api/my-playlist")
        const data = await response.json()
        setMyPlaylist(data)
    }

    useEffect(() => {
        fetchData()
    }, [])

    return (
        <Grid container spacing={1} align="center">
            <Grid item xs={12}>
                <Typography component="h4" variant="h4">
                    My Playlist
                </Typography>
            </Grid>
            {myPlaylist.length > 0 && (
                <Grid item xs={12}>
                {myPlaylist.map(song => (
                    <Typography component="h6" variant="h6" key={song.id}>
                        {song.title} by {song.artists}
                    </Typography>
                ))}
                </Grid>
            )}
            <Grid item xs={12}>
                <Button color="secondary" variant="contained" to="/" component={Link}>
                    Back
                </Button>
            </Grid>
        </Grid>
    )
}

export default MyPlaylist
