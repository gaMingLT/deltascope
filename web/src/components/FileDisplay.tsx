import { Box, Grid, TextareaAutosize, Typography } from "@mui/material";
import Textarea from '@mui/joy/Textarea';
import { useEffect, useState } from "react";

const FileDisplay = ({ fileBlob }: { fileBlob: Blob | undefined }) => {
  const [fileContent, setFileContent] = useState<string | ArrayBuffer | null>(
    ""
  );
  const [fileSet, setFileSet] = useState<boolean>(false);

  useEffect(() => {
    console.log('On effect!')
    if (!fileSet && fileBlob) {
      console.log('Loading content of file')
      loadFile()
      setFileSet(true)
    }
  })

  const loadFile = () => {
    const reader = new FileReader();
    console.log("Reading file");

    reader.addEventListener(
      "load",
      () => {
        // this will then display a text file
        console.log("Result: ", reader.result);
        setFileContent(reader.result);
      },
      false
    );

    if (fileBlob) {
      reader.readAsText(fileBlob);
    }
  };

  return (
    <>
      <Grid item container spacing={4} xs direction="column">
        <Grid item>
          <Box>
            <Typography variant="h5" >File Name here</Typography>
          </Box>
        </Grid>
        <Grid item>
          <Box padding={0.5} >
            <TextareaAutosize
                minRows={15}
                style={{ width: 350 }}
                onClick={loadFile}
                value={fileContent?.toString()}
              />
          </Box>
        </Grid>
      </Grid>
    </>
  );
};

export default FileDisplay;
