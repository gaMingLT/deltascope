import { Box, Button, Grid } from "@mui/material"
import { useState } from "react";
import FileDisplay from "./FileDisplay"


const DisplayFiles = ({ directoryName }: {
  directoryName: string;
}) => { 

  const [files, setFiles] = useState<any>({})

  const baseToFile = (base: any): any => {
    console.log('Base: ', atob(base));
    return [atob(base)]
  }

  const getFiles = () => {
    const data = { directoryName: directoryName };

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

      });
  }




  return(
  <>
    <Box sx={{ width: '100%', display: 'flex', justifyContent: 'space-between' }} >
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
    </Box>
  </>
  )
}

export default DisplayFiles
