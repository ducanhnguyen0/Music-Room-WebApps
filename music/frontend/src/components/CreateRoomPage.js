import React, { useState } from 'react';
import {
    Button,
    Grid,
    Typography,
    TextField,
    FormHelperText,
    FormControl,
    Radio,
    RadioGroup,
    FormControlLabel,
    Collapse
} from '@material-ui/core';
import { Link, useNavigate } from "react-router-dom";
import { Alert } from "@material-ui/lab";

function CreateRoomPage(props) {

    const navigate = useNavigate();
    const [votesToSkip, setVotesToSkip] = useState(props.votesToSkip);
    const [guestCanPause, setGuestCanPause] = useState(props.guestCanPause);
    const [message, setMessage] = useState("");

    const handleVotesChanged = (e) => {
        e.persist();
        setVotesToSkip(e.target.value);
    };

    const handleGuestCanPauseChanged = (e) => {
        e.persist();
        setGuestCanPause(e.target.value=='true'?true:false);
    };

    const handleCreateRoomButtonPressed = async () => {
        const response = await fetch('/api/create-room', {
            method:"POST",
            headers:{ "Content-Type":"application/json" },
            body:JSON.stringify({
                votes_to_skip: votesToSkip,
                guest_can_pause: guestCanPause,
            })
        });
        const data = await response.json();
        navigate("/room/" + data.code)
    };

    const handleUpdateRoomButtonPressed = async () => {
        const response = await fetch('/api/update-room', {
            method:"PATCH",
            headers:{ "Content-Type":"application/json" },
            body:JSON.stringify({
                votes_to_skip: votesToSkip,
                guest_can_pause: guestCanPause,
                code: props.roomCode,
            })
        });
        if (response.ok) {
            setMessage("Room updated successfully!");
        }
        else {
            setMessage("Error! Failed to update room!");
        }
        props.updateCallback()
    };

    const renderCreateButton = () => {
        return (
            <Grid container spacing={1} align="center">
                <Grid item xs={12}>
                    <Button
                    color="primary"
                    variant="contained"
                    onClick={handleCreateRoomButtonPressed}
                    >
                            Create A Room
                    </Button>
                </Grid>
                <Grid item xs={12}>
                    <Button
                    color="secondary"
                    variant="contained"
                    to="/"
                    component={Link}
                    >
                        Back
                    </Button>
                </Grid>
            </Grid>
        );
    };

    const renderUpdateButton = () => {
        return (
            <Grid item xs={12} align="center">
                <Button
                color="primary"
                variant="contained"
                onClick={handleUpdateRoomButtonPressed}
                >
                        Update Room Settings
                </Button>
            </Grid>
        );
    };

    const title = props.update ? "Update Room Settings": "Create a Room";

    return (
        <Grid container spacing={1} align="center">
            <Grid item xs={12}>
                <Collapse in={message != ""}>
                    {message == "Room updated successfully!" ? (
                        <Alert
                        severity="success"
                        onClose={() => {setMessage("")}}
                        >
                            {message}
                        </Alert>
                    ) : (
                        <Alert
                        severity="error"
                        onClose={() => {setMessage("")}}
                        >
                            {message}
                        </Alert>
                    )}
                </Collapse>
            </Grid>
            <Grid item xs={12}>
                <Typography component="h4" variant="h4">
                    { title }
                </Typography>
            </Grid>
            <Grid item xs={12}>
                <FormControl component="fieldset">
                    <FormHelperText>
                        <div align="center">
                            Guest Control of Playback State
                        </div>
                    </FormHelperText>
                    <RadioGroup
                    row
                    defaultValue={guestCanPause.toString()}
                    onChange={handleGuestCanPauseChanged}
                    >
                        <FormControlLabel value="true"
                        control={
                            <Radio color="primary"/>
                        }
                        label="Play/Pause"
                        labelPlacement="bottom"
                        />
                        <FormControlLabel value="false"
                        control={
                            <Radio color="secondary"/>
                        }
                        label="No Control"
                        labelPlacement="bottom"
                        />
                    </RadioGroup>
                </FormControl>
            </Grid>
            <Grid item xs={12}>
                <FormControl>
                    <TextField
                    required={true}
                    type="number"
                    onChange={handleVotesChanged}
                    defaultValue={votesToSkip}
                    inputProps={{
                        min:1,
                        style:{
                            textAlign:"center"
                        }
                    }}
                    />
                    <FormHelperText>
                        <div align="center">
                            Votes required to skip song
                        </div>
                    </FormHelperText>
                </FormControl>
            </Grid>
            {props.update ? renderUpdateButton() : renderCreateButton()}
        </Grid>
    );
}

CreateRoomPage.defaultProps = {
    update: false,
    guestCanPause: true,
    votesToSkip: 2,
    roomCode: "",
    updateCallback: () => {},
  }

export default CreateRoomPage
