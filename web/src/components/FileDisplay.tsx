import { Box, Grid, TextareaAutosize, Typography } from "@mui/material";
import Textarea from '@mui/joy/Textarea';
import { useState } from "react";

const FileDisplay = ({ fileBlob }: { fileBlob: Blob }) => {
  const [fileContent, setFileContent] = useState<string | ArrayBuffer | null>(
    ""
  );

  const loadFile = () => {
    const reader = new FileReader();
    console.log("Load file");

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
          <Box>
            <TextareaAutosize
                minRows={5}
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
