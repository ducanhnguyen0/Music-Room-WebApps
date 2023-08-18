import React, {  useState, useEffect } from "react";
import { useParams, useNavigate } from 'react-router-dom';
import { Grid, Button, Typography, Collapse } from "@material-ui/core";
import { Alert } from "@material-ui/lab";
import CreateRoomPage from "./CreateRoomPage";
import MusicPlayer from "./MusicPlayer";


function Room(props) {

    const navigate = useNavigate();
    const { roomCode } = useParams();
    const [votesToSkip, setVotesToSkip] = useState(2);
    const [guestCanPause, setGuestCanPause] = useState(false);
    const [isHost, setIsHost] = useState(false);
    const [showSettings, setShowSettings] = useState(false);
    const [spotifyAuthenticated, setSpotifyAuthenticated] = useState(false);
    const [song, setSong] = useState({});
    const [message, setMessage] = useState("");

    useEffect(() => {
      getRoomDetails();
    },[]);

    useEffect(() => {
      getCurrentSong();
    },[song]);

    const getRoomDetails = async () => {
      try {
        const response = await fetch("/api/get-room" + "?code=" + roomCode);
        if (!response.ok) {
          props.leaveRoomCallback();
          navigate("/");
          return;
        }
        const data = await response.json();
        setVotesToSkip(data.votes_to_skip);
        setGuestCanPause(data.guest_can_pause);
        setIsHost(data.is_host);
        if (data.is_host) {
          await authenticateSpotify();
        }
      } catch (error) {
        // Handle any errors that occur during the fetch or authentication process
        console.error("Error fetching room details:", error);
      }
    };

    const authenticateSpotify = async () => {
      try {
        const response = await fetch("/spotify/authenticate");
        if (!response.ok) {
          console.error("Error checking Spotify authentication");
          return;
        }
        const data = await response.json();
        setSpotifyAuthenticated(data.status);
        console.log(data.status);
        if (!data.status) {
          const authUrlResponse = await fetch("/spotify/authorize");
          if (!authUrlResponse.ok) {
            console.error("Error fetching Spotify authorization URL");
            return;
          }
          const authUrlData = await authUrlResponse.json();
          window.location.replace(authUrlData.url);
        }
      } catch (error) {
        console.error("Error authenticating with Spotify:", error);
      }
    };

    const getCurrentSong = async () => {
      const response = await fetch("/spotify/current-song");
      if (!response.ok) {
        return {};
      }
      const data = await response.json();
      console.log(data);
      setSong(data);
    };

    const handleAddButtonPressed = async () => {
      const response = await fetch("/spotify/add-song", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
      });
      if (response.ok) {
        setMessage("Song added successfully to your playlist!");
      }
    };

    const handleLeaveButtonPressed = async () => {
      const response = await fetch("/api/leave-room", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
      });
      props.leaveRoomCallback();
      navigate("/")
    };

    const handleDeleteButtonPressed = async () => {
      const response = await fetch("/api/delete-room", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
      });
      props.deleteRoomCallback();
      navigate("/")
    };

    const renderDeleteButton = () => {
      return (
        <Button
        color="secondary"
        onClick={handleDeleteButtonPressed}
        >
          Delete Room
        </Button>
      );
    };

    const updateShowSettings = (v) => {
      setShowSettings(v);
    };

    const renderSettings = () => {
      return (
        <Grid container spacing={1} align="center">
          <Grid item xs={12}>
            <CreateRoomPage
            update={true}
            guestCanPause={guestCanPause}
            votesToSkip={votesToSkip}
            roomCode={roomCode}
            updateCallback={getRoomDetails}
            />
          </Grid>
          <Grid item xs={12}>
            <Button
            variant="contained"
            color="secondary"
            onClick={() => updateShowSettings(false)}
            >
              Close
            </Button>
          </Grid>
        </Grid>
      );
    };

    const renderSettingsButton = () => {
      return (
        <Button
        color="primary"
        onClick={() => updateShowSettings(true)}
        >
          Settings
        </Button>
      );
    };

    if (showSettings) {
      return renderSettings();
    }

    return (
      <Grid
      container
      spacing={2}
      direction="column"
      alignItems="center"
      justify="center"
      style={{ minHeight: '100vh' }}
      >
        <Grid item xs={12}>
          <Collapse in={message != ""}>
            {message == "Song added successfully to your playlist!" ? (
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
          <Typography variant="h4" component="h4">
            Code: {roomCode}
          </Typography>
        </Grid>
        <Grid item xs={12}>
          <MusicPlayer {...song}/>
        </Grid>
        <Grid item xs={12}>
          <div>
            <Button
            color="secondary"
            onClick={handleAddButtonPressed}
            >
              Add to Playlist
            </Button>
            {isHost ? renderSettingsButton() : null}
            {isHost ? renderDeleteButton() : null}
            <Button
            color="primary"
            onClick={handleLeaveButtonPressed}
            >
              Leave Room
            </Button>
          </div>
        </Grid>
      </Grid>
    );
  }

  export default Room
