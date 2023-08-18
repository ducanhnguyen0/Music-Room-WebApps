import React, { Component, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { TextField, Button, Grid, Typography } from  "@material-ui/core";

function JoinRoomPage(props) {
  const navigate = useNavigate();

  const[roomCode,setRoomCode] = useState('');
  const[error,setError] = useState('');


  const handleTextFieldChange = (e) => {
    e.persist();
    setRoomCode(e.target.value);
  };

  const handleEnterRoomButtonPressed = async () => {
    const response = await fetch("/api/join-room", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          code: roomCode,
        }),
      });
      if (response.ok) {
        navigate(`/room/${roomCode}`)
      } else {
        setError("Room not found.");
      }
  };

  return (
    <Grid container spacing={1} align="center">
      <Grid item xs={12}>
        <Typography variant="h4" component="h4">
          Join a Room
        </Typography>
      </Grid>
      <Grid item xs={12}>
        <TextField
          error={error}
          label="Code"
          placeholder="Enter a Room Code"
          value={roomCode}
          helperText={error}
          variant="outlined"
          onChange={handleTextFieldChange}
        />
      </Grid>
      <Grid item xs={12}>
        <Button
          variant="contained"
          color="primary"
          onClick={handleEnterRoomButtonPressed}
        >
          Enter Room
        </Button>
      </Grid>
      <Grid item xs={12}>
        <Button
        variant="contained"
        color="secondary"
        to="/"
        component={Link}
        >
          Back
        </Button>
      </Grid>
    </Grid>
  );
}

export default JoinRoomPage
