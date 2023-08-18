import React, { Component, useState, useEffect } from "react";
import { Grid, Button, Typography } from "@material-ui/core";
import JoinRoomPage from "./JoinRoomPage";
import CreateRoomPage from "./CreateRoomPage";
import MyRoom from "./MyRoom";
import MyPlaylist from "./MyPlaylist";
import Room from "./Room";
import {
    BrowserRouter as Router,
    Routes,
    Route,
    Link,
    Navigate
} from "react-router-dom";


function HomePage(props) {

    const[roomCode,setRoomCode] = useState(null);

    useEffect(() => {
        fetch('/api/user-in-room')
        .then(response => response.json())
        .then(data => {
            setRoomCode(data.code);
        })
    },[]);

    const clearRoomCode = () => {
        setRoomCode(null)
    }

    const renderHomePage = () => {
        return (
            <Grid container spacing={3} align="center">
                <Grid item xs={12}>
                    <Typography variant="h3" compact="h3">
                        Music Room
                    </Typography>
                </Grid>
                <Grid item xs={12}>
                    <div>
                        <Button color="primary" to="/join" component={Link}>
                            Join a Room
                        </Button>
                        <Button color="secondary" to="/create" component={Link}>
                            Create a Room
                        </Button>
                        <Button color="primary" to="/my-room" component={Link}>
                            My Room
                        </Button>
                        <Button color="secondary" to="/my-playlist" component={Link}>
                            My Playlist
                        </Button>
                    </div>
                </Grid>
            </Grid>
        );
    }

    return (
        <Router>
            <Routes>
                <Route
                path='/'
                element={roomCode ? <Navigate to={`/room/${roomCode}`} /> : renderHomePage()}
                />
                <Route path='/join' element={<JoinRoomPage/>} />
                <Route path='/create' element={<CreateRoomPage/>} />
                <Route path='/my-room' element={<MyRoom/>} />
                <Route path='/my-playlist' element={<MyPlaylist/>} />
                <Route
                path='/room/:roomCode'
                element={<Room leaveRoomCallback={clearRoomCode} deleteRoomCallback={clearRoomCode} />}
                />
            </Routes>
        </Router>
    )
}

export default HomePage
