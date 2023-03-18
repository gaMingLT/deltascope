import { Alert, Box, Button, Grid, Typography } from "@mui/material"
import { useState } from "react";
import FileDisplay from "./FileDisplay"


const DisplayFiles = ({ directoryName }: {
  directoryName: string;
}) => { 

  const [files, setFiles] = useState<any>({})
  const [directoryPath, setDirectoryName] = useState<string>(directoryName)
  const [ErrorMessage, setDeltaError] = useState<string>("");
  const [displayError, setDisplayErrorMessage] = useState<boolean>(false);

  const baseToFile = (base: any): any => {
    console.log('Base: ', atob(base));
    return [atob(base)]
  }

  const getFiles = () => {
    const data = { "directoryName": directoryName };

    if (!directoryName) {
      setDisplayErrorMessage(true);
      setDeltaError("No images selected for comparison");
      setTimeout(() => setDisplayErrorMessage(false), 5000);
      return;
    } 

    fetch("http://localhost:8000/diff/files", {
      method: "POST",
      body: JSON.stringify(data),
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then(async (e) => {
        let data = await e.json();
        console.log("Data: ", data);
        setFiles(data["diff_files"])
      })
      .catch((e) => {
        setDisplayErrorMessage(true);
        setDeltaError("Unable to retrieve files");
        setTimeout(() => setDisplayErrorMessage(false), 5000);
      });
  }




  return(
  <>
    <Grid container /*spacing={2} */ columnGap={5} >
      <Grid item container spacing={2}  direction="column" xs={2} style={{ border: '2px solid white', borderRadius: '5px', padding: '0.5rem' }} >
        <Grid item>
          <Box >
            <Typography variant="h5" >Modified Files</Typography>
          </Box>
        </Grid>
        <Grid item container spacing="2" direction="column">
          <Grid item>
            <Box bgcolor="pink" px={0.5} py={0.5} >
              Files Name 1
            </Box>
          </Grid>
          <Grid item>
            <Box bgcolor="pink" px={0.5} py={0.5}>
              Files Name 2
            </Box>
          </Grid>
        </Grid>
      </Grid>
      <Grid item container spacing={2}  xs={6} style={{ border: '2px solid white', borderRadius: '5px' }} >
        {
          Object.keys(files).map((key: string, index: number) => { 
            return (
              <FileDisplay key={index} fileBlob={new Blob(baseToFile(files[key]))} />
            )
          })
        }
      </Grid>
      <Grid item container spacing={2} direction="column">
        <Grid item>
          <Box>
            <Button variant="contained" sx={{ margin: "1rem" }} onClick={getFiles}>
              Get Files
          </Button>
          </Box>
        </Grid>
        <Grid>
          <Box>
            {displayError ? (
              <Alert sx={{ marginTop: "1rem" }} severity="error">
                {ErrorMessage}
              </Alert>
            ) : (
              ""
            )}
          </Box>
        </Grid>
      </Grid>
    </Grid>
  </>
  )
}

export default DisplayFiles
