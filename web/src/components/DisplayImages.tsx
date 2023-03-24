import { Alert, Box, Button, CircularProgress, Grid, LinearProgress } from "@mui/material";
import { Typography } from "@mui/material";
import React, { useState } from "react";

const DisplayImages = ({
  setParentDirectoryName,
  setImages,
}: {
  setParentDirectoryName: any;
  setImages: any;
}) => {
  const [availableImages, setAvailableImages] = useState<Array<string>>([]);
  const [selectedImages, setSelectedImages] = useState<Array<string>>([]);
  const [ErrorMessage, setDeltaError] = useState<string>("");
  const [displayError, setDisplayErrorMessage] = useState<boolean>(false);
  const [message, setMessage] = useState<string>("");
  const [displayMessage, setDisplayMessage] = useState<boolean>(false);
  const [displayLoading, setDisplayLoading] = useState<boolean>(false);

  const getAvailableImages = () => {
    console.log("Fetching available images");
    fetch("http://localhost:8000/images/list")
      .then((response) => response.json())
      .then((json) => {
        setAvailableImages(json.images);
      })
      .catch((e) => {
        setDisplayErrorMessage(true);
        setDeltaError("Unable to retrieve available images for comparison");
      });
  };

  const initiateDelta = () => {
    if (selectedImages.length < 2) {
      setDisplayErrorMessage(true);
      setDeltaError(
        "Unable to initiate delta - amount of selected images to low"
      );
      setTimeout(() => setDisplayErrorMessage(false), 2000);
    } else {
      const data = { images: selectedImages, directoryNames: "" };

      setDisplayLoading(true);
      fetch("http://localhost:8000/delta", {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
          "Content-Type": "application/json",
        },
      })
        .then(async (e) => {
          let data = await e.json();
          console.log("Data: ", data);
          setParentDirectoryName(data["directoryName"]);
          setImages(data["images"]);
          setMessage("Deltaing images - succesfull!");
          setDisplayMessage(true);
          setTimeout(() => setDisplayMessage(false), 5000);
          setDisplayLoading(false);
        })
        .catch((e) => {
          setDisplayErrorMessage(true);
          setDeltaError("Unable to initiate delta beteween selected images");
          setTimeout(() => setDisplayErrorMessage(false), 5000);
        });
    }
  };

  const addImageForComparison = (e: any) => {
    const image = e.target.getAttribute("data-name");
    setSelectedImages((selectedImages) => {
      if (selectedImages.includes(image)) {
        const imagesArray = selectedImages.filter((name) => image !== name);
        return imagesArray;
      } else {
        return [image, ...selectedImages];
      }
    });
  };

  return (
    <>
      <Grid item xs={4}>
        <Box /* bgcolor="primary.light" */ padding="1rem">
          <Box textAlign="center">
            <h2>Images</h2>
          </Box>
          <Grid item style={{ padding: "1rem" }}>
            <Box textAlign="center">
              <h3>Selected Images</h3>
            </Box>
            <Grid item container direction="row" spacing="10">
              {selectedImages.map((name, index) => (
                <Grid item key={index} onClick={addImageForComparison} >
                  <Box
                    py={0.75} px={0.75} borderRadius="10px" bgcolor="white" data-name={name}
                  >
                    {name}
                  </Box>
                </Grid>
              ))}
            </Grid>
          </Grid>
          <Grid item style={{ padding: "1rem" }}>
            <Box textAlign="center">
              <h3>Available Images</h3>
            </Box>
            <Grid
              item
              container
              direction="column"
              spacing="8"
              style={{ textAlign: "center" }}
            >
              {availableImages.map((name, index) => (
                <Grid item key={index} onClick={addImageForComparison}>
                  <Box
                    py={0.5} px={1} bgcolor="white" data-name={name}
                  >
                    {name}
                  </Box>
                </Grid>
              ))}
            </Grid>
          </Grid>
          <Grid item container direction="column" rowGap="1rem">
            <Grid item>
              <Box style={{ display: "flex", justifyContent: "center" }}>
                <Button
                  variant="contained"
                  sx={{ marginTop: "1rem" }}
                  onClick={getAvailableImages}
                >
                  Retrieve Images
                </Button>
              </Box>
            </Grid>
            <Grid item>
              <Box style={{ display: "flex", justifyContent: "center" }}>
                <Button
                  variant="contained"
                  sx={{ marginTop: "1rem" }}
                  onClick={initiateDelta}
                >
                  Initiate Delta
                </Button>
              </Box>
            </Grid>
            <Grid item>
              <Box>
                {displayError ? (
                  <Alert sx={{ marginTop: "1rem" }} severity="error">
                    {ErrorMessage}
                  </Alert>
                ) : (
                  ""
                )}
              </Box>
              <Box>
                {displayMessage ? (
                  <Alert sx={{ marginTop: "1rem" }} severity="success">
                    {message}
                  </Alert>
                ) : (
                  ""
                )}
              </Box>
              <Box bgcolor="white">
                {displayLoading ? (
                  <LinearProgress color="primary" />
                ) : ("")
                }
              </Box>
            </Grid>
          </Grid>
        </Box>
      </Grid>
    </>
  );
};

export default DisplayImages;
