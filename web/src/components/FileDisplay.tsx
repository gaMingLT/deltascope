import { Box } from "@mui/material";
import { useState } from "react";


const FileDisplay = ({ fileBlob }: { fileBlob: Blob}) => {
  const [fileContent, setFileContent] = useState<string | ArrayBuffer | null>('')

  const loadFile = () => {
    const reader = new FileReader();
    console.log('Load file')
  
    reader.addEventListener(
      "load",
      () => {
        // this will then display a text file
        console.log('Result: ', reader.result)
        setFileContent(reader.result);
      },
      false
    );
  
    if (fileBlob) {
      reader.readAsText(fileBlob);
    }
  }
  
  
  return (
    <>
    <Box onClick={loadFile} sx={{ width: '100%', padding: '1rem', margin: '1rem', border: '1px solid white' }} >
      <h1>File</h1>
      <Box>
        {fileContent?.toString()}
      </Box>
    </Box>
    </>
  )
}

export default FileDisplay;
