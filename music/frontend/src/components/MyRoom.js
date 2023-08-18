import React, { useState, useEffect } from "react";
import { Grid, Button, Typography, IconButton } from "@material-ui/core";
import { Link } from "react-router-dom";


function MyRoom(props) {

    const [myRoom, setMyRoom] = useState([])

    const fetchData = async () => {
        const response = await fetch("/api/my-room")
        const data = await response.json()
        setMyRoom(data)
    }

    useEffect(() => {
        fetchData()
    }, [])

    return (
        <Grid container spacing={1} align="center">
            <Grid item xs={12}>
                <Typography component="h4" variant="h4">
                    My Room
                </Typography>
            </Grid>
            {myRoom.length > 0 && (
                <Grid item xs={12}>
                {myRoom.map(room => (
                    <Button color="primary" variant="contained" to={{ pathname: `/room/${room.code}` }} component={Link} key={room.id}>
                        Room Code: {room.code}
                    </Button>
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

export default MyRoom
