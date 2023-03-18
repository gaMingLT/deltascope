import { Alert, Box, Button, CircularProgress, Grid } from "@mui/material";
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

      setDisplayLoading(true)
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
          setDisplayLoading(false)
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
      <Grid
        container
        spacing={8}
        direction={"column"}
        xs={
          12
        }
        zeroMinWidth
      >
        {/* Selected Images */}
        <Grid container spacing={2} direction="column" justifyContent="center" alignItems="center" sx={{ marginBottom: '1.5rem' }} >
          <Typography
            variant="h5"
            sx={{ fontSize: "1.5rem", fontWeight: "bolder", textAlign: 'center' }}
          >
            Selected Images
          </Typography>
          <Grid
            container
            spacing={2}
            item
            xs={
              6
            }
            direction="column"
          >
            {selectedImages.map((name, index) => (
              <Box
                key={index}
                data-name={name}
                onClick={addImageForComparison}
                sx={{
                  textAlign: "center",
                  fontSize: 18,
                  fontWeight: "bold",
                  margin: "1rem",
                  padding: "0.75rem",
                  color: "black",
                  backgroundColor: "lightblue",
                  cursor: "pointer",
                  borderRadius: "5px",
                }}
              >
                {name}
              </Box>
            ))}
          </Grid>          
        </Grid>


        {/* Available Images! */}
        <Grid container spacing={4} direction="column" justifyContent="center" alignItems="center" zeroMinWidth>
          <Typography
            variant="h5"
            sx={{ fontSize: "1.5rem", fontWeight: "bolder" }}
          >
            Available Images
          </Typography>
          <Grid container spacing={2} direction={"column"} xs={6} zeroMinWidth>
            {availableImages.map((name, index) => (
              <Box
                key={index}
                data-name={name}
                onClick={addImageForComparison}
                sx={{
                  textAlign: "center",
                  fontSize: 24,
                  fontWeight: "bold",
                  color: "black",
                  margin: "1rem",
                  padding: "0.5rem",
                  border: "2px solid black",
                  borderRadius: "3px",
                  cursor: "pointer",
                }}
              >
                {name}
              </Box>
            ))}
          </Grid>          
        </Grid>


        <Grid
          container
          spacing={2}
          direction={"column"}
          xs={4}
          item
          zeroMinWidth
        >
          <Button
            variant="contained"
            sx={{ marginTop: "1rem" }}
            onClick={getAvailableImages}
          >
            Retrieve Images
          </Button>
          <Button
            variant="contained"
            sx={{ marginTop: "1rem" }}
            onClick={initiateDelta}
          >
            Initiate Delta
          </Button>
          {displayError ? (
            <Alert sx={{ marginTop: "1rem" }} severity="error">
              {ErrorMessage}
            </Alert>
          ) : (
            ""
          )}
          {displayMessage ? (
            <Alert sx={{ marginTop: "1rem" }} severity="success">
              {message}
            </Alert>
          ) : (
            ""
          )}
          {displayLoading ? (
            <CircularProgress
            color="primary"
            size="md"
          />
          ) : ("")

          }
        </Grid>

      </Grid>
    </>
  );
};

export default DisplayImages;
