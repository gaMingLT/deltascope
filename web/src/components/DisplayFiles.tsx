import { Alert, Box, Button, Grid } from "@mui/material"
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
    {/* <Box sx={{ width: '100%', display: 'flex', justifyContent: 'space-between' }} > */}
      <Grid item container spacing={2} zeroMinWidth >
        {
          Object.keys(files).map((key: string, index: number) => { 
            return (
              <FileDisplay key={index} fileBlob={new Blob(baseToFile(files[key]))} />
            )
          })
        }        
        <Button variant="contained" sx={{ margin: "1rem" }} onClick={getFiles}>
            Get Files
        </Button>
        {displayError ? (
            <Alert sx={{ marginTop: "1rem" }} severity="error">
              {ErrorMessage}
            </Alert>
          ) : (
            ""
          )}
      </Grid>
    {/* </Box> */}
  </>
  )
}

export default DisplayFiles
